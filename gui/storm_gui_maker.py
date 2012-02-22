#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from mytablewidget import MyTableWidget
from api import gui_maker
from api.logic_storm_class import LogicStormClass


#TODO: autosugerir el nombre de la clase al nombre del archivo para guardar
#TODO: permitir crear paquete __init__ del objeto en cuestion

class StormGuiMaker(QtGui.QMainWindow):
    """La ventana principal de la aplicación."""
    
    def __init__(self, parent = None):
        FILENAME = 'storm_gui_maker.ui'
        QtGui.QMainWindow.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.padre = parent
        
        self.tablaAtributos = MyTableWidget(
            self.twLista,
            ["Atributo","Storm Type","Widget","Valor por defecto",
            "Primario","Not Null","Referencia","Cruzada"]
        )
            
        self.widgets = []
        self.atributos = {}
        
    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
        
    @QtCore.pyqtSlot()
    def on_btAgregar_clicked(self):
        valido = True
        if self.leNombre.text().isEmpty() :
            self.leNombre.setStyleSheet('background-color: rgb(255, 155, 155);')
            valido = False
            
        if self.leNombreClase.text().isEmpty() :
            self.leNombreClase.setStyleSheet('background-color: rgb(255, 155, 155);')
            valido = False

        if valido == True :
            self.agregarALista()
            self.leNombre.setFocus()
            
    @QtCore.pyqtSlot()
    def on_btQuitar_clicked(self):
        # obtiene el indice en la lista en donde esta ubicado el elemento seleccionado
        indice = self.tablaAtributos.getSelectedCurrentIndex()
        del self.atributos[ indice ]
        # vuelve a cargar la lista
        self.tablaAtributos.addItems( [elemento[1:] for elemento in self.atributos] )
    
    @QtCore.pyqtSlot()
    def on_btExaminar_clicked(self):
        self.leUbicacion.setText(
            self.guardarArchivoPython())
    
    @QtCore.pyqtSlot()
    def on_btGenerar_clicked(self):
        if not self.leUbicacion.text().isEmpty() :
            self.generar()
        else:
            self.leUbicacion.setStyleSheet('background-color: rgb(255, 155, 155);')
        
    def on_twLista_doubleClicked(self , index):
        pass
    
    def on_clbtLevantarClaseStorm_pressed(self):
        self.guardarArchivoPython()
    
    @QtCore.pyqtSlot()
    def on_gbReferencia_clicked(self):
       self.leNombreReferencia.setText(
           unicode(self.leNombre.text().toUtf8(),'utf-8').capitalize())
    
#    @QtCore.pyqtSlot()
#    def on_chkGenerarPaquete_clicked(self):
#        ruta = ''
#        if self.chkGenerarPaquete.isChecked() :
#            ruta = os.path.splitext( unicode(self.leUbicacion.text().toUtf8(),'utf-8') )[0]
#        else:
#            ruta = os.path.splitext( unicode(self.leUbicacion.text().toUtf8(),'utf-8') )[0] + unicode(self.leNombreClase.text().toUtf8(),'utf-8').lower()
#        self.leUbicacion.setText( ruta )
    
