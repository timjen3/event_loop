import threading
import cherrypy


class CherryServer(object):
	def __init__(self):
		pass

	@cherrypy.expose
	@cherrypy.tools.json_out()
	def getValues(self, mode):
		if mode.upper() == "TASKS":
			return [
				("WOOD", 1),
				("WOOD", 1),
				("WOOD", 1),
			]
		elif mode.upper() == "RESOURCES":
			return [
				("WOOD", 100),
				("STONE", 150),
				("GOLD", 150),
			]

	@cherrypy.expose
	def putData(self, app, name, data):
		print(data)


def boot_backend_api(config_file):
	t = threading.Thread(target=lambda: cherrypy.quickstart(CherryServer(), config=config_file))
	t.daemon = True
	t.start()


if __name__ == '__main__':
	cherrypy.quickstart(CherryServer(), config="intapi.ini")
