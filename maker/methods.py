#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2012 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
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

convertToDict = \
'''def convertToDict(self, columnas, datos):
    resultado = {}
    for columna, valor in zip(columnas, datos) :
        resultado[columna] = valor
    return resultado'''

getFechaHoyString = \
'''def getFechaHoyString(self):
    from datetime import datetime
    hoy = datetime.today().strftime('%d-%m-%Y HH:mm:ss')
    return hoy'''

normalizarBlancos = \
'''def normalizarBlancos(self, lista):
    """
    Reemplaza los espacios por un guion medio.
    """
    return map(lambda elemento : elemento if elemento != '' else '-',lista)'''

getTextWidgets = \
'''def getTextWidgets(self, * widgets):
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
        # hack solo para esta situacion
        elif type(widget) is PyQt4.QtGui.QCheckBox :
            if widget.isChecked() is True :
                values.append('SI')
            else:
                values.append('NO')
                
    return values'''
    
cargarWidgets = \
'''def cargarWidgets(self,datos, widgets):
    import PyQt4
    for dato, widget in zip(datos,widgets):
        if type(widget) is PyQt4.QtGui.QLineEdit :
            widget.setText(dato)
        elif type(widget) is PyQt4.QtGui.QComboBox:
            widget.addItem(dato)
        elif type(widget) is PyQt4.QtGui.QLabel:
            widget.setText(dato)
        elif type(widget) is PyQt4.QtGui.QTextEdit:
            widget.setText(dato)'''

metodos = {
'convertToDict':convertToDict,
'getFechaHoyString':getFechaHoyString,
'normalizarBlancos':normalizarBlancos,
'getTextWidgets':getTextWidgets,
'cargarWidgets':cargarWidgets
}
