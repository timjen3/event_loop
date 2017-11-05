"""Starts specified number of event loops with an arbitrary number of tasks loaded in. Processes all the tasks.
On shutdown, persists remaining tasks. Gui demo shows """
from engine.persistence import ProgressStore
from engine.event_loop import EventLoop
from random import randint
from gui.plots import Gui
__VERSION__ = 1.0


class DummyTask:
	RESOURCES = dict()

	def __init__(self, name, amt, ticks):
		self.name = name
		self.amt = amt
		self.ticks = ticks
		self.negligable = 0

	def process(self, evt_loop):
		evt_loop.RESOURCES[self.name] += self.amt
		# print("DONE: n: {:.3s} | t:{:8}s".format(self.name, self.ticks))


def single_thread_demo(plot):
	print("Processing overdue tasks")
	all_loops = list()
	el = EventLoop(uid=str("gui"))
	all_loops.append(el)
	el.do_tasks()
	print("Completed overdue tasks from disk.")
	for s_i_ in range(0, args["powers"]):
		for s_i_n_ in range(0, 1000):
			t_1 = DummyTask(name="{}.{}".format("gui", s_i_), amt=1, ticks=2 ** s_i_)
			t_2 = DummyTask(name="{}.{}".format("gui", s_i_), amt=1, ticks=2 * s_i_n_)
			some_num_ = randint(1, 100)
			t_3 = DummyTask(name="{}.{}".format("gui", s_i_), amt=1, ticks=some_num_)
			el.add_task(task=t_1)
			el.add_task(task=t_2)
			el.add_task(task=t_3)
	print("Booting up threads...")
	EventLoop.bootup()
	print("Boot complete.")
	if plot:
		Gui(method=el.get_update).start()


def multi_thread_demo():
	all_loops = list()
	print("Loading event loops...overdue backlog will be cleared...")
	for i_ in range(0, args["loops"]):
		el = EventLoop(uid=str(i_))
		all_loops.append(el)
		el.do_tasks()
		for s_i_ in range(0, args["powers"]):
			for s_i_n_ in range(0, 1000):
				t_1 = DummyTask(name="{}.{}".format(i_, s_i_), amt=1, ticks=2 ** s_i_)
				el.add_task(task=t_1)
		print("LOADED: {}".format(str(i_)))
		el.do_tasks()
		print("READY: {}".format(str(i_)))
	print("Completed overdue tasks from disk.")
	print("Booting up threads...")
	EventLoop.bootup()
	print("Boot complete.")
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
	parser.add_argument("--plot", dest="plot", type=bool, default=False, required=False, help="plots throuput when only 1 loop")
	# parser.add_argument("--runtime", dest="runtime", type=int, default=10, required=False, help="time in seconds to run")
	args = vars(parser.parse_args())

	# print("main thread will sleep for {} while event loops process created events.".format(args["runtime"]))
	# time.sleep(args["runtime"])
	# print("runtime limit '{}s' reached. Stopping threads and persisting remaining tasks to disk.".format(args["runtime"]))

	if args["loops"] == 1:
		single_thread_demo(plot=args["plot"])
	else:
		multi_thread_demo()

	print("Shutting down engine...")
	EventLoop.shutdown()
	print("Shutdown complete.")

	print("Flushing remaining tasks to disk.")
	ProgressStore.sync()
	print("Flush complete.")
