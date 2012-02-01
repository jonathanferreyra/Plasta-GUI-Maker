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

import methods

#############################################################################################
class LogicMethods():
    
    def __init__(self):
        self.metodos = methods.metodos
        pass
    
    def getListOfMethods(self):
        metodos = self.metodos.keys()
        metodos.sort()
        return metodos
    
    def getTextOfMethods(self, metodos):
        """
        Obtiene una cadena que correspode a los metodos pasados por parametro.
        """
        todo = ''
        for metodo in metodos :
            todo += self.metodos[metodo] + '\n'
        return todo
        
    def generaPlantillaClaseUI(self, 
                                destino, 
                                nombre_ui, 
                                tipo_ventana, 
                                nombre_clase, 
                                metodos_auxiliares, 
                                metodos_seniales):
        """
        """
        plantilla = self.obtenerContenidoPlantilla()
        
        # reemplaza el nombre de la clase
        plantilla = plantilla.replace('%nombre_clase%',nombre_clase)
        # reemplaza el nombre de la clase
        plantilla = plantilla.replace('%tipo_ventana%',tipo_ventana)
        # reemplaza el nombre del ui
        plantilla = plantilla.replace('%nombre_ui%',nombre_ui)
        # reemplaza el nombre de los metodos de las señales
        if metodos_seniales != '' :
            plantilla = plantilla.replace('%metodos_senales%',
                self.aplicarIdentacion(metodos_seniales))
        else:
            plantilla = plantilla.replace('\n%metodos_senales%','')
        
        # reemplaza el nombre de los metodos auxiliares     
        if len(metodos_auxiliares) > 0 :
            st_metodos_auxiliares = self.getTextOfMethods( metodos_auxiliares )
            plantilla = plantilla.replace('%metodos_auxiliares%',
                self.aplicarIdentacion(st_metodos_auxiliares))
        else:
            plantilla = plantilla.replace('\n%metodos_auxiliares%','')
                
        self.guardarPlantilla( destino, plantilla )
        return True
        
    def guardarPlantilla(self, destino, contenido):
        plantilla = open(destino,'w')
        plantilla.write(contenido.encode('utf-8'))
        plantilla.close()
        
    def obtenerContenidoPlantilla(self):
        import os
        plantilla = open(os.getcwd() + '/api/plantilla_clase.py','r')
        contenido = unicode(plantilla.read(),'utf-8')
        plantilla.close()
        return contenido
        
    def aplicarIdentacion(self, texto):
        lineas = texto.split('\n')
        lineas = map(lambda linea : '    ' + linea, lineas)
        return '\n'.join(lineas)
        
if __name__ == "__main__":
    lm = LogicMethods()   
    
