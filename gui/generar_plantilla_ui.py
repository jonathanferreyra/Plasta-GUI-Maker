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

# TODO: historial de archivos abiertos


import os,sys
from PyQt4 import QtCore, QtGui, uic
from images import qtgui_art
from PyQt4.Qsci import QsciScintilla, QsciLexerPython

from logic_generar_senales import LogicaGenerarSenales
from mytablewidget import MyTableWidget
from api.logic_methods import LogicMethods
from TreeView import TreeView
import pathtools

class GenerarPlantillaUI(QtGui.QMainWindow):

    def __init__(self, parent = None):
        FILENAME = 'generar_plantilla_ui.ui'
        QtGui.QMainWindow.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
        self.setWindowState(QtCore.Qt.WindowMaximized)        
        
        # atrubutos e instancias
        self.logica = LogicaGenerarSenales()
        self.lm = LogicMethods()
        self.generar_en = ''
        self.nombre_ui = ''
        self.nombre_clase = ''
        self.nombre_widget = ''
        self.path_ui = ''
        
        self.arbolWidgets = TreeView(self.treeWidgets,self.on_arbolWidgets_selectedItem,self.connect)        
        self.tablaMetodos = MyTableWidget(self.twMetodos,['Metodo'])
        
        # llamada a metodos
        lexer = QsciLexerPython()
        self.qscArchivo.setLexer(lexer)        
        self.__setScintillaProperties(self.qscArchivo)

        self.logica.loadRecentFilesInCombo( self.cbArchivos )
        self.cargarPlantilla()
        self.cargarListaMetodos()
        
    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
        
    @QtCore.pyqtSlot()
    def on_btAbrirPy_clicked(self):
        self.qscArchivo.setText(
                self.logica.abrirArchivoPython())

    @QtCore.pyqtSlot()
    def on_btAbrirUI_clicked(self):
        self.path_ui = self.abrirArchivoUI()
        if self.path_ui != None :
            widgets = self.logica.getWidgetsFromUI( self.path_ui )
            self.logica.saveRecentFile( self.path_ui )
            self.arbolWidgets.insertarEnArbol( widgets )
            self.nombre_ui = self.getFileName( self.path_ui )
        self.logica.loadRecentFilesInCombo( self.cbArchivos )
        
    @QtCore.pyqtSlot(QtCore.QString)
    def on_cbArchivos_currentIndexChanged(self , index):
        self.path_ui = unicode(self.cbArchivos.itemText(
                   self.cbArchivos.currentIndex()).toUtf8(),'utf-8')
        widgets = self.logica.getWidgetsFromUI( self.path_ui )
        self.arbolWidgets.insertarEnArbol( widgets )
        self.nombre_ui = self.getFileName( self.path_ui )
        
    def on_twWidgets_currentItemChanged(self, itema,itemb):
        self.logica.cargarSenalesWidget( self.twWidgets, self.lwSenales )

    @QtCore.pyqtSlot()
    def on_btAgregarSenial_clicked(self):        
        widget, signal = self.logica.obtenerDatosSenalAGenerar(self.lwSenales)
        self.logica.agregarSenial(widget, self.nombre_widget ,signal)                
        metodo = 'on_%s_%s' % (self.nombre_widget, signal)
        self.lwMetodos.addItem( metodo )
        
    @QtCore.pyqtSlot()
    def on_btQuitarMetodo_clicked(self):
        pass
    
    @QtCore.pyqtSlot()
    def on_btSubir_clicked(self):
        pass
    
    @QtCore.pyqtSlot()
    def on_btBajar_clicked(self):
        pass
    
    @QtCore.pyqtSlot()
    def on_btExaminar_clicked(self):
        self.generar_en = self.logica.guardarArchivo()
        self.leUbicacion.setText(self.generar_en)
        
    @QtCore.pyqtSlot()
    def on_btGenerarPlantilla_clicked(self):
        valido = True
        if self.leNombreClase.text().isEmpty() :
            self.leNombreClase.setStyleSheet('background-color: rgb(255, 107, 107);')
            valido = False
        if self.leUbicacion.text().isEmpty() :
            self.leUbicacion.setStyleSheet('background-color: rgb(255, 107, 107);')
            valido = False
        
        if valido :
            self.generarPlantilla()

    def on_lwSenales_itemDoubleClicked(self, item) :
        self.on_btAgregarSenial_clicked()

    def on_arbolWidgets_selectedItem(self, itema, itemb):
        if itema.parent().row() != -1:
            self.tipo_widget =  unicode(itema.parent().data().toString().toUtf8(),'utf-8')
            self.nombre_widget =  unicode(itema.data().toString().toUtf8(),'utf-8')
        
            self.logica.cargarSenalesWidget( self.tipo_widget, self.lwSenales )
        
    
    def __setScintillaProperties(self, editor) :
        editor.setMarginsForegroundColor(QtGui.QColor("#1A1A1A"))
        editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        editor.setCaretLineVisible(True)
        editor.setCaretLineBackgroundColor(QtGui.QColor("#F5F5DC"))
    
    def abrirArchivoUI(self):
        dialog = QtGui.QFileDialog(None, 'Abrir archivo UI')
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        dialog.setDefaultSuffix('ui')
        dialog.setNameFilter('Archivo UI (*.ui)')
        
        if dialog.exec_():
            filename = dialog.selectedFiles()[0] # convierte a unicode el string
            filename = unicode(filename, 'utf-8') #
            return filename
        else : None
        
    def cargarPlantilla(self):
        path = pathtools.getPathProgramFolder() + 'api/plantilla_clase.py'
        plantilla = open(path,'r')
        self.qscArchivo.setText(
            plantilla.read())
        plantilla.close()
        
    def getFileName(self, path):
        import os.path
        return os.path.splitext(
            os.path.split(path)[1])[0]
        
    def cargarListaMetodos(self):
        metodos = self.lm.getListOfMethods()
        metodos = map(lambda item : (item,), metodos)
        self.tablaMetodos.addItems( metodos )
        
    def obtenerMetodosAuxiliares(self):
        items = self.tablaMetodos.getAllItems()
        # obtengo los que estan checkeados
        metodos = []
        for item in items :
            if item[0] is True :
                metodos.append(item[1])
        return metodos
        
    def obtenerTipoVentana(self, path_ui):
        contenido = open(path_ui,'r').read()
        if contenido.find('QMainWindow') != -1 :
            return 'QMainWindow'
        else:
            return 'QDialog'
            
    def generarPlantilla(self):
        self.nombre_clase = unicode(self.leNombreClase.text().toUtf8(),'utf-8')        
        self.lm.generaPlantillaClaseUI(
            self.generar_en,
            self.nombre_ui,
            self.obtenerTipoVentana(self.path_ui),
            self.nombre_clase,
            self.obtenerMetodosAuxiliares(),
            self.logica.generarCodigoFuenteSenales())        
        QtGui.QMessageBox.information(self, "Generar plantilla","Plantilla generada correctamente.")
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = GenerarPlantillaUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
