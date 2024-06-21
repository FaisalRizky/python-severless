from flask import Flask, jsonify
import importlib
import pkgutil
from helper.response_utils import build_success_response
from medical.v1.doctor.core.typeB import __path__ as typeB_path
from medical.v1.doctor.core.typeC import __path__ as typeC_path

app = Flask(__name__)

def get_doctors_schedule():
    data_list = []
    # # Dynamically load and call the get_data function from each module in typeB
    for module_info in pkgutil.iter_modules(typeB_path):
        if module_info.ispkg:
            continue
        module_name = f"medical.v1.doctor.core.typeB.{module_info.name}"
        module = importlib.import_module(module_name)
        if hasattr(module, 'get_data'):
            module_data = module.get_data()
            if module_data:
                data_list.extend(module_data)  # Combine data

    # Dynamically load and call the get_data function from each module in typeC
    for module_info in pkgutil.iter_modules(typeC_path):
        if module_info.ispkg:
            continue
        module_name = f"medical.v1.doctor.core.typeC.{module_info.name}"
        module = importlib.import_module(module_name)
        if hasattr(module, 'get_data'):
            module_data = module.get_data()
            if module_data:
                data_list.extend(module_data)  # Combine data

    # Use build_success_response to structure the response
    response = build_success_response(data_list=data_list)
    return jsonify(response)

def main():
    # Additional logic if needed
    return get_doctors_schedule()

if __name__ == "__main__":
    app.run(debug=True)
