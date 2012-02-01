#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       
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


class Opciones(QtGui.QDialog):
    """La ventana principal de la aplicación."""
    
    def __init__(self, parent = None):
        FILENAME = 'opciones.ui'
        QtGui.QDialog.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
        
        self.papa = parent 

        self.__opcionesGeneracion = {}            
        self.__botones = {}

##########################
# METODOS DE LOS EVENTOS #
##########################

    @QtCore.pyqtSlot()
    def on_rbMainWindow_clicked(self):
        self.rbDialog.setChecked(False)
        self.rbMainWindow.setChecked(True)
        pass
        
    @QtCore.pyqtSlot()
    def on_rbDialog_clicked(self):
        self.rbMainWindow.setChecked(False)
        self.rbDialog.setChecked(True)
        pass
        
    @QtCore.pyqtSlot()
    def on_btCerrar_clicked(self):
        self.papa.setOpcionesGeneracion(
            self.getOpcionesGeneracion() )
        print 'me cerraron...'
        self.close()
    
######################
# METODOS AUXILIARES #
######################

    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
                  
    def getOpcionesGeneracion(self):
        """ """
        if self.chkGenerarPlantilla.isChecked() :            
            self.__opcionesGeneracion['generar_plantilla'] = True
        
        # botones
        
        if self.rbBtnsSA.isChecked() :
            self.__botones['bt_salir_aceptar'] = True
        if self.rbBtnsSG.isChecked() :
            self.__botones['bt_salir_guardar'] = True
        if self.rbBtnsCA.isChecked() :
            self.__botones['bt_cancelar_aceptar'] = True
        if self.chkBtnsLimpiar.isChecked() :
            self.__botones['bt_limpiar'] = True
        
        if self.rbMainWindow.isChecked():
            self.__opcionesGeneracion['tipo'] = 'MainWindow'
        if self.rbDialog.isChecked():
            self.__opcionesGeneracion['tipo'] = 'Dialog'
            
        return self.__opcionesGeneracion, self.__botones
    
def main():
    app = QtGui.QApplication(sys.argv)
    window = Opciones()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
