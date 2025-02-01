from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.parse

# Determine the path to marks.json located one folder above this file.
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'marks.json')

# Attempt to load the JSON dataset.
try:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        DATA = json.load(f)
except Exception as e:
    print("Error loading marks.json:", e)
    DATA = {}

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS preflight requests.
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        # Parse the URL to extract query parameters.
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        # Gets all occurrences of the 'name' parameter as a list.
        names = query_params.get("name", [])

        # Lookup each name in the dataset (defaulting to 0 if not found).
        marks = [DATA.get(name, 0) for name in names]
        result = {"marks": marks}

        # Prepare JSON response.
        response_data = json.dumps(result)

        # Send HTTP status and headers.
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        # Write the JSON response.
        self.wfile.write(response_data.encode("utf-8"))
