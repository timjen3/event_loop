"""Starts specified number of event loops with an arbitrary number of tasks loaded in. Processes all the tasks.
On shutdown, persists remaining tasks."""
from engine.persistence import ProgressStore
from engine.event_loop import EventLoop
from random import randint
__VERSION__ = 1.0


class DummyTask:
	RESOURCES = dict()
	TICKS = {
		"WOOD": 2,
		"STONE": 4,
		"GOLD": 10,
	}

	def __init__(self, name, display, evt=None):
		self.name = name
		self.display = display
		self.ticks = self.TICKS[name]
		self.negligable = 0
		self.evt = evt

	def process(self, evt_loop):
		result = randint(1, 10)
		evt_loop.RESOURCES[self.name] += result
		if self.display:
			print("Mined: n: {:10s} | d: {:6}".format(self.name, result))
		# additional callback. may be removed
		if self.evt is not None:
			self.evt()


def multi_thread_demo(display):
	"""Creates isolated event loops where each one processes 100 * args['powers'] tasks and generates
	its own resource pile. This method appears to scale up fairly well but has hard-limits based on
	maximum number of threads on the machine."""
	all_loops = list()
	print("Loading event loops...overdue backlog will be cleared...")
	for i_ in range(0, args["loops"]):
		el = EventLoop(uid=str(i_))
		all_loops.append(el)
		el.do_tasks()
		for s_i_ in range(0, args["powers"]):
			for s_i_n_ in range(0, 100):
				t_1 = DummyTask(name="WOOD", display=display)
				el.add_task(task=t_1)
		print("LOADED: {}".format(str(i_)))
		el.do_tasks()
		print("READY: {}".format(str(i_)))
	print("Completed overdue tasks from disk.")
	print("Booting up threads...")
	EventLoop.bootup()
	print("Boot complete.")
	for l_ in all_loops:
		l_.start()
	print("COMMAND ?:")
	while input().lower() not in ("q", "quit"):
		print("COMMAND ?:")


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('-h', '--help', '--about', action='help', default=argparse.SUPPRESS, help='multi-threaded schedulable task processor')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__VERSION__), help="Show program's version number and exit.")
	parser.add_argument("--loops", dest="loops", type=int, default=1, required=False, help="number of event loops to start")
	parser.add_argument("--powers", dest="powers", type=int, default=4, required=False, help="tasks w/ticks at powers of 2")
	parser.add_argument("--runtime", dest="runtime", type=int, default=10, required=False, help="time in seconds to run")
	parser.add_argument("--display", dest="display", type=bool, default=False, required=False, help="whether to display individual mining results")
	args = vars(parser.parse_args())

	multi_thread_demo(display=args["display"])

	print("Shutting down engine...")
	EventLoop.shutdown()
	print("Shutdown complete.")

	print(EventLoop.RESOURCES)

	print("Flushing remaining tasks to disk.")
	ProgressStore.sync()
	print("Flush complete.")
