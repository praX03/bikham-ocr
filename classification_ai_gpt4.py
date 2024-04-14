#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import time
import pandas as pd
import datetime
import requests,json
from dateutil.parser import parse
import cv2
import numpy as np
import base64
import openai
import constant

# Initialize the OpenAI client
openai.api_key = constant.api_key
gpt4_api_key = constant.api_key

dictionarypath = 'dictionary/'
debug = True


def get_PLI_data_fromGPT4(image):
    t1 = time.time()

    base64_image = encode_image(image)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gpt4_api_key}"
    }

    prompt_input = f"""
        is this pli document ? 
        if yes, 
        extract data from this image and give me insured name, policy number, coverage limit, policy type, issue date and expiration date. date should be in mm-dd-yyyy format. without to much processing. put none if no data found. 

        else, 
        give me one word answer "no"
    """

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": f"{prompt_input}"
                    },
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    ouput_json = response.json()
    
    #extract and return the generated text from the API response
    assistant_reply = ouput_json['choices'][0]['message']['content']
    
    try:
        gpt_verificationStatus = None

        insured_name = None
        policy_number= None
        policy_issue_date= None
        policy_expiration_date= None
        coverage_limit= None
        policy_type= None

        gpt_arr = assistant_reply.split("\n")

        try:
            if "no" in gpt_arr[0].lower():
                gpt_verificationStatus = False
            else:
                gpt_verificationStatus = True
        except Exception as e:
            gpt_verificationStatus = False
            print(e)
            pass

        for idx, item in enumerate(gpt_arr):
            print(item)
            if 'insured' in item.lower():
                insured_name = item.split(":")[-1].strip()
            elif 'number' in item.lower():        
                policy_number = item.split(":")[-1].strip()
            elif 'issue' in item.lower():        
                policy_issue_date = item.split(":")[-1].strip()
            elif 'expiration' in item.lower():        
                policy_expiration_date = item.split(":")[-1].strip()
            elif 'coverage' in item.lower():        
                coverage_limit = item.split(":")[-1].strip()
            elif 'type' in item.lower():        
                policy_type = item.split(":")[-1].strip()

        t2 = time.time()
        print("Time to get response from GPT (sec): ", t2-t1)

        return insured_name, policy_number, policy_issue_date, policy_expiration_date, coverage_limit, policy_type, assistant_reply, gpt_verificationStatus

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None, None, None, None, None, None

    except Exception as e:
        print(e)
        return None, None, None, None, None, None

def encode_image(image):
    
    # Convert the image to bytes
    _, encoded_image = cv2.imencode('.jpeg', image)
    
    # Encode the image bytes to base64
    return base64.b64encode(encoded_image.tobytes()).decode('utf-8')


def get_provider_data_school_name_fromGPT4(image):
    t1 = time.time()

    # Getting the base64 string
    base64_image = encode_image(image)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gpt4_api_key}"
    }


    prompt_input = f"""
        is this diploma / degree / certificate of completion certificate ? 
        if yes, 
        extract data from this image and give me provider name , degree name , university name, certificate / license no and date of graduation in mm-dd-yyyy format. without to much processing. put none if no data found.

        else, 
        give me one word answer "no"
    """


    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": f"{prompt_input}"
                    },
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    ouput_json = response.json()
    
    # Extract and return the generated text from the API response
  
    assistant_reply = ouput_json['choices'][0]['message']['content']

    try:
        university_name = None
        provider_name = None
        degree_name = None
        issue_year = None
        certificate_no = None
        gpt_verificationStatus = None

        gpt_arr = assistant_reply.split("\n")

        try:
            if ("no" in gpt_arr[0].lower()) or ("not" in gpt_arr[0].lower()):
                gpt_verificationStatus = False
            else:
                gpt_verificationStatus = True
        except Exception as e:
            gpt_verificationStatus = False
            print(e)
            pass

        for idx, item in enumerate(gpt_arr):
            print(item)
            if 'university name' in item.lower():
                university_name = item.split(":")[-1].strip()
            elif 'provider' in item.lower():        
                provider_name = item.split(":")[-1].strip()
            elif 'graduation' in item.lower():        
                issue_year = item.split(":")[-1].strip()
            elif 'degree' in item.lower():        
                degree_name = item.split(":")[-1].strip()
            elif 'certificate' in item.lower():        
                certificate_no = item.split(":")[-1].strip()

        t2 = time.time()
        print("Time to get response from GPT (sec): ", t2-t1)
        print("provider_name", provider_name)

        return university_name, degree_name, provider_name, issue_year, certificate_no, assistant_reply, gpt_verificationStatus

    except Exception as e:
        print(e)
        return None, None, None, None, None, None, None

def extract_names(full_name):
    name_parts = str(full_name).split()

    first_name = ""
    middle_name = ""
    last_name = ""

    num_name_parts = len(name_parts)

    if num_name_parts == 1:
        first_name = name_parts[0]
    elif num_name_parts == 2:
        first_name = name_parts[0]
        last_name = name_parts[1]
    else:
        first_name = name_parts[0]
        last_name = name_parts[-1]
        middle_name = " ".join(name_parts[1:-1])

    return first_name, middle_name, last_name


def document_information_gpt4(image, document_type):
    ## input : Block wise data(data type is array) arrive from the images.
    ## output : classify text into different different classes
    # Variables initialization
    
    if document_type == 'degree': # GPT4 DONE

        School_University_name, Degree_Name, provider_Name, out_issue_date, out_certificate_NO, assistant_reply, gpt_verificationStatus  = get_provider_data_school_name_fromGPT4(image)

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        record = {
                "GptVision_verificationStatus": gpt_verificationStatus,
                "licenseNumber" : out_certificate_NO,
                "licenseType":"Degree/Diploma",
                "issueDate" : out_issue_date,
                "expirationDate" : "",
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "schoolUniversityName": School_University_name,
                "degreeName" : Degree_Name,
                "vision_response" : assistant_reply
            }

    # Liability Certificate – Insured Name, Policy Number, Policy Effective Date, Policy Expiration Date, Coverage Limit(Per Claim Limit, Aggregate), Policy Type
    elif document_type == 'pli': # GPT4 DONE

        insured_name, policy_number, policy_issue_date, policy_expiration_date, coverage_limit, policy_type, assistant_reply, gpt_verificationStatus = get_PLI_data_fromGPT4(image)

        firstName = None
        lastName = None
        middleName = None

        if insured_name is not None:
            firstName, middleName, lastName  = extract_names(insured_name)


        record = {
                "GptVision_verificationStatus" : gpt_verificationStatus,
                "licenseNumber" : policy_number,
                "licenseType":"policyNumber",
                "issueDate" : policy_issue_date,
                "expirationDate" : policy_expiration_date,
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "coverageLimit":coverage_limit,
                "boardName":"",
                "policyType": policy_type,
                "vision_response" : assistant_reply
            }

    else:

        record = {
            "error": "Feature is not avaibale for this document"
        }

    return record
