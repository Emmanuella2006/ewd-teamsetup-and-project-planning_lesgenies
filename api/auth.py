from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import base64
import re

DATA_STORE = [
    {"id": "1", "type": "payment", "amount": 500.0, "sender": "Alice", "receiver": "Bob", "timestamp": "2026-05-27T12:00:00Z"}
]
# For fast lookup
DICTIONARY_STORE = {item["id"]: item for item in DATA_STORE}
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123" 
# hardcorded username and password

class SecureMoMoAPI(BaseHTTPRequestHandler):

    def check_auth(self):
        # Validate basic http authentication
        authentication_header = self.headers.get('Authorization')
        if not authentication_header or not authentication_header.startswith('Basic '):
            return False

        try:
            # Decode the base64 credentials
            encoded_creds = authentication_header.split(' ')[1]
            decoded_creds = base64.b64decode(encoded_creds).decode('utf-8')
            username, password = decoded_creds.split(':', 1)
            return username == VALID_USERNAME and password == VALID_PASSWORD
        except Exception:
            return False

    def send_unauthorized(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Unauthorized"}).encode('utf-8'))

    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


    def do_PUT(self):
        if not self.check_auth():
            return self.send_unauthorized()

        match = re.match(r'^/transactions/([^/]+)$', self.path)
        if match:
            tx_id = match.group(1)
            if tx_id not in DICTIONARY_STORE:
                return self.send_json_response(404, {"error": "Transaction not found"})

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            updated_data = json.loads(body.decode('utf-8'))

            # Update both structures
            DICTIONARY_STORE[tx_id].update(updated_data)
            return self.send_json_response(200, DICTIONARY_STORE[tx_id])

        self.send_json_response(404, {"error": "Route not found"})

    def do_DELETE(self):
        if not self.check_auth():
            return self.send_unauthorized()

        match = re.match(r'^/transactions/([^/]+)$', self.path)
        if match:
            tx_id = match.group(1)
            if tx_id in DICTIONARY_STORE:
                # Remove from both data structures
                del DICTIONARY_STORE[tx_id]
                global DATA_STORE
                DATA_STORE = [tx for tx in DATA_STORE if tx['id'] != tx_id]
                return self.send_json_response(200, {"message": "Transaction deleted successfully"})
            return self.send_json_response(404, {"error": "Transaction not found"})

        self.send_json_response(404, {"error": "Route not found"})


def run(server_class=HTTPServer, handler_class=SecureMoMoAPI, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == '__main__':
    run()

