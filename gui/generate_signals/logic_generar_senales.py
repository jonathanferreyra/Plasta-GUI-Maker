#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       
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

from maker.logic_signals import LogicSignals
import os
from PyQt4 import QtCore, QtGui
 

class LogicaGenerarSenales():
    
    def __init__(self):    
        self.seniales = []
        pass
    
    def obtenerSenalesWidget(self, widget):
        LS = LogicSignals()
        return LS.getWidgetSignalsWithInherit(widget)
    
    def obtenerWidgetDesdeUI(self, pathUI):
        LS = LogicSignals()
        widgets = self.ordenarListaListas(
            LS.getWidgetsFromUI(pathUI),
            0)
        return widgets

    def abrirArchivoPython(self):
        u""" Muestra un cuadro de dialogo desde donde seleccionar un archivo. """
        
        files = QtGui.QFileDialog.getOpenFileNames(None,'Abrir archivo Python','/home',filter = '*.py')
            
        if files: 
            fname = open(files[0])
            data = fname.read()
            return data
        else:
            return ''  
    
    def getWidgetsFromUI(self, ruta):        
        if ruta:             
            widgets = self.obtenerWidgetDesdeUI( ruta )
            return widgets
                        
    def agregarSenial(self, widget, nombre, signal):
        self.seniales.append({
        'widget':widget,
        'nombre':nombre,
        'signal':signal
        })
        
    def generarCodigoFuenteSenales(self):
        LS = LogicSignals()
        return LS.generarCodigoFuenteSenales( self.seniales )
        
    def guardarArchivo(self):
        filename = QtGui.QFileDialog.getSaveFileName(
                    None,
                    'Arhivo Fuente Python',
                    "/home",
                    filter = '*.py')           
        return unicode(filename,'utf-8') + '.py'
        
    def guardarSenalesGeneradas(self, editor) : 
        fileName = QtGui.QFileDialog.getSaveFileName(
                            None,
                            "Guardar",
                            "/home",
                            filter = '*.py')
        
        if fileName:
            filename = fileName[0]
            archivo = open(filename, 'w')
            contenido = unicode(editor.text().toUtf8(),'utf-8')
            archivo.write(contenido)
            archivo.close()
            
    def agregarIdentacion4Espacios(self, editor) :
        texto_actual = unicode(editor.text().toUtf8(),'utf-8')        
        texto_nuevo = map(
            lambda linea : '    ' + linea , 
            texto_actual.split('\n'))
        editor.setText( '\n'.join(texto_nuevo) )
        
    def obtenerDatosSenalAGenerar(self, lista):
        signal = unicode(lista.currentItem().text().toUtf8(),'utf-8')
        signal_index = lista.currentRow()
        encontrado = False
        # obtiene el <padre> a quien corresponde la señal 
        while (signal_index > 0) and (not encontrado):
            signal_index -= 1
            item = lista.item(signal_index)
            item_text = unicode(item.text().toUtf8(),'utf-8')  
            if item_text.find(' :') != -1 :
                encontrado = True
                widget = item_text.replace(' :','')
        return widget, signal
        
    def cargarSenalesWidget(self, widget, lista) :
        lista.clear()
        fuente = QtGui.QFont()
        item = None
        
        widget_signals = self.obtenerSenalesWidget(widget)
        
        for signal in widget_signals :
            item = QtGui.QListWidgetItem(signal)
            if signal.find(' :') != -1 :
                fuente.setBold(True)
                item.setFont(fuente)    
            
            lista.addItem(item) 
            
    def ordenarListaListas(self, lista,nroCampo): 
        """Ordena la lista por el metodo burbuja mejorado.
        Recibe una lista de listas y un numero de campo,
        ordenando por el nro de campo indicado.
        """ 
        intercambios=1 
        pasada=1 
        while pasada<len(lista) and intercambios==1: 
            intercambios=0 
            for i in range(0,len(lista)-pasada): 
                if lista[i][nroCampo] > lista[i+1][nroCampo]: 
                    lista[i], lista[i+1] = lista[i+1], lista[i] 
                    intercambios=1 
            pasada += 1 
        return lista 
        
    def checkHistoryFile(self):
        if not os.path.exists('history') :
            archivo = open('history','w')
            archivo.close()
            
    def getRecentFiles(self):
        self.checkHistoryFile()     
        archivo = open('history','r')
        todo = archivo.readlines()
        validos = []
        for linea in todo:
            if os.path.exists(linea) : 
                validos.append(linea)
        archivo.close()
        return validos
        
    def loadRecentFilesInCombo(self, combo):
        archivos = self.getRecentFiles()
        archivos[::-1]
        archivos = map(lambda archivo : archivo.replace('\n','') , archivos)
        archivos = map(lambda archivo : archivo.replace('\r','') , archivos)
        combo.clear()
        combo.addItems( archivos ) 
        
    def saveRecentFile(self, path) :
        archivo = open('history','r')
        todo = archivo.readlines()
        archivo.close()
        archivo = open('history','w')
        if not path in todo : 
            todo.append(path)
        archivo.write('\n'.join(todo))
        archivo.close()
        
def main():
    lgs = LogicaGenerarSenales()
    lgs.obtenerWidgetDesdeUI('D:\ProyectosOn\MEGLabsMakers\GUIMaker\src\gui\seleccionar_campos.ui')

if __name__ == "__main__":
    main()
