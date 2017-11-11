from api.intapi import boot_server
import webview
import sys


if __name__ == '__main__':
	boot_server("api/intapi.ini")
	webview.create_window("My first HTML5 application", "http://127.0.0.1:8080/index.html")
	sys.exit()
