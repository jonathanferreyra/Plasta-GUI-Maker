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

import os.path
import shutil
import pathtools
import prefijos_widgets
import xml_widgets

############################## Funciones ###############################

def __palabra_mas_larga(palabra1, palabra2):
    """
    Obtiene la longitud del nombre mas largo de los widgets que se estan usando.
    A partir de esta longitud se setean despues la lingitud de los labels en la GUI.
    """
    return palabra1 if len(palabra1) > len(palabra2) else palabra2

def __guardarUI(ruta, contenido):
    archivo_ui = open(ruta,'w')
    archivo_ui.write(contenido)
    archivo_ui.close()
    return True

def __obtenerEventoCerrarVentana(nombre_boton, tipo_ventana) :
    resultado = xml_widgets.evento_cerrar_ventana.replace('#nombre_boton#',nombre_boton)
    resultado = resultado.replace('#tipo_ventana#',tipo_ventana)
    return resultado
    
def __obtenerTextoBotones(botones) : 
    """
    Segun el tipo indicado, devuleve el texto que se seteara en los botones.
    """
    boton1, boton2 = '',''
    if 'bt_salir_aceptar' in botones.keys():
        boton1, boton2 = 'Salir','Aceptar'
    elif 'bt_salir_guardar' in botones.keys():
        boton1, boton2 = 'Salir','Guardar'
    elif 'bt_cancelar_aceptar' in botones.keys():
        boton1, boton2 = 'Cancelar','Aceptar'
    elif 'bt_limpiar' in botones.keys():
        boton1, boton2 = 'Limpiar',''
            
    return boton1, boton2
    
def __generarBotones(codigo, botones = {}):
    """
    Devuelve el codigo xml correspondiente al tipo de botones indicado.
    """
    botonA, botonB = '',''
    if botones : 
        # obtiene que botones se van a generar
        botonA, botonB = __obtenerTextoBotones(botones)
        resultado = xml_widgets.par_botones.replace('###',botonA)
        resultado = resultado.replace('%%%',botonB)
        return resultado
    else:
        return codigo
    pass
    

def __getXmlWidget(campos):
    """
    Segun el tipo de widget, devuelve el XML correspondiente que representa
    ese widget en una gui Qt. 
    """
    # si este campo posee referencia, agrega el boton junto al lineedit
    xml_widget = ''
    if (campos['widget_type'] == 'QLineEdit') and (campos['reference'] == True):
        xml_widget = xml_widgets.source_widgets['QLineEditWithReference']
    else:
        xml_widget = xml_widgets.source_widgets[campos['widget_type']]
    return xml_widget

def __generarWidgets(dic_campos, botones = {}):
    """
    Genera el codigo xml correspondiente a los campos indicados.
    """
    
    # el diccionario que se recibe, cada elemento tiene este formato
    # {'atribute':'apellido','widget_type':'QLineEdit','reference':False},
    
    codigo_widgets = ''
    tamano_layout = 20 # se incrementa de a 40 pixeles
        
    # con esto se obtiene la longitud del label para que quede todo ordenadito :)
    longitud_labels = __obtenerLongitudLabels(dic_campos)    
    cant_campos = len(dic_campos)
    for nro_campo in range(cant_campos) :
        campos = dic_campos[nro_campo] 
        nombre_campo = __normalizarNombreCampo( campos['atribute'] )
        nombre_widget = __normalizarNombreWidget( campos['atribute'] )
        prefijo_widget = prefijos_widgets.prefijos[ campos['widget_type'] ]
        # primero, obtiene el xml correspondiente al tipo de widget actual, 
        # y lo mezcla con el del label
        # luego, reemplaza los %--% por el nombre actual del campo
        
        xml_widget = __getXmlWidget(campos)
        widget_actual = (xml_widgets.par_label_layout % (longitud_labels, xml_widget))            
        # si este widget, posee nombre de campo, lo reemplaza
        if widget_actual.find(u'#nombre_campo#') != -1 :
            widget_actual = widget_actual.replace(u'#nombre_campo#',nombre_campo)
        # reemplaza el prefijo del widget
        widget_actual = widget_actual.replace(u'#prefijo#',prefijo_widget)
        
        widget_actual = widget_actual.replace(u'#nombre_widget#',nombre_widget)
        tamano_layout += 40 # incrementa para  ubicar el proximo widget
        codigo_widgets +=  widget_actual + '\n'

    # genera el codigo correspondiente a los botones en caso de que 
    # se reciba algun valor como parametro
    if botones :
        codigo_widgets += __generarBotones(codigo_widgets, botones)
    
    return codigo_widgets

