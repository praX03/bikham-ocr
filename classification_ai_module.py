#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import time
import pandas as pd
import datetime
import requests,json
from dateutil.parser import parse

import openai
import constant

# Initialize the OpenAI client
openai.api_key = constant.api_key

dictionarypath = 'dictionary/'
debug = True


def get_board_certificate_data_fromGPT(ocrdata= ''):
    t1 = time.time()
    data = """You are a helpful assistant and this is your knowledge """

    data += ocrdata
    

    conversation = [
        {"role": "system", "content": data},
    ]
    user_input = 'this is a raw data extracted from ocr give me board name, provider name, specialty name , certificate no , issue date and expiration date, date should be in mm-dd-yyyy format, most of time future date is expiration date'

    conversation.append({"role": "user", "content": user_input})
    
    # print(" :: Conversation ::")
    # print(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=conversation,
        max_tokens=50,
    )
    assistant_reply = response.choices[0].message["content"]

    try:
        print("assistant_reply: ", assistant_reply)

        board_name = None
        provider_name = None
        issue_date = None
        expiration_date = None
        specialty_name = None
        certificate_no = None

        gpt_arr = assistant_reply.split("\n")
        print("gpt_arr")
        print(gpt_arr)
        
        for idx, item in enumerate(gpt_arr):
            # print(item)
            if 'board name' in item.lower():
                board_name = item.split(":")[-1].strip()
            elif 'provider' in item.lower():        
                provider_name = item.split(":")[-1].strip()
            elif 'issue' in item.lower():        
                issue_date = item.split(":")[-1].strip()
            elif 'expiration' in item.lower():        
                expiration_date = item.split(":")[-1].strip()
            elif 'specialty' in item.lower():        
                specialty_name = item.split(":")[-1].strip()
            elif 'certificate' in item.lower():        
                certificate_no = item.split(":")[-1].strip()

        print(board_name)
        print(provider_name)
        print(issue_date)
        print(expiration_date)

        t2 = time.time()
        print("Time to get response from GPT (sec): ", t2-t1)

        return board_name, provider_name, issue_date, expiration_date, specialty_name,certificate_no

    except Exception as e:
        print(e)
        return None, None, None, None ,  None,  None


def get_professional_license_data_fromGPT(ocrdata= ''):
    t1 = time.time()
    data = """You are a helpful assistant and this is your knowledge """

    data += ocrdata
    
    # print(data)

    conversation = [
        {"role": "system", "content": data},
    ]
    user_input = 'this is a raw data extracted from ocr give me license Number, provider name, issue date and expiration date, date should be in mm-dd-yyyy format'

    conversation.append({"role": "user", "content": user_input})
    
    # print(" :: Conversation ::")
    # print(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=conversation,
        max_tokens=50,
    )
    assistant_reply = response.choices[0].message["content"]

    try:
        print("assistant_reply: ", assistant_reply)

        license_number = None
        provider_name = None
        issue_date = None
        expiration_date = None

        gpt_arr = assistant_reply.split("\n")
        # print("gpt_arr")
        # print(gpt_arr)
        
        for idx, item in enumerate(gpt_arr):
            print(item)
            if 'license' in item.lower():
                license_number = item.split(":")[-1].strip()
            elif 'provider' in item.lower():        
                provider_name = item.split(":")[-1].strip()
            elif 'issue' in item.lower():        
                issue_date = item.split(":")[-1].strip()
            elif 'expiration' in item.lower():        
                expiration_date = item.split(":")[-1].strip()


        # print(license_number.strip())
        # print(provider_name.strip())
        # print(issue_date.strip())
        # print(expiration_date.strip())

        t2 = time.time()
        print("Time to get response from GPT (sec): ", t2-t1)

        return license_number, provider_name, issue_date, expiration_date

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None, None, None, None

    except Exception as e:
        print(e)
        return None, None, None, None

def get_PLI_data_fromGPT(ocrdata= ''):
    t1 = time.time()
    data = """You are a helpful assistant and this is your knowledge """

    data += ocrdata
    
    # print(data)

    conversation = [
        {"role": "system", "content": data},
    ]
    user_input = 'this is a raw data extracted from ocr give me insured name, policy number, coverage limit, policy type, issue date and expiration date. date should be in mm-dd-yyyy format'

    conversation.append({"role": "user", "content": user_input})
    
    # print(" :: Conversation ::")
    # print(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=conversation,
        max_tokens=200,
    )
    assistant_reply = response.choices[0].message["content"]

    try:
        print("assistant_reply: ", assistant_reply)

        insured_name = None
        policy_number= None
        policy_issue_date= None
        policy_expiration_date= None
        coverage_limit= None
        policy_type= None

        # license_number = None
        # provider_name = None
        # issue_date = None
        # expiration_date = None

        gpt_arr = assistant_reply.split("\n")
        print("gpt_arr")
        print(gpt_arr)
        
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

        # print(license_number.strip())
        # print(provider_name.strip())
        # print(issue_date.strip())
        # print(expiration_date.strip())

        t2 = time.time()
        print("Time to get response from GPT (sec): ", t2-t1)

        return insured_name, policy_number, policy_issue_date, policy_expiration_date, coverage_limit, policy_type

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None, None, None, None

    except Exception as e:
        print(e)
        return None, None, None, None



def get_provider_data_fromGPT(ocrdata= ''):
    t1 = time.time()
    data = """You are a helpful assistant and this is your knowledge """

    data += ocrdata
    
    # print(data)

    conversation = [
        {"role": "system", "content": data},
    ]
    user_input = 'give me provider name and issue date in dict format'

    conversation.append({"role": "user", "content": user_input})
    
    # print(" :: Conversation ::")
    # print(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=conversation,
        max_tokens=50,
    )
    assistant_reply = response.choices[0].message["content"]

    try:
        response_dict = json.loads(assistant_reply)
        print("response_dict: ", response_dict)

        provider_name = None

        for key, value in response_dict.items():
            print(f"{key}: {value}")
            if 'provider' in key.lower():        
                provider_name = value

        t2 = time.time()
        print("Time to get response from GPT (sec): ", t2-t1)


        return provider_name

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None 

    except Exception as e:
        print(e)
        return None 

