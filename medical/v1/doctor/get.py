from flask import Flask, jsonify
import importlib
import pkgutil
from lib.response_utils import build_success_response
from medical.v1.doctor.core.TypeB import __path__ as typeB_path

app = Flask(__name__)

def get_doctors_schedule():
    data = None
    
    # Dynamically load and call the get_data function from each module in TypeB
    for module_info in pkgutil.iter_modules(typeB_path):
        if module_info.ispkg:
            continue
        module_name = f"medical.v1.doctor.core.TypeB.{module_info.name}"
        module = importlib.import_module(module_name)
        if hasattr(module, 'get_data'):
            module_data = module.get_data()
            if module_data:
                data= module_data

    # Use build_success_response to structure the response
    response = build_success_response(data_list=data)
    return jsonify(response)

def main():
    # Additional logic if needed
    return get_doctors_schedule()
