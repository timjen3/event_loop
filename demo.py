"""Starts specified number of event loops with an arbitrary number of tasks loaded in. Processes all the tasks.
On shutdown, persists remaining tasks."""
from engine.event_loop2 import EventLoop as EventLoop2
from engine.persistence import ProgressStore
from resources.tasks import Mine
from quests.quests import Quest
from engine.event_loop import EventLoop
import time
__VERSION__ = 1.0


def dumb_callback(task, bounty):
	result = "{}: n: {:10s} | b: {}".format(task.__class__.__name__, task.name, bounty)
	print(result)


def single_thread_quest_demo(runtime, cycles):
	"""Quests finish at a specified time, period."""
	thread_name = "quest"
	el = EventLoop(uid=thread_name)
	EventLoop.bootup()
	el.start()
	# TODO: generator to return quests and send available workers (ex: 3 max) on quests on soon as they become available.
	print("Quests restored from disk which are past completion time will be completed!")
	for i_ in range(0, cycles):
		print("starting 3 quests.")
		t_1 = Quest(name="LEVEL1", callback=dumb_callback)
		t_2 = Quest(name="LEVEL2", callback=dumb_callback)
		t_3 = Quest(name="LEVEL3", callback=dumb_callback)
		el.add_task(task=t_1)
		el.add_task(task=t_2)
		el.add_task(task=t_3)
		print("main thread will sleep for {}s while quests are completed.".format(args["runtime"]))
		time.sleep(runtime)


def single_thread_work_demo(runtime, tasks):
	"""Work requires resources to be applied to the tasks in order to complete."""
	thread_name = "work"
	el = EventLoop2(uid=thread_name)
	for i_ in range(0, tasks):
		t_1 = Mine(name="WOOD", callback=dumb_callback)
		t_2 = Mine(name="STONE", callback=dumb_callback)
		t_3 = Mine(name="GOLD", callback=dumb_callback)
		el.add_task(task=t_1)
		el.add_task(task=t_2)
		el.add_task(task=t_3)
	print("Booting up threads...")
	EventLoop2.bootup()
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
	parser.add_argument("--tasks", dest="tasks", type=int, default=500, required=False, help="How many tasks to make")
	parser.add_argument("--runtime", dest="runtime", type=int, default=10, required=False, help="time in seconds to run")
	parser.add_argument("--demo", dest="demo", type=str, default=10, required=False, choices=["quest", "work"], help="which demo to run")
	args = vars(parser.parse_args())

	if args["demo"] == "quest":
		single_thread_quest_demo(runtime=args["runtime"], cycles=args["tasks"])
	else:
		single_thread_work_demo(runtime=args["runtime"], tasks=args["tasks"])

	print(EventLoop.RESOURCES)

	print("Shutting down engine...")
	EventLoop.shutdown()
	print("Shutdown complete.")

	print("Flushing remaining tasks to disk.")
	ProgressStore.sync()
	print("Flush complete.")
