from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from twilio.rest import Client
from dotenv import load_dotenv
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/oauthredirect":
            self.handle_oauth_redirect(query_params)
        else:
            self.handle_not_found()

    def handle_oauth_redirect(self, params):
        # Prepare SMS content
        sms_content = "\n".join([f"{key}: {','.join(value)}" for key, value in params.items()])
        self.send_sms(sms_content)

        # Respond to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"SMS sent with parameters.")

    def handle_not_found(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Not Found")

    def send_sms(self, message):
        # Your Account SID and Auth Token from twilio.com/console
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)

        # Sending SMS
        message = client.messages.create(
            body=message,
            from_=os.environ.get('TWILIO_NUMBER'),
            to=os.environ.get('DST_NUMBER')
        )
        print(message.sid)

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    load_dotenv()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server starting on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
