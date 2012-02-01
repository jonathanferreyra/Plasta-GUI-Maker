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

import os,sys
from PyQt4 import QtCore, QtGui, uic


class Main(QtGui.Q%%%):
    """La ventana principal de la aplicación."""
    
    def __init__(self):
        FILENAME = '&&&.ui'
        QtGui.Q%%%.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()

##########################
# METODOS DE LOS EVENTOS #
##########################

    @QtCore.pyqtSlot()
    def on_btXXX_clicked(self):
        pass
        
    @QtCore.pyqtSlot(int)
    def on_cbXXX_currentIndexChanged(self):
        pass
    
######################
# METODOS AUXILIARES #
######################

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
    
def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
