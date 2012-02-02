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

QObject = {
'inherits':None,
'signals':{
    'destroyed ()':'|',
    'destroyed (QObject*)':'|object'
    }
}

QWidget = {
'inherits':'QObject',
'signals':{
    'customContextMenuRequested (const QPoint&)':'point'
    }
}

QLineEdit = {
'inherits':'QWidget',
'signals':{
    'cursorPositionChanged (int,int)':'x, y',
    'editingFinished ()':'',
    'returnPressed ()':'',
    'selectionChanged ()':'',
    'textChanged (const QString&)':'text',
    'textEdited (const QString&)':'text'
    }
}

QAction = {
'inherits':'QObject',
'signals':{
    'changed ()':'',
    'hovered ()':'',
    'toggled (bool)':'value',
    'triggered (bool = 0)':'value'
    }
}

QCheckBox = {
'inherits':'QAbstractButton',
'signals':{
    'stateChanged (int)':'index'
    }
}

QAbstractButton = {
'inherits':'QWidget',
'signals':{
    'clicked ()':'|',
    'clicked (bool)':'|value',
    'pressed ()':'',
    'released ()':'',
    'toggled (bool)':'value'
    }
}

QComboBox = {
'inherits':'QWidget',
'signals':{
    'activated (int)':'int|value',
    'activated (const QString&)':'QtCore.QString|value',
    'currentIndexChanged (int)':'int|index',
    'currentIndexChanged (const QString&)':'QtCore.QString|index',
    'editTextChanged (const QString&)':'text',
    'highlighted (int)':'int|value',
    'highlighted (const QString&)':'QtCore.QString|value',
    }
}

QDialog = {
'inherits':'QWidget',
'signals':{
    'accepted ()':'',
    'finished (int)':'int|value',
    'rejected ()':''
    }
}

QPlainTextEdit = {
'inherits':None,
'signals':{
    'blockCountChanged (int)':'value',
    'copyAvailable (bool)':'value',
    'cursorPositionChanged ()':'',
    'modificationChanged (bool)':'value',
    'redoAvailable (bool)':'value',
    'selectionChanged ()':'',
    'textChanged ()':'',
    'undoAvailable (bool)':'value',
    'updateRequest (const QRect&,int)':'rect, value'
    }
}

QGroupBox = {
'inherits':'QWidget',
'signals':{
    'clicked (bool = 0)':'value',
    'toggled (bool)':'value'
    }
}

QLabel = {
'inherits':None,
'signals':{
    'linkActivated (const QString&)':'text',
    'linkHovered (const QString&)':'text',
    }
}

QListView = {
'inherits':'QAbstractItemView',
'signals':{
    'indexesMoved (const QModelIndexList&)':'index'
    }
}

QAbstractItemView = {
#'inherits':'QAbstractScrollArea',
'inherits':None,
'signals':{
    'activated (const QModelIndex&)':'index',
    'clicked (const QModelIndex&)':'index',
    'doubleClicked (const QModelIndex&)':'index',
    'entered (const QModelIndex&)':'index',
    'pressed (const QModelIndex&)':'index',
    'viewportEntered ()':''
    }
}

QListWidget = {
'inherits':'QListView',
'signals':{
    'currentItemChanged (QListWidgetItem *,QListWidgetItem *)':'item_a, item_b',
    'currentRowChanged (int)':'index',
    'currentTextChanged (const QString&)':'text',
    'itemActivated (QListWidgetItem *)':'item',
    'itemChanged (QListWidgetItem *)':'item',
    'itemClicked (QListWidgetItem *)':'item',
    'itemDoubleClicked (QListWidgetItem *)':'item',
    'itemEntered (QListWidgetItem *)':'item',
    'itemPressed (QListWidgetItem *)':'item',
    'itemSelectionChanged ()':''
    }
}

QMainWindow = {
'inherits':'QWidget',
'signals':{
    'iconSizeChanged (const QSize&)':'size',
    'toolButtonStyleChanged (Qt::ToolButtonStyle)':'style'
    }
}

QMenu = {
'inherits':'QWidget',
'signals':{
    'aboutToHide ()':'',
    'aboutToShow ()':'',
    'hovered (QAction *)':'action',
    'triggered (QAction *)':'action'
    }
}

QMenuBar = {
'inherits':'QWidget',
'signals':{
    'hovered (QAction *)':'action',
    'triggered (QAction *)':'action'
    }
}

QProgressBar = {
'inherits':'QWidget',
'signals':{
    'valueChanged (int)':'value'
    }
}

