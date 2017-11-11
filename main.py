"""
	FIRST MILESTONE: GET FOUNDATIONAL COMPONENTS WORKING AS PROOF OF CONCEPT
		COMPLETED 11/11/2017: LAUNCH main.py WITH OPTIONAL ARGUMENTS
	SECOND MILESTONE: GET EVENT LOOP GUI BUILT AND 1 API CALL FOR READ ONLY VIEW OF DATA IN LOCALHOST ENVIRONMENT
	THIRD MILESTONE: ADD UI COMPONENTS FOR INTERACTIVITY WITH EVENT LOOP
	FOURTH MILESTONE: GET APP WORKING TO SERVE REMOTE CLIENTS
"""
from gui.api.intapi import boot_backend_api
import argparse
import webview
import sys


def serve_app(app, bind="127.0.0.1", port=8080, **kwargs):
	"""default is to load main app and bind to localhost:8080."""
	if app:
		full_url = "http://{bind}:{port}/{app}/index.html".format(bind=bind, port=port, app=app)
	else:
		full_url = "http://{bind}:{port}/index.html".format(bind=bind, port=port, app=app)
		app = "Main"
	webview.create_window(title=app, url=full_url)
	sys.exit(0)


def branch_app():
	parser = argparse.ArgumentParser()
	parser.add_argument("--app", type=str, default="", choices=["tetris", "flatui"], help="exclude arg to load main app")

	subparsers = parser.add_subparsers()
	remote_parser = subparsers.add_parser("remote")
	remote_parser.add_argument("--bind", type=str, help="what address to bind server to")
	remote_parser.add_argument("--port", type=int, help="what port to bind server to")

	argvs = parser.parse_args()

	serve_app(**vars(argvs))


if __name__ == "__main__":
	# start launching server
	boot_backend_api("gui/api/intapi.ini")

	# process cmd args
	branch_app()
