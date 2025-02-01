from http.server import BaseHTTPRequestHandler
import urllib.parse
import urllib.request
import json
import traceback

# URL of the raw JSON marks file.
MARKS_URL = "https://raw.githubusercontent.com/Shahbaaz-Singh-IITM/student-marks-api/refs/heads/main/marks.json"

def load_marks_data():
    """Fetch and return the marks data from the remote URL.
       If the data is a list (each element with "name" and "mark"), convert it to a dict.
       Otherwise, if it is already a dict, return as is.
    """
    try:
        with urllib.request.urlopen(MARKS_URL) as response:
            content = response.read().decode("utf-8")
            loaded_data = json.loads(content)
        if isinstance(loaded_data, list):
            data = {}
            for item in loaded_data:
                if isinstance(item, dict) and "name" in item and "mark" in item:
                    data[item["name"]] = item["mark"]
                else:
                    print("Invalid item in remote marks data:", item)
            return data
        elif isinstance(loaded_data, dict):
            return loaded_data
        else:
            print("Remote marks.json has an unsupported format.")
            return {}
    except Exception as e:
        print("Error loading remote marks.json:", e)
        return {}

# Load the marks data once, when the module is imported.
DATA = load_marks_data()
print("Loaded DATA keys:", list(DATA.keys()))

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
            # Parse query parameters from the URL.
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            # Extract all "name" parameters as a list.
            names = query_params.get("name", [])
            
            marks = []
            for name in names:
                orig_name = name.strip()
                # First try an exact lookup.
                mark = DATA.get(orig_name)
                if mark is None:
                    # If not found, try by converting to lowercase.
                    mark = DATA.get(orig_name.lower(), 0)
                marks.append(mark if mark is not None else 0)
            
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