QPushButton = {
'inherits':'QAbstractButton',
'signals':{

    }
}

QCalendarWidget = {
'inherits':'QWidget',
'signals':{
    'activated (const QDate&)':'date',
    'clicked (const QDate&)':'date',
    'currentPageChanged (int,int)':'x, y',
    'selectionChanged ()':''
    }
}

QRadioButton = {
'inherits':'QAbstractButton',
'signals':{
    }
}

QSpinBox = {
'inherits':'QAbstractSpinBox',
'signals':{
    'valueChanged (int)':'int|value',
    'valueChanged (const QString&)':'QtCore.QString|value'
    }
}

QAbstractSpinBox = {
'inherits':'QWidget',
'signals':{
    'editingFinished ()':''
    }
}

QStatusBar = {
'inherits':'QWidget',
'signals':{
    'messageChanged (const QString&)':'message'
    }
}

QTableView = {
'inherits':'QAbstractItemView',
'signals':{

    }
}

QTableWidget = {
'inherits':'QTableView',
'signals':{
    'cellActivated (int,int)':'x, y',
    'cellChanged (int,int)':'x, y',
    'cellClicked (int,int)':'x, y',
    'cellDoubleClicked (int,int)':'x, y',
    'cellEntered (int,int)':'x, y',
    'cellPressed (int,int)':'x, y',
    'currentCellChanged (int,int,int,int)':'a,b,c,d',
    'currentItemChanged (QTableWidgetItem *,QTableWidgetItem *)':'item_a, item_b',
    'itemActivated (QTableWidgetItem *)':'item',
    'itemChanged (QTableWidgetItem *)':'item',
    'itemClicked (QTableWidgetItem *)':'item',
    'itemDoubleClicked (QTableWidgetItem *)':'item',
    'itemEntered (QTableWidgetItem *)':'item',
    'itemPressed (QTableWidgetItem *)':'item',
    'itemSelectionChanged ()':''
    }
}

QTabWidget = {
'inherits':'QWidget',
'signals':{
    'currentChanged (int)':'index',
    'tabCloseRequested (int)':'index'
    }
}

QTextEdit = {
'inherits':None,
'signals':{
    'copyAvailable (bool)':'value',
    'currentCharFormatChanged (const QTextCharFormat&)':'text',
    'cursorPositionChanged ()':'',
    'redoAvailable (bool)':'value',
    'selectionChanged ()':'',
    'textChanged ()':'',
    'undoAvailable (bool)':'value'
    }
}

QTreeView = {
'inherits':'QAbstractItemView',
'signals':{
    'collapsed (const QModelIndex&)':'index',
    'expanded (const QModelIndex&)':'index'
    }
}

QTreeWidget = {
'inherits':'QTreeView',
'signals':{
    'currentItemChanged (QTreeWidgetItem *,QTreeWidgetItem *)':'itema, itemb',
    'itemActivated (QTreeWidgetItem *,int)':'item, value',
    'itemChanged (QTreeWidgetItem *,int)':'item, value',
    'itemClicked (QTreeWidgetItem *,int)':'item, value',
    'itemCollapsed (QTreeWidgetItem *)':'item',
    'itemDoubleClicked (QTreeWidgetItem *,int)':'item, value',
    'itemEntered (QTreeWidgetItem *,int)':'item, value',
    'itemExpanded (QTreeWidgetItem *)':'item',
    'itemPressed (QTreeWidgetItem *,int)':'item, value',
    'itemSelectionChanged ()':''
    }
}

QDateTimeEdit = {
'inherits':'QAbstractSpinBox',
'signals':{
    "dateChanged (const QDate&)":"date",
    "dateTimeChanged (const QDateTime&)":"datetime",
    "timeChanged (const QTime&)":"time",
    }
}

QDateEdit = {
'inherits':'QDateTimeEdit',
'signals':{
    }
}

QWizard = {
'inherits':'QDialog',
'signals':{
    "currentIdChanged (int)":"index",
    "customButtonClicked (int)":"index",
    "helpRequested ()":"",
    "pageAdded (int)":"index",
    "pageRemoved (int)":"index"
    }
}

QToolButton = {
'inherits':'QAbstractButton',
'signals':{
    'triggered (QAction *)':'action'
    }
}

QCommandLinkButton = {
'inherits':'QPushButton',
'signals':{
    }
}

QDialogButtonBox = {
'inherits':'QWidget',
'signals':{
    "accepted ()":"",
    "clicked (QAbstractButton *)":"",
    "helpRequested ()":"",
    "rejected ()":""
    }
}

