# medical/doctor/v1/core/typeA/rs_kariadi_semarang.py
import sys
import os
from bs4 import BeautifulSoup
from helper.html_data_utils import get_data_url
from helper.logger_utils import write_response_from_scrap

def get_data():
    """
    This class is used to scrape data from a URL, specifically targeting data within 
    tbody td elements. The data scraped using this class contains unique values that 
    can be used to identify the doctor, their specialty, and their schedule. These 
    unique values are represented in the data cell ID.

    This class uses these patterns to determine the relationship between the data cells 
    and extract meaningful information about doctors, their specialties, and their schedules.
    """
    # Get the path of the current script file for mock data purposes
    script_path = os.path.realpath(__file__)
   
    # URL to scrape
    url = 'https://perjanjian.rskariadi.id/Admission/JadwalDokterView'

    # Get HTML content from the URL
    html_content = get_data_url(url, script_path)

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get the doctor's specialty schedule
    speciality_schedule = get_speciality_schedule(soup)

    # Write Data result
    write_response_from_scrap(speciality_schedule, script_path)

    # Return the JSON formatted results
    return speciality_schedule

def get_speciality_schedule(soup):
    results = []

    # Find all tables with id 'wpdtSimpleTable-1'
    tables = soup.find_all('tbody')
    
    for table in tables:
        # Get all rows in the table
        doctor_lists = table.find_all('tr')
        
        for doctor_list in doctor_lists[1:]:
            doctor_details = doctor_list.find_all('td')
            row_details = []
            # Get doctor info
            for index, doctor_detail in enumerate(doctor_details):
                # Get all <span> elements within the <td> and collect their text
                if index == 1 or index == 0:
                    column_details =  doctor_detail.find_all('span')
                    column_details_data =  []
                    for column_detail in column_details:
                        column_details_data.append(column_detail.get_text(strip=True))
                    row_details.append(column_details_data)
                else:
                    row_details.append(doctor_detail.get_text(strip=True))
            results.append(row_details)
    if results:
        results = build_data(results)
    else:
        results.append({
            'speciality': 'Speciality not found',
            'schedule': 'Schedule not found'
        })

    return results

def build_data(datas):
    results = []
    # Iterate through each data
    for data in datas:
        speciality_name = data[0][1]
        doctor_name = data[0][0]
        schedule_data = mapping_to_days(data[3:])
        results.append({
                    'doctor_name': doctor_name,
                    'speciality': speciality_name,
                    'hospital_name': "RS Kariadi Semarang",  # This is from the file name
                    'hospital_type': "Type A",  # This is from the file name
                    'schedule': schedule_data
                })
    return results

def mapping_to_days(data):
    keys = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    result = {}
    default_value = "-"

    for i, key in enumerate(keys):
        if i < len(data):
            if data[i] == "":
                result[key] = default_value
            else:
                result[key] = data[i]
        else:
            result[key] = default_value

    return result
