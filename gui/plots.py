from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class Gui:
	def __init__(self, method):
		self.method = method  # data ref

		self.app = QtGui.QApplication([])
		self.mw = QtGui.QMainWindow()
		self.mw.setWindowTitle('pyqtgraph example: PlotWidget')
		self.mw.resize(800, 600)
		self.cw = QtGui.QWidget()
		self.mw.setCentralWidget(self.cw)
		self.l = QtGui.QVBoxLayout()
		self.cw.setLayout(self.l)
		self.pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
		self.l.addWidget(self.pw)
		self.mw.show()
		self.pl = self.pw.plot()
		self.pl.setPen((200, 200, 100))
		self.pw.setLabel('left', 'Value', units='V')
		self.pw.setLabel('bottom', 'Time', units='s')
		self.pw.setXRange(0, 10)
		self.pw.setYRange(0, 1000)

	def updateData(self):
		new_x, new_y = self.method()
		print(new_x, new_y)
		self.pl.setData(y=new_y, x=new_x)

	def start(self):
		t = QtCore.QTimer()
		t.timeout.connect(self.updateData)
		t.start(500)
		QtGui.QApplication.instance().exec_()
