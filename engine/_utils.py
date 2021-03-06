from threading import Timer, Thread
from abc import abstractmethod


def intermittent_threaded_(fun):
	"""decorate a class method with this if you want it to run repeatedly until the instance.stopped = True"""
	def start(self, *args):
		th_ = Thread(target=wrapped_, args=[self, *args], daemon=False)
		th_.start()
		return th_

	def wrapped_(self, *args):
		"""executes function, waits for it to finish, and runs function again, ad-infinitum unless stopped."""
		while not self.stopped:
			t_ = Timer(interval=self.check_interval, function=fun, args=[self, *args])
			t_.start()
			t_.join()

	return lambda c: start(c)


class SingleThreaded:
	"""Exposes start() method that will process tasks in a new thread.
	Exposes stop() method that will flag the thread to stop processing tasks."""
	INSTANCES = list()

	@classmethod
	def shutdown(cls):
		for inst_ in cls.INSTANCES:
			inst_.stop()
		for inst_ in cls.INSTANCES:
			inst_.wait()

	def __init__(self):
		self.stopped = False
		self.__event_loop_ = None
		SingleThreaded.INSTANCES.append(self)

	@property
	def uid(self):
		raise NotImplementedError("Must implement abstract method!!")

	def start(self):
		self.stopped = False
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
