import threading
import cherrypy
import json


class CherryServer(object):
	def __init__(self):
		pass

	# @cherrypy.expose
	# def index(self):
	# 	return open("app_web/index.html").read()

	@cherrypy.expose
	def getData(self):
		return json.dumps(
			{
				"derp": 1,
				"derp derp": 2,
			},
			sort_keys=True
		)

	@cherrypy.expose
	def putData(self, app, name, data):
		print(data)


def boot_backend_api(config_file):
	server = lambda c_=config_file: cherrypy.quickstart(CherryServer(), config=c_)
	t = threading.Thread(target=server)
	t.daemon = True
	t.start()


if __name__ == '__main__':
	cherrypy.quickstart(CherryServer(), config="intapi.ini")
