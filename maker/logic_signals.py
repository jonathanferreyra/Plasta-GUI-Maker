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

import signals

#############################################################################################
class LogicSignals():
    
    def __init__(self):
        pass
    
    def getListOfWidgets(self):
        """
        Obtiene una lista con todos los widtgets disponibles en la api.
        """
        widgets = signals.Widgets.keys()
        widgets.sort()
        return widgets
    
    def getWidgetInherit(self, widget):
        """    
        Devuelve una lista con todas las señales de la herencia de un widget.        
        """        
        senales,senales_herencia = [],[]        
        try:
            herencia = signals.Widgets[widget]['inherits']
        except KeyError :
            herencia = None
        if herencia != None :                                            
            # agrega el nombre de la herencia
            senales.append( herencia + ' :' )
            # agrega las señales de la herencia
            aux = signals.Widgets[herencia]['signals'].keys()
            aux.sort()
            senales += aux
            # obtiene als señales de la herencia de la herencia
            senales_herencia = self.getWidgetInherit( 
                    signals.Widgets[herencia]['inherits'] )
            if senales_herencia :
                senales += senales_herencia
        else :
            # sino tiene herencia devuelve las señales del actual widget
            if widget != None : 
                senales.append( widget + ' :' )
                senales += signals.Widgets[widget]['signals'].keys()
        
        return senales
            
    def getWidgetSignals(self, nameWidget):
        """
        """
        senales = []
        try:
            senales.append( nameWidget + ' :' )
            senales += signals.Widgets[nameWidget]['signals'].keys()
        except KeyError :
            # quita el ultimo elemento agregado, en este caso el titulo
            senales.put()
        return senales
    
    def getWidgetSignalsWithInherit(self, nameWidget):
        """
        """
        senales = self.getWidgetSignals( nameWidget )
        if signals.Widgets[nameWidget]['inherits'] != None :
            senales_herencia = self.getWidgetInherit( nameWidget )
            senales += senales_herencia
        return senales
        
    def getWidgetsFromUI(self, pathUI):
        """
        Devuelve un diccionario con los widgets contenidos en un .ui,
        con el formato {nombreWidget:tipoWidget}. 
        """
        import re   
        ui = open(pathUI,'r')
        fuente_ui = ui.read()
        ui.close()
        return re.findall('<widget class="(.+)\" name="(.+)\">',fuente_ui)
    
    def generarCodigoFuenteSenales(self, datos_senales):
        """
        Genera el codigo fuente para cada señal del widget.
        """
        #~ print 'generarCodigoFuenteSenales>> ', datos_senales
        #  cada elemento del diccionario correspondera a un metodo que 
        #  se generara para el manejo de una señal determinada para un 
        #  widget.
        
        #  formato elemento diccionario:
        #  ejemplo = {'QPushButton_btGuardar':{
        #  'widget':'QPushButton',
        #  'nombre':'btGuardar',
        #  'signal': 'clicked ()'}}
        
        #  primero pregunta si hay una sobrecarga para el mismo metodo.        
        #  si es asi, obtiene el parametro correspondiente y agrega el 
        #  parametro al metodo. despues reemplaza el nombre del widget 
        #  y por ultimo elo nombre de la señal.
        all_fuente = ''
        for senal in datos_senales :            
            all_fuente += self.generarCodigoFuenteSenal(
                senal['widget'],
                senal['nombre'],
                senal['signal'])
        return all_fuente
        
    def generarCodigoFuenteSenal(self, widget, nombreWidget, senial) :
        """
        """
        
        metodo = signals.plantilla_metodo
        if self.tieneSobrecarga(widget, senial) == True :
            decorador = signals.plantilla_decorador
            parametros = signals.Widgets[widget]['signals'][senial].split('|')
            decorador = decorador.replace('()','('+ parametros[0] + ')')
            if parametros[1] != '' : 
                metodo = metodo.replace('self','self , ' + parametros[1])
            metodo = decorador + metodo
        else :
            parametros = signals.Widgets[widget]['signals'][senial]
            if parametros != '' :
                metodo = metodo.replace('self','self , ' + parametros)
        metodo = metodo.replace('nombreWidget',nombreWidget)
        metodo = metodo.replace('senial',senial.split()[0])
        return metodo
        
    def tieneSobrecarga(self, widget, signal) :
        """
        Devuelve True, si la señal indicada posee sobrecarga.
        """
        all_signals = signals.Widgets[widget]['signals'].keys()        
        veces = 0
        for metodo in all_signals :
            if metodo.find(signal.split()[0]) != -1 : 
                veces += 1
        return True if veces > 1 else False    
        
if __name__ == "__main__":
    ls = LogicSignals()   
    
    #~ a = ls.getWidgetSignalsWithInherit('QObject')
    #~ for e in a : print e        
    #~ print ls.tieneSobrecarga('QAbstractButton','clicked ()')
    #~ datos = {
    #~ 'QComboBox_cbNombre':{
    #~ 'widget':'QComboBox',
    #~ 'nombre':'cbNombre',
    #~ 'signal':'editTextChanged (const QString&)'},
    #~ 'QListWidget_lwNombres':{
    #~ 'widget':'QListWidget',
    #~ 'nombre':'lwNombres',
    #~ 'signal':'currentItemChanged (QListWidgetItem *,QListWidgetItem *)'},
    #~ 'QAbstractButton_btAceptar':{
    #~ 'widget':'QAbstractButton',
    #~ 'nombre':'btAceptar',
    #~ 'signal':'clicked ()'}
    #~ }
    #~ print ls.generarCodigoFuenteSenales(datos)
    
