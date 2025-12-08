from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QPlainTextEdit

class LimitedPlainTextEdit(QPlainTextEdit):
    """QPlainTextEdit that enforces a maximum character length on insert and paste.

    This prevents typing or pasting more than `max_length` characters.
    """
    def __init__(self, max_length: int = 300, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = int(max_length)

    def insertPlainText(self, text: str) -> None:
        cur = self.toPlainText()
        # account for selected text which will be replaced
        cursor = self.textCursor()
        sel_len = len(cursor.selectedText()) if cursor is not None else 0
        allowed = self.max_length - (len(cur) - sel_len)
        if allowed <= 0:
            return
        if len(text) > allowed:
            text = text[:allowed]
        super().insertPlainText(text)

    def insertFromMimeData(self, source) -> None:
        # handle paste operations
        try:
            text = source.text()
        except Exception:
            text = ''
        cur = self.toPlainText()
        cursor = self.textCursor()
        sel_len = len(cursor.selectedText()) if cursor is not None else 0
        allowed = self.max_length - (len(cur) - sel_len)
        if allowed <= 0:
            return
        if len(text) > allowed:
            text = text[:allowed]
        md = QtCore.QMimeData()
        md.setText(text)
        super().insertFromMimeData(md)

    def keyPressEvent(self, event):
        # Allow navigation and editing keys (so backspace/delete still work)
        key = event.key()
        navigation_keys = {
            QtCore.Qt.Key_Backspace,
            QtCore.Qt.Key_Delete,
            QtCore.Qt.Key_Left,
            QtCore.Qt.Key_Right,
            QtCore.Qt.Key_Home,
            QtCore.Qt.Key_End,
            QtCore.Qt.Key_Up,
            QtCore.Qt.Key_Down,
            QtCore.Qt.Key_PageUp,
            QtCore.Qt.Key_PageDown,
        }
        if key in navigation_keys:
            return super().keyPressEvent(event)

        # Allow common shortcuts (Ctrl+C/X/V/A/Z/Y etc.) to be handled normally
        if event.modifiers() & (QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier):
            return super().keyPressEvent(event)

        # For printable input, enforce the remaining allowed characters (accounting for selection)
        text = event.text()
        if not text:
            return super().keyPressEvent(event)

        cur = self.toPlainText()
        cursor = self.textCursor()
        sel_len = len(cursor.selectedText()) if cursor is not None else 0
        allowed = self.max_length - (len(cur) - sel_len)
        if allowed <= 0:
            # nothing allowed — ignore printable input
            return
        if len(text) > allowed:
            # insert truncated text
            self.insertPlainText(text[:allowed])
            return

        return super().keyPressEvent(event)