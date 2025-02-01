from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.parse
import traceback

# Determine the absolute path to marks.json in the repository root.
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'marks.json')

# Load the JSON dataset from marks.json.
try:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        DATA = json.load(f)
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
            # Parse the query parameters from the request URL.
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            # Get all "name" query parameters as a list.
            names = query_params.get("name", [])
            
            # For each provided name, lookup the corresponding mark in DATA.
            # If a name is not found, 0 is returned as default.
            marks = [DATA.get(name, 0) for name in names]
            result = {"marks": marks}
            
            # Prepare the JSON response.
            response_data = json.dumps(result)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response_data.encode("utf-8"))
        except Exception as e:
            # Print the traceback for debugging.
            error_details = traceback.format_exc()
            print(error_details)
            # Return a JSON error response.
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode("utf-8"))
