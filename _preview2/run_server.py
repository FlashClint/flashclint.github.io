import http.server, socketserver, os
os.chdir("D:/personal_blog/_preview2")
h = http.server.SimpleHTTPRequestHandler
h.extensions_map = h.extensions_map | {"": "text/html; charset=utf-8", ".html": "text/html; charset=utf-8", ".htm": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "application/javascript; charset=utf-8"}
s = socketserver.TCPServer(("127.0.0.1", 4000), h)
print("Server at http://127.0.0.1:4000")
s.serve_forever()
