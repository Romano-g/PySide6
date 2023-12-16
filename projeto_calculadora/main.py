import sys

from main_window import MainWindow
from display import Display
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from info import Info
from variables import ICON_PATH
from styles import setupTheme

if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()
    icon = QIcon(str(ICON_PATH))

    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    info = Info('Label')
    window.addWidgetToLayout(info)

    display = Display()
    display.setPlaceholderText('0')
    window.addWidgetToLayout(display)

    window.adjustFixedSize()
    window.show()
    app.exec()
