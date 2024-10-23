#!/usr/bin/env python3
"""
File name d75_cat_control.py:
Project Name: D75 CAT Control
Author: Ben Kozlowski - K7DMG
Created: 2024-10-22
Version: 1.0.0
Description: 
    CAT Control Software for the Kenwood D75/D75

License: 
    This file is part of D75 CAT Control.

D75 CAT Control is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

D75 CAT Control is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details.

    You should have received a copy of the GNU General Public License along with D75 CAT Control. If not, see <https://www.gnu.org/licenses/>.
Contact: k7dmg@protonmail.com
Dependencies: PySide6==6.7.1, PySide6_Addons==6.7.1, PySide6_Essentials==6.7.1
"""

import sys, logging
from PySide6.QtGui import QIcon, QPalette
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication
from UI.MainWindow import MainWindow

# os.chdir(sys.path[0])
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        FORMAT = '%(asctime)s %(message)s'
        logging.basicConfig(filename='connection.log', level=logging.INFO, format=FORMAT)
        app = QApplication(sys.argv)

        is_dark_mode = app.palette().color(QPalette.Window).lightness() < 128

        app_icon = QIcon()
        app_icon.addFile(f'./icon.png', QSize(16,16))
        app_icon.addFile(f'./icon.png', QSize(24,24))
        app_icon.addFile(f'./icon.png', QSize(32,32))
        app_icon.addFile(f'./icon.png', QSize(48,48))
        app_icon.addFile(f'./icon.png', QSize(256,256))
        app.setWindowIcon(app_icon)
        
        widget = MainWindow()
        widget.is_dark_mode = is_dark_mode
        widget.show()
        sys.exit(app.exec())
    except Exception as ex:
        print(ex)