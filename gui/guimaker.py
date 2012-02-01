#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os,sys
# Importamos los módulos de Qt
from PyQt4 import QtCore, QtGui, uic
from mytablewidget import MyTableWidget 
import pathtools
import api

class GuiMaker(QtGui.QMainWindow):
    """La ventana principal de la aplicación."""
    
    def __init__(self, parent = None):
        FILENAME = 'guimaker.ui'
        QtGui.QMainWindow.__init__(self)
    #cargamos la interfaz desde el archivo .ui
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__center()
        
        self.gui = parent
        self.lwWidgets = MyTableWidget(self.lstWidgets,['Nombre','Widget'],False)
        #~ self.lwCamposBD = MyTableWidget(self.lstCamposBD,['Campo','Tipo'],False)
        ### Atributos
        
        self.__widgets = []
        self.datosCampos = None
        self.opcionesGeneracion = {}
        
        self.__setCurrentUserPath()        
        
##########################
# METODOS DE LOS EVENTOS #
##########################

    @QtCore.pyqtSlot()
    def on_btGenerar_clicked(self):
        if self.leSalida.text() == '' :
            QtGui.QMessageBox.warning(self, "Qt Gui Maker","No se ha seleccionado un destino para el archivo de salida.")
        else:
            self.__generarUI()            
        pass
    
    @QtCore.pyqtSlot()
    def on_btAgregar_clicked(self):
        item = [self.__toUnicode(self.leNombre.text()), 
                self.__toUnicode(
                    self.cbWidget.itemText(self.cbWidget.currentIndex()))]
        self.lwWidgets.appendItem(item)        
        self.leNombre.setText('')      
        
        self.__widgets.append([len(self.__widgets), item[0], item[1] ])  
    
    @QtCore.pyqtSlot()
    def on_btArriba_clicked(self):
        pass
    
    @QtCore.pyqtSlot()
    def on_btAbajo_clicked(self):
        pass
        
    @QtCore.pyqtSlot()
    def on_btExaminar_clicked(self):
        self.leSalida.setText(
            self.__guardarArchivo())
        pass
    
    @QtCore.pyqtSlot()
    def on_btAbrirSqlite_clicked(self):
        self.__abrirSqlite()
    
    @QtCore.pyqtSlot()
    def on_btOpciones_clicked(self):
        self.gui.showOpciones()
        
    @QtCore.pyqtSlot()
    def on_btIncuirSenales_clicked(self):
        self.gui.showInculirSenales(self, self.__widgets )
        
    def on_leNombre_returnPressed(self):
        self.on_btAgregar_clicked()
        
    def on_arbolWidgets_selectedItem(self):
		pass
		
######################
# METODOS AUXILIARES #
######################

    def __center(self):
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
            dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
            dialog.setDefaultSuffix("db")
            dialog.setNameFilter('SQLite Databases (*.db)')
            
            if dialog.exec_():
                filename = dialog.selectedFiles()[0] # convierte a unicode el string
                filename = unicode(filename, 'utf-8') # 
                                   
                self.gui.showSeleccionarCampos(self,filename)                                        
                
    def __generarUI(self):
        """
        """        
        widgets_a_generar = {}
        
        for widget in self.__widgets :
            widgets_a_generar[widget[0]] = {widget[1]:widget[2]}
                                
        opts, btns = self.gui.getOpcionesGeneracion()  
        print opts, btns
        api.generarUI(
            self.__toUnicode(self.leSalida.text()),
            widgets_a_generar,
            botones = btns,
            opciones = opts)
        
        QtGui.QMessageBox.information(self, "Qt Gui Maker",u"Generación realizada con éxito.")
            
    def __toUnicode(self,myQstring):
        u""" Convierte a UTF8 el objeto QString recibido. """
        #~ print myQstring
        return unicode(myQstring.toUtf8(),'utf-8')
        
    def cargarCamposDesdeBD(self, datos) : 
        # carga en al lsita lso datos recibidos desde el dialogo
        self.lwWidgets.addItems(datos)
        
        for item in datos :
            self.__widgets.append(item)
            
    def __crearPlantilla(self, destino):
        import shutil
        import os.path
        
        origen = pathtools.convertPath(
            pathtools.getPathRootFolder()+'/api/plantilla.py')
        
        nombre_archivo = os.path.basename(destino)[:-3]
        
        destino = nombre_archivo + '.py'
        
        shutil.copy(origen, destino)
        
        plantilla = open(destino,'r')
        contenido = plantilla.read()
        plantilla.close()
        contenido = contenido.replace(u'###',nombre_archivo)
        plantilla = open(destino,'w')
        plantilla.write(contenido)
        plantilla.close()
        
    def __setCurrentUserPath(self):
        homedir = os.path.expanduser("~")
        homedir = pathtools.convertPath(homedir + '/untitled.ui')
        self.leSalida.setText(homedir)
    
def main():
    app = QtGui.QApplication(sys.argv)
    window = GuiMaker()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
