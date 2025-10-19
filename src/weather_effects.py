import random, math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QPointF
from PyQt6.QtGui import QColor, QPainter, QBrush

class WeatherEffect(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.effect = "sunny"
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)

    def initParticles(self):
        w, h = self.width() or 800, self.height() or 600
        if self.effect == "rain":
            self.particles = [(random.randint(0, w), random.randint(-100, h)) for _ in range(120)]
        elif self.effect == "snow":
            self.particles = [(random.randint(0, w), random.randint(-100, h)) for _ in range(80)]
        elif self.effect == "cloudy":
            self.particles = [(random.randint(0, w), random.randint(0, h)) for _ in range(12)]
        else:
            self.particles = [(random.randint(0, w), random.randint(0, h)) for _ in range(10)]

    def animate(self):
        w, h = self.width(), self.height()
        if self.effect == "rain":
            self.particles = [(x, y + 10 if y < h else random.randint(0, w)) for x, y in self.particles]
        elif self.effect == "snow":
            self.particles = [(x + random.uniform(-0.8, 0.8), y + 2)
                              if y < h else (random.randint(0, w), -10) for x, y in self.particles]
        elif self.effect == "cloudy":
            self.particles = [((x + random.uniform(0.1, 0.3)) % w, 
                       (y + random.uniform(-0.1, 0.1)) % h) for x, y in self.particles]
        self.update()

    def paintEvent(self, event):
        if not self.particles:
            return
        painter = QPainter(self)
        painter.setOpacity(0.7)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.effect == "rain":
            painter.setPen(QColor(180, 220, 250, 200))
            for x, y in self.particles:
                painter.drawLine(x, y, x - 2, y + 12)
        elif self.effect == "snow":
            painter.setBrush(QBrush(QColor(255, 255, 255, 230)))
            painter.setPen(Qt.PenStyle.NoPen)
            for x, y in self.particles:
                painter.drawEllipse(QPointF(x, y), 2.3, 2.3)
        elif self.effect == "cloudy":
            for x, y in self.particles:
                painter.setBrush(QBrush(QColor(230, 230, 240, 210)))
                painter.drawEllipse(QPointF(x, y), 70, 30)
                painter.setBrush(QBrush(QColor(220, 220, 230, 180)))
                painter.drawEllipse(QPointF(x + 35, y - 10), 50, 25)
                painter.setBrush(QBrush(QColor(225, 225, 235, 190)))
                painter.drawEllipse(QPointF(x - 25, y + 8), 40, 20)
        elif self.effect == "sunny":
            painter.setBrush(QBrush(QColor(255, 255, 180, 220)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(80, 80), 40, 40)
            for i in range(12):
                angle = i * 30
                rad = math.radians(angle)
                x1, y1 = 80 + 45 * math.cos(rad), 80 + 45 * math.sin(rad)
                x2, y2 = 80 + 70 * math.cos(rad), 80 + 70 * math.sin(rad)
                painter.setPen(QColor(255, 255, 200, 180))
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def showEvent(self, event):
        super().showEvent(event)
        self.initParticles()