def __generarPlantilla(destino, tipo, metodos = None):
    """
    """
    nombre_archivo = os.path.basename(destino).split('.')[0] + '.py'
    ruta_destino = pathtools.convertPath(os.path.dirname(destino)+'/'+nombre_archivo)
    shutil.copyfile(
            pathtools.convertPath( pathtools.getPathProgramFolder()+'/plantillas/plantilla.py' ),
            ruta_destino)
    
    archivo = open(ruta_destino,'r')
    contenido = archivo.read()
    archivo.close()
    
    # reemplaza en el texto los campos de la plantilla
    contenido = contenido.replace('%%%',tipo)
    contenido = contenido.replace('&&&',os.path.basename(destino).split('.')[0])
    archivo = open(ruta_destino,'w')
    archivo.write(contenido)
    archivo.close()
    return True
    
def __obtenerLongitudLabels(campos) :
    """
    Devuelve la longitud que deberan tener los labels para que "quede
    ordenado" en la interfaz.
    """
    palabras = map(lambda elemento : elemento.keys()[0] ,campos.values())
    return len(reduce(__palabra_mas_larga,  palabras )) * 8
    
def __obtenerAltoVentana(campos):
    return int((len(campos.keys()) * 40) * 1.5)
    
def __normalizarNombreCampo(nombre):
    """
    Verifica que el nombre no contenga espacios.
    """
    while nombre.find('  ') != -1 :
        nombre.replace('  ',' ')
    nombre = nombre.capitalize()
    return nombre
    
def __normalizarNombreWidget(nombre):
    """
    Verifica que el nombre no contenga espacios.
    """
    while nombre.find('  ') != -1 :
        nombre.replace('  ',' ')
    nombre = nombre.replace(' ','_')
    nombre = nombre.capitalize()    
    return nombre

def generarUI(  destino, 
                campos,                  
                botones = {}, 
                opciones = {}
            ):
    """ 
    Genera un archivo .ui con los datos que recibe del diccionario campos.     
    campos = {'nombre_campo':tipo_widget}
    
    destino = ruta donde se genera el ui
    campos = diccionario que contiene la informacion de los campos para generar la gui
    botones = tipo de boton que se agregara a la ventana
    opciones = diccionario con opciones extra que se involucren en la generacion del ui
    """
    ### Atributos    
    ancho_ventana = 400 
    alto_ventana = __obtenerAltoVentana(campos)  
    widgets = __generarWidgets(campos, botones)    
    resultado = ''    
    tipo_ventana = opciones['tipo']
    opciones_generacion = opciones.keys()
   
    # reemplaza el ancho
    resultado = xml_widgets.todo.replace('%ancho%',str(ancho_ventana))
    # reemplaza el alto
    resultado = resultado.replace('%alto%',str(alto_ventana))
    # reemplaza los widgets
    resultado = resultado.replace('%widgets%',widgets)
    
    # reemplaza la señal del boton que cierra la ventana
    btn1, btn2 = __obtenerTextoBotones(botones)
    codigo_evento = __obtenerEventoCerrarVentana(btn1,tipo_ventana)
    resultado = resultado.replace('<connections/>',codigo_evento)
    
    # establece el tipo de ventana
    if 'tipo' in opciones_generacion :
        resultado = resultado.replace('###',tipo_ventana)
        
    # guarda el resultado del parseo en el archivo .ui
    __guardarUI(destino,resultado)
    
    # genera la plantilla para levantar el ui
    if ('generar_plantilla' in opciones) and (opciones['generar_plantilla'] == True) :
        __generarPlantilla(destino,opciones['tipo'])

    print '>>> Archivo .ui generado.'
    return True

################################ Extras ################################

#def prueba(campos):
#    return __generarPlantilla('/media/Data/ProyectosOn/GUIMaker/src/api/mike.ui','MainWindow')
    
#campos_ejemplo = {
#'apellido':'QLineEdit',
#'nombre':'QLineEdit',
#'dni':'QLineEdit',
#'direccion':'QLineEdit'
#}

campos_ejemplo = {
0:{'atribute':'nombres','widget_type':'QLineEdit','reference':False},
1:{'atribute':'telefono','widget_type':'QLineEdit','reference':False},
2:{'atribute':'domicilio','widget_type':'QLineEdit','reference':False},
3:{'atribute':'zona','widget_type':'QLineEdit','reference':False},
4:{'atribute':'CP','widget_type':'QLineEdit','reference':False},
5:{'atribute':'localidad','widget_type':'QLineEdit','reference':False},
6:{'atribute':'fecha cumpleaños','widget_type':'QLineEdit','reference':False},
7:{'atribute':'correo electronico','widget_type':'QLineEdit','reference':False}

}

opciones_ejemplo = {
'tipo':'MainWindow'
}

botones_ejemplo = {
'bt_salir_guardar':True
}

#generarUI('/home/mike/agregarCliente.ui',
#campos_ejemplo,
#opciones = opciones_ejemplo,
#botones = botones_ejemplo)

#~ print prueba(pru)
