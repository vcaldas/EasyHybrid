# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Fri May 12 15:57:36 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
 

import sys

#from PySide.QtGui import *
#from PySide.QtCore import *

from PySide import QtCore, QtGui

from GUI.untitled      import Ui_MainWindow

from GLarea.easyMolObj import EasyMolSession
from GLarea.GLWidget   import GLWidget







class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setupUi(self)
        
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.open_list_view_menu)
        #self.treeWidget.clicked.connect(self.on_treeView_clicked)
        #QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL("itemClicked(QtreeWidgetItem*)"), self.on_treeView_item_clicked)
        #QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL("clicked(QModelIndex)"),          self.on_clicked_QModelIndex)
        #QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL("itemClicked(QtreeWidgetItem*)"), self.on_treeView_item_clicked)
        QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.itemClicked)
        
        self.actionOpen.triggered.connect(self.showDialog)
        glmenu = [self.actionOpen]
        self.current_row = None     # selected row from the treeview menu


        self.Action_delete = QtGui.QAction('Delete', self)
        self.Action_delete.setStatusTip('Delete Object')
        self.Action_delete.triggered.connect(self.delete_obj)

        self.Action1 = QtGui.QAction('Exit', self)
        self.Action1.setShortcut('Ctrl+Q')
        self.Action1.setStatusTip('Exit application')
        self.Action1.triggered.connect(self.close)













        self.glwidget = GLWidget(self, glmenu = glmenu)
        self.EasyMol  = EasyMolSession(glwidget =  self.glwidget)

        self.setCentralWidget(self.glwidget)
        self.show()
    
    def on_clicked_QModelIndex(self, model):
        """ Function doc """
        print (model)
   
    def on_treeView_item_clicked (self,  item):
        """ Function doc """
        print (item)
        print (item.checkState())
        state = item.checkState()
        
        if state == QtCore.Qt.CheckState.Unchecked:
            item.setCheckState(QtCore.Qt.CheckState.Checked)
        
        if state == QtCore.Qt.CheckState.Checked:
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)

    def itemClicked (self, item, Int):
        #print (item, Int)
        #print (item.text(0),item.text(1))
        
        state = item.checkState(0)
        #print ('state: ',state)
        object_id = int(item.text(1))
        #print (object_id)
        if state == QtCore.Qt.CheckState.Unchecked:
            #setCheckState(int column, Qt::CheckState state)
            item.setCheckState(0, QtCore.Qt.CheckState.Checked)
            self.EasyMol.enable(int(object_id))
            #print (self.EasyMol.Vobjects[object_id].actived)
            
        if state == QtCore.Qt.CheckState.Checked:
            item.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
            self.EasyMol.disable(int(object_id))
            #print (self.EasyMol.Vobjects[object_id].actived)

        
        
        
    def setup_icons (self):
        """ Function doc """
        icon6 = QIcon()
        icon6.addPixmap(QPixmap("/home/fernando/programs/EasyHybrid/easyhybrid/QtEasyMol/GUI/NewProject.png"), QIcon.Normal, QIcon.Off)
        self.actionNew_Project.setIcon(icon6)
        

    def showDialog(self):
        '''
        dir = self.sourceDir
        filters = "Text files (*.txt);;Images (*.png *.xpm *.jpg)"
        selected_filter = "Images (*.png *.xpm *.jpg)"
        options = "" # ???
        fileObj = QFileDialog.getOpenFileName(self, " File dialog ", dir, filters, selected_filter, options)
        '''
        
        filters = "PDB files (*.pdb);;XYZ (*.xyz);;All (*)"
        #selected_filter = "Images (*.png *.xpm *.jpg)"
        options = "" # ???
        
        dialog = QtGui.QFileDialog()
        fname, _ = dialog.getOpenFileName(self, 'Open file','/home', filters, options)
        
        if self.EasyMol.load(fname):
            self.update_list_view()
        else:
            pass


    def update_list_view (self):
        """ Function doc """
        Vobjects_list = self.EasyMol.get_vobject_list()
        self.treeWidget.clear()

        for key in Vobjects_list:
            item = QtGui.QTreeWidgetItem(self.treeWidget)
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            
            if self.EasyMol.Vobjects[int(key)].actived:
                item.setCheckState(0, QtCore.Qt.Checked)           
            else:
                item.setCheckState(0, QtCore.Qt.Unchecked)           
            
            item.setText(1, QtGui.QApplication.translate("MainWindow", str(key)          , None, QtGui.QApplication.UnicodeUTF8))
            item.setText(2, QtGui.QApplication.translate("MainWindow", Vobjects_list[key], None, QtGui.QApplication.UnicodeUTF8))
            item.setText(3, QtGui.QApplication.translate("MainWindow", "12"              , None, QtGui.QApplication.UnicodeUTF8))
            item.setText(4, QtGui.QApplication.translate("MainWindow", "123"             , None, QtGui.QApplication.UnicodeUTF8))
            item.setText(5, QtGui.QApplication.translate("MainWindow", "no"              , None, QtGui.QApplication.UnicodeUTF8))            

    
    
    def open_list_view_menu(self, position):
        #print ('menu')
        
        
        
        indexes = self.treeWidget.selectedIndexes()
        
        #print (position)
        #index = indexes[0]
        #for index in indexes:
        #    print ('index.parent().isValid()', index.parent().isValid())
        #    print ('index.parent()'          , index.parent())
        #    print ('index '                  , index )
        #    print ('index.row() '                  , index.row() )

            
            #print (indexes[0].model ())
        index =  indexes[0]
        self.current_row = index.row()
        
        if len(indexes) > 0:
        
             level = 0
             index = indexes[0]
             while index.parent().isValid():
                 index = index.parent()
                 
                 #print (index.checkState())
                 level += 1
         
        menu = QtGui.QMenu()
        if level == 0:
            menu.addAction(self.tr("Show"))
            menu.addAction(self.tr("Hide"))
            menu.addAction(self.Action_delete)
            
            menuHelp_2 = menu.addMenu("&Format")
            menuHelp_2.setObjectName("menuHelp_2")
            #menuHelp_2.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
            menuHelp_2.addAction(self.tr("Show"))
            menuHelp_2.addAction(self.tr("Hide"))
            menuHelp_2.addAction(self.tr("Delete"))
            
        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))

        #self.menubar = QtGui.QMenuBar(MainWindow)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        #self.menubar.setObjectName("menubar")
        #self.menuFile = QtGui.QMenu(self.menubar)
        #self.menuFile.setObjectName("menuFile")
        #self.menuEdit = QtGui.QMenu(self.menubar)
        #self.menuEdit.setObjectName("menuEdit")
        #self.menuView = QtGui.QMenu(self.menubar)
        #self.menuView.setObjectName("menuView")
        #
        #self.menuHelp = QtGui.QMenu(self.menubar)
        #self.menuHelp.setObjectName("menuHelp")
        #self.menuHelp_2 = QtGui.QMenu(self.menuHelp)
        #self.menuHelp_2.setObjectName("menuHelp_2")
    
    def delete_obj (self, index = 0):
        """ Function doc """
        self.EasyMol.delete(self.current_row)
        self.update_list_view()
        
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )
'''
