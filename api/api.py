# Building the http.server skeleton, implementing GET /transactions and GET /transactions/{id},implementing POST /transactions

import http.server
import socketserver
import json
import os
import urllib.parse

# Configuration
PORT = 8000
DATA_FILE = os.path.join('data', 'transactions.json')

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Simple Auth Check 
# Username and password 
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

def check_auth(headers):
    """
    Check if the request has valid Basic Auth credentials.
    Returns True if valid, False if not.
    """
    import base64
    auth_header = headers.get('Authorization')

    # If there is no Authorization header, should be rejected
    if not auth_header:
        return False

    # Authorization header looks like: "Basic YWRtaW46cGFzc3dvcmQxMjM="
    try:
        # Split "Basic <encoded>" and decode the encoded part
        encoded = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        username, password = decoded.split(":", 1)
        return username == VALID_USERNAME and password == VALID_PASSWORD
    except Exception:
        return False


class MoMoRequestHandler(http.server.BaseHTTPRequestHandler):

    # Helper method to load transactions from the JSON file
    def _load_transactions(self):
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    # Helper method to save transactions to the JSON file
    def _save_transactions(self, transactions):
        with open(DATA_FILE, 'w') as f:
            json.dump(transactions, f, indent=4)

    # Helper method to send JSON responses
    def _send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):

        # ── Auth Check ──
        if not check_auth(self.headers):
            self._send_json_response(401, {"error": "Unauthorized. Please provide valid credentials."})
            return

        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')

        # Endpoint: GET /transactions (List all)
        if parsed_path.path == '/transactions':
            transactions = self._load_transactions()
            self._send_json_response(200, transactions)
            return

        # Endpoint: GET /transactions/{id} (View one)
        elif len(path_parts) == 2 and path_parts[0] == 'transactions':
            transaction_id = path_parts[1]
            transactions = self._load_transactions()

            # Using Linear Search to find the record
            found_record = None
            for t in transactions:
                if str(t.get('id')) == str(transaction_id):
                    found_record = t
                    break

            if found_record:
                self._send_json_response(200, found_record)
            else:
                self._send_json_response(404, {"error": "Transaction not found"})
            return

        # 404 for undefined paths
        self._send_json_response(404, {"error": "Endpoint not found"})

    def do_POST(self):

        # Auth check
        if not check_auth(self.headers):
            self._send_json_response(401, {"error": "Unauthorized. Please provide valid credentials."})
            return

        # Endpoint: POST /transactions
        if self.path == '/transactions':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                new_transaction = json.loads(post_data.decode('utf-8'))

                # Validate required fields
                # Using "readable_date" to match Member 1's JSON format
                required_fields = ['type', 'body', 'readable_date', 'address']
                for field in required_fields:
                    if field not in new_transaction:
                        self._send_json_response(400, {"error": f"Missing required field: '{field}'"})
                        return

                # Load existing data to find next ID
                transactions = self._load_transactions()

                # Auto-generate ID
                max_id = 0
                for t in transactions:
                    if isinstance(t.get('id'), int) and t['id'] > max_id:
                        max_id = t['id']

                new_transaction['id'] = max_id + 1

                # Add to list and save
                transactions.append(new_transaction)
                self._save_transactions(transactions)

                # Return created record with 201 Created
                self._send_json_response(201, new_transaction)
                return

            except json.JSONDecodeError:
                self._send_json_response(400, {"error": "Invalid JSON in request body"})
                return

        self._send_json_response(404, {"error": "Endpoint not found"})

    def do_PUT(self):
 
        # Auth check
        if not check_auth(self.headers):
            self._send_json_response(401, {"error": "Unauthorized. Please provide valid credentials."})
            return
 
        # Endpoint: PUT /transactions/{id}
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
 
        if len(path_parts) == 2 and path_parts[0] == 'transactions':
            transaction_id = path_parts[1]
            transactions = self._load_transactions()
 
            for i, t in enumerate(transactions):
                if str(t.get('id')) == str(transaction_id):
                    content_length = int(self.headers['Content-Length'])
                    body = self.rfile.read(content_length)
                    updated_data = json.loads(body.decode('utf-8'))
                    transactions[i].update(updated_data)
                    self._save_transactions(transactions)
                    self._send_json_response(200, transactions[i])
                    return
 
            self._send_json_response(404, {"error": "Transaction not found"})
            return
 
        self._send_json_response(404, {"error": "Endpoint not found"})
 
    def do_DELETE(self):
 
        # Auth check
        if not check_auth(self.headers):
            self._send_json_response(401, {"error": "Unauthorized. Please provide valid credentials."})
            return
 
        # Endpoint: DELETE /transactions/{id}
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
 
        if len(path_parts) == 2 and path_parts[0] == 'transactions':
            transaction_id = path_parts[1]
            transactions = self._load_transactions()
 
            new_transactions = [t for t in transactions if str(t.get('id')) != str(transaction_id)]
 
            if len(new_transactions) == len(transactions):
                self._send_json_response(404, {"error": "Transaction not found"})
                return
 
            self._save_transactions(new_transactions)
            self._send_json_response(200, {"message": "Transaction deleted successfully"})
            return
 
        self._send_json_response(404, {"error": "Endpoint not found"})




# Start the server
def run_server():
    with socketserver.TCPServer(("", PORT), MoMoRequestHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print(f"Username: {VALID_USERNAME} | Password: {VALID_PASSWORD}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
