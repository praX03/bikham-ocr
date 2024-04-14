#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# To run : python training.py

import cv2 
import pickle
import sys
import matplotlib.pyplot as plt
import os
import pypdfium2 as pdfium

def get_image_paths(root_folder):
    image_paths = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.pdf')):
                image_paths.append(os.path.join(root, file))
    return image_paths

#resize images to a similar dimension
def imageResizeTrain(image):
    maxD = 1024
    height,width = image.shape
    aspectRatio = width/height
    if aspectRatio < 1:
        newSize = (int(maxD*aspectRatio),maxD)
    else:
        newSize = (maxD,int(maxD/aspectRatio))
    image = cv2.resize(image,newSize)
    return image

sift = cv2.SIFT_create()

def computeSIFT(image):
    return sift.detectAndCompute(image, None)

def generate_vectores_file(image_paths):
    #grayscale images for generating keypoints
    imagesBW = []
    for imageName in image_paths:
        print("Current doc name: ", imageName)
        extension = imageName.split(".")[-1]
        if extension == "pdf":

            #load a document
            pdf = pdfium.PdfDocument(imageName)

            # render a first page
            page = pdf[0]
            image = page.render(scale=4).to_numpy()
            pdf.close()
            
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            imagesBW.append(imageResizeTrain(image_gray))
        else:
            imagesBW.append(imageResizeTrain(cv2.imread(imageName,0)))

    keypoints = []
    descriptors = []
    for i,image in enumerate(imagesBW):
        print("Starting for image keypoints: " + image_paths[i])
        keypointTemp, descriptorTemp = computeSIFT(image)
        keypoints.append(keypointTemp)
        descriptors.append(descriptorTemp)
        print("Ending for image keypoints: " + image_paths[i])

    for i,keypoint in enumerate(keypoints):
        print("Starting for image descriptors: " + image_paths[i])
        deserializedKeypoints = []
        try:
            filepath = str(image_paths[i].split('.')[0].replace('image_template', 'keypoints')) + ".txt"

            folder_path = os.path.dirname(filepath)
            os.makedirs(folder_path, exist_ok=True)

            for point in keypoint:
                temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id)
                deserializedKeypoints.append(temp)
            
            with open(filepath, 'wb') as fp:
                pickle.dump(deserializedKeypoints, fp)   
            os.chmod(filepath, 0o666)  

        except Exception as e:
            print(f"An error occurred: {e}")

        print("Ending for image descriptors: " + image_paths[i])

    for i,descriptor in enumerate(descriptors):
        try:
            filepath = str(image_paths[i].split('.')[0].replace('image_template', 'descriptors')) + ".txt"

            folder_path = os.path.dirname(filepath)

            os.makedirs(folder_path, exist_ok=True)

            with open(filepath, 'wb') as fp:
                pickle.dump(descriptor, fp)
            os.chmod(filepath, 0o666)  
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":

    TEMPLATES_PATH = 'images/image_template'
    image_paths = get_image_paths(TEMPLATES_PATH)

    # Generate_vectores_file
    generate_vectores_file(image_paths)
    print("Success")
