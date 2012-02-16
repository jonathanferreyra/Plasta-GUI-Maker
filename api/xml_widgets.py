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

#~ Orden de los valores que se reemplazaran en la plantilla: <todo>
#~ 1- Nombre clase o tipo de Ventana [MainWindow, Dialog]
#~ 2- Ancho y Alto
#~ 3- Widgets

todo = u'''<?xml version="1.0" encoding="UTF-8"?>
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

par_label_layout = u'''<item>
     <layout class="QHBoxLayout" name="hl###"><!-- Cambio -->
      <item>
       <widget class="QLabel" name="lb#nombre_widget#"><!-- Cambio -->
        <property name="minimumSize">
         <size>
          <width>%d</width><!-- aca va el nombre mas grande x 8 -->
          <height>0</height>
         </size>
        </property>
        <property name="text">
            <string>#nombre_campo#</string><!-- Cambio -->
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

par_botones = u'''<item>
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

evento_cerrar_ventana = u'''<connections>
  <connection>
   <sender>bt#nombre_boton#</sender>
   <signal>clicked()</signal>
   <receiver>#tipo_ventana#</receiver>
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

lineedit = u'''<item>
       <widget class="QLineEdit" name="le#nombre_widget#">
        <property name="sizePolicy">
         <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
          <horstretch>0</horstretch>
          <verstretch>0</verstretch>
         </sizepolicy>
        </property>
       </widget>
      </item>'''
      
lineedit_with_btref = u'''<item><layout class="QHBoxLayout" name="hl_#nombre_widget#">
       <property name="spacing">
        <number>0</number>
       </property>
       <item>
        <widget class="QLineEdit" name="le#nombre_widget#">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="text">
          <string/>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="bt#nombre_widget#">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Preferred">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="maximumSize">
          <size>
           <width>30</width>
           <height>26</height>
          </size>
         </property>
         <property name="cursor">
          <cursorShape>PointingHandCursor</cursorShape>
         </property>
         <property name="text">
          <string/>
         </property>
         <property name="icon">
          <iconset>
           <normaloff>%imagen_boton%</normaloff>%imagen_boton%</iconset>
         </property>
         <property name="iconSize">
          <size>
           <width>20</width>
           <height>20</height>
          </size>
         </property>
        </widget>
       </item>
      </layout>
      </item>'''

#~ Orden de los valores que se reemplazaran en la plantilla: <combobox>
#~ 1- Nombre del combo

combobox = u'''<item>
       <widget class="QComboBox" name="cb#nombre_widget#"><!-- Cambio -->
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

radiobutton = u'''<item>
       <widget class="QRadioButton" name="rb#nombre_widget#">
        <property name="text">
         <string>#nombre_campo#</string>
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

checkbox = u'''<item>
       <widget class="QCheckBox" name="chk#nombre_widget#">
        <property name="text">
         <string>#nombre_campo#</string>
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
'QLineEditWithReference':lineedit_with_btref
}

#TODO : agregar soporte para QDateEdit 
#TODO : agregar soporte para QSpinBox
