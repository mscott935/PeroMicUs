import os
import re
import sys

import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

import exceptions
import outputmodel
import pipeline
import utils


class Ui_MainWindow(object):
    # UI generated using QtDesigner, translated into Python with pyuic5.
    # Worth reorganizing and renaming elements.
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Pero-Mic-Us")
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_input = QtWidgets.QWidget()
        self.tab_input.setObjectName("tab_input")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_input)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_filesList = QtWidgets.QFrame(self.tab_input)
        self.frame_filesList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_filesList.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_filesList.setObjectName("frame_filesList")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_filesList)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.frame_filesList)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.listWidget_inputFiles = QtWidgets.QListWidget(self.frame_filesList)
        self.listWidget_inputFiles.setObjectName("listWidget_inputFiles")
        self.verticalLayout.addWidget(self.listWidget_inputFiles)
        self.gridLayout_4.addWidget(self.frame_filesList, 2, 0, 1, 1)
        self.frame_inputDir = QtWidgets.QFrame(self.tab_input)
        self.frame_inputDir.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_inputDir.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_inputDir.setObjectName("frame_inputDir")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_inputDir)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_inputDir = QtWidgets.QLineEdit(self.frame_inputDir)
        self.lineEdit_inputDir.setObjectName("lineEdit_inputDir")
        self.horizontalLayout.addWidget(self.lineEdit_inputDir)
        self.pushButton_inputDir = QtWidgets.QPushButton(self.frame_inputDir)
        self.pushButton_inputDir.setObjectName("pushButton_inputDir")
        self.horizontalLayout.addWidget(self.pushButton_inputDir)
        self.gridLayout_4.addWidget(self.frame_inputDir, 0, 0, 1, 2)
        self.frame_outputDir = QtWidgets.QFrame(self.tab_input)
        self.frame_outputDir.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_outputDir.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_outputDir.setObjectName("frame_outputDir")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_outputDir)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_outputDir = QtWidgets.QLineEdit(self.frame_outputDir)
        self.lineEdit_outputDir.setObjectName("lineEdit_outputDir")
        self.horizontalLayout_2.addWidget(self.lineEdit_outputDir)
        self.pushButton_outputDir = QtWidgets.QPushButton(self.frame_outputDir)
        self.pushButton_outputDir.setObjectName("pushButton_outputDir")
        self.horizontalLayout_2.addWidget(self.pushButton_outputDir)
        self.gridLayout_4.addWidget(self.frame_outputDir, 1, 0, 1, 2)
        self.frame_inputOptions = QtWidgets.QFrame(self.tab_input)
        self.frame_inputOptions.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_inputOptions.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_inputOptions.setObjectName("frame_inputOptions")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_inputOptions)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 1, 2, 1, 1)
        self.pushButton_analyze = QtWidgets.QPushButton(self.frame_inputOptions)
        self.pushButton_analyze.setObjectName("pushButton_analyze")
        self.gridLayout_3.addWidget(self.pushButton_analyze, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        self.toolBox_inputOptions = QtWidgets.QToolBox(self.frame_inputOptions)
        self.toolBox_inputOptions.setObjectName("toolBox_inputOptions")
        self.page_ioSettings = QtWidgets.QWidget()
        self.page_ioSettings.setGeometry(QtCore.QRect(0, 0, 449, 304))
        self.page_ioSettings.setObjectName("page_ioSettings")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_ioSettings)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_ioSettings = QtWidgets.QFrame(self.page_ioSettings)
        self.frame_ioSettings.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ioSettings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ioSettings.setObjectName("frame_ioSettings")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_ioSettings)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.checkBox_spectrograms = QtWidgets.QCheckBox(self.frame_ioSettings)
        self.checkBox_spectrograms.setEnabled(True)
        self.checkBox_spectrograms.setChecked(True)
        self.checkBox_spectrograms.setObjectName("checkBox_spectrograms")
        self.gridLayout_5.addWidget(self.checkBox_spectrograms, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(173, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 4, 1, 1, 1)
        self.lineEdit_endTime = QtWidgets.QLineEdit(self.frame_ioSettings)
        self.lineEdit_endTime.setObjectName("lineEdit_endTime")
        self.lineEdit_endTime.setDisabled(True)
        self.gridLayout_5.addWidget(self.lineEdit_endTime, 3, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_ioSettings)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEdit_startTime = QtWidgets.QLineEdit(self.frame_ioSettings)
        self.lineEdit_startTime.setPlaceholderText("")
        self.lineEdit_startTime.setObjectName("lineEdit_startTime")
        self.lineEdit_startTime.setDisabled(True)
        self.gridLayout_5.addWidget(self.lineEdit_startTime, 2, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(173, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem4, 1, 1, 1, 1)
        self.checkBox_setTime = QtWidgets.QCheckBox(self.frame_ioSettings)
        self.checkBox_setTime.setChecked(True)
        self.checkBox_setTime.setObjectName("checkBox_setTime")
        self.gridLayout_5.addWidget(self.checkBox_setTime, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_ioSettings)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 2, 0, 1, 1)
        self.checkBox_removeClipped = QtWidgets.QCheckBox(self.frame_ioSettings)
        self.checkBox_removeClipped.setObjectName("checkBox_removeClipped")
        self.checkBox_removeClipped.setChecked(True)
        self.gridLayout_5.addWidget(self.checkBox_removeClipped, 6, 0, 1, 1)
        self.checkBox_deleteClips = QtWidgets.QCheckBox(self.frame_ioSettings)
        self.checkBox_deleteClips.setObjectName("checkBox_deleteClips")
        self.gridLayout_5.addWidget(self.checkBox_deleteClips, 5, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_ioSettings, 0, 0, 1, 1)
        self.toolBox_inputOptions.addItem(self.page_ioSettings, "")
        self.page_fileParsing = QtWidgets.QWidget()
        self.page_fileParsing.setGeometry(QtCore.QRect(0, 0, 494, 304))
        self.page_fileParsing.setObjectName("page_fileParsing")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.page_fileParsing)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frame_filenameParsing = QtWidgets.QFrame(self.page_fileParsing)
        self.frame_filenameParsing.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_filenameParsing.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_filenameParsing.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_filenameParsing.setObjectName("frame_filenameParsing")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_filenameParsing)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.lineEdit_filenameCategories = QtWidgets.QLineEdit(self.frame_filenameParsing)
        self.lineEdit_filenameCategories.setObjectName("lineEdit_filenameCategories")
        self.gridLayout_8.addWidget(self.lineEdit_filenameCategories, 10, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.frame_filenameParsing)
        self.label_6.setObjectName("label_6")
        self.gridLayout_8.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_filenameParsing)
        self.label_2.setObjectName("label_2")
        self.gridLayout_8.addWidget(self.label_2, 6, 0, 1, 1)
        self.lineEdit_filenameDelimiter = QtWidgets.QLineEdit(self.frame_filenameParsing)
        self.lineEdit_filenameDelimiter.setObjectName("lineEdit_filenameDelimiter")
        self.gridLayout_8.addWidget(self.lineEdit_filenameDelimiter, 3, 1, 1, 1)
        self.checkBox_parseFilename = QtWidgets.QCheckBox(self.frame_filenameParsing)
        self.checkBox_parseFilename.setChecked(True)
        self.checkBox_parseFilename.setObjectName("checkBox_parseFilename")
        self.gridLayout_8.addWidget(self.checkBox_parseFilename, 0, 0, 1, 2)
        self.gridLayout_7.addWidget(self.frame_filenameParsing, 0, 0, 1, 1)
        self.toolBox_inputOptions.addItem(self.page_fileParsing, "")
        self.page_vocalSettings = QtWidgets.QWidget()
        self.page_vocalSettings.setGeometry(QtCore.QRect(0, 0, 462, 304))
        self.page_vocalSettings.setObjectName("page_vocalSettings")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.page_vocalSettings)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.frame_vocalSettings = QtWidgets.QFrame(self.page_vocalSettings)
        self.frame_vocalSettings.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_vocalSettings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_vocalSettings.setObjectName("frame_vocalSettings")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frame_vocalSettings)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.frame_silenceFile = QtWidgets.QFrame(self.frame_vocalSettings)
        self.frame_silenceFile.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_silenceFile.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_silenceFile.setObjectName("frame_silenceFile")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_silenceFile)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.checkBox_useSilenceFile = QtWidgets.QCheckBox(self.frame_silenceFile)
        self.checkBox_useSilenceFile.setObjectName("checkBox_useSilenceFile")
        self.verticalLayout_5.addWidget(self.checkBox_useSilenceFile)
        self.lineEdit_silenceFile = QtWidgets.QLineEdit(self.frame_silenceFile)
        self.lineEdit_silenceFile.setObjectName("lineEdit_silenceFile")
        self.lineEdit_silenceFile.setDisabled(True)
        self.verticalLayout_5.addWidget(self.lineEdit_silenceFile)
        self.pushButton_selectSilenceFile = QtWidgets.QPushButton(self.frame_silenceFile)
        self.pushButton_selectSilenceFile.setObjectName("pushButton_selectSilenceFile")
        self.pushButton_selectSilenceFile.setDisabled(True)
        self.verticalLayout_5.addWidget(self.pushButton_selectSilenceFile)
        self.gridLayout_9.addWidget(self.frame_silenceFile, 1, 0, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.frame_vocalSettings)
        self.label_7.setObjectName("label_7")
        self.gridLayout_9.addWidget(self.label_7, 2, 0, 1, 1)
        self.spinBox_silenceThresh = QtWidgets.QSpinBox(self.frame_vocalSettings)
        self.spinBox_silenceThresh.setMinimum(-99)
        self.spinBox_silenceThresh.setMaximum(-1)
        self.spinBox_silenceThresh.setProperty("value", -55)
        self.spinBox_silenceThresh.setObjectName("spinBox_silenceThresh")
        self.gridLayout_9.addWidget(self.spinBox_silenceThresh, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_vocalSettings)
        self.label_8.setObjectName("label_8")
        self.gridLayout_9.addWidget(self.label_8, 3, 0, 1, 1)
        self.spinBox_minSilenceLen = QtWidgets.QSpinBox(self.frame_vocalSettings)
        self.spinBox_minSilenceLen.setMinimum(1)
        self.spinBox_minSilenceLen.setProperty("value", 5)
        self.spinBox_minSilenceLen.setObjectName("spinBox_minSilenceLen")
        self.gridLayout_9.addWidget(self.spinBox_minSilenceLen, 3, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_vocalSettings)
        self.label_9.setObjectName("label_9")
        self.gridLayout_9.addWidget(self.label_9, 4, 0, 1, 1)
        self.spinBox_bufferLen = QtWidgets.QSpinBox(self.frame_vocalSettings)
        self.spinBox_bufferLen.setProperty("value", 5)
        self.spinBox_bufferLen.setObjectName("spinBox_bufferLen")
        self.gridLayout_9.addWidget(self.spinBox_bufferLen, 4, 1, 1, 1)
        self.gridLayout_10.addWidget(self.frame_vocalSettings, 0, 0, 1, 1)
        self.toolBox_inputOptions.addItem(self.page_vocalSettings, "")
        self.gridLayout_3.addWidget(self.toolBox_inputOptions, 0, 0, 1, 3)
        self.gridLayout_4.addWidget(self.frame_inputOptions, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tab_input, "")
        self.tab_output = QtWidgets.QWidget()
        self.tab_output.setObjectName("tab_output")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_output)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_output = QtWidgets.QFrame(self.tab_output)
        self.frame_output.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_output.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_output.setObjectName("frame_output")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.frame_output)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.tableView = QtWidgets.QTableView(self.frame_output)
        self.tableView.setObjectName("tableView")
        self.gridLayout_13.addWidget(self.tableView, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_output)
        self.tabWidget.addTab(self.tab_output, "")
        # PUP TAB
        self.tab_output_agg = QtWidgets.QWidget()
        self.tab_output_agg.setObjectName("tab_output_agg")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_output_agg)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_output_agg = QtWidgets.QFrame(self.tab_output_agg)
        self.frame_output_agg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_output_agg.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_output_agg.setObjectName("frame_output_agg")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.frame_output_agg)
        self.gridLayout_14.setObjectName("gridLayout_output_agg")
        self.tableAggView = QtWidgets.QTableView(self.frame_output_agg)
        self.tableAggView.setObjectName("tableAggView")
        self.gridLayout_14.addWidget(self.tableAggView, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_output_agg)
        self.tabWidget.addTab(self.tab_output_agg, "")


        self.tab_specs = QtWidgets.QWidget()
        self.tab_specs.setObjectName("tab_specs")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_specs)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_specInfo = QtWidgets.QFrame(self.tab_specs)
        self.frame_specInfo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_specInfo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_specInfo.setObjectName("frame_specInfo")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_specInfo)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_specInfo_specFilename = QtWidgets.QLabel(self.frame_specInfo)
        self.label_specInfo_specFilename.setObjectName("label_specInfo_specFilename")
        self.verticalLayout_3.addWidget(self.label_specInfo_specFilename)
        self.label_specInfo_sourceFilename = QtWidgets.QLabel(self.frame_specInfo)
        self.label_specInfo_sourceFilename.setObjectName("label_specInfo_sourceFilename")
        self.verticalLayout_3.addWidget(self.label_specInfo_sourceFilename)
        self.label_specInfo_vocNumber = QtWidgets.QLabel(self.frame_specInfo)
        self.label_specInfo_vocNumber.setObjectName("label_specInfo_vocNumber")
        self.verticalLayout_3.addWidget(self.label_specInfo_vocNumber)
        self.label_specInfo_classification = QtWidgets.QLabel(self.frame_specInfo)
        self.label_specInfo_classification.setObjectName("label_specInfo_classification")
        self.verticalLayout_3.addWidget(self.label_specInfo_classification)
        self.label_specInfo_confidence = QtWidgets.QLabel(self.frame_specInfo)
        self.label_specInfo_confidence.setObjectName("label_specInfo_confidence")
        self.verticalLayout_3.addWidget(self.label_specInfo_confidence)
        self.verticalLayout_4.addWidget(self.frame_specInfo)
        self.frame_tab3_specSelect = QtWidgets.QFrame(self.tab_specs)
        self.frame_tab3_specSelect.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_tab3_specSelect.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tab3_specSelect.setObjectName("frame_tab3_specSelect")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_tab3_specSelect)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_tab3_prev = QtWidgets.QPushButton(self.frame_tab3_specSelect)
        self.pushButton_tab3_prev.setObjectName("pushButton_tab3_prev")
        self.pushButton_tab3_prev.setDisabled(True)
        self.gridLayout.addWidget(self.pushButton_tab3_prev, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.frame_tab3_specSelect)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.insertItem(0, "Select manual classification:")
        self.comboBox.insertItem(1, "Sonic")
        self.comboBox.insertItem(2, "Ultrasonic")
        self.comboBox.insertItem(3, "Scratch")
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.pushButton_tab3_next = QtWidgets.QPushButton(self.frame_tab3_specSelect)
        self.pushButton_tab3_next.setObjectName("pushButton_tab3_next")
        self.pushButton_tab3_next.setDisabled(True)
        self.gridLayout.addWidget(self.pushButton_tab3_next, 1, 2, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.frame_tab3_specSelect)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 0, 1, 1, 1)
        self.verticalLayout_4.addWidget(self.frame_tab3_specSelect)
        self.label_tab3_specImage = QtWidgets.QLabel(self.tab_specs)
        self.label_tab3_specImage.setObjectName("label_tab3_specImage")
        self.verticalLayout_4.addWidget(self.label_tab3_specImage)
        self.tabWidget.addTab(self.tab_specs, "")
        self.horizontalLayout_3.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1017, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.toolBox_inputOptions.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.lineEdit_inputDir)
        MainWindow.setTabOrder(self.lineEdit_inputDir, self.pushButton_inputDir)
        MainWindow.setTabOrder(self.pushButton_inputDir, self.lineEdit_outputDir)
        MainWindow.setTabOrder(self.lineEdit_outputDir, self.pushButton_outputDir)
        MainWindow.setTabOrder(self.pushButton_outputDir, self.checkBox_setTime)
        MainWindow.setTabOrder(self.checkBox_setTime, self.lineEdit_startTime)
        MainWindow.setTabOrder(self.lineEdit_startTime, self.lineEdit_endTime)
        MainWindow.setTabOrder(self.lineEdit_endTime, self.checkBox_spectrograms)
        MainWindow.setTabOrder(self.checkBox_spectrograms, self.checkBox_deleteClips)
        MainWindow.setTabOrder(self.checkBox_deleteClips, self.checkBox_removeClipped)
        MainWindow.setTabOrder(self.checkBox_removeClipped, self.checkBox_parseFilename)
        MainWindow.setTabOrder(self.checkBox_parseFilename, self.lineEdit_filenameDelimiter)
        MainWindow.setTabOrder(self.lineEdit_filenameDelimiter, self.lineEdit_filenameCategories)
        MainWindow.setTabOrder(self.lineEdit_filenameCategories, self.checkBox_useSilenceFile)
        MainWindow.setTabOrder(self.checkBox_useSilenceFile, self.lineEdit_silenceFile)
        MainWindow.setTabOrder(self.lineEdit_silenceFile, self.pushButton_selectSilenceFile)
        MainWindow.setTabOrder(self.pushButton_selectSilenceFile, self.spinBox_silenceThresh)
        MainWindow.setTabOrder(self.spinBox_silenceThresh, self.spinBox_minSilenceLen)
        MainWindow.setTabOrder(self.spinBox_minSilenceLen, self.spinBox_bufferLen)
        MainWindow.setTabOrder(self.spinBox_bufferLen, self.pushButton_analyze)
        MainWindow.setTabOrder(self.pushButton_analyze, self.listWidget_inputFiles)
        MainWindow.setTabOrder(self.listWidget_inputFiles, self.tableView)
        MainWindow.setTabOrder(self.tableView, self.pushButton_tab3_prev)
        MainWindow.setTabOrder(self.pushButton_tab3_prev, self.comboBox)
        MainWindow.setTabOrder(self.comboBox, self.pushButton_tab3_next)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "Files to be analyzed:"))
        self.pushButton_inputDir.setText(_translate("MainWindow", "Choose Input Directory"))
        self.pushButton_outputDir.setText(_translate("MainWindow", "Choose Output Directory"))
        self.pushButton_analyze.setText(_translate("MainWindow", "Analyze"))
        self.checkBox_spectrograms.setText(_translate("MainWindow", "Generate spectrograms"))
        self.lineEdit_endTime.setText(_translate("MainWindow", "180000"))
        self.label_4.setText(_translate("MainWindow", "End time (ms)"))
        self.lineEdit_startTime.setText(_translate("MainWindow", "120000"))
        self.checkBox_setTime.setText(_translate("MainWindow", "Analyze full file length"))
        self.label_3.setText(_translate("MainWindow", "Start time (ms)"))
        self.checkBox_removeClipped.setText(_translate("MainWindow", "Remove clipped audio"))
        self.checkBox_deleteClips.setText(_translate("MainWindow", "Delete clips after analysis"))
        self.toolBox_inputOptions.setItemText(self.toolBox_inputOptions.indexOf(self.page_ioSettings), _translate("MainWindow", "Input/Output Settings"))
        self.lineEdit_filenameCategories.setText(_translate("MainWindow", "species,parents,litter,pup,postnatal_day,date,time"))
        self.label_6.setText(_translate("MainWindow", "Delimiter character:"))
        self.label_2.setText(_translate("MainWindow", "Comma-separated list of categories:"))
        self.lineEdit_filenameDelimiter.setText(_translate("MainWindow", "_"))
        self.checkBox_parseFilename.setText(_translate("MainWindow", "Parse filename for specimen data?"))
        self.toolBox_inputOptions.setItemText(self.toolBox_inputOptions.indexOf(self.page_fileParsing), _translate("MainWindow", "Filename Parsing"))
        self.checkBox_useSilenceFile.setText(_translate("MainWindow", "Infer silence threshold from file?"))
        self.pushButton_selectSilenceFile.setText(_translate("MainWindow", "Select Silence File"))
        self.label_7.setText(_translate("MainWindow", "Silence Threshold (dBFS)"))
        self.label_8.setText(_translate("MainWindow", "Minimum silence length before segmenting (ms):"))
        self.label_9.setText(_translate("MainWindow", "Buffer length (ms):"))
        self.toolBox_inputOptions.setItemText(self.toolBox_inputOptions.indexOf(self.page_vocalSettings), _translate("MainWindow", "Vocalization Detection Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_input), _translate("MainWindow", "Input"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_output), _translate("MainWindow", "Output"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_output_agg), _translate("MainWindow", "Output (aggregate)"))
        self.label_specInfo_specFilename.setText(_translate("MainWindow", "Spectrogram filename:"))
        self.label_specInfo_sourceFilename.setText(_translate("MainWindow", "Source file:"))
        self.label_specInfo_vocNumber.setText(_translate("MainWindow", "Vocalization number:"))
        self.label_specInfo_classification.setText(_translate("MainWindow", "Classification:"))
        self.label_specInfo_confidence.setText(_translate("MainWindow", "Classification Confidence:"))
        self.pushButton_tab3_prev.setText(_translate("MainWindow", "<- Previous"))
        self.pushButton_tab3_next.setText(_translate("MainWindow", "Next ->"))
        self.label_15.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Manual classification:</span></p></body></html>"))
        self.label_tab3_specImage.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">No spectrograms in output!</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_specs), _translate("MainWindow", "Spectrograms"))

        ### Connecting buttons ###
        # Checkboxes to enable/disable lineedits
        self.checkBox_setTime.toggled.connect(self.lineEdit_startTime.setDisabled)
        self.checkBox_setTime.toggled.connect(self.lineEdit_endTime.setDisabled)
        self.checkBox_parseFilename.toggled.connect(self.lineEdit_filenameDelimiter.setEnabled)
        self.checkBox_parseFilename.toggled.connect(self.lineEdit_filenameCategories.setEnabled)
        self.checkBox_useSilenceFile.toggled.connect(self.lineEdit_silenceFile.setEnabled)
        self.checkBox_useSilenceFile.toggled.connect(self.pushButton_selectSilenceFile.setEnabled)

        # Connect buttons to functions
        self.pushButton_analyze.clicked.connect(self.analyze)
        self.pushButton_inputDir.clicked.connect(self.loadInputDirectory)
        self.pushButton_outputDir.clicked.connect(self.loadOutputDirectory)
        self.pushButton_tab3_next.clicked.connect(self.nextSpectrogram)
        self.pushButton_tab3_prev.clicked.connect(self.prevSpectrogram)
        self.comboBox.activated.connect(self.updateSpectrogramClassification)


    def loadInputDirectory(self):
        self.inputDir = QtWidgets.QFileDialog.getExistingDirectory()
        self.lineEdit_inputDir.setText(self.inputDir)
        self.updateInputFileList()


    def updateInputFileList(self):
        # Clear listWidget of earlier entries
        self.listWidget_inputFiles.clear()
        for file in os.listdir(self.inputDir):
            if file.endswith(".wav"):
                self.listWidget_inputFiles.addItem(file)


    # TODO: Add check that output directory is empty and warn user if not
    def loadOutputDirectory(self):
        self.outputDir = QtWidgets.QFileDialog.getExistingDirectory()
        self.lineEdit_outputDir.setText(self.outputDir)

    # TODO
    def observeProgress(self, func=None):
        pass
    
    def analyze(self):
        # Update application copy of input/output dir (in case user didn't use buttons)
        self.inputDir = self.lineEdit_inputDir.text()
        self.outputDir = self.lineEdit_outputDir.text()
        # Get all user options
        opts = {
            'input_dir': self.inputDir,
            'output_dir': self.outputDir,
            'bool_analyze_full': self.checkBox_setTime.checkState(),
            'start_time': utils.toInt(self.lineEdit_startTime.text()),
            'end_time': utils.toInt(self.lineEdit_endTime.text()),
            'bool_removeClipped': self.checkBox_removeClipped.checkState(),
            'bool_deleteClips': self.checkBox_deleteClips.checkState(),
            'bool_makeSpectrograms': self.checkBox_spectrograms.checkState(),
            'bool_parseFilename': self.checkBox_parseFilename.checkState(),
            'filename_delimiter': self.lineEdit_filenameDelimiter.text(),
            'filename_categories': [s for s in self.lineEdit_filenameCategories.text().split(',')],
            'bool_inferSilence': self.checkBox_useSilenceFile.checkState(),
            'silenceFilename': self.lineEdit_silenceFile.text(),
            'silenceThreshold': self.spinBox_silenceThresh.value(),
            'silenceBuffer': self.spinBox_bufferLen.value(),
            'silenceMinLen': self.spinBox_minSilenceLen.value()
        }
        
        # TODO: Generalize error catching
        try:
            progress = QtWidgets.QProgressDialog("Processing files...", "Abort", 0, len(os.listdir(opts['input_dir'])))
            progress.setWindowModality(QtCore.Qt.WindowModal)
            self.vocBatch = pipeline.pipe(opts)
        except exceptions.TimeBoundError as error:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowModality(QtCore.Qt.WindowModal)
            error_dialog.showMessage(error.error_string())
            error_dialog.exec_()
            return
        except exceptions.FilenameParseError as error:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowModality(QtCore.Qt.WindowModal)
            error_dialog.showMessage(error.error_string())
            error_dialog.exec_()
            return
        except exceptions.NoInputError as error:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowModality(QtCore.Qt.WindowModal)
            error_dialog.showMessage(error.error_string())
            error_dialog.exec_()
            return
        
        self.loadOutputTables(self.lineEdit_outputDir.text())
        if opts['bool_makeSpectrograms']:
            self.loadSpectrograms(opts['output_dir'])


    def loadOutputTables(self, outputDir):
        # Initialize view/model for vocalization table and aggregated table
        tableView, tableModel = self.tableView, outputmodel.OutputTableModel()
        tableAggView, tableAggModel = self.tableAggView, outputmodel.OutputTableModel()

        # Load data into each
        tableModel.loadData(outputDir + '/vocalizations.csv')
        tableView.setModel(tableModel)
        tableAggModel.loadData(outputDir + '/pups.csv')
        tableAggView.setModel(tableAggModel)
        tableView.horizontalHeader().setModel(tableModel)
        tableAggView.horizontalHeader().setModel(tableModel)


    def loadSpectrograms(self, outputDir):
        self._spectrogramIndex = 0

        # Load first spectrogram
        self.updateSpectrogram()

        # Enable next/prev buttons
        self.pushButton_tab3_next.setEnabled(True)
        self.pushButton_tab3_prev.setEnabled(True)


    def updateSpectrogram(self):
        currentVoc = self.vocBatch[self._spectrogramIndex]
        pixmap = QtGui.QPixmap(currentVoc['spectrogram_file'])
        self.label_tab3_specImage.setScaledContents(True)
        self.label_tab3_specImage.setPixmap(pixmap)
        self.label_specInfo_specFilename.setText(f"Spectrogram file: {currentVoc['spectrogram_file']}")
        self.label_specInfo_sourceFilename.setText(f"Source file: {currentVoc['source_file']}")
        self.label_specInfo_vocNumber.setText(f"Vocalization number: {currentVoc['clip_number']}")
        self.label_specInfo_classification.setText(f"Classification: {currentVoc['type_svm']}")
        # Check if vocalization was manually classified and display accordingly
        if currentVoc['svm_confidence']: confidence = currentVoc['svm_confidence']
        else: confidence = "Manually classified"
        self.label_specInfo_confidence.setText(f"Classification confidence: {confidence}")

        self.comboBox.setCurrentIndex(0)


    def nextSpectrogram(self):
        self._spectrogramIndex = (self._spectrogramIndex + 1) % len(self.vocBatch)
        self.updateSpectrogram()


    def prevSpectrogram(self):
        self._spectrogramIndex = (self._spectrogramIndex - 1) % len(self.vocBatch)
        self.updateSpectrogram()


    def updateSpectrogramClassification(self, boxIndex):
        classifications = {
            1: 'sonic',
            2: 'ultrasonic',
            3: 'scratch'
        }
        if boxIndex != 0:
            try:
                df = pd.read_csv(f"{self.outputDir}/vocalizations.csv")
                df.loc[df.index == self._spectrogramIndex, 'type_svm'] = classifications[boxIndex]
                df.loc[df.index == self._spectrogramIndex, 'svm_confidence'] = None
                df.to_csv(f"{self.outputDir}/vocalizations.csv", index=False)

                self.label_specInfo_classification.setText(f"Classification: {classifications[boxIndex]}")
                self.label_specInfo_confidence.setText(f"Classification confidence: Manually classified")

                self.vocBatch[self._spectrogramIndex]['type_svm'] = classifications[boxIndex]
                self.vocBatch[self._spectrogramIndex]['svm_confidence'] = None
            except PermissionError:
                print("Error opening vocalizations.csv. Please close before attempting manual classification.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
