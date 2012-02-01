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

from TreeView import TreeView

class GenerarSenalesPy(QtGui.QMainWindow):

    def __init__(self, parent = None, cliptboard = None):
        FILENAME = 'generateSignals.ui'
        QtGui.QMainWindow.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
        self.setWindowState(QtCore.Qt.WindowMaximized)

        lexer = QsciLexerPython()
        self.qscArchivo.setLexer(lexer)
        self.qscSignals.setLexer(lexer)

        self.__setScintillaProperties(self.qscArchivo)
        self.__setScintillaProperties(self.qscSignals)

        self.logica = LogicaGenerarSenales()
        #~ self.tabla = MyTableWidget(self.twWidgets,["Tipo","Nombre"],False)
        self.arbolWidgets = TreeView(self.treeWidgets,self.on_arbolWidgets_selectedItem,self.connect)
        self.arbolWidgets.widget.setAcceptDrops(True)
        self.connect(self.arbolWidgets.widget, QtCore.SIGNAL('dropEvent()'),self.dropEventTree)
        self.connect(self.arbolWidgets.widget, QtCore.SIGNAL('dragEnterEvent()'),self.dragEnterEventTree)
        self.connect(self.arbolWidgets.widget, QtCore.SIGNAL('dragMoveEvent()'),self.dragMoveEventTree)
        self.cliptboard = cliptboard
        self.nombre_widget = ''
                
        self.logica.loadRecentFilesInCombo( self.cbArchivos )

    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def dropEventTree(self, event):
        
        print 'ohhhhhhhhhhhhh'
        print event.mimeData().hasUrls()
        pass
        
    def dragEnterEventTree(self, event):
        event.acceptProposedAction()
        
    def dragMoveEventTree(self, event):
        event.acceptProposedAction()
        
    @QtCore.pyqtSlot()
    def on_btAbrirPy_clicked(self):
        self.qscArchivo.setText(
                self.logica.abrirArchivoPython())

    @QtCore.pyqtSlot()
    def on_btAbrirUI_clicked(self):
        path = self.abrirArchivoUI()
        if path != None :
            widgets = self.logica.getWidgetsFromUI( path )
            self.logica.saveRecentFile( path )
            self.arbolWidgets.insertarEnArbol( widgets )
        self.logica.loadRecentFilesInCombo( self.cbArchivos )

    @QtCore.pyqtSlot(QtCore.QString)
    def on_cbArchivos_currentIndexChanged(self , index):
        path = unicode(self.cbArchivos.itemText(
                   self.cbArchivos.currentIndex()).toUtf8(),'utf-8')
        widgets = self.logica.getWidgetsFromUI( path )
        self.arbolWidgets.insertarEnArbol( widgets )
        
    def on_twWidgets_currentItemChanged(self, itema,itemb):
        self.logica.cargarSenalesWidget( self.twWidgets, self.lwSenales )

    @QtCore.pyqtSlot()
    def on_btAgregarSenial_clicked(self):        
        widget, signal = self.logica.obtenerDatosSenalAGenerar(self.lwSenales)
        self.logica.agregarSenial(widget, self.nombre_widget ,signal)
        self.qscSignals.setText( self.logica.generarCodigoFuenteSenales() )
        self.logica.agregarIdentacion4Espacios(self.qscSignals)

    @QtCore.pyqtSlot()
    def on_btQuitarSenial_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def on_btSaveFile_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def on_btUndo_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def on_btAddToFile_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def on_btSaveSignals_clicked(self):
        self.logica.guardarSenalesGeneradas(self.qscSignals)

    @QtCore.pyqtSlot()
    def on_btAddIdentation_clicked(self):
        self.logica.agregarIdentacion4Espacios(self.qscSignals)

    @QtCore.pyqtSlot()
    def on_btCopyCliptboard_clicked(self):
        self.cliptboard.setText(
            unicode(self.qscSignals.text().toUtf8(),'utf-8'))

    def on_qscArchivo_textChanged(self):
        pass

    def on_lwSenales_itemDoubleClicked(self, item) :
        self.on_btAgregarSenial_clicked()

    def on_arbolWidgets_selectedItem(self, itema, itemb):
        if itema.parent().row() != -1:
            self.tipo_widget =  unicode(itema.parent().data().toString().toUtf8(),'utf-8')
            self.nombre_widget =  unicode(itema.data().toString().toUtf8(),'utf-8')
        
            self.logica.cargarSenalesWidget( self.tipo_widget, self.lwSenales )
        
    def on_treeWidgets_doubleClicked(self , index):
        if self.chkAgregarSelf.isChecked() :
            self.teWidgets.append( "self." + self.nombre_widget )
        else:
            self.teWidgets.append( self.nombre_widget )
    
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
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = GenerarSenalesPy()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
