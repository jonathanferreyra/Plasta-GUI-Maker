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

#~ Orden de los valores que se reemplazaran en la plantilla: <todo>
#~ 1- Nombre clase o tipo de Ventana [MainWindow, Dialog]
#~ 2- Ancho y Alto
#~ 3- Widgets

def __palabra_mas_larga(palabra1, palabra2):
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
    """
    values = {'bt_salir_aceptar':False,'bt_salir_guardar':False,
        'bt_cancelar_aceptar':False,'bt_limpiar':False}
    for k, v in botones.iteritems():
        values[k] = v
    boton1, boton2 = '',''
    if values['bt_salir_aceptar']:
        boton1, boton2 = 'Salir','Aceptar'
    elif values['bt_salir_guardar']:
        boton1, boton2 = 'Salir','Guardar'
    elif values['bt_cancelar_aceptar']:
        boton1, boton2 = 'Cancelar','Aceptar'
    elif values['bt_limpiar']:
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

def __generarWidgets(dic_campos, botones = {}):
    """
    Genera el codigo xml correspondiente a los campos indicados.
    """
    codigo_widgets = ''
    tamano_layout = 20 # se incrementa de a 40 pixeles

    # con esto se obtiene la longitud del label para que quede todo ordenadito
    longitud_labels = __obtenerLongitudLabels(dic_campos)
    cant_campos = len(dic_campos)
    for nro_campo in range(cant_campos) :
        campos = dic_campos[nro_campo]
        campo = campos.keys()[0]
        widget = campos.values()[0]
        # primero, obtiene el xml correspondiente al tipo de widget actual,
        # y lo mezcla con el del label
        # luego, reemplaza los ### por el nombre actual del campo
        xml_widget = xml_widgets.source_widgets[campos[campo]]
        widget_actual = (xml_widgets.par_label_layout % (longitud_labels, xml_widget)).replace('#nombre_widget#',campo.capitalize())
        prefijo_widget = prefijos_widgets.prefijos[ widget ]
        widget_actual = widget_actual.replace(u'#prefijo#',prefijo_widget)
        widget_actual = widget_actual.replace(u'#nombre_campo#',campo)
        tamano_layout += 40 # incrementa para  ubicar el proximo widget
        codigo_widgets +=  widget_actual + '\n'

    # genera el codigo correspondiente a los botones en caso de que
    # se reciba algun valor como parametro
    if botones :
        codigo_widgets += __generarBotones(codigo_widgets, botones)

    return codigo_widgets

def __generarPlantilla(destino, tipo, metodos = None):
    """
    {str} tipo = Dialog | MainWindow
    """
    nombre_archivo = os.path.basename(destino).split('.')[0] + '.py'
    ruta_destino = pathtools.convertPath(os.path.dirname(destino)+'/'+nombre_archivo)
    shutil.copyfile(
            pathtools.convertPath( pathtools.getPathProgramFolder()+'plantillas/plantilla.py' ),
            ruta_destino)

    archivo = open(ruta_destino,'r')
    contenido = archivo.read()
    archivo.close()

    # reemplaza en el texto los campos de la plantilla
    contenido = contenido.replace(u'%%%',tipo)
    contenido = contenido.replace(u'&&&',os.path.basename(destino).split('.')[0])
    archivo = open(ruta_destino,'w')
    archivo.write(contenido)
    archivo.close()
    print '>>> Plantilla .py generada'
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

def generarUI(  destino,
                campos,
                botones = {},
                opciones = {}
            ):
    """
    Genera un archivo .ui con los datos que recibe del diccionario campos.
    Params:
    {str}  destino = ubicacion de destino
    {dict} campos = {0: {u'field1': u'QLineEdit'}, 1: {u'field2': u'QLineEdit'}, ...}
    {dict} botones = {'bt_limpiar': False, 'bt_cancelar_aceptar': False, 'bt_salir_guardar': True, 'bt_salir_aceptar': False}
    {dict} opciones = {'tipo': 'Dialog', 'generar_plantilla': False}
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
        # si la ventana es del tipo QMainWindow agrega la siguiente linea
        if tipo_ventana == 'MainWindow':
            layout = '<layout class="QVBoxLayout" name="verticalLayout_2">'
            resultado = resultado.replace(
                layout,
                '<widget class="QWidget" name="centralwidget">\n   ' + layout
            )
            resultado = resultado.replace(
                ' </widget>\n <resources/>',
                '  </widget> </widget>\n <resources/>'
            )
    # guarda el resultado del parseo en el archivo .ui
    __guardarUI(destino, resultado)

    # genera la plantilla para levantar el ui
    if opciones['generar_plantilla'] == True :
        __generarPlantilla(destino,opciones['tipo'])

    print '>>> Archivo .ui generado'
    return True
