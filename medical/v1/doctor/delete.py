import os
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

def cleanup_cache(directory):
    """
    Removes all cached files in the specified directory except those
    with today's date in the filename.
    """
    today_str = datetime.now().strftime('%Y-%m-%d')
    try:
        for subdir, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    # Extract date from filename
                    filename, file_date = file.rsplit('_', 1)
                    file_date = file_date.split('.')[0]  # Remove .json extension
                    
                    # Check if the file date does not match today's date
                    if file_date != today_str:
                        os.remove(os.path.join(subdir, file))
        return jsonify({
                        'status' : 'Success',
                        'message': 'Cache cleanup completed successfully.'                     
                       })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    """Endpoint to clean up old cached files except for today's files."""
    cache_directory = 'logger/medical/v1/doctor/core'  # Update this path if needed
    return cleanup_cache(cache_directory)

if __name__ == "__main__":
    app.run(debug=True)
