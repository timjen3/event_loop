"""Starts specified number of event loops with an arbitrary number of tasks loaded in. Processes all the tasks.
On shutdown, persists remaining tasks."""
from engine.event_loop2 import EventLoop as EventLoop2
from engine.event_loop import EventLoop
from engine.persistence import IoStore
from quests.quests import BasicQuest
from work.tasks import Mine
import tkinter
import time
__VERSION__ = 1.0


q_1 = lambda s: BasicQuest(name="LEVEL1", callback=s.callback)
q_2 = lambda s: BasicQuest(name="LEVEL2", callback=s.callback)
q_3 = lambda s: BasicQuest(name="LEVEL3", callback=s.callback)
q_4 = lambda s: BasicQuest(name="LEVEL4", callback=s.callback)
m_1 = lambda s: Mine(name="WOOD", callback=s.callback)
m_2 = lambda s: Mine(name="STONE", callback=s.callback)
m_3 = lambda s: Mine(name="GOLD", callback=s.callback)
m_4 = lambda s: Mine(name="EMERALD", callback=s.callback)


class Gui:
	root = tkinter.Tk()

	def __init__(self):
		self.master = tkinter.Frame(self.root)
		self.el = EventLoop(name="main")

		self.out = tkinter.StringVar()
		tb = tkinter.Label(self.master, textvariable=self.out).grid(row=0, column=0)
		btn1 = tkinter.Button(self.master, text="Add", command=q_1(self)).grid(row=1, column=0)
		btn2 = tkinter.Button(self.master, text="Add", command=q_2(self)).grid(row=2, column=0)
		btn3 = tkinter.Button(self.master, text="Add", command=q_3(self)).grid(row=3, column=0)
		btn4 = tkinter.Button(self.master, text="Add", command=q_4(self)).grid(row=4, column=0)
		btn5 = tkinter.Button(self.master, text="Add", command=m_1(self)).grid(row=5, column=0)
		btn6 = tkinter.Button(self.master, text="Add", command=m_2(self)).grid(row=6, column=0)
		btn7 = tkinter.Button(self.master, text="Add", command=m_3(self)).grid(row=7, column=0)
		btn8 = tkinter.Button(self.master, text="Add", command=m_4(self)).grid(row=8, column=0)
		btn9 = tkinter.Button(self.master, text="Add", command=self.quit).grid(row=9, column=0)
		self.master.grid(row=0, column=0)
		self.root.mainloop()

	def callback(self, event_loop, task, bounty):
		self.out.set(self.el.RESOURCES)

	def quit(self):
		EventLoop.shutdown()
		IoStore.sync()


if __name__ == "__main__":
	Gui()
