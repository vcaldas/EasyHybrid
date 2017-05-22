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
        
        
        #icon6 = QIcon()
        #icon6.addPixmap(QPixmap("/home/fernando/programs/EasyHybrid/easyhybrid/QtEasyMol/GUI/NewProject.png"), QIcon.Normal, QIcon.Off)
        #self.actionNew_Project.setIcon(icon6)
        
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.openMenu)
        self.actionOpen.triggered.connect(self.showDialog)
        glmenu = [self.actionOpen]
        

        self.glwidget = GLWidget(self, glmenu = glmenu)
        self.EasyMol  = EasyMolSession(glwidget =  self.glwidget)
        
        
        #import GLarea.vis_parser as vp
        #self.glwidget.data = vp.parse_pdb("/home/fernando/programs/EasyHybrid/easyhybrid/QtEasyMol/QtMol/pdbs/1l2y.pdb")
        
        self.setCentralWidget(self.glwidget)
        self.show()
        #self.EasyMol.load("/home/fernando/programs/EasyHybrid/easyhybrid/QtEasyMol/QtMol/pdbs/1l2y.pdb")
        #self.EasyMol.load("/home/fernando/programs/EasyHybrid/pdbs/glicose2.pdb")
    
   
    
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
        
        self.EasyMol.load(fname)
        
        self.updateGui()
        
        return fname
        #f = open(fname, 'r')


    def updateGui (self):
        """ Function doc """
        lista = self.EasyMol.get_vobject_list()
        print(lista)
        tree        = self.treeWidget
        headerItem  = QTreeWidgetItem()
        item        = QTreeWidgetItem()

        for i in lista:
            parent = QTreeWidgetItem(tree)
            parent.setText(0, lista[i])
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            parent.setCheckState(0, Qt.Unchecked)
        tree.show() 

    def openMenu(self, position):
        #print ('menu')
        
        indexes = self.treeWidget.selectedIndexes()
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

        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))




        
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )
'''
