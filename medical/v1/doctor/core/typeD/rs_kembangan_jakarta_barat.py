# medical/doctor/v1/core/typeD/rs_kembangan_jakarta_barat.py
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
    url = 'https://www.rsukembangan.com/#'

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
        
        for doctor_list in doctor_lists:
            doctor_details = doctor_list.find_all('td')
           
            row_details = []
            # Get doctor info
            for doctor_detail in doctor_details:
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
    # Iterate through each data [1, dr. Derfiani Prinanda H, Sp.N, SARAF, 08.00 - 12.00, -, -, -, 13.30 - 16.00, -]
    for data in datas:
        speciality_name = data[2]
        doctor_name = data[1]
        schedule_data = mapping_to_days(data[3:])
        results.append({
                    'doctor_name': doctor_name,
                    'speciality': 'Spesialis '+ speciality_name,
                    'hospital_name': "RSUD Kembangan Jakarta Barat",  # This is from the file name
                    'hospital_type': "Type D",  # This is from the file name
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
