import json
__BASIC_QUEST_TICKS__ = json.load(fp=open("_resources/quests/ticks.json", "r"))
__BASIC_QUEST_BOUNTY__ = json.load(fp=open("_resources/quests/bounty.json", "r"))


class __Quest_Interface_:
	def __init__(self, name, ticks, bounty_dict, callback=None):
		super().__init__()
		self.name = name
		self.ticks = ticks
		self.bounty = bounty_dict
		self.callback = callback

	def process(self, evt_loop):
		for r_, amt_ in self.bounty.items():
			evt_loop.RESOURCES[r_] += amt_

		if self.callback is not None:
			self.callback(event_loop=evt_loop, task=self, bounty=self.bounty)


class BasicQuest(__Quest_Interface_):
	def __init__(self, name, callback=None):
		name = name
		ticks = __BASIC_QUEST_TICKS__[name]
		bounty = __BASIC_QUEST_BOUNTY__[name]
		callback = callback
		super().__init__(
			name=name,
			ticks=ticks,
			bounty_dict=bounty,
			callback=callback,
		)
