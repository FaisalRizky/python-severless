# medical/doctor/v1/core/typeB/rs_tebet.py
import sys
import os
from bs4 import BeautifulSoup
from helper.html_data_utils import get_data_url

def get_data():
    """
    This class is used to scrape data from a URL, specifically targeting data within 
    tbody td elements. The data scraped using this class contains unique values that 
    can be used to identify the doctor, their specialty, and their schedule. These 
    unique values are represented in the data cell ID.

    This class uses these patterns to determine the relationship between the data cells 
    and extract meaningful information about doctors, their specialties, and their schedules.
    """
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
        specialities = table.find_all('tr')
        is_next_speciality_name = False

        # specialities schedulle [[speciality name, [schdules]], [speciality name, [schdules]], [speciality name, [schdules]]]
        raw_specialities_schedule = []
        current_speciality_name = '' 
        speciality_schedule = []

        row_speciality_schedule = []

        for index, speciality in enumerate(specialities):
           schedules = speciality.find_all('td')
           # Check if all empty
           all_empty = all('wpdt-empty-cell' in td['class'] for td in schedules)

           if row_speciality_schedule :
              speciality_schedule.append(row_speciality_schedule)
              row_speciality_schedule = []

           for index_1, schedule in enumerate(schedules):
            td_string = schedule.get_text(separator=" ", strip=True)
            if index == 0 and index_1 == 0:
                current_speciality_name = td_string
                break
            elif 'wpdt-merged-cell' in schedule.get('class', []) or all_empty:
                if current_speciality_name and speciality_schedule:
                    results.append([current_speciality_name , speciality_schedule])
                speciality_schedule = []
                is_next_speciality_name = True
                break
            elif is_next_speciality_name and td_string:
                current_speciality_name = td_string
                is_next_speciality_name = False
            else:
                row_speciality_schedule.append(td_string)
        results.append([current_speciality_name , speciality_schedule])
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
    # Iterate through each [Speciality name, [[Doctor schedule 1], [Doctor schedule 2]], [Doctor schedule 3]]
    for data in datas:
        # Speciality
        speciality_name = data[0]

        # Iterate through each [[Doctor schedule 1], [Doctor schedule 2]], [Doctor schedule 3]]
        for schedule in data[1]:
            # Iterate through each <tr> element
            schedule_data = mapping_to_days(schedule[1:])
            doctor_name = schedule[0]
            results.append({
                'doctor_name': doctor_name,
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

