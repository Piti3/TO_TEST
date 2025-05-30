from PyQt6.QtWidgets import QCalendarWidget
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QBrush, QPainter, QColor

class MarkedCalendar(QCalendarWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.marked_dates = set()

    def paintCell(self, painter: QPainter, rect: QRect, date):
        super().paintCell(painter, rect, date)

        py_date = date.toPyDate()
        if py_date in self.marked_dates:
            color = QColor(255, 255, 0, 80)
            painter.save()
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(rect)
            painter.restore()

            painter.save()
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(
                rect,
                Qt.AlignmentFlag.AlignCenter,
                str(date.day())
            )
            painter.restore()
