import math

from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        font.setBold(True)
        self.setMinimumSize(75, 75)
        self.setFont(font)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '÷'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N', '0', '.', '='],
        ]

        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._left = None  # type:ignore
        self._right = None
        self._operator = None

        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._equal)
        self.display.delPressed.connect(self._backspace)
        self.display.escPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)
        self.display.negativePressed.connect(self._negativeNumber)

        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, i, j)

                buttonSlot = self._makeSlot(
                    self._insertToDisplay,
                    buttonText,
                )
                self._connectButtonClicked(button, buttonSlot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        elif text in '+-÷x^':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._configLeftOp, text)
            )

        elif text == '=':
            self._connectButtonClicked(button, self._equal)

        elif text == '◀':
            self._connectButtonClicked(button, self._backspace)

        elif text == 'N':
            self._connectButtonClicked(button, self._negativeNumber)

    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _negativeNumber(self, text):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        text = -float(displayText)
        self.display.setText(str(text))
        self.display.setFocus()

    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._operator = None
        self.equation = ''
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Valor inválido')
            return

        elif self._left is None:
            self._left = float(displayText)

        self._operator = text
        self.equation = f'{self._left} {self._operator}'
        self.display.setFocus()

    @Slot()
    def _equal(self):
        displayText = self.display.text()
        result = 'Error'

        if not isValidNumber(displayText) or self._left is None:
            self._showInfo('Você não digitou um dos valores.')
            return

        self._left: float  # type:ignore
        self._right = float(displayText)
        self.equation = f'{self._left} {self._operator} {self._right}'

        if self._operator == 'x':
            result = self._left * self._right
            self.display.setFocus()

        if self._operator == '÷':
            try:
                result = self._left / self._right
                self.display.setFocus()
            except ZeroDivisionError:
                self._showError('Não existe divisão por 0.')

        if self._operator == '^':
            try:
                result = math.pow(self._left, self._right)
                self.display.setFocus()
            except OverflowError:
                self._showInfo('O resultado é muito grande.')

        if self._operator == '+' or self._operator == '-':
            result = eval(self.equation)
            self.display.setFocus()

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result  # type:ignore
        self._right = None
        self.display.setFocus()

        if result == 'Error':
            self._left = None  # type:ignore

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()
