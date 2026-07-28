import http.server
import socketserver
import os

PORT = 4000
DIR = "D:/personal_blog/_preview2"

class UTF8HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    
    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isfile(path):
            # Get the default response
            response = super().send_head()
            # For HTML files, ensure UTF-8 charset
            if path.endswith(('.html', '.htm')):
                self.send_header("Content-Type", "text/html; charset=utf-8")
            elif path.endswith('.css'):
                self.send_header("Content-Type", "text/css; charset=utf-8")
            elif path.endswith('.js'):
                self.send_header("Content-Type", "application/javascript; charset=utf-8")
            elif path.endswith('.json'):
                self.send_header("Content-Type", "application/json; charset=utf-8")
        return response

    def end_headers(self):
        # Ensure charset for HTML
        if self.path.endswith(('.html', '.htm')):
            self.send_header("Content-Type", "text/html; charset=utf-8")
        super().end_headers()

os.chdir(DIR)
server = socketserver.TCPServer(("127.0.0.1", PORT), UTF8HTTPRequestHandler)
print(f"Preview server at http://127.0.0.1:{PORT}")
server.serve_forever()
