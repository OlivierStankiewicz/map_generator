from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QLabel

from PySide6.QtGui import QPainter, QPainterPath, QPen, QColor, QFontMetrics

class OutlinedLabel(QLabel):
    """QLabel that draws a hard outline around the text using QPainterPath.

    This produces a solid sharp border (miter join) around the text rather
    than a soft blurred shadow.
    """
    def __init__(self, *args, outline_width: int = 2, outline_color: str = 'black', **kwargs):
        super().__init__(*args, **kwargs)
        self._outline_width = int(outline_width)
        self._outline_color = QColor(outline_color)

    def paintEvent(self, event):
        text = self.text() or ''
        if not text:
            return super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        font = self.font()
        fm = QFontMetrics(font)
        rect = self.rect()

        # Compute coordinates for left-aligned, vertically centered text
        tw = fm.horizontalAdvance(text)
        th = fm.height()
        x = 0
        y = int((rect.height() + fm.ascent() - fm.descent()) / 2)

        path = QPainterPath()
        path.addText(x, y, font, text)

        pen = QPen(self._outline_color)
        pen.setWidth(self._outline_width)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        painter.setPen(pen)
        painter.drawPath(path)

        # draw filled text on top using the widget's palette/stylesheet color
        # Use drawText to respect alignment and eliding behavior
        painter.setPen(self.palette().color(self.foregroundRole()))
        painter.drawText(rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)

        painter.end()