import gui.api.controllers.resources as ResourceApi
import threading
import cherrypy


class CherryServer(object):
	def __init__(self):
		# TODO: start up an event loop instance and serve data to gui
		self.controllers = {
			"flatui": ResourceApi.CherryServer()
		}

	def _cp_dispatch(self, vpath):
		print(vpath)
		if len(vpath) == 1:
			return self
		if vpath[1] in self.controllers:
			return self.controllers.get(vpath[1])

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
