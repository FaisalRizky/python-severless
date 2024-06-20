# medical/doctor/v1/core/typeB/rs_tebet.py
import sys
import os
from bs4 import BeautifulSoup
from helper.html_data_utils import get_data_url

def get_data():
    # Get the path of the current script file, this will use for mock data purpose
    script_path = os.path.realpath(__file__)
   
    # Get Url
    # url = 'https://rstebet.co.id/jadwal-dokter/'
    url = ""

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

    # Find all elements with class 'elementor-widget-heading'
    specialities = soup.find_all(class_='elementor-widget-heading')[1:]

    # Iterate through each speciality element
    for speciality in specialities:
        speciality_name = speciality.text.strip()  # Extract text from the <h2> tag

        # Find the next sibling with class 'elementor-widget-shortcode' for schedule
        schedule_element = speciality.find_next(class_='elementor-widget-shortcode')

        if schedule_element:
            data = build_data(schedule_element, speciality_name)
            results.extend(data)
        else:
            results.append({
                'speciality': speciality_name,
                'schedule': 'Schedule not found'
            })

    return results

def build_data(schedule_element, speciality_name):
    results = []

    # Find all tables with the specified class
    tables = schedule_element.find_all('table', class_='wptb-preview-table wptb-element-main-table_setting-1384')

    # Iterate through each table
    for table in tables:
        # Find all <tr> elements within the table
        rows = table.find_all('tr')[1:]

        # Iterate through each <tr> element
        for row in rows:
            row_data = extract_row_data(row)
            if row_data:
                schedule_data = mapping_to_days(row_data)
                results.append({
                    'doctor_name': row_data[0],
                    'speciality': speciality_name,
                    'hospital_name': "RS TEBET", #This from name file
                    'hospital_type': "Type B", #This from name file
                    'schedule': schedule_data
                })

    return results

def extract_row_data(row):
    row_data = []
    p_tags = row.find_all('p')

    for p in p_tags:
        text = p.text.strip()
        if text:
            row_data.append(text)

    return row_data

def mapping_to_days(data):
    keys = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    result = {}
    default_value = "-"

    for i, key in enumerate(keys):
        if i < len(data) - 1:
            result[key] = data[i + 1]
        else:
            result[key] = default_value

    return result

