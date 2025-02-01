import os
import json

# Determine the path to marks.json at the repository root.
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'marks.json')

# Try to load the JSON data when the module is imported.
try:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        DATA = json.load(f)
except Exception as e:
    # Log error and default to an empty dataset.
    print("Error loading marks.json:", e)
    DATA = {}

def handler(request, response):
    try:
        # Set CORS headers to allow requests from any origin.
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET,OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"

        # Handle preflight OPTIONS request.
        if request.method == "OPTIONS":
            response.status_code = 200
            return

        # Extract the 'name' query parameter(s)
        # request.query may provide getlist() or just a dictionary.
        if hasattr(request.query, "getlist"):
            names = request.query.getlist("name")
        else:
            # If multiple names are provided as comma‐separated, split them.
            names = request.query.get("name", "")
            names = names.split(",") if names else []

        # For each provided name, lookup the mark; default is 0 when not found.
        marks = [DATA.get(name, 0) for name in names]

        # Create the JSON response.
        result = {"marks": marks}
        response.status_code = 200
        response.send(json.dumps(result))
    except Exception as err:
        # In case of error, respond with a 500 and the error message.
        response.status_code = 500
        response.send(json.dumps({"error": str(err)}))