########################################################################
    
    def guardarArchivoPython(self):
        u""" Muestra un cuadro de dialogo desde donde seleccionar un archivo. """
        nombre_archivo = unicode(self.leNombreClase.text().toUtf8(),'utf-8')
        dialog = QtGui.QFileDialog()   
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        filename = dialog.getSaveFileName(self, 'Abrir archivo Python',filter='*.py')
        if filename != '' :
            filename = unicode(filename, 'utf-8') + '.py' 
            
            return filename
        else:
            return ''
            
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
    
    def generar(self):
        logSC = LogicStormClass()
        
        destino = unicode(self.leUbicacion.text().toUtf8(),'utf-8')
        nombre_clase = unicode(self.leNombreClase.text().toUtf8(),'utf-8')
        
        logSC.generarClase(
            destino,
            nombre_clase,
            self.atributos,
            package = self.chkGenerarPaquete.isChecked())
        
        QtGui.QMessageBox.information(self, "Generar clase Storm + .ui",u"Generación realizada con éxito")
        
    
    def agregarALista(self):        
        elemento = self.getTextWidgets(
            self.leNombre,
            self.cbStormType,
            self.cbWidget,
            self.leValorPorDefecto,
            self.chkPrimario,
            self.chkNotNull)
        if self.gbReferencia.isChecked() :
            referencia = self.getTextWidgets(
            self.leNombreReferencia,
            self.chkCruzada)
            elemento += referencia
        else:
            elemento += ['','']
            
        un_atributo = self.convertToDict(
            ["atributo","storm_type","widget","default","primario","not_null","referencia","cruzada"],
            elemento
        )
        # agrega un atributo para generarse 
        self.atributos[ len(self.atributos) ] = un_atributo
        
        # agrega una fila a la tabla 
        self.tablaAtributos.appendItem( elemento )
        
        self.reestablecerCampos()
        
    def cargarWidgets(self,datos, widgets):
        import PyQt4        
        
        for dato, widget in zip(datos,widgets):         
            if type(widget) is PyQt4.QtGui.QLineEdit :
                widget.setText(dato)
            elif type(widget) is PyQt4.QtGui.QComboBox:                 
                widget.setCurrentIndex(
                    widget.findText(dato))
            elif type(widget) is PyQt4.QtGui.QLabel:
                widget.setText(dato)
            elif type(widget) is PyQt4.QtGui.QTextEdit:
                widget.setText(dato)
            elif type(widget) is PyQt4.QtGui.QDateEdit:                
                if len(dato) == 4 :
                    widget.setDate(PyQt4.QtCore.QDate(int(dato),1,1))
                elif len(dato) == 10 :
                    widget.setDate(PyQt4.QtCore.QDate(
                        int(dato[6:]),int(dato[3:5]),int(dato[:2])))
            elif type(widget) is PyQt4.QtGui.QSpinBox:    
                widget.setValue(int(dato))
            elif type(widget) is PyQt4.QtGui.QCheckBox:
                if dato == 'True' :
                    widget.setChecked(True)
                else:
                    widget.setChecked(False)

    def getTextWidgets(self, * widgets):
        """
        Devuelve una lista con el valor cargado segun el widget
        """
        import PyQt4
        values = []
        for widget in widgets :
            if type(widget) is PyQt4.QtGui.QLineEdit :
                values.append(
                    unicode(widget.text().toUtf8(),'utf-8'))
            elif type(widget) is PyQt4.QtGui.QComboBox:
                values.append(
                    unicode(
                        widget.itemText(widget.currentIndex()).toUtf8(),
                        'utf-8'))
            elif type(widget) is PyQt4.QtGui.QLabel:
                values.append(
                    unicode(widget.text().toUtf8(),'utf-8'))
            elif type(widget) is PyQt4.QtGui.QDateEdit:
                values.append(
                    unicode(
                        widget.date().toString(widget.displayFormat()).toUtf8(),
                        'utf-8'))
            elif type(widget) is PyQt4.QtGui.QTextEdit:
                values.append(
                    unicode(widget.toPlainText().toUtf8(),'utf-8'))
            elif type(widget) is PyQt4.QtGui.QSpinBox:
                values.append(
                    unicode(str(widget.value()),'utf-8')
                    )
            elif type(widget) is PyQt4.QtGui.QCheckBox :
                if widget.isChecked() == True :
                    values.append('True')
                else:
                    values.append('False')
                    
        return values
        
    def convertToDict(self, columnas, datos):
        resultado = {}
        for columna, valor in zip(columnas, datos) :
            resultado[columna] = valor
        return resultado
        
    def reestablecerCampos(self):
        self.cargarWidgets(
             [
             "",
             "Unicode",
             "QLineEdit",
             "",
             "False",
             "False",
             "",
             "False"
            ],
            [
             self.leNombre,
             self.cbStormType,
             self.cbWidget,
             self.leValorPorDefecto,
             self.chkPrimario,
             self.chkNotNull,
             self.leNombreReferencia,
             self.chkCruzada
             ]
        )
        self.gbReferencia.setChecked(False)
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = StormGuiMaker()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
