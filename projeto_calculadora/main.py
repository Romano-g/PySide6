import sys

from main_window import MainWindow
from display import Display
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from info import Info
from variables import ICON_PATH
from styles import setupTheme
from buttons import ButtonsGrid

if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()
    icon = QIcon(str(ICON_PATH))

    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    info = Info()
    window.addWidgetToVLayout(info)

    display = Display()
    display.setPlaceholderText('0')
    window.addWidgetToVLayout(display)

    buttonsGrid = ButtonsGrid(display, info, window)
    window.mainLayout.addLayout(buttonsGrid)

    window.adjustFixedSize()
    window.show()
    app.exec()
