from random import randint
import json
__TICKS__ = json.load(fp=open("quests/ticks.json", "r"))
__RESULTS__ = json.load(fp=open("quests/bounty.json", "r"))


class Quest:
	def __init__(self, name, callback=None):
		self.name = name
		self.ticks = __TICKS__[name]
		self.result = __RESULTS__[name]
		self.callback = callback

	def process(self, evt_loop):
		for r_, amt_ in self.result.items():
			evt_loop.RESOURCES[r_] += amt_

		if self.callback is not None:
			self.callback(self, self.result)
