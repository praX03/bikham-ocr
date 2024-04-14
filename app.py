from flask import Flask, render_template,redirect, send_from_directory, jsonify, request, url_for, make_response , flash, send_file
import requests
import json
from PIL import Image
import os
from random import randint
from text_recognition import processing, processing_gpt4
from werkzeug.utils import secure_filename
import subprocess
import cv2
import pypdfium2 as pdfium
import time

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['DEBUG'] = 1
app.secret_key = "platform"
UPLOAD_FOLDER = 'images/image_template'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# for CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def list_folder_contents(folder_path):
    subfolders = sorted([f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))])
    files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    return subfolders, files

@app.route('/view_folder/<path:folder_path>', methods=['GET'])
def view_folder(folder_path):
    full_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_path)

    if os.path.exists(full_folder_path) and os.path.isdir(full_folder_path):
        subfolders, files = list_folder_contents(full_folder_path)
        return render_template('index.html', current_path=folder_path, subfolders=subfolders, files=files)
    else:
        flash('Invalid folder path')
        return redirect(url_for('index'))

@app.route('/upload_files/<path:folder_path>', methods=['POST'])
def upload_files(folder_path):
    full_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_path)

    tot_file =  len(request.files.getlist('file'))
    rcv_data = request.files
    if tot_file <=0:
        flash('No files part', 'error')
        print("No file part ")
        return redirect(url_for('index'))

    files = request.files.getlist('file')
    
    for file in files:
        if file.filename == '':
            continue 
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(full_folder_path, filename))
        else:
            flash('Allowed file types are pdf, png, jpg, jpeg')
            return redirect(url_for('view_folder', folder_path=folder_path))
        
    flash('Files uploaded successfully', 'success')
    return redirect(url_for('view_folder', folder_path=folder_path))





@app.route('/view_file/<path:filepath>', methods=['GET'])
def view_file(filepath):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filepath)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('File not found')

    return redirect(url_for('index', path=os.path.dirname(filepath)))




@app.route('/')
@app.route('/view_folder/')
def index():
    current_path = request.args.get('path', '')
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], current_path)

    if os.path.isdir(folder_path):
        subfolders = sorted([f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))])
        files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        return render_template('index.html', current_path=current_path, subfolders=subfolders, files=files)
    else:
        flash('Invalid folder path')
        return redirect(url_for('index'))


@app.route('/create_folder/', methods=['POST'])
def create_folder():
    new_folder_name = request.form.get('new_folder_name')

    # Check if new_folder_name is provided
    if not new_folder_name:
        flash('Folder name is required.')
        return redirect(request.referrer)

    full_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder_name)

    try:
        os.makedirs(full_folder_path)
        flash(f'Folder "{new_folder_name}" created successfully')
    except FileExistsError:
        flash(f'Folder "{new_folder_name}" already exists')
        return redirect(request.referrer)
    except Exception as e:
        flash(f'Error creating folder: {str(e)}')
        return redirect(request.referrer)
    
    return redirect(url_for('view_folder', folder_path=new_folder_name))

@app.route('/start_training', methods=['POST'])
def start_training():
    try:

        command = ['python', 'training.py']

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        stdout, stderr = process.communicate()
        last_file = stdout.split("\n")[-2]
        if process.returncode == 0:
            result = {"success": True, "message": "Training completed successfully."}
        else:
            message  = "Training failed... issue with: "+ last_file
            result = {"success": False, "message": message, "error": stderr}

        return jsonify(result)
    except Exception as e:
        result = {"success": False, "message": "An error occurred.", "error": str(e)}
        return jsonify(result)


@app.route('/delete/<path:filepath>', methods=['GET'])
def delete_file(filepath):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filepath)

    if os.path.exists(file_path):
        os.remove(file_path)
        flash('File deleted successfully')
    else:
        flash('File not found')

    return redirect(url_for('index', path=os.path.dirname(filepath)))


tasks = []

@app.route('/upload', methods=['GET'])
def image_process():
    return render_template("home.html")

@app.route('/vision', methods=['GET'])
def vision_process():
    return render_template("home_gpt4.html")


