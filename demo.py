"""Starts specified number of event loops with an arbitrary number of tasks loaded in. Processes all the tasks.
On shutdown, persists remaining tasks."""
from engine.persistence import ProgressStore
from engine.event_loop import EventLoop
from random import randint
import time
__VERSION__ = 1.0


class DummyTask:
	RESOURCES = dict()
	TICKS = {
		"WOOD": 2,
		"STONE": 4,
		"GOLD": 10,
	}

	def __init__(self, name, evt=lambda: None):
		self.name = name
		self.ticks = self.TICKS[name]
		self.negligable = 0
		self.evt = evt

	def process(self, evt_loop):
		result = randint(1, 10)
		evt_loop.RESOURCES[self.name] += result
		print("Mined: n: {:10s} | d: {:6}".format(self.name, result))
		self.evt()


def single_thread_demo(runtime):
	print("Processing overdue tasks")
	thread_name = "single"
	all_loops = list()
	el = EventLoop(uid=thread_name)
	all_loops.append(el)
	el.do_tasks()
	print("Completed overdue tasks from disk.")
	for s_i_ in range(0, args["powers"]):
		for s_i_n_ in range(0, 100):
			t_1 = DummyTask(name="WOOD")
			t_2 = DummyTask(name="STONE")
			t_3 = DummyTask(name="GOLD")
			el.add_task(task=t_1)
			el.add_task(task=t_2)
			el.add_task(task=t_3)
	print("Booting up threads...")
	EventLoop.bootup()
	print("Boot complete.")
	el.start()
	print("main thread will sleep for {} while event loops process created events.".format(args["runtime"]))
	time.sleep(runtime)
	print("runtime limit '{}s' reached. Stopping threads and persisting remaining tasks to disk.".format(args["runtime"]))


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('-h', '--help', '--about', action='help', default=argparse.SUPPRESS, help='schedulable task processor')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__VERSION__), help="Show program's version number and exit.")
	parser.add_argument("--powers", dest="powers", type=int, default=4, required=False, help="tasks w/ticks at powers of 2")
	parser.add_argument("--runtime", dest="runtime", type=int, default=10, required=False, help="time in seconds to run")
	args = vars(parser.parse_args())

	single_thread_demo(runtime=args["runtime"])

	print(EventLoop.RESOURCES)

	print("Shutting down engine...")
	EventLoop.shutdown()
	print("Shutdown complete.")

	print("Flushing remaining tasks to disk.")
	ProgressStore.sync()
	print("Flush complete.")
