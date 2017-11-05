"""Starts specified number of event loops with an arbitrary number of tasks loaded in. Processes all the tasks.
On shutdown, persists remaining tasks."""
from engine.event_loop2 import EventLoop as EventLoop2
from engine.persistence import ProgressStore
from engine.event_loop import EventLoop
from quests.quests import BasicQuest
from work.tasks import Mine
import time
__VERSION__ = 1.0


def dumb_callback(task, bounty):
	result = "{}: n: {:10s} | b: {}".format(task.__class__.__name__, task.name, bounty)
	print(result)


def single_thread_quest_demo(cycles):
	"""Quests finish at a specified time, period."""
	thread_name = "quest"
	el = EventLoop(uid=thread_name)
	for i_ in range(0, cycles):
		t_1 = BasicQuest(name="LEVEL1", callback=dumb_callback)
		t_2 = BasicQuest(name="LEVEL2", callback=dumb_callback)
		t_3 = BasicQuest(name="LEVEL3", callback=dumb_callback)
		t_4 = BasicQuest(name="LEVEL4", callback=dumb_callback)
		el.add_task(task=t_1)
		el.add_task(task=t_2)
		el.add_task(task=t_3)
		el.add_task(task=t_4)
		print("main thread will sleep for 15s so 3 of 4 added quests complete this cycle, 1 finishes next cycle!")
		el.start()
		time.sleep(16)  # since math.floor(time()), wait 1s extra
	EventLoop.shutdown()
	print("Engine shut down.")
	print(el.RESOURCES)


def single_thread_work_demo(cycles):
	"""Work requires work to be applied to the tasks in order to complete."""
	thread_name = "work"
	el = EventLoop2(uid=thread_name)
	for i_ in range(0, cycles):
		t_1 = Mine(name="WOOD", callback=dumb_callback)
		t_2 = Mine(name="STONE", callback=dumb_callback)
		t_3 = Mine(name="GOLD", callback=dumb_callback)
		t_4 = Mine(name="EMERALD", callback=dumb_callback)
		el.add_task(task=t_1)
		el.add_task(task=t_2)
		el.add_task(task=t_3)
		el.add_task(task=t_4)
	el.start()
	# Creates 3 tasks per cycle, total units of work required is 16, units per second is 10
	# So to process all tasks across i cycles: i * 1.6s = t
	sleep_time = cycles * 1.6
	print("main thread will sleep for {}s while event loop completes {} new. Disable t_4 if you do not want tasks to remain unfinished!".format(sleep_time, cycles))
	time.sleep(sleep_time + 1.0)  # since math.floor(time()), wait 1s extra
	EventLoop2.shutdown()
	print("Engine shut down.")
	print(el.RESOURCES)


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('-h', '--help', '--about', action='help', default=argparse.SUPPRESS, help='schedulable task processor')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__VERSION__), help="Show program's version number and exit.")
	parser.add_argument("--cycles", dest="cycles", type=int, default=500, required=False, help="How many tasks to make")
	parser.add_argument("--demo", dest="demo", type=str, choices=["quest", "work"], help="which demo to run")
	args = vars(parser.parse_args())

	print("Running selected demo: '{}'...".format(args["demo"]))
	{
		"quest": single_thread_quest_demo,
		"work": single_thread_work_demo
	}[args["demo"]](cycles=args["cycles"])

	print("Flushing remaining tasks to disk.")
	ProgressStore.sync()
	print("Flush complete.")
