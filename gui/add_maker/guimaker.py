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
from gui.mytablewidget import MyTableWidget
from gui import pathtools
from maker import add_maker_simple as gui_maker

class GuiMaker(QtGui.QMainWindow):

    def __init__(self, parent = None):
        FILENAME = 'guimaker.ui'
        QtGui.QMainWindow.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.setWindowTitle("Crear ui - Plasta GUI Maker")
        self.__center()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)
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
            QtGui.QMessageBox.warning(self, "Crear Ui","No se ha seleccionado un destino para el archivo de salida.")
        else:
            if len(self.__widgets) != 0 :

                widgets_a_generar = self.obtenerWidgetsAGenerer()
                opts, btns = self.getOpcionesGeneracion()
                destino = self.__toUnicode(self.leSalida.text())

                if self.generarUI( destino, widgets_a_generar, opts, btns) :
                    QtGui.QMessageBox.information(self, "Crear Ui",u"Generación realizada con éxito.")
                    self.close()
            else:
                QtGui.QMessageBox.warning(self, "Crear Ui","No hay widgets para generar.")

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
            filename = QtGui.QFileDialog.getSaveFileName(self,"Guardar .ui")
            if filename:
                filename = unicode(filename, 'utf-8')
                if filename.find('.ui') == -1:
                    filename += '.ui'
                return filename
            return ''

    def __abrirSqlite(self):
            """ """
            filename = QtGui.QFileDialog.getOpenFileName(self,"Abrir archivo SQLite")
            if filename:
                filename = unicode(filename, 'utf-8')
                self.lbArchivoSqlite.setText(filename)
                self.gui.showSeleccionarCampos(self,filename)

    def generarUI(self, destino, widgets_a_generar, opts, btns):
        """
        """
        return gui_maker.generarUI(
            destino,
            widgets_a_generar,
            botones = btns,
            opciones = opts)

    def obtenerWidgetsAGenerer(self):
        widgets_a_generar = {}
        for widget in self.__widgets :
            widgets_a_generar[widget[0]] = {widget[1]:widget[2]}
        return widgets_a_generar

    def __toUnicode(self,myQstring):
        u""" Convierte a UTF8 el objeto QString recibido. """
        return unicode(myQstring.toUtf8(),'utf-8')

    def cargarCamposDesdeBD(self, datos) :
        # carga en al lista lso datos recibidos desde el dialogo
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