@app.route('/predict', methods=["POST"])
def predict():
    t1 =time.time()
    if not os.path.exists('static/api_data'):
        os.makedirs('static/api_data')

    random_id = randint(0,999999999999)
    doc_type = request.form["document_type"]
    
    # print("doc_type", doc_type)
    if doc_type=='dl' or doc_type=='article' or doc_type=='fl' or doc_type=='collaborative_agreement' or doc_type == 'professional_license':
        state = request.form["state"]
        doc_type += "_"
        doc_type += str(state)
    
    if 'input_url' in request.form:
        input_url = request.form['input_url']
        response = requests.get(input_url)
        
        if response.status_code == 200:
            # Get the content type from the response headers
            content_type = response.headers.get('Content-Type')
            print("content_type: ", content_type)
            if 'pdf' in content_type:
                file_extension = 'pdf'
            elif 'image' in content_type:
                if 'jpeg' in content_type:
                    file_extension = 'jpg'
                elif 'jpg' in content_type:
                    file_extension = 'jpg'
                elif 'png' in content_type:
                    file_extension = 'png'
            elif 'jpg' in content_type:
                file_extension = 'jpg'
            elif 'png' in content_type:
                file_extension = 'png'

            # Process the content of the response
            content = response.content
            pure_name = f'file_{random_id}'
            extension = file_extension
            ori_img_new = f"file_{random_id}.{file_extension}"
            
            # Save the content to a file
            image_path = os.path.join('static/api_data', ori_img_new)
            with open(image_path, 'wb') as file:
                file.write(content)            
        else:
            return "Failed to fetch URL content"

    elif 'input_file' in request.files:
        ori_file = request.files['input_file']
        pure_name = ori_file.filename.split(".")[0]
        extension = ori_file.filename.split(".")[-1]
    
        ori_img_new = f"{pure_name}_{random_id}.{extension}"
        ori_path = os.path.join("static/api_data", ori_img_new)
        ori_file.save(ori_path)

        image_path = "static/api_data/" + ori_img_new

    ama_images = []

    if extension == "pdf":
        pdf = pdfium.PdfDocument(image_path)

        page = pdf[0]
        image = page.render(scale=4).to_numpy()

        ori_img_new = f"{pure_name}_{random_id}.jpg"

        if doc_type == "ama":
            num_pages = len(pdf)

            for i in range(num_pages):
                ama_page = pdf[i]
                ama_image = ama_page.render(scale=4).to_numpy()
                ama_images.append(ama_image)

        pdf.close()

    else:
        image = cv2.imread(image_path)

    print("doc_type", doc_type)
    image, json_data = processing(image, document_type=doc_type, img_arr = ama_images)

    try:
        if os.path.exists(image_path):
            os.remove(image_path)
    except Exception as e:
        print(e)
        pass

    t2 =time.time()
    elapsed = t2-t1
    print("elapsed: ", elapsed)


    if not tasks:
        id = 1
    else:
        id = tasks[-1]["id"] + 1

    data = {
        "id" : id,
        "original-image" : ori_img_new,
        "predicted-image" : "predict_{}_{}.jpg".format(pure_name, random_id),
    }
    tasks.append(data)

    return jsonify(json_data)


@app.route('/predict_with_vision', methods=["POST"])
def predict_with_vision():
    t1 =time.time()
    if not os.path.exists('static/api_data'):
        os.makedirs('static/api_data')

    random_id = randint(0,999999999999)
    doc_type = request.form["document_type"]
    
    # print("doc_type", doc_type)
    if doc_type=='dl' or doc_type=='article' or doc_type=='fl' or doc_type=='collaborative_agreement' or doc_type == 'professional_license':
        state = request.form["state"]
        doc_type += "_"
        doc_type += str(state)
    
    if 'input_url' in request.form:
        input_url = request.form['input_url']
        response = requests.get(input_url)
        
        if response.status_code == 200:
            # Get the content type from the response headers
            content_type = response.headers.get('Content-Type')
            print("content_type: ", content_type)
            if 'pdf' in content_type:
                file_extension = 'pdf'
            elif 'image' in content_type:
                if 'jpeg' in content_type:
                    file_extension = 'jpg'
                elif 'jpg' in content_type:
                    file_extension = 'jpg'
                elif 'png' in content_type:
                    file_extension = 'png'
            elif 'jpg' in content_type:
                file_extension = 'jpg'
            elif 'png' in content_type:
                file_extension = 'png'

            # Process the content of the response
            content = response.content
            pure_name = f'file_{random_id}'
            extension = file_extension
            ori_img_new = f"file_{random_id}.{file_extension}"
            
            # Save the content to a file
            image_path = os.path.join('static/api_data', ori_img_new)
            with open(image_path, 'wb') as file:
                file.write(content)            
        else:
            return "Failed to fetch URL content"

    elif 'input_file' in request.files:
        ori_file = request.files['input_file']
        pure_name = ori_file.filename.split(".")[0]
        extension = ori_file.filename.split(".")[-1]
    
        ori_img_new = f"{pure_name}_{random_id}.{extension}"
        ori_path = os.path.join("static/api_data", ori_img_new)
        ori_file.save(ori_path)

        image_path = "static/api_data/" + ori_img_new

    ama_images = []

    if extension == "pdf":
        pdf = pdfium.PdfDocument(image_path)

        page = pdf[0]
        image = page.render(scale=4).to_numpy()

        ori_img_new = f"{pure_name}_{random_id}.jpg"

        if doc_type == "ama":
            num_pages = len(pdf)

            for i in range(num_pages):
                ama_page = pdf[i]
                ama_image = ama_page.render(scale=4).to_numpy()
                ama_images.append(ama_image)

        pdf.close()

    else:
        image = cv2.imread(image_path)

    print("doc_type", doc_type)
    image, json_data = processing_gpt4(image, document_type=doc_type, img_arr = ama_images)

    try:
        if os.path.exists(image_path):
            os.remove(image_path)
    except Exception as e:
        print(e)
        pass


    # print(json_data)
    t2 =time.time()
    elapsed = t2-t1
    print("elapsed: ", elapsed)


    if not tasks:
        id = 1
    else:
        id = tasks[-1]["id"] + 1

    data = {
        "id" : id,
        "original-image" : ori_img_new,
        "predicted-image" : "predict_{}_{}.jpg".format(pure_name, random_id),
    }
    tasks.append(data)

    return jsonify(json_data)


@app.route('/predicted-image/<int:taskId>', methods=['GET'])
def pred_image(taskId):
    print(taskId)
    task = [task for task in tasks if task["id"] == taskId]
    return send_from_directory("static/api_data", task[0]["predicted-image"])


@app.route('/ori-image/<int:taskId>', methods=['GET'])
def ori_image(taskId):
    print("taskId ori e\image" + str(taskId))
    task = [task for task in tasks if task["id"] == taskId]
    print(task[0]["original-image"])

    return send_from_directory("static/api_data", task[0]["original-image"])

if __name__ == "__main__":
    app.run()
