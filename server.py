from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL and query parameters
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Check if the path is /oauthredirect and handle accordingly
        if parsed_path.path == "/oauthredirect":
            self.handle_oauth_redirect(query_params)
        else:
            self.handle_not_found()

    def handle_oauth_redirect(self, params):
        # Log the parameters
        print("Received parameters:")
        for key, value in params.items():
            print(f"{key}: {value}")

        # Respond to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Parameters received and logged.")

    def handle_not_found(self):
        # Respond with a 404 Not Found if path is not /oauthredirect
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Not Found")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server starting on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
