"""
	This event loop is oriented around completing piles of work with a fixed number of workers.
	This event loop is not ideal for tasks that finish in a specified number of ticks.

	Good task:
		Tasks you may start / stop, such as while you shift workers from one thing to another.
	Bad task:
		Sending workers on a quest.
"""
from .persistence import ProgressStore
from collections import defaultdict
from ._utils import SingleThreaded
__DEFAULT_CHECK_INTERVAL__ = 1  # seconds between intervals


class EventLoop(SingleThreaded):
	RESOURCES = defaultdict(int)
	# TODO: TASK_LIMIT SHOULD START AT 0 AND BE ADJUSTED BY USER..BUT FOR PROTOTYPING CAN START AT FIXED NUMBER
	TASK_LIMIT = 10  # maximum number of tasks processed per increment

	def __init__(self, uid):
		"""
			:param tasks: list of tasks can be passed if you want to begin with some tasks to process in place.
				should be of form (ticks, Task())
		"""
		self.uid = uid
		self.check_interval = __DEFAULT_CHECK_INTERVAL__
		self.stopped = False
		self.__tasks_ = ProgressStore.list(inst=self, uid=uid, name="tasks")
		super().__init__()

	def add_task(self, task):
		"""
			:param task: object implementing the work.tasks.Task() abstract class interface
		"""
		self.__tasks_.append(task)

	def do_tasks(self):
		"""Processes all tasks in queue."""
		work_ = self.TASK_LIMIT
		while True:
			if len(self.__tasks_) == 0 or work_ <= 0:
				break
			self.__tasks_[0].work(self)
			if self.__tasks_[0].completed:
				self.__tasks_.pop(0)

			work_ -= 1
