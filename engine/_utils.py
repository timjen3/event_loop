from threading import Timer, Thread
from abc import abstractmethod
from collections import defaultdict
from math import floor
from time import time


def intermittent_threaded_(fun):
	"""decorate a class method with this if you want it to run repeatedly until the instance.stopped = True"""
	def start(self, *args):
		th_ = Thread(target=wrapped_, args=[self, *args], daemon=False)
		th_.start()
		return th_

	def wrapped_(self, *args):
		"""executes function, waits for it to finish, and runs function again, ad-infinitum unless stopped."""
		while self.started and not self.stopped:
			t_ = Timer(interval=self.check_interval, function=fun, args=[self, *args])
			t_.start()
			t_.join()

	return lambda c: start(c)


class SingleThreaded:
	"""Exposes start() method that will process tasks in a new thread.
	Exposes stop() method that will flag the thread to stop processing tasks."""
	INSTANCES = list()
	DATAOUT = defaultdict(list)
	STARTUPTICKS = floor(time())  # when processing overdue tasks at startup don't re-calculate time

	@classmethod
	def shutdown(cls):
		for inst_ in cls.INSTANCES:
			inst_.stop()
		for inst_ in cls.INSTANCES:
			inst_.wait()

	def __init__(self, clear_backlog=False):
		self.started = False
		self.stopped = False
		self.__event_loop_ = None
		SingleThreaded.INSTANCES.append(self)
		if clear_backlog:
			print("Clearing out due tasks loaded from disk.")
			self.__do_tasks_()

	"""calling start will fire off a new thread which will process all tasks every 1s unless the stop() 
	method is called."""
	def start(self):
		self.started = True
		self.__event_loop_ = self.__do_tasks_()

	@intermittent_threaded_
	def __do_tasks_(self):
		self.do_tasks()

	@abstractmethod
	def do_tasks(self):
		pass

	def stop(self):
		"""Flags thread to stop."""
		self.stopped = True

	def wait(self):
		"""waits for thread to finish."""
		self.__event_loop_.join()
