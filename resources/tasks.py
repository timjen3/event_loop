from random import randint
import json
__TICKS__ = json.load(fp=open("resources/ticks.json", "r"))
__RESULTS__ = json.load(fp=open("resources/results.json", "r"))


class Mine:
	def __init__(self, name, callback=None):
		self.name = name
		self.ticks = __TICKS__[name]
		self.callback = callback
		self.bounty = randint(__RESULTS__[name][0], __RESULTS__[name][1])

	@property
	def completed(self):
		if self.ticks <= 0:
			return True

	def work(self, evt_loop):
		self.ticks -= 1
		if self.ticks <= 0:
			evt_loop.RESOURCES[self.name] += self.bounty

			if self.callback is not None:
				self.callback(self, self.bounty)
