#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       
#       Copyright 2011 Jonathan Ferreyra <jalejandroferreyra@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os,sys
from PyQt4 import QtCore, QtGui, uic
from images import qtgui_art


class MainForm(QtGui.QMainWindow):

    def __init__(self, parent = None, pathBD = None):
        FILENAME = 'mainform.ui'
        QtGui.QMainWindow.__init__(self)    
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
        
        self.gui = parent
        #self.hover = QtGui.QHoverEvent( QtCore.QEvent.HoverEnter )
        #self.connect(self.hover, QtCore.SIGNAL('registerEventType ()'),self.on_btUINuevo_registerEventType)
        
        #self.connect(self.btUINuevo, QtCore.SIGNAL('enterEvent ()'),self.mouse_enterEvent)
        self.btUINuevo.installEventFilter(self)
        self.btSenalesPy.installEventFilter(self)
        self.btGenerarPlantilla.installEventFilter(self)
        self.btGenerarStormUi.installEventFilter(self)
        
    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))    
    
    @QtCore.pyqtSlot()
    def on_btSenalesPy_clicked(self):
        from generate_signals.generar_senales import GenerarSenalesPy
        self.senales = GenerarSenalesPy(cliptboard = self.gui.cliptboard)
        self.senales.show()
    
    @QtCore.pyqtSlot()
    def on_btUINuevo_clicked(self):
        from add_maker.guimaker import GuiMaker
        self.gm = GuiMaker(self.gui)
        self.gm.show()
          
    @QtCore.pyqtSlot()
    def on_btGenerarPlantilla_clicked(self):
        from generate_ui.generar_plantilla_ui import GenerarPlantillaUI
        self.gpui = GenerarPlantillaUI(self.gui)
        self.gpui.show()
        
    @QtCore.pyqtSlot()
    def on_btGenerarStormUi_clicked(self):
        from storm_maker.storm_gui_maker import StormGuiMaker
        self.sgm = StormGuiMaker(self.gui)
        self.sgm.show()
        
    def eventFilter(self, widget, event):        
        if (type(widget) is  QtGui.QPushButton) and (type(event) is QtGui.QHoverEvent) :            
            if widget is self.btUINuevo :
                self.lbDescripcion.setText(
                    u'Crear una pantalla tipo <alta de un registro>.')
            elif widget is self.btSenalesPy :
                self.lbDescripcion.setText(
                    u'Generar el codigo fuente para los widgets y las señales indicadas.')
            elif widget is self.btGenerarPlantilla :
                self.lbDescripcion.setText(
                    u'Generar la clase para controlar el archivo .ui seleccionado.')
            elif widget is self.btGenerarStormUi :
                self.lbDescripcion.setText(
                    u'Generar clase Storm para un objeto.')
            return 0
        else:            
            return QtGui.QMainWindow.eventFilter(self, widget, event)
def main():
    app = QtGui.QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
