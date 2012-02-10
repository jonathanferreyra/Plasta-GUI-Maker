#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
#       Copyright 2011 Fernandez, Emiliano <emilianohfernandez@gmail.com>
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
from PyQt4 import QtCore, QtGui


class MyTableWidget():

    def __init__(self,TW,listadecolumnas):
        self.__widget = TW
        self.__widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        quitAction = QtGui.QAction("Quit", self.__widget)
        self.__widget.addAction(quitAction)
        self.__widget.horizontalHeader().setResizeMode(1)#maximixa los campos en la tabla
        self.__widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.__widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        self.__widget.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )

        self.__columns=listadecolumnas

    def appendItem(self,listadedatos):
        widget = self.__widget
        y = widget.rowCount()
        if listadedatos != None:
            widget.setRowCount(y+1)
            for x, cell in enumerate(listadedatos):
                item = QtGui.QTableWidgetItem(unicode(cell))# the text
                #~ print item.flags(QtCore.QAbstractTableModel.flags( self, index ))
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable )
                item.setTextAlignment(QtCore.Qt.AlignCenter)# the alignment
                widget.setItem(y, x, item)

    def addItems(self, DATA):
        """
        DATA debe ser una lista de listas
        """
        if DATA != None:
            agregado = 0
            columns = self.__columns
            widget = self.__widget
            widget.setColumnCount(len(self.__columns)+agregado)
            widget.setRowCount(len(DATA))
            for i in range(widget.rowCount()):     # delete vertical headers
                widget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem())
            for i in xrange(widget.columnCount()):  # set horizontal headers
                item = QtGui.QTableWidgetItem(columns[i].capitalize())# the text
                item.setTextAlignment(QtCore.Qt.AlignCenter)# the alignment
                widget.setHorizontalHeaderItem(i, item)
            
            self.fullClear()
            map(self.appendItem,DATA)

    def getRowString(self, item = 'null'):
        """Devuelve una tupla con los datos de el tablewidget en la fila seleccionada
        devuelve los datos en unicode"""
        tablewidget = self.__widget
        tamano = tablewidget.columnCount()
        try:
            if item != 'null':
                x = item
            else:
                x = tablewidget.currentItem().row()  
            datos=[]
            for num in range(tamano):
                qs = tablewidget.item(x,num).text()
                datos.append(unicode(qs.toUtf8(),'utf-8'))
            return tuple(datos)
        except Exception :
            return None
    
    def getListSelectedRows(self):
        rows = [] 
        seleccionados = self.__widget.selectionModel().selectedRows()
        for idx in  seleccionados :
            rows.append(self.getRowString(idx.row()))
        return rows

    def getAllItems(self):
        tamano = self.__widget.rowCount()
        allitemstring = []
        for y in range(tamano):
            allitemstring.append(self.getRowString(y))
        return allitemstring

    def fullClear(self):
        tamano = self.__widget.rowCount()
        coordenadas = list(range(tamano))
        coordenadas.reverse()
        map(self.__widget.removeRow,coordenadas)

    def __get_widget(self):
        return self.__widget

    def __set_widget(self, value):
        self.__widget = value 

    widget = property(__get_widget, __set_widget, "widget's docstring")

    def getSelectedCurrentIndex(self):
        return self.__widget.currentItem().row() 
    
    
        
def main():

    return 0

if __name__ == '__main__':
    main()

