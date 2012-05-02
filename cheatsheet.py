#!/usr/bin/env python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import * 
import sys, os
from ui_cheatsheet import Ui_CSDialog

class CSWindow ( QDialog , Ui_CSDialog):
	
	settings = QSettings()
	settings.setFallbacksEnabled(False)
	html_cs = ""
	html_style = "<html>\n<head>\n<style>\n%s\n</style>\n</head>\n<body>\n"
	html_thead = "\n<table><tr style='font-weight:bold'><td>Action</td><td>HotKey</td></tr>"
	html_def = ""
	def __init__ ( self, parent = None ):
		QDialog.__init__( self, parent )
		self.ui = Ui_CSDialog()
		self.ui.setupUi( self )
		self.ui.saveButton.clicked.connect(self.saveHTML)
		self.ui.closeButton.clicked.connect(self.accept)
		self.loadHotkeys()
		self.show()

	def loadHotkeys(self):
		fname = './hotkeys/'+self.settings.value('file_name_default').toString()
		dom = QDomDocument()
		error = None
		fh = None
		try:
			fh = QFile(fname)
			if not fh.open(QIODevice.ReadOnly):
				raise IOError, unicode(fh.errorString())
			if not dom.setContent(fh):
				raise ValueError, "could not parse XML"
		except (IOError, OSError, ValueError), e:
			error = "Failed to import: {0}".format(e)
		finally:
			if fh is not None:
				fh.close()
			if error is not None:
				return False, error
		root = dom.documentElement()
		if not root.hasAttribute('fileversion'):
			QMessageBox.information(self.window(), "LearnHotkeys","The file {} is not an LearnHotkeys definition file." % self.settings.value('file_name_default').toString())
			return False
		self.html_def += root.attribute('software')+" - "+root.attribute('softwareversion')+" - "+root.attribute('def')+"<br>\n<a href='"+root.attribute('softwaresite')+"'>" \
		+root.attribute('softwaresite')+"</a><br> CheatSheet version: "+root.attribute('fileversion')
		child = root.firstChildElement('hotkey')
		while not child.isNull():
			self.html_cs += "\n<tr><td>%s</td><td>%s</td></tr>" % (child.firstChildElement('question').text(),child.firstChildElement('key').text())
			child = child.nextSiblingElement('hotkey')
		self.html_cs += "</table></body></html>"
		self.ui.csView.setHtml((self.html_style % self.get_file_content('./style/blue-light.css'))+self.html_thead+self.html_cs)
		
	def saveHTML(self):
		filename =  QFileDialog.getSaveFileName(self, 'Save HTML CheatSheet', self.settings.value('file_name_default').toString()[:-4]+'.html')
		fname = open(filename, 'w')
		html = (self.html_style% self.get_file_content('./style/blue-light.css'))+self.html_def+self.html_thead+self.html_cs
		fname.write(html.toUtf8()+"\n")
		fname.close() 
	
	def get_file_content(self,file):
		f = open(file, 'r')
		c = f.read()
		f.close()
		return c
