#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
from PyQt4 import QtCore, QtGui, uic


class %nombre_clase%(QtGui.%tipo_ventana%):

    def __init__(self, parent = None):
        FILENAME = '%nombre_ui%.ui'
        QtGui.%tipo_ventana%.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()

        self.parent = parent

    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

%metodos_auxiliares%
%metodos_senales%

def main():
    app = QtGui.QApplication(sys.argv)
    window = %nombre_clase%()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
