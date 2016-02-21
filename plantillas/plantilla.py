#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
from PyQt4 import QtCore, QtGui, uic


class Main(QtGui.Q%%%):

    def __init__(self):
        FILENAME = '&&&.ui'
        QtGui.Q%%%.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)), FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()

########################
# FUNCIONES AUXILIARES #
########################

    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __toUnicode(self, MyQString):
        return unicode(MyQString.toUtf8(),'utf-8')

    def XXX(self):
        """ """
        pass

############################
# FUNCIONES DE LOS EVENTOS #
############################

    @QtCore.pyqtSlot()
    def on_btXXX_clicked(self):
        pass

def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
