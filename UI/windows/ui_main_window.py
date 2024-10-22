# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QStatusBar, QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(862, 429)
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.actionPort = QAction(MainWindow)
        self.actionPort.setObjectName(u"actionPort")
        self.actionConnect = QAction(MainWindow)
        self.actionConnect.setObjectName(u"actionConnect")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_7 = QWidget(self.centralwidget)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, 0, 6, 0)
        self.widget_10 = QWidget(self.widget_7)
        self.widget_10.setObjectName(u"widget_10")
        self.verticalLayout_8 = QVBoxLayout(self.widget_10)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.bandControlCbx = QComboBox(self.widget_10)
        self.bandControlCbx.setObjectName(u"bandControlCbx")
        self.bandControlCbx.setMinimumSize(QSize(100, 0))

        self.verticalLayout_8.addWidget(self.bandControlCbx)

        self.bandCbx = QComboBox(self.widget_10)
        self.bandCbx.setObjectName(u"bandCbx")
        font = QFont()
        font.setPointSize(9)
        self.bandCbx.setFont(font)
        self.bandCbx.setModelColumn(0)

        self.verticalLayout_8.addWidget(self.bandCbx)

        self.radioUpdateChbx = QCheckBox(self.widget_10)
        self.radioUpdateChbx.setObjectName(u"radioUpdateChbx")

        self.verticalLayout_8.addWidget(self.radioUpdateChbx)


        self.horizontalLayout_3.addWidget(self.widget_10)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.txBtn = QPushButton(self.widget_7)
        self.txBtn.setObjectName(u"txBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txBtn.sizePolicy().hasHeightForWidth())
        self.txBtn.setSizePolicy(sizePolicy)
        self.txBtn.setMinimumSize(QSize(0, 50))
        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(True)
        self.txBtn.setFont(font1)
        self.txBtn.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.txBtn)

        self.widget_27 = QWidget(self.widget_7)
        self.widget_27.setObjectName(u"widget_27")
        self.verticalLayout_20 = QVBoxLayout(self.widget_27)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.upBtn = QPushButton(self.widget_27)
        self.upBtn.setObjectName(u"upBtn")

        self.verticalLayout_20.addWidget(self.upBtn)

        self.dwnBtn = QPushButton(self.widget_27)
        self.dwnBtn.setObjectName(u"dwnBtn")

        self.verticalLayout_20.addWidget(self.dwnBtn)


        self.horizontalLayout_3.addWidget(self.widget_27)

        self.widget_4 = QWidget(self.widget_7)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_8 = QWidget(self.widget_4)
        self.widget_8.setObjectName(u"widget_8")
        self.verticalLayout_6 = QVBoxLayout(self.widget_8)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label = QLabel(self.widget_8)
        self.label.setObjectName(u"label")

        self.verticalLayout_6.addWidget(self.label)

        self.volumeSlider = QSlider(self.widget_8)
        self.volumeSlider.setObjectName(u"volumeSlider")
        self.volumeSlider.setMinimum(6)
        self.volumeSlider.setMaximum(193)
        self.volumeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout_6.addWidget(self.volumeSlider)


        self.verticalLayout_3.addWidget(self.widget_8)

        self.widget_5 = QWidget(self.widget_4)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, 0)
        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_10.addWidget(self.label_3)

        self.backlightCbx = QComboBox(self.widget_5)
        self.backlightCbx.setObjectName(u"backlightCbx")

        self.horizontalLayout_10.addWidget(self.backlightCbx)

        self.btEnabledChbx = QCheckBox(self.widget_5)
        self.btEnabledChbx.setObjectName(u"btEnabledChbx")

        self.horizontalLayout_10.addWidget(self.btEnabledChbx)

        self.gpsEnabledChbx = QCheckBox(self.widget_5)
        self.gpsEnabledChbx.setObjectName(u"gpsEnabledChbx")

        self.horizontalLayout_10.addWidget(self.gpsEnabledChbx)

        self.gpsPcOutChbx = QCheckBox(self.widget_5)
        self.gpsPcOutChbx.setObjectName(u"gpsPcOutChbx")

        self.horizontalLayout_10.addWidget(self.gpsPcOutChbx)


        self.verticalLayout_3.addWidget(self.widget_5)

        self.label_2 = QLabel(self.widget_4)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.widget_6 = QWidget(self.widget_4)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_11 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.tncModeCbx = QComboBox(self.widget_6)
        self.tncModeCbx.setObjectName(u"tncModeCbx")

        self.horizontalLayout_11.addWidget(self.tncModeCbx)

        self.tncBandCbx = QComboBox(self.widget_6)
        self.tncBandCbx.setObjectName(u"tncBandCbx")

        self.horizontalLayout_11.addWidget(self.tncBandCbx)

        self.beaconCbx = QComboBox(self.widget_6)
        self.beaconCbx.setObjectName(u"beaconCbx")

        self.horizontalLayout_11.addWidget(self.beaconCbx)


        self.verticalLayout_3.addWidget(self.widget_6)


        self.horizontalLayout_3.addWidget(self.widget_4)


        self.verticalLayout.addWidget(self.widget_7)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.widget_12 = QWidget(self.centralwidget)
        self.widget_12.setObjectName(u"widget_12")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.bandAWidget = QWidget(self.widget_12)
        self.bandAWidget.setObjectName(u"bandAWidget")
        self.verticalLayout_15 = QVBoxLayout(self.bandAWidget)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label_5 = QLabel(self.bandAWidget)
        self.label_5.setObjectName(u"label_5")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.label_5.setFont(font2)

        self.verticalLayout_15.addWidget(self.label_5)

        self.widget_3 = QWidget(self.bandAWidget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.bandAMeter = QProgressBar(self.widget_3)
        self.bandAMeter.setObjectName(u"bandAMeter")
        self.bandAMeter.setMinimumSize(QSize(0, 15))
        self.bandAMeter.setBaseSize(QSize(0, 15))
        self.bandAMeter.setStyleSheet(u"")
        self.bandAMeter.setMaximum(5)
        self.bandAMeter.setValue(0)
        self.bandAMeter.setTextVisible(False)

        self.horizontalLayout_9.addWidget(self.bandAMeter)

        self.bandASquelchCbx = QComboBox(self.widget_3)
        self.bandASquelchCbx.setObjectName(u"bandASquelchCbx")

        self.horizontalLayout_9.addWidget(self.bandASquelchCbx)

        self.bandAMonitorBtn = QToolButton(self.widget_3)
        self.bandAMonitorBtn.setObjectName(u"bandAMonitorBtn")
        self.bandAMonitorBtn.setMinimumSize(QSize(25, 25))
        self.bandAMonitorBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.bandAMonitorBtn.setAutoRaise(True)

        self.horizontalLayout_9.addWidget(self.bandAMonitorBtn)


        self.verticalLayout_15.addWidget(self.widget_3)

        self.widget_21 = QWidget(self.bandAWidget)
        self.widget_21.setObjectName(u"widget_21")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_21)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.widget_22 = QWidget(self.widget_21)
        self.widget_22.setObjectName(u"widget_22")
        self.verticalLayout_16 = QVBoxLayout(self.widget_22)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.widget_22)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bandAChannelLbl = QLabel(self.widget)
        self.bandAChannelLbl.setObjectName(u"bandAChannelLbl")
        self.bandAChannelLbl.setMaximumSize(QSize(16777215, 25))
        self.bandAChannelLbl.setFont(font2)

        self.horizontalLayout.addWidget(self.bandAChannelLbl)

        self.bandAChannelCbx = QComboBox(self.widget)
        self.bandAChannelCbx.setObjectName(u"bandAChannelCbx")
        self.bandAChannelCbx.setMinimumSize(QSize(100, 0))
        self.bandAChannelCbx.setEditable(True)

        self.horizontalLayout.addWidget(self.bandAChannelCbx)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_16.addWidget(self.widget)

        self.widget_23 = QWidget(self.widget_22)
        self.widget_23.setObjectName(u"widget_23")
        self.widget_23.setMinimumSize(QSize(20, 0))
        self.horizontalLayout_7 = QHBoxLayout(self.widget_23)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.bandAFreqText = QLineEdit(self.widget_23)
        self.bandAFreqText.setObjectName(u"bandAFreqText")
        self.bandAFreqText.setMaximumSize(QSize(150, 16777215))
        font3 = QFont()
        font3.setPointSize(24)
        font3.setBold(True)
        self.bandAFreqText.setFont(font3)
        self.bandAFreqText.setMaxLength(7)
        self.bandAFreqText.setFrame(True)
        self.bandAFreqText.setCursorPosition(7)
        self.bandAFreqText.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_7.addWidget(self.bandAFreqText)

        self.freq_ch_label_3 = QLabel(self.widget_23)
        self.freq_ch_label_3.setObjectName(u"freq_ch_label_3")
        font4 = QFont()
        font4.setPointSize(24)
        self.freq_ch_label_3.setFont(font4)

        self.horizontalLayout_7.addWidget(self.freq_ch_label_3)


        self.verticalLayout_16.addWidget(self.widget_23)


        self.horizontalLayout_6.addWidget(self.widget_22)

        self.widget_24 = QWidget(self.widget_21)
        self.widget_24.setObjectName(u"widget_24")
        self.verticalLayout_17 = QVBoxLayout(self.widget_24)
        self.verticalLayout_17.setSpacing(2)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(9, 0, 0, 0)
        self.bandAPwrCbx = QComboBox(self.widget_24)
        self.bandAPwrCbx.setObjectName(u"bandAPwrCbx")

        self.verticalLayout_17.addWidget(self.bandAPwrCbx)

        self.bandAMemoryModeCbx = QComboBox(self.widget_24)
        self.bandAMemoryModeCbx.setObjectName(u"bandAMemoryModeCbx")

        self.verticalLayout_17.addWidget(self.bandAMemoryModeCbx)

        self.bandAModeCbx = QComboBox(self.widget_24)
        self.bandAModeCbx.setObjectName(u"bandAModeCbx")

        self.verticalLayout_17.addWidget(self.bandAModeCbx)


        self.horizontalLayout_6.addWidget(self.widget_24)

        self.widget_25 = QWidget(self.widget_21)
        self.widget_25.setObjectName(u"widget_25")
        self.verticalLayout_18 = QVBoxLayout(self.widget_25)
        self.verticalLayout_18.setSpacing(2)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_6.addWidget(self.widget_25)

        self.widget_26 = QWidget(self.widget_21)
        self.widget_26.setObjectName(u"widget_26")
        self.verticalLayout_19 = QVBoxLayout(self.widget_26)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")

        self.horizontalLayout_6.addWidget(self.widget_26)


        self.verticalLayout_15.addWidget(self.widget_21)


        self.horizontalLayout_8.addWidget(self.bandAWidget)

        self.bandBWidget = QWidget(self.widget_12)
        self.bandBWidget.setObjectName(u"bandBWidget")
        self.verticalLayout_2 = QVBoxLayout(self.bandBWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.bandBWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)

        self.verticalLayout_2.addWidget(self.label_4)

        self.widget_9 = QWidget(self.bandBWidget)
        self.widget_9.setObjectName(u"widget_9")
        self.horizontalLayout_12 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.bandBMeter = QProgressBar(self.widget_9)
        self.bandBMeter.setObjectName(u"bandBMeter")
        self.bandBMeter.setMinimumSize(QSize(0, 15))
        self.bandBMeter.setMaximum(5)
        self.bandBMeter.setValue(0)
        self.bandBMeter.setTextVisible(False)

        self.horizontalLayout_12.addWidget(self.bandBMeter)

        self.bandBSquelchCbx = QComboBox(self.widget_9)
        self.bandBSquelchCbx.setObjectName(u"bandBSquelchCbx")

        self.horizontalLayout_12.addWidget(self.bandBSquelchCbx)

        self.bandBMonitorBtn = QToolButton(self.widget_9)
        self.bandBMonitorBtn.setObjectName(u"bandBMonitorBtn")
        self.bandBMonitorBtn.setMinimumSize(QSize(25, 25))
        self.bandBMonitorBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.bandBMonitorBtn.setAutoRaise(True)

        self.horizontalLayout_12.addWidget(self.bandBMonitorBtn)


        self.verticalLayout_2.addWidget(self.widget_9)

        self.widget_14 = QWidget(self.bandBWidget)
        self.widget_14.setObjectName(u"widget_14")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_14)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_15 = QWidget(self.widget_14)
        self.widget_15.setObjectName(u"widget_15")
        self.verticalLayout_11 = QVBoxLayout(self.widget_15)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.widget_15)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.bandBChannelLbl = QLabel(self.widget_2)
        self.bandBChannelLbl.setObjectName(u"bandBChannelLbl")
        self.bandBChannelLbl.setMaximumSize(QSize(16777215, 25))
        self.bandBChannelLbl.setFont(font2)

        self.horizontalLayout_2.addWidget(self.bandBChannelLbl)

        self.bandBChannelCbx = QComboBox(self.widget_2)
        self.bandBChannelCbx.setObjectName(u"bandBChannelCbx")
        self.bandBChannelCbx.setMinimumSize(QSize(100, 0))
        self.bandBChannelCbx.setEditable(True)

        self.horizontalLayout_2.addWidget(self.bandBChannelCbx)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout_11.addWidget(self.widget_2)

        self.widget_16 = QWidget(self.widget_15)
        self.widget_16.setObjectName(u"widget_16")
        self.widget_16.setMinimumSize(QSize(20, 0))
        self.horizontalLayout_5 = QHBoxLayout(self.widget_16)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.bandBFreqText = QLineEdit(self.widget_16)
        self.bandBFreqText.setObjectName(u"bandBFreqText")
        self.bandBFreqText.setMaximumSize(QSize(150, 16777215))
        self.bandBFreqText.setFont(font3)
        self.bandBFreqText.setMaxLength(7)
        self.bandBFreqText.setFrame(True)
        self.bandBFreqText.setCursorPosition(7)
        self.bandBFreqText.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.bandBFreqText)

        self.freq_ch_label_2 = QLabel(self.widget_16)
        self.freq_ch_label_2.setObjectName(u"freq_ch_label_2")
        self.freq_ch_label_2.setFont(font4)

        self.horizontalLayout_5.addWidget(self.freq_ch_label_2)


        self.verticalLayout_11.addWidget(self.widget_16)


        self.horizontalLayout_4.addWidget(self.widget_15)

        self.widget_17 = QWidget(self.widget_14)
        self.widget_17.setObjectName(u"widget_17")
        self.verticalLayout_12 = QVBoxLayout(self.widget_17)
        self.verticalLayout_12.setSpacing(2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(9, 0, 0, 0)
        self.bandBPwrCbx = QComboBox(self.widget_17)
        self.bandBPwrCbx.setObjectName(u"bandBPwrCbx")

        self.verticalLayout_12.addWidget(self.bandBPwrCbx)

        self.bandBMemoryModeCbx = QComboBox(self.widget_17)
        self.bandBMemoryModeCbx.setObjectName(u"bandBMemoryModeCbx")

        self.verticalLayout_12.addWidget(self.bandBMemoryModeCbx)

        self.bandBModeCbx = QComboBox(self.widget_17)
        self.bandBModeCbx.setObjectName(u"bandBModeCbx")

        self.verticalLayout_12.addWidget(self.bandBModeCbx)


        self.horizontalLayout_4.addWidget(self.widget_17)

        self.widget_18 = QWidget(self.widget_14)
        self.widget_18.setObjectName(u"widget_18")
        self.verticalLayout_13 = QVBoxLayout(self.widget_18)
        self.verticalLayout_13.setSpacing(2)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_4.addWidget(self.widget_18)

        self.widget_19 = QWidget(self.widget_14)
        self.widget_19.setObjectName(u"widget_19")
        self.verticalLayout_14 = QVBoxLayout(self.widget_19)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")

        self.horizontalLayout_4.addWidget(self.widget_19)


        self.verticalLayout_2.addWidget(self.widget_14)


        self.horizontalLayout_8.addWidget(self.bandBWidget)


        self.verticalLayout.addWidget(self.widget_12)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 862, 17))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuRadio = QMenu(self.menubar)
        self.menuRadio.setObjectName(u"menuRadio")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRadio.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuRadio.addAction(self.actionPort)
        self.menuRadio.addAction(self.actionConnect)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"D74/75 CAT Control Software", None))
        self.actionPort.setText(QCoreApplication.translate("MainWindow", u"Port...", None))
        self.actionConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.bandControlCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Dual Band", None))
        self.bandCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Band A", None))
        self.radioUpdateChbx.setText(QCoreApplication.translate("MainWindow", u"Auto Update", None))
        self.txBtn.setText(QCoreApplication.translate("MainWindow", u"TX", None))
        self.upBtn.setText(QCoreApplication.translate("MainWindow", u"\u25b2", None))
        self.dwnBtn.setText(QCoreApplication.translate("MainWindow", u"\u25bc", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Volume Level", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Backlight", None))
        self.backlightCbx.setCurrentText("")
        self.backlightCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Off", None))
        self.btEnabledChbx.setText(QCoreApplication.translate("MainWindow", u"BT", None))
        self.gpsEnabledChbx.setText(QCoreApplication.translate("MainWindow", u"GPS", None))
        self.gpsPcOutChbx.setText(QCoreApplication.translate("MainWindow", u"GPS PC", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TNC", None))
        self.tncModeCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Off", None))
        self.tncBandCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Band A", None))
        self.beaconCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Band A", None))
        self.bandAMonitorBtn.setText(QCoreApplication.translate("MainWindow", u"MONI", None))
        self.bandAChannelLbl.setText(QCoreApplication.translate("MainWindow", u"Ch:", None))
        self.bandAFreqText.setText(QCoreApplication.translate("MainWindow", u"147.520", None))
        self.freq_ch_label_3.setText(QCoreApplication.translate("MainWindow", u"Mhz", None))
        self.bandAPwrCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"EL", None))
        self.bandAMemoryModeCbx.setCurrentText("")
        self.bandAMemoryModeCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"VFO", None))
        self.bandAModeCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"FM", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Band B", None))
        self.bandBMonitorBtn.setText(QCoreApplication.translate("MainWindow", u"MONI", None))
        self.bandBChannelLbl.setText(QCoreApplication.translate("MainWindow", u"Ch:", None))
        self.bandBFreqText.setText(QCoreApplication.translate("MainWindow", u"147.520", None))
        self.freq_ch_label_2.setText(QCoreApplication.translate("MainWindow", u"Mhz", None))
        self.bandBPwrCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"EL", None))
        self.bandBMemoryModeCbx.setCurrentText("")
        self.bandBMemoryModeCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"VFO", None))
        self.bandBModeCbx.setPlaceholderText(QCoreApplication.translate("MainWindow", u"FM", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuRadio.setTitle(QCoreApplication.translate("MainWindow", u"Radio", None))
    # retranslateUi

