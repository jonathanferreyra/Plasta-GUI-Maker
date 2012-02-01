#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Emiliano Fernandez <emilianohfernandez@gmail.com>
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

    def __init__(self,TW,listadecolumnas,checkeable=False):
        self.__widget = TW
        self.__widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        quitAction = QtGui.QAction("Quit", self.__widget)
        self.__widget.addAction(quitAction)
        self.__widget.horizontalHeader().setStretchLastSection(True)#maximixa los campos en la tabla
        self.__widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.__widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        self.__widget.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )

        self.__columns=listadecolumnas
        self.__itemsChecked = []
        self.__checkeable = checkeable

    def getItemsChecked(self):
        return self.__itemsChecked

    def checkeado(self):
        """des/checkea el item seleccionado en el list widget"""
        item = self.getRowString()
        if not (item in self.__itemsChecked):
            self.__itemsChecked.append(item)
            return True
        else:
            self.__itemsChecked.remove(item)
            return False

    def appendItem(self,listadedatos):
        widget = self.__widget
        y = widget.rowCount()
        #~ print y
        if listadedatos != None:
            agregado = 1 if self.__checkeable else 0
            if self.__checkeable:
                item = self.__setCheckItem(listadedatos,y)

            widget.setRowCount(y+1)

            for x, cell in enumerate(listadedatos):
                #~ print x,cell
                # the text
                item = QtGui.QTableWidgetItem(cell)
                #~ print item.flags(QtCore.QAbstractTableModel.flags( self, index ))
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable )
                # the alignment
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                widget.setItem(y, x+agregado, item)
            widget.resizeColumnsToContents()
        pass

    def addItems(self, DATA):
        """
        DATA debe ser una lista de listas
        """
        if DATA != None:
            if self.__checkeable:
                agregado = 1#1 si es chequed
                columns = [''] + self.__columns
            else:
                agregado = 0
                columns = self.__columns

            #~ print "Cargando datos...."
            widget = self.__widget
            widget.setColumnCount(len(self.__columns)+agregado)
            widget.setRowCount(len(DATA))
            # delete vertical headers
            for i in range(widget.rowCount()):
                widget.setVerticalHeaderItem(i, QtGui.QTableWidgetItem())
            # set horizontal headers
            for i in xrange(widget.columnCount()):
                # the text
                item = QtGui.QTableWidgetItem(columns[i].capitalize())
                # the alignment
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                widget.setHorizontalHeaderItem(i, item)

            # set data
            for y, row in enumerate(DATA):
                #~ print '>>>>>>>>>>',row
                if agregado:
                    item = self.__setCheckItem(row,y)
                for x, cell in enumerate(row):
                    # the text
                    item = QtGui.QTableWidgetItem(cell)
                    #~ print item.flags(QtCore.QAbstractTableModel.flags( self, index ))
                    item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable )
                    # the alignment
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    widget.setItem(y, x+agregado, item)
            widget.resizeColumnsToContents()

    def __setCheckItem(self,row,y):
        """Metodo utilizado para checked en add_data
        Agrega un item checkeable al principio de la fila y lo checkea
        si esta en self.__itemsChecked"""
        item = QtGui.QTableWidgetItem('')
        check = (True,) + row
        if check in self.__itemsChecked :
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(False)
        # the alignment
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        #meter item
        self.__widget.setItem(y, 0, item)
        return item

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
                #se pregunta si el primero es check(debe tener el texto vacio "")
                if (num == 0) and (tablewidget.item(x,0).text() == ""):
                    #verifica el estado del check
                        #Qt.Unchecked   0   The item is unchecked.
                        #Qt.PartiallyChecked    1   The item is partially checked. It
                        #Qt.Checked 2   The item is checked.
                    if tablewidget.item(x,0).checkState() == 0:
                        datos.append(False)
                    else:
                        datos.append(True)
                else:
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
        print tamano
        coordenadas = list(range(tamano))
        coordenadas.reverse()
        for y in coordenadas:
            print 'y:',y
            self.__widget.removeRow(y)

    def __get_widget(self):
        return self.__widget

    def __set_widget(self, value):
        self.__widget = value 

    widget = property(__get_widget, __set_widget, "widget's docstring")

    
    
        
def main():

    return 0

if __name__ == '__main__':
    main()