def get_provider_data_with_business_name_fromGPT(ocrdata= ''):
    t1 = time.time()
    data = """You are a helpful assistant and this is your knowledge """

    data += ocrdata
    
    # print(data)

    conversation = [
        {"role": "system", "content": data},
    ]
    user_input = 'give me provider name and business name in dict format'

    conversation.append({"role": "user", "content": user_input})
    
    # print(" :: Conversation ::")
    # print(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=conversation,
        max_tokens=50,
    )
    assistant_reply = response.choices[0].message["content"]

    try:
        response_dict = json.loads(assistant_reply)
        print("response_dict: ", response_dict)

        provider_name = None
        business_name = None

        for key, value in response_dict.items():
            print(f"{key}: {value}")
            if 'provider' in key.lower():        
                provider_name = value
            elif 'business' in key.lower():        
                business_name = value


        t2 = time.time()
        print("Time to get response from GPT (sec): ", t2-t1)


        return provider_name, business_name

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None 

    except Exception as e:
        print(e)
        return None 

def get_provider_data_with_business_name_with_account_type_account_number_fromGPT(ocrdata= ''):
    t1 = time.time()
    data = """You are a helpful assistant and this is your knowledge """

    data += ocrdata
    
    # print(data)

    conversation = [
        {"role": "system", "content": data},
    ]
    user_input = 'this is a raw data extracted from ocr give me provider name and business name, account type (either saving or checking), account number and routing number'

    conversation.append({"role": "user", "content": user_input})
    
    # print(" :: Conversation ::")
    # print(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=conversation,
        max_tokens=50,
    )
    assistant_reply = response.choices[0].message["content"]

    try:
        print("assistant_reply: ", assistant_reply)

        provider_name = None
        business_name = None
        account_type = None
        account_number = None
        routing_number = None

        gpt_arr = assistant_reply.split("\n")
        # print("gpt_arr")
        # print(gpt_arr)
        
        for idx, item in enumerate(gpt_arr):
            print(item)
            if 'business' in item.lower():
                business_name = item.split(":")[-1].strip()
            elif 'provider' in item.lower():        
                provider_name = item.split(":")[-1].strip()
            elif 'account type' in item.lower():        
                account_type = item.split(":")[-1].strip()
            elif 'account number' in item.lower():        
                account_number = item.split(":")[-1].strip()
            elif 'routing' in item.lower():        
                routing_number = item.split(":")[-1].strip()

        t2 = time.time()
        print("Time to get response from GPT (sec): ", t2-t1)


        return provider_name, business_name, account_type, account_number, routing_number

    except Exception as e:
        print(e)
        return None, None, None, None, None

def get_provider_data_with_business_name_board_name_fromGPT(ocrdata= ''):
    t1 = time.time()
    data = """You are a helpful assistant and this is your knowledge """

    data += ocrdata
    
    # print(data)

    conversation = [
        {"role": "system", "content": data},
    ]
    user_input = 'this is a raw data extracted from ocr give me provider name , board name, license number, license type, and business name'

    conversation.append({"role": "user", "content": user_input})
    
    # print(" :: Conversation ::")
    # print(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=conversation,
        max_tokens=50,
    )
    assistant_reply = response.choices[0].message["content"]

    try:
        # response_dict = json.loads(assistant_reply)
        # print("response_dict: ", response_dict)
        gpt_arr = assistant_reply.split("\n")

        provider_name = None
        business_name = None
        board_name = None
        gpt_license_no = None
        gpt_license_type = None

        for idx, item in enumerate(gpt_arr):
            print(item)
            if 'business' in item.lower():
                business_name = item.split(":")[-1].strip()
            elif 'provider' in item.lower():        
                provider_name = item.split(":")[-1].strip()
            elif 'board name' in item.lower():        
                board_name = item.split(":")[-1].strip()
            elif 'license number' in item.lower():        
                gpt_license_no = item.split(":")[-1].strip()
            elif 'license type' in item.lower():        
                gpt_license_type = item.split(":")[-1].strip()

        t2 = time.time()
        print("Time to get response from GPT (sec): ", t2-t1)

        return provider_name, business_name, board_name, gpt_license_no, gpt_license_type

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None, None, None, None, None 

    except Exception as e:
        print(e)
        return None, None, None, None, None


def get_provider_data_school_name_fromGPT(ocrdata= ''):
    t1 = time.time()
    data = """You are a helpful assistant and this is your knowledge """

    data += ocrdata
    
    # print(data)

    conversation = [
        {"role": "system", "content": data},
    ]
    user_input = 'this is a raw data extracted from ocr give me provider name , degree name , university name, certificate / license no and date of graduation in mm-dd-yyyy format'

    conversation.append({"role": "user", "content": user_input})
    
    # print(" :: Conversation ::")
    # print(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=conversation,
        max_tokens=50,
    )
    assistant_reply = response.choices[0].message["content"]

    try:
        university_name = None
        provider_name = None
        degree_name = None
        issue_year = None
        certificate_no = None

        gpt_arr = assistant_reply.split("\n")
        print("gpt_arr")
        print(gpt_arr)
        
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


        return university_name, degree_name, provider_name, issue_year, certificate_no

    except Exception as e:
        print(e)
        return None, None, None, None, None


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

# Function to replace multiple charector from line
def replaceMultiple(mainString, toBeReplaces, newString):
    #iterate over the strings to be replaced
    for elem in toBeReplaces :
        #check if string is in the main string
        if elem in mainString :
            #replace the string
            mainString = mainString.replace(elem, newString)
    
    return  mainString 

