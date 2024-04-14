#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# To run : python text_recognition.py images/1.jpg

import cv2
import numpy as np
import time
import sys
import os
from validation import validate
from classification_ai_module import document_information
from paddleocr import PaddleOCR
from classification_ai_gpt4 import document_information_gpt4


#initialize PaddleOCR with eng
ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False, use_gpu=False, det=False, ocr_version='PP-OCRv2')

def perfrom_ocr(image):
    text_list = []

    result = ocr.ocr(image)

    merged_text = ' \n '.join([res[1][0] for res in result[0]])

    text_list.append(merged_text)        

    return text_list

def perfrom_ocr_multiple_image(images):

    text_list = []

    for image in images:
        result = ocr.ocr(image)

        merged_text = ' \n '.join([res[1][0] for res in result[0]])

        text_list.append(merged_text)

    merged_texts = '\n\n'.join(text_list)

    return [merged_texts]

def frameResize(image,scale_percent):
    if int(image.shape[0]) > 850:
        output_height = 850

        #calculate the width based on the aspect ratio
        original_height, original_width, _ = image.shape
        aspect_ratio = original_width / original_height
        target_width = int(output_height * aspect_ratio)

        frame = cv2.resize(image, (target_width, output_height))
    else:
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        frame = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return frame

def processing(frame, document_type, img_arr = []):
    
    json_data = {}
    json_data['data'] = []

    validation_status = validate(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), document_type)

    json_data['verificationStatus'] = validation_status
    print("Validation_status: ", validation_status)

    if not validation_status:
        return frame, json_data
    
    # print(document_type)
    if document_type.startswith('collaborative_agreement'):
        return frame, json_data

    frame = frameResize(image= frame, scale_percent = 99)
    width = int(frame.shape[1])
    height = int(frame.shape[0])
    dim = (width, height)

    img = frame
    # aa = time.time()

    print("len img_arr : ", len(img_arr))
    if len(img_arr) > 0:
        blockwisedata = perfrom_ocr_multiple_image(img_arr)
    else:
        blockwisedata = perfrom_ocr(img)

    if len(blockwisedata)!=0:
        json_data['rawData'] = blockwisedata[0]

        output_data = document_information(blockwisedata, document_type)

        json_data['data'].append(output_data)    

    return frame, json_data

def processing_gpt4(frame, document_type, img_arr = []):
    
    json_data = {}
    json_data['data'] = []

    validation_status = validate(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), document_type)

    json_data['verificationStatus'] = validation_status
    print("Validation_status: ", validation_status)

    if not validation_status:
        return frame, json_data
    
    if document_type.startswith('collaborative_agreement'):
        return frame, json_data

    if frame is not None:

        output_data = document_information_gpt4(frame, document_type)
        try:
            json_data['GptVision_verificationStatus'] = output_data['GptVision_verificationStatus']
            del output_data['GptVision_verificationStatus']
        except Exception as e:
            print(e)
            pass
        
        json_data['data'] = output_data

    return frame, json_data


if __name__ == "__main__":

    import pypdfium2 as pdfium

    #Load an image using OpenCV
    image_path = sys.argv[1]

    if image_path.split(".")[-1] == "pdf":
        pdf = pdfium.PdfDocument(image_path)
        page = pdf[0]
        frame = page.render(scale=4).to_numpy()
        pdf.close()

    else:
        frame = cv2.imread(image_path)

    frame, json_data = processing_gpt4(frame, "degree")
    print(json_data)

