from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.parse
import traceback

# Determine the absolute path to marks.json, assumed to be one folder above this file.
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'marks.json')

# Load the JSON dataset from marks.json.
try:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    # If the loaded data is a list, convert it into a dictionary.
    if isinstance(loaded_data, list):
        DATA = {}
        for item in loaded_data:
            if isinstance(item, dict) and "name" in item and "mark" in item:
                # Convert keys to lowercase for case-insensitive matching.
                DATA[item["name"].lower()] = item["mark"]
            else:
                print("Invalid item in marks.json:", item)
    elif isinstance(loaded_data, dict):
        # Create a new dictionary with lowercase keys.
        DATA = {key.lower(): value for key, value in loaded_data.items()}
    else:
        print("marks.json has an unsupported format. Using empty dataset.")
        DATA = {}
except Exception as e:
    print("Error loading marks.json:", e)
    DATA = {}

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        try:
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET,OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
        except Exception as e:
            error_details = traceback.format_exc()
            print(error_details)
            self.send_error(500, str(e))

    def do_GET(self):
        try:
            # Parse the URL to extract query parameters.
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            # Get all occurrences of "name" as a list.
            names = query_params.get("name", [])
            
            # Convert each name in the query parameters to lowercase before lookup.
            marks = [DATA.get(name.strip().lower(), 0) for name in names]
            result = {"marks": marks}
            
            response_data = json.dumps(result)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response_data.encode("utf-8"))
        except Exception as e:
            error_details = traceback.format_exc()
            print(error_details)
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode("utf-8"))
