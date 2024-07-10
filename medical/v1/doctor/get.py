from flask import Flask, jsonify, request
import importlib
import pkgutil
import os
import json
from datetime import datetime
from helper.response_utils import build_success_response
from medical.v1.doctor.core.typeA import __path__ as typeA_path
from medical.v1.doctor.core.typeB import __path__ as typeB_path
from medical.v1.doctor.core.typeC import __path__ as typeC_path
from medical.v1.doctor.core.typeD import __path__ as typeD_path

app = Flask(__name__)

# Function to get the module path and name based on the hospital type
def get_module_details(hospital_type):
    """Return the module path and name based on the hospital type."""
    if hospital_type == 'A':
        return typeA_path, "medical.v1.doctor.core.typeA"
    elif hospital_type == 'B':
        return typeB_path, "medical.v1.doctor.core.typeB"
    elif hospital_type == 'C':
        return typeC_path, "medical.v1.doctor.core.typeC"
    elif hospital_type == 'D':
        return typeD_path, "medical.v1.doctor.core.typeD"
    else:
        return None, None

# Function to check if the log file for the current date exists
def check_log_file(module_name, filename):
    """Check if the log file for the current date exists."""
    log_dir = f"logger/{module_name.replace('.', '/')}"
    if not os.path.exists(log_dir):
        return None
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"{filename}_{current_date}.json")
    return log_file if os.path.exists(log_file) else None

# Function to load and process modules, filtering data based on hospital name if provided
def load_and_process_modules(module_name, path, hospital_name, data_list):
    """Load and process modules, optionally filtering by hospital name."""
    for module_info in pkgutil.iter_modules(path):
        if module_info.ispkg:
            continue
        full_module_name = f"{module_name}.{module_info.name}"
        log_file = check_log_file(module_name, module_info.name)
        if log_file:
            with open(log_file, 'r') as f:
                module_data = json.load(f)
            data_list.extend(module_data)
        else:
            module = importlib.import_module(full_module_name)
            if hasattr(module, 'get_data'):
                module_data = module.get_data()
                if module_data:
                    if hospital_name:
                        # Filter data to include only items where hospital_name is like the specified hospital_name
                        filtered_data = [item for item in module_data if hospital_name.lower() in item.get('hospital_name', '').lower()]
                        data_list.extend(filtered_data)
                    else:
                        data_list.extend(module_data)
                    # Save the data to the log file for future use
                    os.makedirs(os.path.dirname(log_file), exist_ok=True)
                    with open(log_file, 'w') as f:
                        json.dump(module_data, f)

# Function to process modules based on given parameters, dynamically load if not specified
def process_modules(module_name=None, path=None, hospital_name=None):
    """Process modules based on the provided parameters."""
    data_list = []
    if module_name and path:
        load_and_process_modules(module_name, path, hospital_name, data_list)
    else:
        # Dynamically load and call the get_data function from each module in typeA, typeB, typeC, and typeD
        for type_path, type_module_name in [(typeA_path, "medical.v1.doctor.core.typeA"),
                                            (typeB_path, "medical.v1.doctor.core.typeB"),
                                            (typeC_path, "medical.v1.doctor.core.typeC"),
                                            (typeD_path, "medical.v1.doctor.core.typeD")]:
            load_and_process_modules(type_module_name, type_path, hospital_name, data_list)
    return data_list

# Function to get doctors' schedules based on hospital type and name
def get_doctors_schedule(hospital_type=None, hospital_name=None):
    """Get doctors' schedule based on hospital type and name."""
    path, module_name = get_module_details(hospital_type)

    if not hospital_type and not hospital_name:
        # If all params are empty, process all modules
        data_list = process_modules()
    elif not hospital_type and hospital_name:
        # If hospital type not specified but hospital name is, process all types and find the desired name
        data_list = process_modules(hospital_name=hospital_name)
    elif hospital_type and not hospital_name:
        # If only hospital_type is specified, process all hospital names in the specified type
        data_list = process_modules(module_name, path)
    elif hospital_type and hospital_name:
        # Process the specific type and hospital name
        data_list = process_modules(module_name, path, hospital_name)
    else:
        data_list = []

    # Use build_success_response to structure the response
    response = build_success_response(data_list=data_list)
    return jsonify(response)

@app.route('/get_doctors_schedule', methods=['GET'])
def main():
    """Main route to handle the request and return doctors' schedules."""
    # Query Params
    type_param = request.args.get('type')
    rs_name_param = request.args.get('hospital_name')
    return get_doctors_schedule(type_param, rs_name_param)

if __name__ == "__main__":
    app.run(debug=True)
