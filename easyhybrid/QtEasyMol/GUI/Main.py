# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Fri May 12 15:57:36 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
 

import sys

from PySide.QtGui import *

from PySide.QtCore import *

from GUI.untitled      import Ui_MainWindow

from GLarea.easyMolObj import EasyMolSession
from GLarea.GLWidget   import GLWidget







class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setupUi(self)
        
        self.listView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listView.customContextMenuRequested.connect(self.open_list_view_menu)
        self.actionOpen.triggered.connect(self.showDialog)
        glmenu = [self.actionOpen]

        self.glwidget = GLWidget(self, glmenu = glmenu)
        self.EasyMol  = EasyMolSession(glwidget =  self.glwidget)

        self.setCentralWidget(self.glwidget)
        self.show()
    
   
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
        
        dialog = QFileDialog()
        fname, _ = dialog.getOpenFileName(self, 'Open file','/home', filters, options)
        
        if self.EasyMol.load(fname):
            self.update_list_view()
        else:
            pass
            
        #return fname

    def update_list_view (self):
        """ Function doc """
        Vobjects_list = self.EasyMol.get_vobject_list()
        
        
        model = QStandardItemModel(self.listView)
        
        for key in Vobjects_list:
            # create an item with a caption
            item = QStandardItem(Vobjects_list[key])

            # add a checkbox to it
            item.setCheckable(True)

            # Add the item to the model
            model.appendRow(item)

        # Apply the model to the list view
        self.listView.setModel(model)
 

    def open_list_view_menu(self, position):
        #print ('menu')
        pass
        
        indexes = self.listView.selectedIndexes()
        print (indexes)
        
        if len(indexes) > 0:
        
             level = 0
             index = indexes[0]
             while index.parent().isValid():
                 index = index.parent()
                 
                 print (index.checkState())
                 level += 1
         
        menu = QMenu()
        if level == 0:
            menu.addAction(self.tr("Edit person"))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))
        elif level == 2:
            menu.addAction(self.tr("Edit object"))
        
        menu.exec_(self.listView.viewport().mapToGlobal(position))




        
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )
'''
