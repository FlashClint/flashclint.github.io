import http.server, socketserver, os
os.chdir("D:/personal_blog/_preview2")
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.path.endswith((".html", ".htm")):
            self.send_header("Content-Type", "text/html; charset=utf-8")
        super().end_headers()
s = socketserver.TCPServer(("127.0.0.1", 4000), H)
print("Server at http://127.0.0.1:4000")
s.serve_forever()