QColumnView = {
'inherits':'QAbstractItemView',
'signals':{
    'updatePreviewWidget (const QModelIndex&)':'index'
    }
}

QScrollArea = {
'inherits':'QAbstractScrollArea',
'signals':{
	}
}

QFrame = {
'inherits':'QWidget',
'signals':{
	}
}

QToolBox= {
'inherits':'QFrame',
'signals':{"currentChanged (int)":"index"
	}
}

QTabWidget = {
'inherits':'QWidget',
'signals':{
			"currentChanged (int)":'index',
			"tabCloseRequested (int)":'index'
	}
}

QMdiArea = {
'inherits':'QAbstractScrollArea',
'signals':{
		"subWindowActivated (QMdiSubWindow *)":""
	}
}

QDockWidget = {
'inherits':'QWidget',
'signals':{
		'allowedAreasChanged (Qt::DockWidgetAreas)':'',
		'dockLocationChanged (Qt::DockWidgetArea)':'',
		'featuresChanged (QDockWidget::DockWidgetFeatures)':'',
		'topLevelChanged (bool)':'value',
		'visibilityChanged (bool)':'value'
	}
}

QFontComboBox = {
'inherits':'QComboBox.',
'signals':{
		'currentFontChanged (const QFont&)':'font'
	}
}

QTextBrowser = {
'inherits':'QTextEdit',
'signals':{
	'anchorClicked (const QUrl&)':'value',
	'backwardAvailable (bool)':'value',
	'forwardAvailable (bool)':'value',
	'highlighted (const QUrl&)':'QUrl|value',
	'highlighted (const QString&)':'QCore.QString|value',
	'historyChanged ()':'',
	'sourceChanged (const QUrl&)':'value'
	}
}

QGraphicsView = {
'inherits':'QAbstractScrollArea.',
'signals':{
	}
}

QWebView = {
'inherits':'QWidget',
'signals':{
	'iconChanged ()':'',
	'linkClicked (const QUrl&)':'index',
	'loadFinished (bool)':'value',
	'loadProgress (int)':'value',
	'loadStarted ()':'',
	'selectionChanged ()':'',
	'statusBarMessage (const QString&)':'value',
	'titleChanged (const QString&)':'text',
	'urlChanged (const QUrl&)':'txturl'
	}
}


QLine = {
'inherits':None,
'signals':{
	}
}


#~ = {
#~ 'inherits':'',
#~ 'signals':{
	#~ }
#~ }



#############################################################################################

Widgets = {
'QAbstractButton':QAbstractButton,
'QAbstractItemView':QAbstractItemView,
'QAbstractSpinBox':QAbstractSpinBox,
'QAction':QAction,
'QCalendarWidget':QCalendarWidget,
'QCheckBox':QCheckBox,
'QColumnView':QColumnView,
'QComboBox':QComboBox,
'QCommandLinkButton':QCommandLinkButton,
'QDateEdit':QDateEdit,
'QDateTimeEdit':QDateTimeEdit,
'QDialog':QDialog,
'QDialogButtonBox':QDialogButtonBox,
'QDockWidget':QDockWidget,
'QFontComboBox':QFontComboBox,
'QFrame':QFrame,
'QGraphicsView':QGraphicsView,
'QGroupBox':QGroupBox,
'QLabel':QLabel,
'QLine':QLine,
'QLineEdit':QLineEdit,
'QListView':QListView,
'QListWidget':QListWidget,
'QMainWindow':QMainWindow,
'QMdiArea':QMdiArea,
'QMenu':QMenu,
'QMenuBar':QMenuBar,
'QObject':QObject,
'QPlainTextEdit':QPlainTextEdit,
'QProgressBar':QProgressBar,
'QPushButton':QPushButton,
'QRadioButton':QRadioButton,
'QScrollArea':QScrollArea,
'QSpinBox':QSpinBox,
'QStatusBar':QStatusBar,
'QTableView':QTableView,
'QTableWidget':QTableWidget,
'QTabWidget':QTabWidget,
'QTabWidget':QTabWidget,
'QTextBrowser':QTextBrowser,
'QTextEdit':QTextEdit,
'QToolBox':QToolBox,
'QToolButton':QToolButton,
'QTreeView':QTreeView,
'QTreeWidget':QTreeWidget,
'QWebView':QWebView,
'QWidget':QWidget,
'Qwizard':QWizard
}

plantilla_metodo = 'def on_nombreWidget_senial(self):\n    pass\n\n'
plantilla_decorador = '@QtCore.pyqtSlot()\n'
