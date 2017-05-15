# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Fri May 12 15:57:36 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
import sys

from PySide import QtCore, QtGui
from MainWindow import Ui_EasyMol
from GLWidget import GLWidget



class MainWindows(QtGui.QMainWindow, QtGui.QWidget):
    
    def __init__(self):
        super(MainWindows, self).__init__()
        
        self.initUI()
        
    def initUI(self):               
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('.icon_MD_24x24.png'))
        self.center()

        '''
        # toolbar buttons
        #---------------------------------------------------------------
        self.Action1 = QtGui.QAction('Exit', self)
        self.Action1.setShortcut('Ctrl+Q')
        self.Action1.setStatusTip('Exit application')
        self.Action1.triggered.connect(self.close)

        self.Action2 = QtGui.QAction(QtGui.QIcon('.icon_MD_24x24.png'), 'Something', self)
        self.Action2.setShortcut('Ctrl+T')
        self.Action2.setStatusTip('Print something')
        self.Action2.triggered.connect(self.print_something)
        #---------------------------------------------------------------

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.Action1)
        fileMenu.addAction(self.Action2)
        
        fileMenu = menubar.addMenu('&Edit')
        fileMenu = menubar.addMenu('&View')
        fileMenu = menubar.addMenu('&Help')
        '''

        self.menubar = self.menuBar()

        #self.menubar = QtGui.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1026, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuCalculate = QtGui.QMenu(self.menubar)
        self.menuCalculate.setObjectName("menuCalculate")
        self.menuAnalysis = QtGui.QMenu(self.menubar)
        self.menuAnalysis.setObjectName("menuAnalysis")
        self.menuExtensions = QtGui.QMenu(self.menubar)
        self.menuExtensions.setObjectName("menuExtensions")
        self.menuHelp_2 = QtGui.QMenu(self.menubar)
        self.menuHelp_2.setObjectName("menuHelp_2")
        self.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtGui.QToolBar(self)
        self.toolBar_2.setObjectName("toolBar_2")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)
        self.toolBar_3 = QtGui.QToolBar(self)
        self.toolBar_3.setObjectName("toolBar_3")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_3)
        self.dockWidget = QtGui.QDockWidget(self)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeWidget = QtGui.QTreeWidget(self.dockWidgetContents)
        self.treeWidget.setUniformRowHeights(True)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setDefaultSectionSize(50)
        self.treeWidget.header().setHighlightSections(False)
        self.treeWidget.header().setSortIndicatorShown(False)
        self.treeWidget.header().setStretchLastSection(False)
        self.horizontalLayout.addWidget(self.treeWidget)
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.actionNew = QtGui.QAction(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/NewProject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtGui.QAction(self)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/Open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(self)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/Save2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtGui.QAction(self)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/Save_as.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_As.setIcon(icon3)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionMesure = QtGui.QAction(self)
        self.actionMesure.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/measure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMesure.setIcon(icon4)
        self.actionMesure.setObjectName("actionMesure")
        self.actionSelections = QtGui.QAction(self)
        self.actionSelections.setObjectName("actionSelections")
        self.actionQuantum_Chemistry = QtGui.QAction(self)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/.icon_psi24x24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuantum_Chemistry.setIcon(icon5)
        self.actionQuantum_Chemistry.setObjectName("actionQuantum_Chemistry")
        self.actionProperties = QtGui.QAction(self)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/systemCheck.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProperties.setIcon(icon6)
        self.actionProperties.setObjectName("actionProperties")
        self.actionCalculate_Energy = QtGui.QAction(self)
        
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/.icon_single_point_24x24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.actionCalculate_Energy.setIcon(icon7)
        self.actionCalculate_Energy.setObjectName("actionCalculate_Energy")
        self.actionGeometry_Optimization = QtGui.QAction(self)
        
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/.icon_minimization_24x24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.actionGeometry_Optimization.setIcon(icon8)
        self.actionGeometry_Optimization.setObjectName("actionGeometry_Optimization")
        self.actionMolecular_Dynamics = QtGui.QAction(self)
        
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/.icon_MD_24x24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.actionMolecular_Dynamics.setIcon(icon9)
        self.actionMolecular_Dynamics.setObjectName("actionMolecular_Dynamics")
        self.actionDelete_System = QtGui.QAction(self)
        
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/deleteSystem.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.actionDelete_System.setIcon(icon10)
        self.actionDelete_System.setObjectName("actionDelete_System")
        self.actionShow_Cell = QtGui.QAction(self)
        self.actionShow_Cell.setCheckable(True)
        
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("icons/ShowCell.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.actionShow_Cell.setIcon(icon11)
        self.actionShow_Cell.setObjectName("actionShow_Cell")
        self.actionPreferences = QtGui.QAction(self)
        self.actionPreferences.setObjectName("actionPreferences")
        
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPreferences)
        
        self.menuEdit.addAction(self.actionMesure)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuCalculate.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menuExtensions.menuAction())
        self.menubar.addAction(self.menuHelp_2.menuAction())
        
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSave_As)
        self.toolBar.addAction(self.actionDelete_System)
        self.toolBar_2.addAction(self.actionMesure)
        self.toolBar_2.addAction(self.actionShow_Cell)
        self.toolBar_2.addAction(self.actionQuantum_Chemistry)
        self.toolBar_3.addAction(self.actionProperties)
        self.toolBar_3.addAction(self.actionCalculate_Energy)
        self.toolBar_3.addAction(self.actionGeometry_Optimization)
        self.toolBar_3.addAction(self.actionMolecular_Dynamics)








        self.setWindowTitle(QtGui.QApplication.translate("EasyMol", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("EasyMol", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("EasyMol", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("EasyMol", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("EasyMol", "Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.menuCalculate.setTitle(QtGui.QApplication.translate("EasyMol", "Calculate", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAnalysis.setTitle(QtGui.QApplication.translate("EasyMol", "Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.menuExtensions.setTitle(QtGui.QApplication.translate("EasyMol", "Extensions", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp_2.setTitle(QtGui.QApplication.translate("EasyMol", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("EasyMol", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_2.setWindowTitle(QtGui.QApplication.translate("EasyMol", "toolBar_2", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_3.setWindowTitle(QtGui.QApplication.translate("EasyMol", "toolBar_3", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("EasyMol", "Id", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(1, QtGui.QApplication.translate("EasyMol", "Object", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(2, QtGui.QApplication.translate("EasyMol", "Atoms", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(3, QtGui.QApplication.translate("EasyMol", "Frames", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(4, QtGui.QApplication.translate("EasyMol", "Active", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, QtGui.QApplication.translate("EasyMol", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(0).setText(1, QtGui.QApplication.translate("EasyMol", "new_system", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(0).setText(2, QtGui.QApplication.translate("EasyMol", "12", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(0).setText(3, QtGui.QApplication.translate("EasyMol", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.topLevelItem(0).setText(4, QtGui.QApplication.translate("EasyMol", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.actionNew.setText(QtGui.QApplication.translate("EasyMol", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("EasyMol", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("EasyMol", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("EasyMol", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMesure.setText(QtGui.QApplication.translate("EasyMol", "Mesure", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelections.setText(QtGui.QApplication.translate("EasyMol", "Selections", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuantum_Chemistry.setText(QtGui.QApplication.translate("EasyMol", "Quantum Chemistry", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProperties.setText(QtGui.QApplication.translate("EasyMol", "Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCalculate_Energy.setText(QtGui.QApplication.translate("EasyMol", "Calculate Energy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGeometry_Optimization.setText(QtGui.QApplication.translate("EasyMol", "Geometry Optimization", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMolecular_Dynamics.setText(QtGui.QApplication.translate("EasyMol", "Molecular Dynamics", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete_System.setText(QtGui.QApplication.translate("EasyMol", "Delete System", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Cell.setText(QtGui.QApplication.translate("EasyMol", "Show Cell", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("EasyMol", "Preferences", None, QtGui.QApplication.UnicodeUTF8))













        self.glWidget = GLWidget(self)
        self.setCentralWidget(self.glWidget)
        self.setWindowTitle(self.tr("Hello GL"))        
        
        
        '''
        self.dockWidget_4 = QtGui.QDockWidget(self)
        self.dockWidget_4.setObjectName("dockWidget_4")
        self.dockWidgetContents_4 = QtGui.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.dockWidgetContents_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.treeWidget = QtGui.QTreeWidget(self.dockWidgetContents_4)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.horizontalLayout_2.addWidget(self.treeWidget)
        self.dockWidget_4.setWidget(self.dockWidgetContents_4)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_4)

        #tree        = QtGui.QTreeWidget (self.dockWidgetContents)
        headerItem  = QtGui.QTreeWidgetItem()
        item        = QtGui.QTreeWidgetItem()
        
        
        self.treeWidget.doubleClicked.connect(self.treeWidget_doubleClicked)
        self.treeWidget.clicked.connect(self.treefunction)
        #self.treeMedia.doubleClicked.connect(self.treeMedia_doubleClicked)
        
        for i in range(3):
            parent = QtGui.QTreeWidgetItem(self.treeWidget)
            parent.setText(0, "Parent {}".format(i))
            parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            for x in range(5):
                child = QtGui.QTreeWidgetItem(parent)
                child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
                child.setText(0, "Child {}".format(x))
                child.setCheckState(0, QtCore.Qt.Unchecked)

                #QtCore.QObject.connect(child, QtCore.SIGNAL("clicked(bool)"), toolbar.setShown)
                
                #child.icon(QtGui.QIcon('.icon_MD_24x24.png'))
                
        '''
        #mainLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        ##mainLayout.addWidget(self.glWidget)
        ##mainLayout.setSpacing(0)
        #mainLayout.addWidget(self.xSlider)
        #mainLayout.addWidget(self.ySlider)
        #mainLayout.addWidget(self.zSlider)



        #btn = QtGui.QPushButton('Button', self)
        #btn.setToolTip('This is a <b>QPushButton</b> widget')
        #btn.resize(btn.sizeHint())
        #btn.move(500, 50)
        #btn.clicked.connect(self.print_something)
        #
        #self.setGeometry(300, 300, 350, 250)
        #self.setWindowTitle('Main window')    
        self.show()
    
    
    #def contextMenuEvent(self, event):
    #    menu = QtGui.QMenu(self)
    #    menu.addAction(self.Action1)
    #    menu.addAction(self.Action2)
    #    #menu.addAction(self.pasteAct)
    #    menu.exec_(event.globalPos())
    
    def treeWidget_doubleClicked (self):
        """ Function doc """
        item = self.treeWidget.selectedIndexes()[0]
        #print (item.model().itemFromIndex(index).text())
        #print (item)                   
        #print (item.flags ()           )
        #print (item.isValid ()         )
        #print (item.model ()           )
        print (item.parent ()          )
        print (item.row ()             )
        
        '''
        def child (row, column)
        def column ()
        def data ([role=Qt.DisplayRole])
        def flags ()
        def internalId ()
        def internalPointer ()
        def isValid ()
        def model ()
        def parent ()
        def row ()
        def sibling (row, column)
        '''
    
    def treefunction (self):
        """ Function doc """
        print('uhuuu')
        item = self.treeWidget.selectedIndexes()[0]
        print (item.parent ().row ()  )
        print (item.row ()            )
        
        
        
        
        
        
    def print_something (self):
        """ Function doc """
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to print?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            print ('something')
            self.statusBar().showMessage('something')

        else:
            print ('print nothing')
            self.statusBar().showMessage('print nothing')

    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   
    
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def createSlider(self, changedSignal, setterSlot):
        slider = QtGui.QSlider(QtCore.Qt.Vertical)

        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QtGui.QSlider.TicksRight)

        self.glWidget.connect(slider, QtCore.SIGNAL("valueChanged(int)"), setterSlot)
        self.connect(self.glWidget, changedSignal, slider, QtCore.SLOT("setValue(int)"))

        return slider


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MainWindows()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



