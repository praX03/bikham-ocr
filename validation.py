#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# To run : python validation.py images/12363.jpg 

import cv2 
import pickle
import sys
from random import randint
import os
import time

debug = False

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

def fetchKeypointFromFile(file, document_type):
    filepath = "images/keypoints/" + str(document_type) + "/" + str(file) + ".txt"
    keypoint = []
    file = open(filepath,'rb')
    deserializedKeypoints = pickle.load(file)
    file.close()
    for point in deserializedKeypoints:
        temp = cv2.KeyPoint(
            x=point[0][0],
            y=point[0][1],
            size=point[1],
            angle=point[2],
            response=point[3],
            octave=point[4],
            class_id=point[5]
        )
        keypoint.append(temp)
    return keypoint

def fetchDescriptorFromFile(file,document_type):
    filepath = "images/descriptors/" + str(document_type) + "/" + str(file) + ".txt"
    file = open(filepath,'rb')
    descriptor = pickle.load(file)
    file.close()
    return descriptor

def fetchKeypointFromTxt(filename):
    filepath = "images/keypoints/temp_data/" + str(filename) + ".txt"
    keypoint = []
    file = open(filepath,'rb')
    deserializedKeypoints = pickle.load(file)
    file.close()
    os.remove(filepath)

    for point in deserializedKeypoints:
        temp = cv2.KeyPoint(
            x=point[0][0],
            y=point[0][1],
            size=point[1],
            angle=point[2],
            response=point[3],
            octave=point[4],
            class_id=point[5]
        )
        keypoint.append(temp)
    return keypoint

def fetchDescriptorFromTxt(filename):
    filepath = "images/descriptors/temp_data/" + str(filename) + ".txt"
    file = open(filepath,'rb')
    descriptor = pickle.load(file)
    file.close()
    os.remove(filepath)
    return descriptor

def calculateScore(matches,keypoint1,keypoint2):
    return 100 * (matches/min(keypoint1,keypoint2))

bf = cv2.BFMatcher()
def calculateMatches(des1,des2):
    matches = bf.knnMatch(des1,des2,k=2)
    topResults1 = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            topResults1.append([m])
            
    matches = bf.knnMatch(des2,des1,k=2)
    topResults2 = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            topResults2.append([m])
    
    topResults = []
    for match1 in topResults1:
        match1QueryIndex = match1[0].queryIdx
        match1TrainIndex = match1[0].trainIdx

        for match2 in topResults2:
            match2QueryIndex = match2[0].queryIdx
            match2TrainIndex = match2[0].trainIdx

            if (match1QueryIndex == match2TrainIndex) and (match1TrainIndex == match2QueryIndex):
                topResults.append(match1)
    return topResults

def generate_temp_data(image, temp_file_name):

    keypoint, descriptor_data = computeSIFT(imageResizeTrain(image))
    # if debug : print(keypoint)
    # if debug : print(descriptor_data)
    deserializedKeypoints = []
    for point in keypoint:
        temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id)
        deserializedKeypoints.append(temp)

    filepath = "images/keypoints/" + "temp_data/" + temp_file_name + ".txt"

    folder_path = os.path.dirname(filepath)
    os.makedirs(folder_path, exist_ok=True)

    with open(filepath, 'wb') as fp:
        pickle.dump(deserializedKeypoints, fp)    
    os.chmod(filepath, 0o666)
    filepath = "images/descriptors/" + "temp_data/"+ temp_file_name + ".txt"

    folder_path = os.path.dirname(filepath)
    os.makedirs(folder_path, exist_ok=True)

    with open(filepath, 'wb') as fp:
        pickle.dump(descriptor_data, fp)
    os.chmod(filepath, 0o666)

def validate(image, document_type):

    templates_path = 'images/image_template/' + document_type

    random_id = randint(0,99999999)

    temp_file_name = f"{random_id}_{document_type}"

    generate_temp_data(image, temp_file_name)

    keypoint1 = fetchKeypointFromTxt(temp_file_name)
    descriptor1 = fetchDescriptorFromTxt(temp_file_name)

    files = get_image_paths(templates_path)

    for i, item in enumerate(files):
        if debug : print(item)
        
        template_path = str(item.split('.')[0].split("/")[-1])
        # if debug : print(template_path)

        keypoint2 = fetchKeypointFromFile(template_path, document_type)
        descriptor2 = fetchDescriptorFromFile(template_path, document_type)
        matches = calculateMatches(descriptor1, descriptor2)
        if debug : print(len(matches))
        if debug : print(len(matches)/len(keypoint2))

        score = calculateScore(len(matches),len(keypoint1),len(keypoint2))
        if debug : print(score)

        if score >2.0:
            return True
    
    return False
    
if __name__ == "__main__":
    
    frame = cv2.imread(sys.argv[1])
    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    t1 =time.time()
    validation_status = validate(frame_bw, 'eg')
    t2 =time.time()
    if debug : print("t2-t1: ", t2-t1)

    print("Validation_status: ", validation_status)

