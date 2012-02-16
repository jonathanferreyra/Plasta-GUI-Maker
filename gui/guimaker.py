#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os,sys
# Importamos los módulos de Qt
from PyQt4 import QtCore, QtGui, uic
from mytablewidget import MyTableWidget 
import pathtools
from api import gui_maker

class GuiMaker(QtGui.QMainWindow):
    """La ventana principal de la aplicación."""
    
    def __init__(self, parent = None):
        FILENAME = 'guimaker.ui'
        QtGui.QMainWindow.__init__(self)
    #cargamos la interfaz desde el archivo .ui
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__center()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        
        self.gui = parent
        self.lwWidgets = MyTableWidget(self.lstWidgets,['Nombre','Widget'])
        #~ self.lwCamposBD = MyTableWidget(self.lstCamposBD,['Campo','Tipo'],False)
        ### Atributos
        
        self.__widgets = []
        self.__opcionesGeneracion = {}            
        self.__botones = {}
        
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
            if len(self.__widgets) != 0 :                
                self.__generarUI()
            else:
                QtGui.QMessageBox.warning(self, "Qt Gui Maker","No hay widgets para generar.")            
    
    @QtCore.pyqtSlot()
    def on_btAgregar_clicked(self):
        if not self.leNombre.text().isEmpty() :
            item = [self.__toUnicode(self.leNombre.text()), 
                    self.__toUnicode(
                        self.cbWidget.itemText(self.cbWidget.currentIndex()))]
            self.lwWidgets.appendItem(item)        
            self.leNombre.setText('')            
            nombre_widget = item[0].replace(' ','_') if item[0].strip().find(' ') != -1 else item[0]
            tipo_widget = item[1]
            self.__widgets.append([len(self.__widgets), nombre_widget, tipo_widget])  
    
    @QtCore.pyqtSlot()
    def on_btArriba_clicked(self):
        indice = self.lwWidgets.getSelectedCurrentIndex()
        print indice
        if indice > 0 :
            valor_up = self.__widgets[indice]
            valor_down = self.__widgets[indice - 1]
            self.__widgets[indice - 1] = valor_up
            self.__widgets[indice] = valor_down
            # vuelve a cargar la lista
            self.lwWidgets.addItems( [elemento[1:] for elemento in self.__widgets] )
            
    @QtCore.pyqtSlot()
    def on_btAbajo_clicked(self):
        indice = self.lwWidgets.getSelectedCurrentIndex()
        if (indice < len(self.__widgets) ) :
            valor_down = self.__widgets[indice]
            valor_up = self.__widgets[indice + 1]
            self.__widgets[indice + 1] = valor_down
            self.__widgets[indice] = valor_up
            # vuelve a cargar la lista
            self.lwWidgets.addItems( [elemento[1:] for elemento in self.__widgets] )
   
    @QtCore.pyqtSlot()
    def on_btQuitar_clicked(self):
        # obtiene el indice en la lista en donde esta ubicado el elemento seleccionado
        indice = self.lwWidgets.getSelectedCurrentIndex()
        del self.__widgets[ indice ]
        # vuelve a cargar la lista
        self.lwWidgets.addItems( [elemento[1:] for elemento in self.__widgets] )
             
    @QtCore.pyqtSlot()
    def on_btExaminar_clicked(self):
        self.leSalida.setText(
            self.__guardarArchivo())
    
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
        
    @QtCore.pyqtSlot()
    def on_rbMainWindow_clicked(self):
        self.rbDialog.setChecked(False)
        self.rbMainWindow.setChecked(True)
        
    @QtCore.pyqtSlot()
    def on_rbDialog_clicked(self):
        self.rbMainWindow.setChecked(False)
        self.rbDialog.setChecked(True)
        
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
            #dialog.setDefaultSuffix("db")
            #dialog.setNameFilter('SQLite Databases (*.db)')
            
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
            
        print widgets_a_generar
                                
        opts, btns = self.getOpcionesGeneracion()  
        gui_maker.generarUI(
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
            pathtools.getPathRootFolder()+'/plantillas/plantilla.py')
        
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
    
    def getOpcionesGeneracion(self):
        """ """
        
        self.__opcionesGeneracion['generar_plantilla'] = self.chkGenerarPlantilla.isChecked()
        
        # botones
        
        
        self.__botones['bt_salir_aceptar'] = self.rbBtnsSA.isChecked()
        self.__botones['bt_salir_guardar'] = self.rbBtnsSG.isChecked()
        self.__botones['bt_cancelar_aceptar'] = self.rbBtnsCA.isChecked()
        self.__botones['bt_limpiar'] = self.chkBtnsLimpiar.isChecked()
        if self.rbMainWindow.isChecked() :
            self.__opcionesGeneracion['tipo'] = 'MainWindow'
        if self.rbDialog.isChecked():
            self.__opcionesGeneracion['tipo'] = 'Dialog'
            
        return self.__opcionesGeneracion, self.__botones
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = GuiMaker()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
