# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'com_port_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ComPortDialog(object):
    def setupUi(self, ComPortDialog):
        if not ComPortDialog.objectName():
            ComPortDialog.setObjectName(u"ComPortDialog")
        ComPortDialog.resize(400, 118)
        self.horizontalLayout = QHBoxLayout(ComPortDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.widget = QWidget(ComPortDialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.portCbx = QComboBox(self.widget)
        self.portCbx.setObjectName(u"portCbx")
        self.portCbx.setMinimumSize(QSize(200, 0))

        self.verticalLayout.addWidget(self.portCbx)

        self.connectBtn = QPushButton(self.widget)
        self.connectBtn.setObjectName(u"connectBtn")

        self.verticalLayout.addWidget(self.connectBtn)


        self.horizontalLayout.addWidget(self.widget)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.retranslateUi(ComPortDialog)

        QMetaObject.connectSlotsByName(ComPortDialog)
    # setupUi

    def retranslateUi(self, ComPortDialog):
        ComPortDialog.setWindowTitle(QCoreApplication.translate("ComPortDialog", u"Com Port", None))
        self.portCbx.setPlaceholderText(QCoreApplication.translate("ComPortDialog", u"Select Port...", None))
        self.connectBtn.setText(QCoreApplication.translate("ComPortDialog", u"Connect", None))
    # retranslateUi

