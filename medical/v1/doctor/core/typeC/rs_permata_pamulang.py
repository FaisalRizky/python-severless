# medical/doctor/v1/core/typeB/rs_tebet.py
import sys
import os
from bs4 import BeautifulSoup
from helper.html_data_utils import get_data_url

def get_data():
    # Get the path of the current script file, this will use for mock data purpose
    script_path = os.path.realpath(__file__)
   
    # Get Url
    url = 'https://rspermatapamulang.co.id/jadwal-dokter/'

    # Get Html Content
    html_content = get_data_url(url, script_path)

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get Doctor Speciality Schedule
    speciality_schedule = get_speciality_schedule(soup)

    # Return the JSON formatted results
    return speciality_schedule

def get_speciality_schedule(soup):
    results = []

    # Find all elements with id 'wpdtSimpleTable-1' Table
    tables = soup.find_all(id='wpdtSimpleTable-1')
    
    for table in tables:
        # rows represent row table
        rows = table.find_all('td')
        previous_element = ""
        group_data = []
        for row in rows:
            # used to determine the schdule speciality of each doctor
            cell_id = row.get('data-cell-id')
            text_row = row.text.strip()
            if len(cell_id) == len(previous_element) and len(cell_id) == 2 and cell_id[1] == previous_element[1]:
                group_data.append(row.text.strip())
            elif len(cell_id) == len(previous_element)  and len(cell_id) != 2  and cell_id[1:-1] == previous_element[1:-1]:
                group_data.append(row.text.strip())
            else:
                previous_element = cell_id
                if group_data:
                    results.append(group_data)
                group_data = []
                group_data.append(row.text.strip())
        results.append(group_data)
    if results:
       results = build_data(results)
    else:
        results.append({
            'speciality': speciality_name,
            'schedule': 'Schedule not found'
        })
    return results

def build_data(datas):
    results = []

    # Remove first row of table
    speciality_name = datas[0][0]
    # Iterate through each table
    for data in datas[1:]:
        # Iterate through each <tr> element
        schedule_data = mapping_to_days(data)
        results.append({
            'doctor_name': data[0],
            'speciality': speciality_name,
            'hospital_name': "RS PERMATA PAMULANG", #This from name file
            'hospital_type': "Type C", #This from name file
            'schedule': schedule_data
        })

    return results

def mapping_to_days(data):
    keys = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    result = {}
    default_value = "-"

    for i, key in enumerate(keys):
        if i < len(data) - 1:
            if data[i + 1] == "":
                result[key] = default_value
            else:
                result[key] = data[i + 1]
        else:
            result[key] = default_value

    return result