# code to remove duplicate elements 
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

def find_lowest_highest_dates(date_strings):
    # Convert date strings to datetime objects
    date_objects = []
    for date_str in date_strings:
        try:
            my_date = parse(date_str) 
            date_objects.append(my_date)
        except Exception as e:
            pass


    # Find the lowest and highest dates
    lowest_date = min(date_objects)
    highest_date = max(date_objects)

    return lowest_date, highest_date

def find_sorted_dates(date_strings):
    # Convert date strings to datetime objects
    date_objects = [parse(date_str) for date_str in date_strings]

    sorted_dates = sorted(date_objects)

    return sorted_dates

def find_license_type_by_most_common_words(line):
    list_containing_all_freq_license_types = ["anesthesiology","cardiology","dermatology","neurology","orthopedics","pediatrics","radiology","gastroenterology","obstetrics and gynecology","psychiatry","ophthalmology","surgery","analyst","nurse","allergy and immunology", "anesthesiology", "dermatology", "diagnostic", "radiology", "emergency", "family", "internal", "medical genetics", "neurology", "nuclear", "obstetrics and gynecology", "ophthalmology", "pathology", "pediatrics", "physical", "rehabilitation", "preventive", "psychiatry", "radiation oncology", "surgery", "urology", "medicine", "clinical", "permit"]
    
    search_for_license_type = None
    line_clean = line.lower()
    line_clean = replaceMultiple(line_clean, ["©","®","€", "(", ")", "|", "/", ",", "#","&", ">", "=", "+", "<", "@", "!", "$", "[", "]",".","-","~","`"], " ")
    
    search_for_license_type = line_clean.strip()

    if search_for_license_type is not None:
        if any(word.lower() in list_containing_all_freq_license_types for word in search_for_license_type.split()):
            return line

def get_license_type(data_array_clean):
    license_type = None
    #loop to find license_type name by most frequent words from remaining details
    for block_no in range(len(data_array_clean)):
        block = data_array_clean[block_no]
        lines_array = list(filter(str.strip, block.splitlines()))
        # print(block)

        for i in range(len(lines_array)):
            line = lines_array[i].strip()  
            if license_type is None and len(line.split())<=7 and line.count(",") <= 2:
                
                license_type = find_license_type_by_most_common_words(line)
                
                if (license_type) is not None:
                    line = line.replace(license_type,"")
                    
            lines_array[i] = line
        
        # print("license_type: ",license_type)
        # input()
        
        block =  '\n'.join(lines_array).strip()
        data_array_clean[block_no] = block
        
    # license_type = find_license_type_by_ein(EIN_NO[0])
    return license_type, data_array_clean

def getFirst(mylist):
    if len(mylist) > 0 :
        final = mylist[0]
    else:
        final = None
    return final

def get_ama_data_fromGPT(ocrdata = ''):
    t1 = time.time()
    data = """You are a helpful assistant and this is your knowledge give user available value form their data if it's not available write null """

    data += ocrdata
    
    # print(data)

    conversation = [
        {"role": "system", "content": data},
    ]
    user_input = 'this is a raw data extracted from ocr give me School name, Degree Awarded in yes or no, Enrollment Date, Degree Type, Degree Date, Sponsoring Institution name, Sponsoring State, Program Name, Specialty, Training Type, Sponsoring Dates, Sponsoring Status (date should be in mm-dd-yyyy format)'

    conversation.append({"role": "user", "content": user_input})
    
    # print(" :: Conversation ::")
    # print(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=conversation,
        max_tokens=300,
    )
    assistant_reply = response.choices[0].message["content"]

    try:
        print("assistant_reply: ", assistant_reply)

        school_name = None
        degree_awarded = None
        enrollment = None
        degree_type = None
        degree_date = None
        sponsoring_institution = None
        sponsoring_state = None
        program_name  = None
        specialty = None
        training_type = None
        sponsoring_dates = None
        sponsoring_status = None

        gpt_arr = assistant_reply.split("\n")
        # print("gpt_arr")
        # print(gpt_arr)
        
        for idx, item in enumerate(gpt_arr):
            # print(item)
            if 'school' in item.lower():
                school_name = item.split(":")[-1].strip()
            elif 'degree awarded' in item.lower():        
                degree_awarded = item.split(":")[-1].strip()
            elif 'enrollment' in item.lower():        
                enrollment = item.split(":")[-1].strip()
            elif 'degree type' in item.lower():        
                degree_type = item.split(":")[-1].strip()
            elif 'degree date' in item.lower():        
                degree_date = item.split(":")[-1].strip()
            elif 'institution' in item.lower():        
                sponsoring_institution = item.split(":")[-1].strip()
            elif 'sponsoring state' in item.lower():        
                sponsoring_state = item.split(":")[-1].strip()
            elif 'program name' in item.lower():        
                program_name = item.split(":")[-1].strip()
            elif 'specialty' in item.lower():        
                specialty = item.split(":")[-1].strip()
            elif 'training type' in item.lower():        
                training_type = item.split(":")[-1].strip()
            elif 'sponsoring date' in item.lower():        
                sponsoring_dates = item.split(":")[-1].strip()
            elif 'sponsoring status' in item.lower():        
                sponsoring_status = item.split(":")[-1].strip()



        # print(license_number.strip())
        # print(provider_name.strip())
        # print(issue_date.strip())
        # print(expiration_date.strip())

        t2 = time.time()
        print("Time to get response from GPT (sec): ", t2-t1)

        return school_name , degree_awarded , enrollment , degree_type , degree_date , sponsoring_institution , sponsoring_state , program_name  , specialty , training_type , sponsoring_dates , sponsoring_status
    except Exception as e:
        print(e)
        return None, None, None, None, None, None, None, None, None, None, None, None

