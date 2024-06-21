import importlib
import os
import traceback
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "description": "API is running smoothly"
    })

@app.route('/<module>/<version>/<submodule>/<function>', methods=['GET'])
def handle_request(module, version, submodule, function):
    # Create module path
    module_path = f"{module}.{version}.{submodule}.{function}"

    try:
        # Import the module dynamically
        module = importlib.import_module(module_path)
        
        # Check if the main function exists in the module
        if hasattr(module, 'main'):
            # Call the function and return its result
            return module.main()
        else:
            raise AttributeError(f"Function 'main' not found in module '{module_path}'")

    except ModuleNotFoundError as e:
        error_message = f"Module not found: {str(e)}"
        error_detail = traceback.format_exc()
        return jsonify({"error": error_message, "details": error_detail.splitlines()}), 404

    except AttributeError as e:
        error_message = f"Attribute error: {str(e)}"
        error_detail = traceback.format_exc()
        return jsonify({"error": error_message, "details": error_detail.splitlines()}), 404

    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        error_detail = traceback.format_exc()
        return jsonify({"error": error_message, "details": error_detail.splitlines()}), 500

@app.route('/apidocs')
def api_docs():
    return render_template('apidocs.html')

@app.route('/swagger.json', methods=['GET'])
def swagger_spec():
    # Serve swagger.json file from the 'static' directory
    try:
        return send_from_directory(os.path.join(app.root_path, 'static'), 'swagger.json')
    except FileNotFoundError:
        return jsonify({"error": "swagger.json not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
