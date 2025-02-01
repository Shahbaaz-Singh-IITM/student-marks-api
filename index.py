import json
import os

# Load the JSON dataset when the function is loaded.
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')
with open(DATA_FILE, encoding='utf-8') as f:
    DATA = json.load(f)

def handler(request, response):
    # Set CORS headers to allow GET requests from any origin.
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        response.status_code = 200
        return

    # Extract query parameters 'name'. The "getlist" method is used to retrieve multiple parameters.
    names = request.query.getlist("name")
    # Retrieve marks for each queried name (defaulting to 0 if a name is not found)
    marks = [DATA.get(name, 0) for name in names]

    # Create a JSON response
    result = { "marks": marks }
    response.status_code = 200
    response.send(json.dumps(result))