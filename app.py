import BaseHTTPServer
import CGIHTTPServer
import webbrowser
import cgitb

PORT = 8080
script_path = "cgi-bin/index.py"

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", PORT)

httpd = server(server_address, handler)
url = 'http://localhost:{0}/{1}'.format(PORT, script_path)

webbrowser.open_new_tab(url)
print "serving at", url
httpd.serve_forever()