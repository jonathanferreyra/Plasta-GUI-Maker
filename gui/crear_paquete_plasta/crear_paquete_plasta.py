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
from gui import pathtools
from PyQt4 import QtCore, QtGui, uic
from maker import make_plasta_package

class CrearPaquetePlasta(QtGui.QMainWindow):

    def __init__(self, parent = None):
        FILENAME = 'crear_paquete_plasta.ui'
        QtGui.QMainWindow.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)

        self.parent = parent
        self.data = {
            'storm_attrs':[], #{'name':'attr1', 'type':'Unicode'}
            'add_attrs':[], #{'widget':'QLineEdit', 'attr':'attr1'}
        }
        self.loadCbTipoAtributoCS()
        self.load_cbWidgetAC()
        self.__setCurrentUserPath()

    def __centerOnScreen (self):
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __setCurrentUserPath(self):
        homedir = os.path.expanduser("~")
        homedir = pathtools.convertPath(homedir)
        self.leUbicacionResultado.setText(homedir)

    def _getValueCombo(self, widget):
        return unicode(widget.itemText(
            widget.currentIndex()).toUtf8(), 'utf-8' )

    def toUnicode(self, text):
        return unicode( text.toUtf8(), 'utf-8' )

    def getData(self):
        data = {
        'className':self.toUnicode(self.leNombreClaseCS.text()),
        'addIdeAttr':self.chkAddIdeAttr.isChecked(),
        'attributes':self.data['storm_attrs'], # {'name':'attr1','type':'Unicode'},
        'widgetToAttr':{
          # 'attr1':'lineEdit',
          # 'attr2':'comboBox',
          # 'attr3':'spinBox',
        },
        'classesToGenerate':{
          'storm':self.btGenerarCS.isChecked(),
          'manager':self.btGenerarCM.isChecked(),
          'gui':self.btGenerarGM.isChecked(),
          'add':self.btGenerarAg.isChecked()
        },
        'outputFolder':self.toUnicode(self.leUbicacionResultado.text())
        }
        for r in self.data['add_attrs']:
            data['widgetToAttr'][r['attr']] = r['widget']
        return data

    ### TAB CLASE STORM

    def loadCbTipoAtributoCS(self):
        types = ['Unicode', 'Int', 'Float', 'Date', 'Time']
        self.cbTipoAtributoCS.clear()
        map( self.cbTipoAtributoCS.addItem, types)


    def reloadListAtributoCS(self):
        self.lwAtributosCS.clear()
        [self.lwAtributosCS.addItem('%s -> %s' % (a['name'], a['type']))
            for a in self.data['storm_attrs']]

    ### TAB AGREGAR

    def load_cbWidgetAC(self):
        types = ['lineEdit', 'comboBox', 'spinBox', 'doubleSpinBox',
            'textEdit','dateEdit','dateTimeEdit','timeEdit']
        self.cbWidgetAC.clear()
        map( self.cbWidgetAC.addItem, types)

    def load_cbAtributoAC(self):
        items = [a['name'] for a in self.data['storm_attrs']]
        self.cbAtributoAC.clear()
        map( self.cbAtributoAC.addItem, items)

    def reload_lwListaAC(self):
        self.lwListaAC.clear()
        [self.lwListaAC.addItem('%s -> %s' % (a['attr'], a['widget']))
            for a in self.data['add_attrs']]

###############################################################################

    def on_leNombreClaseCS_textEdited(self , text):
        value = self.toUnicode(text)
        valueCap = value.capitalize()
        self.leNombreClaseCM.setText(valueCap + "Manager")
        self.leNombreClaseGM.setText(valueCap + "GUI")
        self.leNombreClaseAC.setText("Add" + valueCap)

        self.data['className_parsed'] = value.lower().strip().replace(' ', '_')
        #t = self.toUnicode(self.leUbicacionResultado.text())
        #self.leUbicacionResultado.setText(
        #    pathtools.convertPath(t + '/' + self.data['className_parsed']))

    @QtCore.pyqtSlot()
    def on_btAgregarAtributoCS_clicked(self):
        attr = self.toUnicode(self.leNombreAtributoCS.text())
        if len(attr) > 0:
            if attr not in [a['name'] for a in self.data['storm_attrs']]:
                typeSelected = self._getValueCombo(self.cbTipoAtributoCS)
                self.data['storm_attrs'].append({'name':attr, 'type':typeSelected})
                self.reloadListAtributoCS()
                self.leNombreAtributoCS.setText('')
                self.load_cbAtributoAC()
                self.leNombreAtributoCS.setFocus()

    @QtCore.pyqtSlot()
    def on_btEliminarAtributoCS_clicked(self):
        item = self.lwAtributosCS.currentItem()
        if item:
            idx = self.lwAtributosCS.row(item)
            del self.data['storm_attrs'][idx]
            self.reloadListAtributoCS()

###########################################################

    @QtCore.pyqtSlot()
    def on_btAgregarAC_clicked(self):
        widget = self._getValueCombo(self.cbWidgetAC)
        attr = self._getValueCombo(self.cbAtributoAC)
        if attr not in [a['attr'] for a in self.data['add_attrs']]:
            self.data['add_attrs'].append({'attr':attr, 'widget':widget})
            self.reload_lwListaAC()

    @QtCore.pyqtSlot()
    def on_btEliminarAC_clicked(self):
        item = self.lwListaAC.currentItem()
        if item:
            idx = self.lwListaAC.row(item)
            del self.data['add_attrs'][idx]
            self.reload_lwListaAC()

###########################################################

    @QtCore.pyqtSlot()
    def on_btExaminar_clicked(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, 'Seleccionar carpeta de destino')
        self.leUbicacionResultado.setText(directory)

    @QtCore.pyqtSlot()
    def on_btGenerar_clicked(self):
        data = self.getData()
        if len(data['className']) > 0:
            try:
                import shutil, os.path
                outputFolder = pathtools.convertPath('%s/%s' % (data['outputFolder'], self.data['className_parsed']))
                if os.path.exists(outputFolder):
                    shutil.rmtree(outputFolder)
                make_plasta_package.generatePackage(data)
                QtGui.QMessageBox.information(self, "", "Paquete Plasta generado ok!")
                self.close()
            except Exception, e:
                QtGui.QMessageBox.critical(self, "", "Upps! Algo salio mal :/")
                raise e

def main():
    app = QtGui.QApplication(sys.argv)
    window = CrearPaquetePlasta()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
