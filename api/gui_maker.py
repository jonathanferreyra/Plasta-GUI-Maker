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

#~ Orden de los valores que se reemplazaran en la plantilla: <todo>
#~ 1- Nombre clase o tipo de Ventana [MainWindow, Dialog]
#~ 2- Ancho y Alto
#~ 3- Widgets

todo = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>###</class>
 <widget class="Q###" name="###">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>%ancho%</width>
    <height>%alto%</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>###</string>
  </property>
  
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
   %widgets%
   </layout>
  </widget>
  
 </widget>
 <resources/>
 <connections/>
</ui>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <par_label_layout>
#~ 1- Nombre del layout
#~ 2- Nombre del label
#~ 3- Ancho del label
#~ 4- Etiqueta del label
#~ 5- Widget

par_label_layout = '''<item>
     <layout class="QHBoxLayout" name="hl###"><!-- Cambio -->
      <item>
       <widget class="QLabel" name="lb###"><!-- Cambio -->
        <property name="minimumSize">
         <size>
          <width>%d</width><!-- aca va el nombre mas grande x 8 -->
          <height>0</height>
         </size>
        </property>
        <property name="text">
            <string>###</string><!-- Cambio -->
        </property>
        <property name="alignment">
            <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
        </property>
       </widget>
      </item>
      %s
     </layout>
    </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <par_botones>
#~ 1- Nombre del boton1
#~ 2- Nombre del boton2

par_botones = '''<item>
     <layout class="QHBoxLayout" name="horizontalLayout">
      <item>
       <spacer name="horizontalSpacer">
        <property name="orientation">
         <enum>Qt::Horizontal</enum>
        </property>
        <property name="sizeHint" stdset="0">
         <size>
          <width>40</width>
          <height>20</height>
         </size>
        </property>
       </spacer>
      </item>
      <item>
       <widget class="QPushButton" name="bt###">
        <property name="text">
         <string>###</string>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QPushButton" name="bt%%%">
        <property name="text">
         <string>%%%</string>
        </property>
       </widget>
      </item>
     </layout>
    </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <par_botones>
#~ 1- Nombre del boton al que le asigna el evento
#~ 2- Tipo de ventana

evento_cerrar_ventana = '''<connections>
  <connection>
   <sender>bt###</sender>
   <signal>clicked()</signal>
   <receiver>%%%</receiver>
   <slot>close()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>273</x>
     <y>201</y>
    </hint>
    <hint type="destinationlabel">
     <x>123</x>
     <y>186</y>
    </hint>
   </hints>
  </connection>
 </connections>'''
     
#~ Orden de los valores que se reemplazaran en la plantilla: <lineedit>
#~ 1- Nombre del entry

lineedit = '''<item>
       <widget class="QLineEdit" name="e###"><!-- Cambio -->
        <property name="sizePolicy">
         <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
          <horstretch>0</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
       </widget>
      </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <combobox>
#~ 1- Nombre del combo

combobox = '''<item>
       <widget class="QComboBox" name="cb###"><!-- Cambio -->
        <property name="sizePolicy">
         <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
          <horstretch>0</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
       </widget>
      </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <lineedit>
#~ 1- Nombre del radiobutton
#~ 2- Etiqueta del radiobutton

radiobutton = '''<item>
       <widget class="QRadioButton" name="rb###">
        <property name="text">
         <string>###</string>
        </property>
        <property name="sizePolicy">
         <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
          <horstretch>0</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
       </widget>
      </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <checkbox>
#~ 1- Nombre del checkbox
#~ 2- Etiqueta del checkbox

checkbox = '''<item>
       <widget class="QCheckBox" name="chk###">
        <property name="text">
         <string>###</string>
        </property>
        <property name="sizePolicy">
         <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
          <horstretch>0</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
       </widget>
      </item>'''

# diccionario que contiene el fuente de los distintos widgets
source_widgets = {
'QCheckBox':checkbox,
'QRadioButton':radiobutton,
'QComboBox':combobox,
'QLineEdit':lineedit,
}

############################## Funciones ###############################

def __palabra_mas_larga(palabra1, palabra2):
    return palabra1 if len(palabra1) > len(palabra2) else palabra2

def __guardarUI(ruta, contenido):
    archivo_ui = open(ruta,'w')
    archivo_ui.write(contenido)
    archivo_ui.close()
    return True

def __obtenerEventoCerrarVentana(nombre_boton, tipo_ventana) :
    resultado = evento_cerrar_ventana.replace('###',nombre_boton)
    resultado = resultado.replace('%%%',tipo_ventana)
    return resultado
    
def __obtenerTextoBotones(botones) : 
    """
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
        resultado = par_botones.replace('###',botonA)
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
        campo = self.__normalizarNombreCampo( campos.keys()[0] )
        # primero, obtiene el xml correspondiente al tipo de widget actual, 
        # y lo mezcla con el del label
        # luego, reemplaza los ### por el nombre actual del campo
        xml_widget = source_widgets[campos[campo]]
        widget_actual = (par_label_layout % (longitud_labels, xml_widget)).replace('###',campo.capitalize())
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
            pathtools.convertPath( pathtools.getPathProgramFolder()+'api/plantilla.py' ),
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
    
def __normalizarNombreCampo(self, nombre):
    """
    Verifica que el nombre no contenga espacios.
    """
    while nombre.find('  ') != -1 :
        nombre.replace('  ',' ')
    nombre = nombre.replace(' ','_')
    return nombre
    
def generarUI(  destino, 
                campos,                  
                botones = {}, 
                opciones = {}
            ):
    """ 
    Genera un archivo .ui con los datos que recibe del diccionario campos.     
    campos = {'nombre_campo':tipo_widget}
    """
    ### Atributos    
    ancho_ventana = 400 
    alto_ventana = __obtenerAltoVentana(campos)  
    widgets = __generarWidgets(campos, botones)    
    resultado = ''    
    tipo_ventana = opciones['tipo']
    opciones_generacion = opciones.keys()
   
    # reemplaza el ancho
    resultado = todo.replace('%ancho%',str(ancho_ventana))
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
    if opciones['generar_plantilla'] == True :
        __generarPlantilla(destino,opciones['tipo'])

    print '>>> Archivo .ui generado.'
    return True

################################ Extras ################################

def prueba(campos):
    return __generarPlantilla('/media/Data/ProyectosOn/GUIMaker/src/api/mike.ui','MainWindow')
    
campos_ejemplo = {
'apellido':'QLineEdit',
'nombre':'QLineEdit',
'dni':'QLineEdit',
'direccion':'QLineEdit'
}

opciones_ejemplo = {
'tipo':'MainWindow'
}

botones_ejemplo = {
'bt_salir_guardar':True
}

#~ generarUI('/home/emiliano/git/guimaker/src/prueba001.ui',
    #~ campos_ejemplo,
    #~ plantilla = True,
    #~ opciones = opciones_ejemplo,
    #~ botones = botones_ejemplo)

#~ print prueba(pru)
