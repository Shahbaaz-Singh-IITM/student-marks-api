from http.server import BaseHTTPRequestHandler
import urllib.parse
import urllib.request
import json
import traceback

# URL for the remote JSON marks data.
MARKS_URL = "https://raw.githubusercontent.com/Shahbaaz-Singh-IITM/student-marks-api/refs/heads/main/marks.json"

def load_marks_data():
    """Fetch marks data from the remote URL and return a dictionary with lowercased keys.
       Assumes the remote JSON is an array of objects where each has "name" and "marks" keys.
    """
    try:
        with urllib.request.urlopen(MARKS_URL) as response:
            content = response.read().decode("utf-8")
            loaded_data = json.loads(content)
        # If loaded data is a list, convert it to a dictionary.
        if isinstance(loaded_data, list):
            data = {}
            for item in loaded_data:
                if isinstance(item, dict) and "name" in item and "marks" in item:
                    key = item["name"].strip().lower()
                    data[key] = item["marks"]
                else:
                    print("Invalid item in marks data:", item)
            return data
        elif isinstance(loaded_data, dict):
            # Convert keys to lowercase.
            return {str(key).strip().lower(): value for key, value in loaded_data.items()}
        else:
            print("Remote marks data has an unsupported format.")
            return {}
    except Exception as e:
        print("Error loading remote marks data:", e)
        return {}

# Load the marks data once when the module loads.
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
            # Parse the URL and extract query parameters.
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            # Extract all occurrences of "name" as a list.
            names = query_params.get("name", [])
            
            marks = []
            for name in names:
                # Normalize the query name: trim and convert to lowercase.
                lookup_name = name.strip().lower()
                mark = DATA.get(lookup_name, 0)
                marks.append(mark)
            
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
