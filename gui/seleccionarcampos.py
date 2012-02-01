#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os,sys
# Importamos los módulos de Qt
from PyQt4 import QtCore, QtGui, uic

from sqlite import sqlite
from mytablewidget import MyTableWidget

class SeleccionarCampos(QtGui.QDialog):
    """La ventana principal de la aplicación."""
    
    def __init__(self, parent = None, pathBD = None):
        FILENAME = 'seleccionar_campos.ui'
        QtGui.QDialog.__init__(self)
    #cargamos la interfaz desde el archivo .ui
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.center()
        
        if not pathBD :
            pathBD = '/media/Data/Dropbox/Proyectos/GUIMaker/extras/jaja.db'
        self.__bd = sqlite(pathBD)
        self.__camposSeleccionados = []
        self.__camposActuales = []            
        
        self.papa = parent
        
        self.lbUbicacion.setText(pathBD)
        self.__cargarTablas()
        self.lwCamposElegidos = MyTableWidget(self.lstCamposElegidos, ['Campo', 'Widget'], False)

##########################
# METODOS DE LOS EVENTOS #
##########################    
    
    @QtCore.pyqtSlot()
    def on_btAceptar_clicked(self):        
        self.papa.gui.cargarListaCamposBD(self.__camposSeleccionados)
        self.close()

    @QtCore.pyqtSlot()
    def on_btIncluirCampo_clicked(self):
        self.__incluirCampo()
    
    @QtCore.pyqtSlot()
    def on_btIncluirTodos_clicked(self):
        self.__incluirTodos()
        pass
        
    @QtCore.pyqtSlot(int)
    def on_cbTablas_currentIndexChanged(self):
        self.__cargarCamposTabla()
    
######################
# METODOS AUXILIARES #
######################
 
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
    def __guardarArchivo(self):
            """ """
            dialog = QtGui.QFileDialog(self, 'Guardar .ui')
            dialog.setFileMode(QtGui.QFileDialog.AnyFile)
            dialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
            dialog.setDefaultSuffix("ui")
            dialog.setNameFilter('Designer UI files (*.ui)')
            
            if dialog.exec_():
                filename = dialog.selectedFiles()[0] # convierte a unicode el string
                filename = unicode(filename, 'utf-8') # 
                
                return filename
            else: return ''
            
    def __abrirSqlite(self):
            """ """
            dialog = QtGui.QFileDialog(self, 'Abrir SQLite')
            dialog.setFileMode(QtGui.QFileDialog.AnyFile)
            dialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
            dialog.setDefaultSuffix("db")
            dialog.setNameFilter('SQLite Databases (*.db)')
            
            if dialog.exec_():
                filename = dialog.selectedFiles()[0] # convierte a unicode el string
                filename = unicode(filename, 'utf-8') # 
                
                return filename
            else: return ''
            
    def __cargarTablas(self):        
        self.cbTablas.clear()                
        self.cbTablas.addItems(self.__bd.getTablas())
    
    def __cargarCamposTabla(self):
        tabla = str(self.cbTablas.itemText(
                    self.cbTablas.currentIndex()).toUtf8())
        
        estructura = self.__bd.getEstructuraTabla(tabla)

        self.__camposActuales = []
        self.lwCamposBD = MyTableWidget(self.lstCamposBD,['Campo','Tipo'],False)
        
        for campo in estructura:
            self.__camposActuales.append([campo,estructura[campo]])
            
        self.lwCamposBD.addItems(self.__camposActuales)
        
    def __recargarCamposTabla(self):        
        a_cargar = []
        for campo in self.__camposActuales:
            if campo not in self.__camposSeleccionados :
                a_cargar.append(campo)
        
        self.lwCamposBD.addItems(a_cargar)

    def __incluirCampo(self):
        
        for row in self.lwCamposBD.getListSelectedRows():
            widget = str(self.cbWidget.itemText(self.cbWidget.currentIndex()).toUtf8())
            # agrega solo si ese campo no esta en la lista
            row = list([row[0],widget])
            if row not in self.__camposSeleccionados : 
                self.__camposSeleccionados.append(row)
            
        self.lwCamposElegidos.addItems(self.__camposSeleccionados)
        self.__recargarCamposTabla()

    def __incluirTodos(self):
        todos = self.lwCamposBD.getAllItems()
        for row in todos :
            widget = str(self.cbWidget.itemText(self.cbWidget.currentIndex()).toUtf8())
            # agrega solo si ese campo no esta en la lista
            row = list([row[0],widget])
            if row not in self.__camposSeleccionados : 
                self.__camposSeleccionados.append(row)
                
        self.lwCamposElegidos.addItems(self.__camposSeleccionados)
        self.__recargarCamposTabla()
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = SeleccionarCampos()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
