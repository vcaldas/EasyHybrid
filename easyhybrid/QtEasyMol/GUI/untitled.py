# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Sat May 27 10:41:37 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 675)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 300, 85, 27))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp_2 = QtGui.QMenu(self.menuHelp)
        self.menuHelp_2.setObjectName("menuHelp_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeWidget = QtGui.QTreeWidget(self.dockWidgetContents)
        self.treeWidget.setAutoScrollMargin(0)
        self.treeWidget.setTextElideMode(QtCore.Qt.ElideLeft)
        self.treeWidget.setAutoExpandDelay(-1)
        self.treeWidget.setIndentation(0)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setItemsExpandable(True)
        self.treeWidget.setExpandsOnDoubleClick(False)
        self.treeWidget.setColumnCount(6)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setDefaultSectionSize(30)
        self.treeWidget.header().setMinimumSectionSize(20)
        self.horizontalLayout.addWidget(self.treeWidget)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.dockWidget_3 = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_3.sizePolicy().hasHeightForWidth())
        self.dockWidget_3.setSizePolicy(sizePolicy)
        self.dockWidget_3.setCursor(QtCore.Qt.ArrowCursor)
        self.dockWidget_3.setObjectName("dockWidget_3")
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.gridLayout_2 = QtGui.QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.toolButton_10 = QtGui.QToolButton(self.dockWidgetContents_3)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".backward2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_10.setIcon(icon)
        self.toolButton_10.setObjectName("toolButton_10")
        self.gridLayout_2.addWidget(self.toolButton_10, 0, 0, 1, 1)
        self.toolButton_12 = QtGui.QToolButton(self.dockWidgetContents_3)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(".backward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_12.setIcon(icon1)
        self.toolButton_12.setObjectName("toolButton_12")
        self.gridLayout_2.addWidget(self.toolButton_12, 0, 1, 1, 1)
        self.toolButton_13 = QtGui.QToolButton(self.dockWidgetContents_3)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("deleteSystem.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_13.setIcon(icon2)
        self.toolButton_13.setObjectName("toolButton_13")
        self.gridLayout_2.addWidget(self.toolButton_13, 0, 2, 1, 1)
        self.toolButton_9 = QtGui.QToolButton(self.dockWidgetContents_3)
        self.toolButton_9.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(".play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_9.setIcon(icon3)
        self.toolButton_9.setCheckable(True)
        self.toolButton_9.setChecked(False)
        self.toolButton_9.setObjectName("toolButton_9")
        self.gridLayout_2.addWidget(self.toolButton_9, 0, 3, 1, 1)
        self.toolButton_8 = QtGui.QToolButton(self.dockWidgetContents_3)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(".forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_8.setIcon(icon4)
        self.toolButton_8.setObjectName("toolButton_8")
        self.gridLayout_2.addWidget(self.toolButton_8, 0, 4, 1, 1)
        self.toolButton_7 = QtGui.QToolButton(self.dockWidgetContents_3)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(".forward2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_7.setIcon(icon5)
        self.toolButton_7.setObjectName("toolButton_7")
        self.gridLayout_2.addWidget(self.toolButton_7, 0, 5, 1, 1)
        self.horizontalSlider = QtGui.QSlider(self.dockWidgetContents_3)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout_2.addWidget(self.horizontalSlider, 1, 0, 1, 6)
        self.label = QtGui.QLabel(self.dockWidgetContents_3)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 3)
        self.comboBox = QtGui.QComboBox(self.dockWidgetContents_3)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_2.addWidget(self.comboBox, 2, 3, 1, 3)
        self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_3)
        self.toolBar_2 = QtGui.QToolBar(MainWindow)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)
        self.actionNew_Project = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("NewProject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew_Project.setIcon(icon6)
        self.actionNew_Project.setObjectName("actionNew_Project")
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionViewing = QtGui.QAction(MainWindow)
        self.actionViewing.setCheckable(True)
        self.actionViewing.setChecked(False)
        self.actionViewing.setEnabled(True)
        self.actionViewing.setObjectName("actionViewing")
        self.actionAqui = QtGui.QAction(MainWindow)
        self.actionAqui.setObjectName("actionAqui")
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuHelp_2.addAction(self.actionAqui)
        self.menuHelp.addAction(self.menuHelp_2.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionNew_Project)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSave_As)
        self.toolBar_2.addAction(self.actionViewing)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.toolButton_9, QtCore.SIGNAL("toggled(bool)"), self.pushButton_3.setShown)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp_2.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", " ", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Object", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Atoms", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "Frames", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(5, QtGui.QApplication.translate("MainWindow", "Acitve", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_10.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_12.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_13.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_8.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_7.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_2.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar_2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Project.setText(QtGui.QApplication.translate("MainWindow", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("MainWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.actionViewing.setText(QtGui.QApplication.translate("MainWindow", "Viewing", None, QtGui.QApplication.UnicodeUTF8))
        self.actionViewing.setToolTip(QtGui.QApplication.translate("MainWindow", "Viewing or Editing", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAqui.setText(QtGui.QApplication.translate("MainWindow", "aqui", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

