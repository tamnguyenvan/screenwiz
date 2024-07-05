from PySide6.QtCore import QObject, QSize, QPointF, QPropertyAnimation, QEasingCurve, Property, Slot, Qt
from PySide6.QtGui import  QPainter, QPalette, QLinearGradient, QGradient, QColor, QPen
from PySide6.QtWidgets import QAbstractButton, QApplication, QWidget, QHBoxLayout, QLabel


class SwitchPrivate(QObject):
    def __init__(self, q, parent=None):
        QObject.__init__(self, parent=parent)
        self.mPointer = q
        self.mPosition = 0.0
        self.mGradient = QLinearGradient()
        self.mGradient.setSpread(QGradient.PadSpread)

        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b'position')
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.animation.finished.connect(self.mPointer.update)

        self.enabled = False

    @Property(float)
    def position(self):
        return self.mPosition

    @position.setter
    def position(self, value):
        self.mPosition = value
        self.mPointer.update()

    def draw(self, painter):
        r = self.mPointer.rect()
        margin = r.height()/6
        shadow = self.mPointer.palette().color(QPalette.Dark)
        light = self.mPointer.palette().color(QPalette.Light)
        button = self.mPointer.palette().color(QPalette.Button)
        enabled_color = QColor('#4f46e5')
        painter.setPen(Qt.NoPen)

        if self.mPosition < 0.7:
            self.mGradient.setColorAt(0, 'darkgray')
            self.mGradient.setColorAt(1, 'darkgray')
        else:
            self.mGradient.setColorAt(0, enabled_color)
            self.mGradient.setColorAt(1, enabled_color)
        self.mGradient.setStart(0, r.height())
        self.mGradient.setFinalStop(0, 0)
        painter.setBrush(self.mGradient)
        painter.drawRoundedRect(r, r.height()/2, r.height()/2)

        # outline_color = QColor('darkgray')
        # outline_width = 2
        # painter.setPen(QPen(outline_color, outline_width))
        # painter.setBrush(Qt.NoBrush)
        # painter.drawRoundedRect(r, r.height() / 2, r.height() / 2)

        if self.mPosition < 0.7:
            self.mGradient.setColorAt(0, shadow.darker(140))
            self.mGradient.setColorAt(1, light.darker(160))
        else:
            self.mGradient.setColorAt(0, enabled_color)
            self.mGradient.setColorAt(1, enabled_color)
        self.mGradient.setStart(0, 0)
        self.mGradient.setFinalStop(0, r.height())
        painter.setBrush(self.mGradient)
        margin_ = 2
        painter.drawRoundedRect(r.adjusted(margin_, margin_, -margin_, -margin_), r.height()/2, r.height()/2)


        x = r.height()/2.0 + self.mPosition*(r.width()-r.height())
        if self.mPosition < 0.7:
            self.mGradient.setColorAt(0, 'darkgray')
            self.mGradient.setColorAt(1, 'darkgray')
        else:
            self.mGradient.setColorAt(0, 'black')
            self.mGradient.setColorAt(1, 'black')
        painter.setBrush(self.mGradient)

        painter.drawEllipse(QPointF(x, r.height()/2), r.height()/2-margin, r.height()/2-margin)

    @Slot(bool, name='animate')
    def animate(self, checked):
        self.enabled = not self.enabled
        self.animation.setDirection(QPropertyAnimation.Forward if checked else QPropertyAnimation.Backward)
        self.animation.start()


class SWSwitch(QAbstractButton):
    def __init__(self, checked=False, parent=None):
        QAbstractButton.__init__(self, parent=parent)
        self.dPtr = SwitchPrivate(self)
        self.setCheckable(True)
        self.clicked.connect(self.dPtr.animate)

        if checked:
            self.clicked.emit()

    def sizeHint(self):
        return QSize(84, 42)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.dPtr.draw(painter)

    def resizeEvent(self, event):
        self.update()
