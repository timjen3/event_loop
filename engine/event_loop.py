"""
	This event loop is oriented around tasks that will finish in a specified number of ticks.
	This event loop is not ideal for completing piles of work with a fixed number of workers.

	Good task:
		Sending workers on a quest.
	Bad task:
		Tasks you may start / stop, such as while you shift workers from one thing to another.
"""
from .persistence import ProgressStore
from collections import defaultdict
from ._utils import SingleThreaded
from math import floor
from time import time
__DEFAULT_CHECK_INTERVAL__ = 1  # seconds between intervals


class EventLoop(SingleThreaded):
	RESOURCES = defaultdict(int)
	ticks = floor(time())  # until start() called use startup time

	def __init__(self, uid):
		"""
			:param tasks: list of tasks can be passed if you want to begin with some tasks to process in place.
				should be of form (ticks, Task())
		"""
		self.uid = uid
		self.THROUGHPUT = defaultdict(int)
		self.check_interval = __DEFAULT_CHECK_INTERVAL__
		self.stopped = False
		self.__event_loop_ = None
		self.__tasks_ = ProgressStore.list(inst=self, uid=uid, name="tasks")
		super().__init__(clear_backlog=True)

	def __ticks_(self):
		if self.started:
			return floor(time())
		else:
			return self.ticks

	def add_task(self, task):
		"""
			:param task: object implementing the resource.quests.Task() abstract class interface
			:param ticks: number of ticks needed in order to complete the task
		"""
		self.__tasks_.append(
			(self.__ticks_() + task.ticks, task)
		)

	def do_tasks(self):
		"""Processes all tasks in queue."""
		now_ = self.__ticks_()
		while True:
			baked_ = [i for i, (ticks_, task_) in enumerate(self.__tasks_) if ticks_ <= now_]
			if len(baked_) == 0:
				break

			index_ = baked_.pop(0)
			ticks_, task_ = self.__tasks_.pop(index_)
			task_.process(EventLoop)
