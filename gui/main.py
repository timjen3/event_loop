""""
	REF: https://github.com/r0x0r/pywebview/blob/master/examples/http_server.py
"""
import threading
import webview
import sys


try:
	from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
	from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
	from http.server import SimpleHTTPRequestHandler, HTTPServer


def start_server():
	HandlerClass = SimpleHTTPRequestHandler
	ServerClass = HTTPServer
	Protocol = "HTTP/1.0"
	port = 23948
	server_address = ('127.0.0.1', port)

	HandlerClass.protocol_version = Protocol
	httpd = ServerClass(server_address, HandlerClass)
	httpd.serve_forever()


if __name__ == '__main__':
	t = threading.Thread(target=start_server)
	t.daemon = True
	t.start()

	webview.create_window("My first HTML5 application", "http://127.0.0.1:23948")

	# do clean up procedure and destroy any remaining threads after the window is destroyed
sys.exit()
