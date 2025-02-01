from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.parse

# Compute the absolute path to marks.json in the repository root.
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'marks.json')

# Load the JSON dataset (mapping student names to marks).
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
        # Set response status and headers (including CORS)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        # Parse the query string from self.path
        # For example, if the URL is /api?name=Alice&name=Bob
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        names = query_params.get("name", [])
        
        # Look up each name in the dataset (defaulting to 0 if not found)
        marks = [DATA.get(name, 0) for name in names]
        response = {"marks": marks}

        # Send the JSON response
        self.wfile.write(json.dumps(response).encode("utf-8"))
