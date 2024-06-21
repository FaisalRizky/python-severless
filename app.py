import importlib
import traceback
from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.sort_keys = False

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

if __name__ == '__main__':
    app.run(debug=True)
