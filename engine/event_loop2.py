"""
	This event loop is oriented around completing piles of work with a fixed number of workers.
	This event loop is not ideal for tasks that finish in a specified number of ticks.

	Good task:
		Tasks you may start / stop, such as while you shift workers from one thing to another.
	Bad task:
		Sending workers on a quest.
"""
from collections import defaultdict
from ._utils import SingleThreaded
from .persistence import persisted
__DEFAULT_CHECK_INTERVAL__ = 1  # seconds between intervals


class EventLoop(SingleThreaded):
	# TODO: TASK_LIMIT SHOULD START AT 0 AND BE ADJUSTED BY USER..BUT FOR PROTOTYPING CAN START AT FIXED NUMBER
	TASK_LIMIT = 10  # maximum number of tasks processed per increment

	def __init__(self, name):
		"""
			:param tasks: list of tasks can be passed if you want to begin with some tasks to process in place.
				should be of form (ticks, Task())
		"""
		self.name = name
		self.check_interval = __DEFAULT_CHECK_INTERVAL__
		self.stopped = False
		super().__init__()

	@property
	@persisted
	def RESOURCES(self):
		return defaultdict(int)

	@property
	@persisted
	def tasks(self):
		return []

	@property
	def uid(self):
		return self.name

	def add_task(self, task):
		"""
			:param task: object implementing the work.tasks.Task() abstract class interface
		"""
		self.tasks.append(task)
		print("added work")

	def do_tasks(self):
		"""Processes all tasks in queue."""
		work_ = self.TASK_LIMIT
		while True:
			if len(self.tasks) == 0 or work_ <= 0:
				break
			self.tasks[0].work(self)
			if self.tasks[0].completed:
				self.tasks.pop(0)

			work_ -= 1
