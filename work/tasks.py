from random import randint
import json
__MINE_TICKS__ = json.load(fp=open("_resources/work/ticks.json", "r"))
__MINE_BOUNTY__ = json.load(fp=open("_resources/work/results.json", "r"))


class __Task_Interface_:
	def __init__(self, name, ticks, bounty_amt, callback=None):
		self.name = name
		self.ticks = ticks
		self.callback = callback
		self.bounty = bounty_amt

	@property
	def completed(self):
		if self.ticks <= 0:
			return True

	def work(self, evt_loop):
		self.ticks -= 1
		if self.ticks <= 0:
			evt_loop.RESOURCES[self.name] += self.bounty

			if self.callback is not None:
				self.callback(event_loop=evt_loop, task=self, bounty=self.bounty)


class Mine(__Task_Interface_):
	def __init__(self, name, callback=None):
		name = name
		ticks = __MINE_TICKS__[name]
		bounty = randint(__MINE_BOUNTY__[name][0], __MINE_BOUNTY__[name][1])
		callback = callback

		super().__init__(
			name=name,
			ticks=ticks,
			bounty_amt=bounty,
			callback=callback,
		)
