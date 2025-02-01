from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.parse
import traceback

# Path to marks.json (assumed to be in the repository root)
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'marks.json')

# Load the JSON dataset and, if necessary, convert a list into a dictionary.
try:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    if isinstance(loaded_data, list):
        # Assuming each element is a dict with keys "name" and "mark"
        DATA = {}
        for item in loaded_data:
            if isinstance(item, dict) and "name" in item and "mark" in item:
                DATA[item["name"]] = item["mark"]
            else:
                print("Invalid item in marks.json:", item)
    elif isinstance(loaded_data, dict):
        DATA = loaded_data
    else:
        print("marks.json has unsupported format. Using empty data.")
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
            # Parse the query parameters from the URL.
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            # Get all the "name" parameters as a list.
            names = query_params.get("name", [])
            
            # For each requested name, look up its mark in DATA (defaulting to 0 if not found).
            marks = [DATA.get(name, 0) for name in names]
            result = {"marks": marks}
            
            # Prepare and send the JSON response.
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
