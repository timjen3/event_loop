"""Starts specified number of event loops with an arbitrary number of tasks loaded in. Processes all the tasks.
On shutdown, persists remaining tasks."""
from engine.event_loop2 import EventLoop as EventLoop2
from engine.event_loop import EventLoop
from engine.persistence import IoStore
from quests.quests import BasicQuest
from work.tasks import Mine
import tkinter
__VERSION__ = 1.0


el1 = EventLoop(name="quests")
el1.start()
q_1 = lambda self: lambda s=self: el1.add_task(BasicQuest(name="LEVEL1", callback=s.callback1))
q_2 = lambda self: lambda s=self: el1.add_task(BasicQuest(name="LEVEL2", callback=s.callback1))
q_3 = lambda self: lambda s=self: el1.add_task(BasicQuest(name="LEVEL3", callback=s.callback1))
q_4 = lambda self: lambda s=self: el1.add_task(BasicQuest(name="LEVEL4", callback=s.callback1))


el2 = EventLoop2(name="work")
el2.start()
m_1 = lambda self: lambda s=self: el2.add_task(Mine(name="WOOD", callback=s.callback2))
m_2 = lambda self: lambda s=self: el2.add_task(Mine(name="STONE", callback=s.callback2))
m_3 = lambda self: lambda s=self: el2.add_task(Mine(name="GOLD", callback=s.callback2))
m_4 = lambda self: lambda s=self: el2.add_task(Mine(name="EMERALD", callback=s.callback2))


class Gui:
	root = tkinter.Tk()

	def __init__(self):
		self.master = tkinter.Frame(self.root)
		self.out1 = tkinter.StringVar()
		tb = tkinter.Label(self.master, textvariable=self.out1).grid(row=0, column=0, columnspan=4)
		self.out2 = tkinter.StringVar()
		tb = tkinter.Label(self.master, textvariable=self.out2).grid(row=2, column=0, columnspan=4)
		btn1 = tkinter.Button(self.master, text="Trainee", command=q_1(self)).grid(row=1, column=0)
		btn2 = tkinter.Button(self.master, text="Apprentice", command=q_2(self)).grid(row=1, column=1)
		btn3 = tkinter.Button(self.master, text="Journeyman", command=q_3(self)).grid(row=1, column=2)
		btn4 = tkinter.Button(self.master, text="Master", command=q_4(self)).grid(row=1, column=3)
		btn5 = tkinter.Button(self.master, text="Wood", command=m_1(self)).grid(row=3, column=0)
		btn6 = tkinter.Button(self.master, text="Stone", command=m_2(self)).grid(row=3, column=1)
		btn7 = tkinter.Button(self.master, text="Gold", command=m_3(self)).grid(row=3, column=2)
		btn8 = tkinter.Button(self.master, text="Emerald", command=m_4(self)).grid(row=3, column=3)
		btn9 = tkinter.Button(self.master, text="quit", command=self.quit).grid(row=4, column=1, columnspan=2)
		self.master.grid(row=0, column=0)
		self.root.mainloop()

	def callback1(self, event_loop, task, bounty):
		self.out1.set(dict(event_loop.RESOURCES))

	def callback2(self, event_loop, task, bounty):
		self.out2.set(dict(event_loop.RESOURCES))

	def quit(self):
		EventLoop.shutdown()
		IoStore.sync()
		self.root.destroy()


if __name__ == "__main__":
	Gui()
