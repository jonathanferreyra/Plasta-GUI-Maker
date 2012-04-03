#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os,sys
from PyQt4 import QtGui

from mainform import MainForm
from add_maker.guimaker import GuiMaker
from senales import Senales

class GUI(QtGui.QMainWindow):
    
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        self.cliptboard = app.clipboard()
#        self.gm = GuiMaker(self)
        self.mainform = MainForm(self)
        self.mainform.show()
#        self.gm.show()
        sys.exit(app.exec_())
        
    def showSeleccionarCampos(self, parent, path):
        from seleccionarcampos import SeleccionarCampos
        self.sc = SeleccionarCampos(parent, path)
        self.sc.show()    
        
    def showOpciones(self):
        self.opciones.show()   
        
    def showInculirSenales(self, parent, datos):
        self.senales = Senales(parent, datos)
        self.senales.show() 
        
    def showGenerarPlantillaUI(self, parent = None):
		from generar_plantilla_ui import GenerarPlantillaUI
		self.gpui = GenerarPlantillaUI(parent)
		self.gpui.show()
        		
def main():
    #~ app = QtGui.QApplication(sys.argv)
    gui = GUI()
    #~ window.show()
    #~ sys.exit(app.exec_())

if __name__ == "__main__":
    main()
