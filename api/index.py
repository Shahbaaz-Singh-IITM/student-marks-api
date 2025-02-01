import os
import json
from http.server import BaseHTTPRequestHandler
class handler(BaseHTTPRequestHandler):
def do_GET(self):
self.send_response(200)
self.send_header("Content-Type", "text/plain")
self.end_headers()
self.wfile.write("Hello, world!".encode("utf-8"))

# Load dataset
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'marks.json')
try:
    with open(DATA_FILE, encoding='utf-8') as f:
        DATA = json.load(f)
except Exception as e:
    DATA = {}
    print("Error loading marks.json:", e)

def handler(request, response):
    try:
        # Enable CORS
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        
        # Handle OPTIONS request
        if request.method == "OPTIONS":
            response.status_code = 200
            return
        
        # Get the list of student names
        names = request.query.getlist("name")
        
        # Retrieve marks for each name (or 0 if not found)
        marks = [DATA.get(name, 0) for name in names]
        result = { "marks": marks }
        response.status_code = 200
        response.send(json.dumps(result))
    except Exception as error:
        # Send error details for debugging (you might remove detailed errors later for production)
        response.status_code = 500
        response.send(json.dumps({"error": str(error)}))