def document_information(data_array, document_type):
    ## input : Block wise data(data type is array) arrive from the images.
    ## output : classify text into different different classes
    # Variables initialization

    regex_for_date = r"\b((?:\d{4}-\d{1,2}-\d{1,2})|(?:\d{1,2}-\d{1,2}-\d{4})|(?:\d{1,2}/\d{1,2}/\d{4})|(?:\d{1,2}/\d{1,2}/\d{2})|(?:\d{1,2}\.\d{1,2}\.\d{4})|(?:\d{2}\.\d{2}\.\d{2})|(?:\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s\d{4})|(?:\d{1,2}\s(?:January|February|March|April|May|June|July|August|September|October|November|December|january|february|march|april|may|june|july|august|september|october|november|december)\s\d{4})|(?:\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s\d{1,2})|(?:\w+\s(?:[1-9]|0[1-9]|[12]\d|3[01])(?:,)?\s\d{4})|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[/\s]\d{1,2}[/\s]\d{2})\b"
    
    data_array_clean = []
    # CLEANING Blocks
    for block in data_array:
        if block not in ('\n','',' ', '  '):
            data_array_clean.append(block)

    if document_type == 'dea':

        DEA_NO = []
        is_dea = False
        issue_date = []
        expiration_date = []
        date_list = []

        other_details = []

        expiration_identifier = ["expires", "expiration"]
        issue_identifier = ["issue"]

        regex_for_DEA = r"\b[A-Za-z]{2}[\doO]{6}[\doO]\b"

        # get data
        for block_no in range(len(data_array_clean)):
            block = data_array_clean[block_no]

            lines_array = list(filter(str.strip, block.splitlines()))

            for i in range(len(lines_array)):
                line = lines_array[i] 

                # find DEA number
                if is_dea == False:
                    deas = re.findall(regex_for_DEA, line)
                    if len(deas) >= 1 :
                        print("Found DEA number!")
                        num = deas[0].replace("o","0")
                        num = num.replace("O","0")
                        DEA_NO.append(num)
                        is_dea = True

                # find dates
                dates = re.findall(regex_for_date, line)
                if len(dates) >= 1 :
                    date_list.extend(dates)

                    for date in dates:
                        try: 
                            temp_str = lines_array[i-1].lower() + " " + lines_array[i].lower()
                            if any([x in temp_str for x in expiration_identifier]):
                                print("Found Expires date!")
                                try:
                                    expiration_date.append(parse(date).strftime('%m-%d-%Y'))
                                    line = line.replace(date,'')
                                    date = date.replace(" ","")
                                except Exception as e:
                                    print(e)
                                    pass

                            elif any([x in temp_str for x in issue_identifier]):
                                print("Found Issue date!")                                
                                try:
                                    issue_date.append(parse(date).strftime('%m-%d-%Y'))
                                    line = line.replace(date,'')
                                    date = date.replace(" ","")
                                except Exception as e:
                                    print(e)
                                    pass

                        except Exception as e:
                            pass

                lines_array[i] = line

            block =  '\n'.join(lines_array)
            data_array_clean[block_no] = block

        if len(issue_date)==0:
            clean_dt = Remove(date_list)
            if len(clean_dt) > 1:
                try:
                    lowest_date, highest_date = find_lowest_highest_dates(clean_dt)
                    issue_date.append(lowest_date.strftime('%m-%d-%Y'))
                except Exception as e:
                    pass

        if len(expiration_date)==0:
            clean_dt = Remove(date_list)
            if len(clean_dt) > 1:
                try:
                    lowest_date, highest_date = find_lowest_highest_dates(clean_dt)
                    # print(highest_date)
                    expiration_date.append(highest_date.strftime('%m-%d-%Y'))
                except Exception as e:
                    pass

        # print dates 
        if debug:
            print("Expiration date", (expiration_date))
            print("Issue date", (issue_date))
            # print("all_date", (date_list))
                    
        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)

        provider_Name = get_provider_data_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        record = {
                "licenseNumber" : getFirst(Remove(DEA_NO)),
                "licenseType":"deaNo",
                "issueDate" : getFirst(Remove(issue_date)),
                "expirationDate" : getFirst(Remove(expiration_date)),
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""
            }

    elif document_type == 'bank_letter':

        Account_Type = None

        # get data
        provider_Name, bussiness_name, Account_Type, account_number, routing_number  = get_provider_data_with_business_name_with_account_type_account_number_fromGPT(data_array_clean[0])


        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
          
        record = {
                "licenseNumber" : routing_number,
                "licenseType":"bankLetter(routingNo)",
                "accountNo" : account_number,
                "bussinessName" : bussiness_name,
                "accountType" : Account_Type,
                "issueDate" : "",
                "expirationDate" : "",
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""
            }

    elif document_type == 'board_certificates':
        
        board_name, provider_Name, out_issue_date, out_expiration_date, specialty_name, out_certificate_NO = get_board_certificate_data_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        record = {
                "licenseNumber" : out_certificate_NO,
                "licenseType":"boardCertificates(certificateNo)",
                "issueDate" : out_issue_date,
                "expirationDate" : out_expiration_date,
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName": board_name,
                "specialty" : specialty_name,
            }

    elif document_type == 'degree':
        
        School_University_name, Degree_Name, provider_Name, out_issue_date, out_certificate_NO  = get_provider_data_school_name_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        record = {
                "licenseNumber" : out_certificate_NO,
                "licenseType":"Degree/Diploma",
                "issueDate" : out_issue_date,
                "expirationDate" : "",
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "schoolUniversityName": School_University_name,
                "degreeName" : Degree_Name
            }

    elif document_type == 'check':

        provider_Name, bussiness_name  = get_provider_data_with_business_name_fromGPT(data_array_clean[0])

        if debug:
            print("Bussiness Name::",bussiness_name) 
        

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)


        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
    
        record = {
                "licenseNumber":"",
                "licenseType":"check",
                "expirationDate":"",
                "issueDate":"",
                "bussiness_name": bussiness_name,
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""
            }

    elif document_type == 'clia':

        CLIA_NO = []
        is_CLIA = False
        issue_date = []
        expiration_date = []
        date_list = []
        certificate_type = None

        other_details = []

        expiration_identifier = ["expires", "expiration"]
        issue_identifier = ["issue", "start", "effective"]

        regex_for_CLIA = r'\b\d{2}D\d{7}\b'

        # get data
        for block_no in range(len(data_array_clean)):
            block = data_array_clean[block_no]
            lines_array = list(filter(str.strip, block.splitlines()))

            for i in range(len(lines_array)):
                line = lines_array[i] 
                # print(line)

                # find CLIA number
                if is_CLIA == False:
                    CLIAs = re.findall(regex_for_CLIA, line)
                    # print(CLIAs)
                    if len(CLIAs) >= 1 :
                        print("Found CLIA number!")
                        num = CLIAs[0].replace("o","0")
                        num = num.replace("O","0")
                        CLIA_NO.append(num)
                        is_CLIA = True
                        line = line.replace(num,'')

                if certificate_type is None:
                    line_words = line.lower().split(" ")
                    if "waiver" in line_words:
                        certificate_type = "Waiver"
                    elif "registration" in line_words:
                        certificate_type = "Registration"
                    elif "compliance" in line_words:
                        certificate_type = "Compliance"
                    elif "accreditation" in line_words:
                        certificate_type = "Accreditation"

                # find dates
                dates = re.findall(regex_for_date, line)
                if len(dates) >= 1 :
                    date_list.extend(dates)
                    # print("dates: ", dates)
                    # print("cr line: ", line)

                    for date in dates:
                        try: 
                            temp_str = lines_array[i-1].lower() + " " + lines_array[i].lower()
                            if any([x in temp_str for x in expiration_identifier]):
                                print("Found Expires date!")
                                try:
                                    expiration_date.append(parse(date).strftime('%m-%d-%Y'))
                                    line = line.replace(date,'')
                                    date = date.replace(" ","")
                                except Exception as e:
                                    print(e)
                                    pass

                            elif any([x in temp_str for x in issue_identifier]):
                                print("Found Issue date!")                                
                                try:
                                    issue_date.append(parse(date).strftime('%m-%d-%Y'))
                                    line = line.replace(date,'')
                                    date = date.replace(" ","")
                                except Exception as e:
                                    print(e)
                                    pass
                               

                        except Exception as e:
                            pass

                lines_array[i] = line

            block =  '\n'.join(lines_array)
            data_array_clean[block_no] = block

        if len(issue_date)==0:
            clean_dt = Remove(date_list)
            if len(clean_dt) > 1:
                try:
                    lowest_date, highest_date = find_lowest_highest_dates(clean_dt)
                    issue_date.append(lowest_date.strftime('%m-%d-%Y'))
                except Exception as e:
                    pass

        if len(expiration_date)==0:
            clean_dt = Remove(date_list)
            if len(clean_dt) > 1:
                try:
                    lowest_date, highest_date = find_lowest_highest_dates(clean_dt)
                    # print(highest_date)
                    expiration_date.append(highest_date.strftime('%m-%d-%Y'))
                except Exception as e:
                    pass

        
        print("data_array_clean: ", data_array_clean)
        # print dates 
        provider_Name, bussiness_name  = get_provider_data_with_business_name_fromGPT(data_array_clean[0])


        if debug:
            print("CLIA_NO", (CLIA_NO))
            print("Expiration date", (expiration_date))
            print("Issue date", (issue_date))
            print("Bussiness Name::",bussiness_name) 
            print("certificate_type ::",certificate_type) 


            # print("all_date", (date_list))

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        
        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
    
        record = {
                "licenseNumber" : getFirst(Remove(CLIA_NO)),
                "licenseType":"cliaNo",
                "bussinessName" : bussiness_name,
                "certificateType" : certificate_type,
                "issueDate" : getFirst(Remove(issue_date)),
                "expirationDate" : getFirst(Remove(expiration_date)),
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""

            }

    elif document_type == 'irs':

        EIN_NO = []

        is_EIN = False
        other_details = []

        regex_for_EIN = r'\b\d{2}-\d{7}\b'

        # get data
        for block_no in range(len(data_array_clean)):
            block = data_array_clean[block_no]

            lines_array = list(filter(str.strip, block.splitlines()))

            for i in range(len(lines_array)):
                line = lines_array[i] 

                # find EIN number
                if is_EIN == False:
                    eins = re.findall(regex_for_EIN, line)
                    # print(eins)
                    if len(eins) >= 1 :
                        print("Found EIN number!")
                        num = eins[0].replace("o","0")
                        num = num.replace("O","0")
                        EIN_NO.append(num)
                        is_EIN = True

                lines_array[i] = line

            block =  '\n'.join(lines_array)
            data_array_clean[block_no] = block
           
        if debug:
            print("EIN_NO", (EIN_NO))

        provider_Name, bussiness_name  = get_provider_data_with_business_name_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
    
        record = {
                "licenseNumber" : getFirst(Remove(EIN_NO)),
                "licenseType":"ein_No",
                "bussinessName" : bussiness_name,
                "issueDate" : "",
                "expirationDate" : "",
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""
            }

    elif document_type == 'sdat':

        EIN_NO = []

        is_EIN = False
        other_details = []

        regex_for_EIN = r'\b\d{2}-\d{7}\b'

        # get data
        for block_no in range(len(data_array_clean)):
            block = data_array_clean[block_no]

            lines_array = list(filter(str.strip, block.splitlines()))

            for i in range(len(lines_array)):
                line = lines_array[i] 
                # print(line)

                # find EIN number
                if is_EIN == False:
                    eins = re.findall(regex_for_EIN, line)
                    # print(eins)
                    if len(eins) >= 1 :
                        print("Found EIN number!")
                        num = eins[0].replace("o","0")
                        num = num.replace("O","0")
                        EIN_NO.append(num)
                        is_EIN = True

                lines_array[i] = line

            block =  '\n'.join(lines_array)
            data_array_clean[block_no] = block
        
        provider_Name, bussiness_name  = get_provider_data_with_business_name_fromGPT(data_array_clean[0])
   
        # print("output data_array_clean: ", data_array_clean)
        if debug:
            # print("Business Name", (issue_date))
            print("EIN_NO", (EIN_NO))
            print("Bussiness Name::",bussiness_name) 


        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
    
        record = {
                "licenseNumber" : getFirst(Remove(EIN_NO)),
                "licenseType":"ein_No",
                "bussinessName" : bussiness_name,
                "issueDate" : "",
                "expirationDate" : "",
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""
            }

    elif document_type == 'accreditation':
        ID_NO = []
        is_ID = False
        issue_date = []
        date_list = []

        other_details = []

        id_identifier = [" id ", "au-id"]
        issue_identifier = ["issue"]

        # get data
        for block_no in range(len(data_array_clean)):
            block = data_array_clean[block_no]

            lines_array = list(filter(str.strip, block.splitlines()))
            # print(lines_array)

            for i in range(len(lines_array)):
                line = lines_array[i] 
                # print(line)

                # find ID number
                if is_ID == False:
                    temp_str = lines_array[i].lower()
                    if any([x in temp_str for x in id_identifier]):
                        print("Found ID!")
                        print(line)
                        if len(line.split(" ")) <= 3:
                            if ":"  in line:
                                try:
                                    id = line.split(":")[1]
                                    ID_NO.append(id.strip())
                                    line = line.replace(id,'')
                                    is_ID = True

                                except Exception as e:
                                    print(e)
                                    pass

                            else:
                                try:
                                    ID_NO.append(line)
                                    line = line.replace(line,'')
                                    is_ID = True

                                except Exception as e:
                                    print(e)
                                    pass

                # find dates
                dates = re.findall(regex_for_date, line)
                if len(dates) >= 1 :
                    date_list.extend(dates)
                    # print("dates: ", dates)
                    # print("cr line: ", line)

                    for date in dates:
                        try: 
                            temp_str = lines_array[i-1].lower() + " " + lines_array[i].lower()

                            if any([x in temp_str for x in issue_identifier]):
                                print("Found Issue date!")                                
                                try:
                                    issue_date.append(parse(date).strftime('%m-%d-%Y'))
                                    line = line.replace(date,'')
                                    date = date.replace(" ","")
                                except Exception as e:
                                    print(e)
                                    pass
                               

                        except Exception as e:
                            pass

                lines_array[i] = line

            block =  '\n'.join(lines_array)
            data_array_clean[block_no] = block

        if len(issue_date)==0:
            clean_dt = Remove(date_list)
            if len(clean_dt) > 1:
                try:
                    lowest_date, highest_date = find_lowest_highest_dates(clean_dt)
                    issue_date.append(lowest_date.strftime('%m-%d-%Y'))
                except Exception as e:
                    pass

        # print dates 
        if debug:
            print("ID", (ID_NO))
            print("Issue date", (issue_date))
            # print("Bussiness Name::",bussiness_name) 
            
        provider_Name, bussiness_name  = get_provider_data_with_business_name_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
    
        record = {
                "licenseNumber" : getFirst(Remove(ID_NO)),
                "licenseType":"accreditationNumber",
                "bussinessName" : bussiness_name,
                "issueDate" : getFirst(Remove(issue_date)),
                "expirationDate" : "",
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""
            }

    elif document_type == 'nv_state_businees_license':

        expiration_date = []
        date_list = []
        other_details = []
        expiration_identifier = ["expires", "expiration"]

        # get data
        for block_no in range(len(data_array_clean)):
            block = data_array_clean[block_no]

            lines_array = list(filter(str.strip, block.splitlines()))

            for i in range(len(lines_array)):
                line = lines_array[i] 
                # find dates
                dates = re.findall(regex_for_date, line)
                if len(dates) >= 1 :
                    date_list.extend(dates)

                    for date in dates:
                        try: 
                            temp_str = lines_array[i-1].lower() + " " + lines_array[i].lower()
                            if any([x in temp_str for x in expiration_identifier]):
                                print("Found Expires date!")
                                try:
                                    expiration_date.append(parse(date).strftime('%m-%d-%Y'))
                                    line = line.replace(date,'')
                                    date = date.replace(" ","")
                                except Exception as e:
                                    print(e)
                                    pass
                               
                        except Exception as e:
                            pass

                lines_array[i] = line

            block =  '\n'.join(lines_array)
            data_array_clean[block_no] = block

        if len(expiration_date)==0:
            clean_dt = Remove(date_list)
            if len(clean_dt) > 1:
                try:
                    lowest_date, highest_date = find_lowest_highest_dates(clean_dt)
                    expiration_date.append(highest_date.strftime('%m-%d-%Y'))
                except Exception as e:
                    pass

        provider_Name, bussiness_name  = get_provider_data_with_business_name_fromGPT(data_array_clean[0])

        # print dates 
        if debug:
            print("expiration_date", (expiration_date))
            print("Bussiness Name::",bussiness_name) 
            
        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
    
        record = {
                "licenseNumber" : None,
                "licenseType":"nv_state_businees_license",
                "bussinessName" : bussiness_name,
                "issueDate" : "",
                "expirationDate" : getFirst(Remove(expiration_date)),
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""
            }

    # Liability Certificate – Insured Name, Policy Number, Policy Effective Date, Policy Expiration Date, Coverage Limit(Per Claim Limit, Aggregate), Policy Type
    elif document_type == 'pli':

        insured_name, policy_number, policy_issue_date, policy_expiration_date, coverage_limit, policy_type = get_PLI_data_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if insured_name is not None:
            firstName, middleName, lastName  = extract_names(insured_name)

        record = {
                "licenseNumber" : policy_number,
                "licenseType":"policyNumber",
                "issueDate" : policy_issue_date,
                "expirationDate" : policy_expiration_date,
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "coverageLimit":coverage_limit,
                "boardName":"",
                "policyType": policy_type
            }


    elif document_type == 'ama':

        school_name , degree_awarded , enrollment , degree_type , degree_date , sponsoring_institution , sponsoring_state , program_name  , specialty , training_type , sponsoring_dates , sponsoring_status  = get_ama_data_fromGPT(data_array_clean[0])

 
        record = {
                # "school_name" : school_name,
                # "degree_awarded" : degree_awarded,
                # "enrollment" : enrollment,
                # "degree_type" : degree_type,
                # "degree_date" : degree_date,
                # "sponsoring_institution" : sponsoring_institution,
                # "sponsoring_state" : sponsoring_state,
                # "program_name " : program_name,
                # "specialty" : specialty,
                # "training_type" : training_type,
                # "sponsoring_dates" : sponsoring_dates,
                # "sponsoring_status" : sponsoring_status
            }
        
        record["medical_school"] = {
                "school_name" : school_name,
                "degree_awarded" : degree_awarded,
                "enrollment" : enrollment,
                "degree_type" : degree_type,
                "degree_date" : degree_date       
        }
        record["training"] = {
                "sponsoring_institution" : sponsoring_institution,
                "sponsoring_state" : sponsoring_state,
                "program_name " : program_name,
                "specialty" : specialty,
                "training_type" : training_type,
                "sponsoring_dates" : sponsoring_dates,
                "sponsoring_status" : sponsoring_status            
        }


    elif document_type.startswith('dl'):
    
        DL_NO = []
        is_DL = False
        issue_date = None
        expiration_date = None
        other_details = []
        date_list = []

        regex_for_DL = r'\b(?:[A-Z]{1,2}[0-9]{1,8}|[0-9]{7,9}|[0-9]{5}-[0-9]{5,6})\b'

        # get data
        for block_no in range(len(data_array_clean)):
            block = data_array_clean[block_no]

            lines_array = list(filter(str.strip, block.splitlines()))

            for i in range(len(lines_array)):
                line = lines_array[i] 

                # find DL number
                if is_DL == False:
                    DLs = re.findall(regex_for_DL, line)
                    # print(DLs)
                    if len(DLs) >= 1 :
                        print("Found DL number!")
                        num = DLs[0].replace("o","0")
                        num = num.replace("O","0")
                        DL_NO.append(num)
                        is_DL = True
                        line = line.replace(num,'')

                # find dates
                dates = re.findall(regex_for_date, line)
                if len(dates) >= 1 :

                    for date in dates:
                        try: 
                            date_list.append(parse(date).strftime('%m-%d-%Y'))
                            line = line.replace(date,'')
                            date = date.replace(" ","")

                        except Exception as e:
                            pass
                    
                lines_array[i] = line

            block =  '\n'.join(lines_array)
            data_array_clean[block_no] = block

        clean_dt = Remove(date_list)
        current_year = datetime.datetime.now().year                

        if len(clean_dt) > 1:
            try:
                sorted_date = find_sorted_dates(clean_dt)

                for idx, each_date in enumerate(sorted_date):
                    if idx == 0:
                        continue
                    # print("date: ", each_date)
                    year_difference = each_date.year - sorted_date[idx-1].year 
                    crr_year_difference = current_year - each_date.year  

                    if year_difference > 0 and year_difference <= 10:
                        expiration_date = each_date.strftime('%m-%d-%Y')
                        issue_date = sorted_date[idx-1].strftime('%m-%d-%Y')
                    elif year_difference > 10 and crr_year_difference >=-8:
                        issue_date = each_date.strftime('%m-%d-%Y')
            except Exception as e:
                print(e)
                pass

        elif len(clean_dt) == 1:
            try:
                year_difference = current_year - parse(clean_dt[0]).year
                if year_difference < 0:
                    expiration_date = parse(clean_dt[0]).strftime('%m-%d-%Y')
                elif year_difference >= 0 and year_difference < 50:
                    issue_date = parse(clean_dt[0]).strftime('%m-%d-%Y')
            except Exception as e:
                print(e)
                pass

        # print dates 
        if debug:
            print("clean_dt", (clean_dt))
            print("DL_NO", (DL_NO))
            print("Expiration date", (expiration_date))
            print("Issue date", (issue_date))

        
        provider_Name = get_provider_data_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)


        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
    
        record = {
                "licenseNumber" : getFirst(Remove(DL_NO)),
                "licenseType":"licenseNumber",
                "issueDate" : issue_date,
                "expirationDate" : expiration_date,
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""
            }

    elif document_type.startswith('fl'):

        License_NO = []
        is_License = False
        issue_date = []
        expiration_date = []
        License_Type = None
        date_list = []
        other_details = []

        expiration_identifier = ["expires", "expiration"]
        issue_identifier = ["issue", "start", "effective"]


        regex_for_License = r'\b\d{2}D\d{7}\b'

        # get data
        for block_no in range(len(data_array_clean)):
            block = data_array_clean[block_no]

            lines_array = list(filter(str.strip, block.splitlines()))

            for i in range(len(lines_array)):
                line = lines_array[i] 

                # find License number
                if is_License == False:
                    Licenses = re.findall(regex_for_License, line)
                    # print(Licenses)
                    if len(Licenses) >= 1 :
                        print("Found License number!")
                        num = Licenses[0].replace("o","0")
                        num = num.replace("O","0")
                        License_NO.append(num)
                        is_License = True
                        line = line.replace(num,'')

                # find dates
                dates = re.findall(regex_for_date, line)
                if len(dates) >= 1 :
                    date_list.extend(dates)

                    for date in dates:
                        try: 
                            temp_str = lines_array[i-1].lower() + " " + lines_array[i].lower()
                            if any([x in temp_str for x in expiration_identifier]):
                                print("Found Expires date!")
                                try:
                                    expiration_date.append(parse(date).strftime('%m-%d-%Y'))
                                    line = line.replace(date,'')
                                    date = date.replace(" ","")
                                except Exception as e:
                                    print(e)
                                    pass

                            elif any([x in temp_str for x in issue_identifier]):
                                print("Found Issue date!")                                
                                try:
                                    issue_date.append(parse(date).strftime('%m-%d-%Y'))
                                    line = line.replace(date,'')
                                    date = date.replace(" ","")
                                except Exception as e:
                                    print(e)
                                    pass
                               

                        except Exception as e:
                            pass              
                
                lines_array[i] = line

            block =  '\n'.join(lines_array)
            data_array_clean[block_no] = block

        if len(issue_date)==0:
            clean_dt = Remove(date_list)
            if len(clean_dt) > 1:
                try:
                    lowest_date, highest_date = find_lowest_highest_dates(clean_dt)
                    issue_date.append(lowest_date.strftime('%m-%d-%Y'))
                except Exception as e:
                    pass

        if len(expiration_date)==0:
            clean_dt = Remove(date_list)
            if len(clean_dt) > 1:
                try:
                    lowest_date, highest_date = find_lowest_highest_dates(clean_dt)
                    # print(highest_date)
                    expiration_date.append(highest_date.strftime('%m-%d-%Y'))
                except Exception as e:
                    pass

        License_Type, data_array_clean = get_license_type(data_array_clean)

        temp_License_NO = Remove(License_NO),
        temp_issue_date = Remove(issue_date),
        temp_expiration_date = Remove(expiration_date),
        
        out_License_NO = temp_License_NO[0][0] if len(temp_License_NO[0]) > 0 else None
        out_issue_date = temp_issue_date[0][0] if len(temp_issue_date[0]) > 0 else None
        out_expiration_date = temp_expiration_date[0][0] if len(temp_expiration_date[0]) > 0 else None

        if debug:
            print("License_NO", (temp_License_NO))
            print("Expiration date", (temp_issue_date))
            print("Issue date", (temp_expiration_date))
            print("License_Type::", License_Type) 
    
        provider_Name, bussiness_name, board_name, gpt_license_no, gpt_license_type  = get_provider_data_with_business_name_board_name_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
    
        record = {
                "licenseNumber" : gpt_license_no,
                "licenseType": gpt_license_type,
                "issueDate" : out_issue_date,
                "expirationDate" : out_expiration_date,
                "boardName": board_name,
                "bussinessName" : bussiness_name,
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
            }

    elif document_type.startswith('article'):
    
        is_bname = False

        provider_Name, bussiness_name  = get_provider_data_with_business_name_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        if debug:
            print("Bussiness Name::",bussiness_name) 

        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
    
        record = {
                "licenseNumber" : None,
                "licenseType":"articleNumber",
                "issueDate" : "",
                "expirationDate" : "",
                "bussinessName" : bussiness_name,
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""

            }

    elif document_type.startswith('professional_license'):

        license_no, provider_Name,out_issue_date, out_expiration_date  = get_professional_license_data_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName, lastName  = extract_names(provider_Name)

        record = {
                "licenseNumber" : license_no,
                "licenseType":"professionalLicense",
                "issueDate" : out_issue_date,
                "expirationDate" : out_expiration_date,
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""
            }

    else:
        issue_date = []
        expiration_date = []
        other_details = []
        date_list = []

        # get data
        for block_no in range(len(data_array_clean)):
            block = data_array_clean[block_no]

            lines_array = list(filter(str.strip, block.splitlines()))

            for i in range(len(lines_array)):
                line = lines_array[i] 

                if ',' in line and line.index(',') < len(line) - 1 and line[line.index(',') + 1] != ' ':
                    line = line[:line.index(',') + 1] + ' ' + line[line.index(',') + 1:]

                # find dates
                dates = re.findall(regex_for_date, line)
                if len(dates) >= 1 :

                    for date in dates:
                        try: 
                            date_list.append(parse(date).strftime('%m-%d-%Y'))
                            line = line.replace(date,'')
                            date = date.replace(" ","")

                        except Exception as e:
                            pass
                    
                lines_array[i] = line

            block =  '\n'.join(lines_array)
            data_array_clean[block_no] = block

        clean_dt = Remove(date_list)

        if len(clean_dt) > 1:
            lowest_date, highest_date = find_lowest_highest_dates(clean_dt)
            issue_date.append(lowest_date.strftime('%m-%d-%Y'))
            expiration_date.append(highest_date.strftime('%m-%d-%Y'))
        elif len(clean_dt) == 1:
            issue_date.append(clean_dt[0])

        if debug:
            print("Expiration date", (expiration_date))
            print("Issue date", (issue_date))

        # Remaining information    
        other_details = data_array_clean
        if debug:
            print("\nRemaining Data::", data_array_clean)
    

        provider_Name = get_provider_data_fromGPT(data_array_clean[0])

        firstName = None
        lastName = None
        middleName = None

        if provider_Name is not None:
            firstName, middleName,lastName  = extract_names(provider_Name)

        record = {
                "issueDate" : getFirst(Remove(issue_date)),
                "expirationDate" : getFirst(Remove(expiration_date)),
                "firstName":firstName,
                "lastName":lastName,
                "middleName":middleName,
                "boardName":""
            }

    return record
