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

from maker import pathtools

#############################################################################################

_thisFolder = pathtools.getPathProgramFolder() + pathtools.convertPath('plantillas/object')[1:]

_meta = {
  'widgets':{
    'lineEdit':'le',
    'comboBox':'cb',
    'spinBox':'sb',
    'doubleSpinBox':'dsb',
    'textEdit':'te',
    'dateEdit':'dt',
    'dateTimeEdit':'dte',
    'timeEdit':'tme',
    'checkBox':'chk',
  }
}

def generatePackage(objInfo):

  _generateFiles(objInfo)
  _generateContentFiles(objInfo)

def _generateContentFiles(objInfo):
  contentFiles = _readContentFiles()
  ############################################################
  ## Generate 'storm' file
  ############################################################
  if objInfo['classesToGenerate']['storm']:
    print 'generating file storm...'
    # generate attrs
    attrs = ''
    if objInfo['addIdeAttr']:
      attrs += 'ide = Int(primary = True)\n'
    for attr in objInfo['attributes']:
      attrs += '    %s = %s()\n' % (attr['name'], attr['type'])

    # generate init method
    initMethod = 'def __init__(self, {params}):\n{attrs}'
    classAttrs = [attr['name'] for attr in objInfo['attributes']]
    initMethod = initMethod.replace('{params}', ', '.join(classAttrs))
    # generate init attrs
    initAttrs = ''
    for attr in classAttrs:
      initAttrs += ' ' * 8 + 'self.' + attr + ' = ' + attr + '\n'
    initMethod = initMethod.replace('{attrs}', initAttrs)
    # generate content the file
    content = contentFiles['storm']
    content = content.replace('%Object_name%', objInfo['className'])
    content = content.replace('%object_name%', objInfo['className'].lower())
    content = content.replace('{attributes}', attrs)
    content = content.replace('{init_method}', initMethod)
    _writeContentFile(objInfo, 'storm', content)

  ############################################################
  ## Generate 'add' file
  ############################################################
  if objInfo['classesToGenerate']['add']:
    # generate attrs
    attrs = ''
    for attr, widget in objInfo['widgetToAttr'].iteritems():
      widgetName = _meta['widgets'][widget] + attr.lower().capitalize()
      attrs += ' ' * 10 + '{self.%s:%s.%s},\n' % (widgetName, objInfo['className'], attr)
    # generate content the file
    content = contentFiles['add']
    content = content.replace('%Object_name%', objInfo['className'])
    content = content.replace('%object_name%', objInfo['className'].lower())
    content = content.replace('{attributes}', attrs)
    _writeContentFile(objInfo, 'add', content)

  ############################################################
  ## Generate 'gui' file
  ############################################################
  if objInfo['classesToGenerate']['gui']:
    # generate attrs
    attrs = ''
    for attr, widget in objInfo['widgetToAttr'].iteritems():
      attrs += ' ' * 10 + "#{u'%s':%s.%s},\n" % (attr.lower().capitalize(), objInfo['className'], attr)
    # generate content the file
    content = contentFiles['gui']
    content = content.replace('%Object_name%', objInfo['className'])
    content = content.replace('%object_name%', objInfo['className'].lower())
    content = content.replace('{attributes}', attrs)
    _writeContentFile(objInfo, 'gui', content)

  ############################################################
  ## Generate 'manager' file
  ############################################################
  if objInfo['classesToGenerate']['manager']:
    # generate content the file
    content = contentFiles['manager']
    content = content.replace('%Object_name%', objInfo['className'])
    content = content.replace('%object_name%', objInfo['className'].lower())
    _writeContentFile(objInfo, 'manager', content)

def _generateFiles(data):
  nameFolder = pathtools.convertPath(
    '/' + data['className'].replace(" ", "").lower())
  outputFolder = data['outputFolder'] + nameFolder
  data['outputNameFolder'] = outputFolder
  import shutil
  shutil.copytree(_thisFolder, outputFolder)
  print 'generate files...ok'

def _readContentFiles():
  return {
    'storm':open(_thisFolder + '/__init__.py', 'r').read(),
    'add':open(_thisFolder + '/add.py', 'r').read(),
    'gui':open(_thisFolder + '/gui.py', 'r').read(),
    'manager':open(_thisFolder + '/manager.py', 'r').read()
  }

def _writeContentFile(objInfo, fileType, content):
  nameFile = {
    'storm':'__init__.py',
    'add':'add.py',
    'gui':'gui.py',
    'manager':'manager.py',
  }[fileType]
  f = open(objInfo['outputNameFolder'] + '/' + nameFile, 'w')
  f.write(content)
  f.close()
  print 'writed file <', fileType, '>...ok'

def main():
    pass

if __name__ == "__main__":
  # attrs = Unicode, Int, Date, Float, Time
  data = {
  'className':'Myclass',
  'addIdeAttr':True,
  'attributes':[
      {'name':'attr1','type':'Unicode'},
      {'name':'attr2','type':'Unicode'},
      {'name':'attr3','type':'Int'},
    ],
  'widgetToAttr':{
    'attr1':'lineEdit',
    'attr2':'comboBox',
    'attr3':'spinBox',
  },
  'classesToGenerate':{
    'storm':True,'manager':True,'gui':True,'add':True
  },
  'outputFolder':''
  }

  print data
  #main()