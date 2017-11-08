"""
	This event loop is oriented around tasks that will finish in a specified number of ticks.
	This event loop is not ideal for completing piles of work with a fixed number of workers.

	Good task:
		Sending workers on a quest.
	Bad task:
		Tasks you may start / stop, such as while you shift workers from one thing to another.
"""
from collections import defaultdict
from ._utils import SingleThreaded
from .persistence import persisted
from math import floor
from time import time
__DEFAULT_CHECK_INTERVAL__ = 1  # seconds between intervals


class EventLoop(SingleThreaded):

	def __init__(self, name):
		self.name = name
		self.check_interval = __DEFAULT_CHECK_INTERVAL__
		self.stopped = False
		self.__started_ = False
		super().__init__()
		print("Clearing out due tasks loaded from disk.")

		# CALCULATE time() once at start, clear out overdue tasks, then switch to normal.
		self.ticks = floor(time())
		self.started = False
		self.do_tasks()  # synchronous
		self.started = True

	@property
	@persisted
	def RESOURCES(self):
		return defaultdict(int)

	@property
	@persisted
	def quests(self):
		return []

	@property
	def uid(self):
		return self.name

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
		self.quests.append(
			(self.__ticks_() + task.ticks, task)
		)

	def do_tasks(self):
		"""Processes all tasks in queue."""
		now_ = self.__ticks_()
		while True:
			baked_ = [i for i, (ticks_, task_) in enumerate(self.quests) if ticks_ <= now_]
			if len(baked_) == 0:
				break

			index_ = baked_.pop(0)
			ticks_, task_ = self.quests.pop(index_)
			task_.process(self)
