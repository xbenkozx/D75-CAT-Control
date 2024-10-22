import serial, sys, logging, os

from PySide6.QtGui import QIcon
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

        app_icon = QIcon()
        app_icon.addFile(f'./icon.png', QSize(16,16))
        app_icon.addFile(f'./icon.png', QSize(24,24))
        app_icon.addFile(f'./icon.png', QSize(32,32))
        app_icon.addFile(f'./icon.png', QSize(48,48))
        app_icon.addFile(f'./icon.png', QSize(256,256))
        app.setWindowIcon(app_icon)
        
        widget = MainWindow()
        widget.show()
        sys.exit(app.exec())
    except Exception as ex:
        print(ex)