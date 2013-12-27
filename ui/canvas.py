import random

from PySide import QtCore, QtGui

class Canvas(QtGui.QWidget):
    def __init__(self):
        super(Canvas, self).__init__()
        self.setMouseTracking(True)
        self.setGeometry(0, 900/4, 1440/2, 900/2)
        self.setWindowTitle("Antimony")

        self.center = QtCore.QPointF(0, 0)
        self.scale = 10.0 # scale is measured in pixels/mm

        self.dragging = False
        self.mouse_pos = QtCore.QPointF(self.width()/2, self.height()/2)

        self.scatter_points(2)
        self.make_circle()
        self.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_pos = event.pos()
            self.dragging = True

    def mouseMoveEvent(self, event):
        p = event.pos()
        if self.dragging:
            delta = p - self.mouse_pos
            self.drag(-delta.x() / self.scale, delta.y() / self.scale)
        self.mouse_pos = p

    def wheelEvent(self, event):
        pos = self.pixel_to_mm(self.mouse_pos.x(), self.mouse_pos.y())
        factor = 1.001 if event.delta() > 0 else 1/1.001
        for d in range(abs(event.delta())):
            self.scale *= factor
        new_pos = self.pixel_to_mm(self.mouse_pos.x(), self.mouse_pos.y())
        self.center += QtCore.QPointF(*pos) - QtCore.QPointF(*new_pos)
        self.sync_all_children()
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False

    def drag(self, dx, dy):
        self.center += QtCore.QPointF(dx, dy)
        self.update()
        self.sync_all_children()

    def paintEvent(self, paintEvent):
        painter = QtGui.QPainter(self)
        painter.setBackground(QtGui.QColor(20, 20, 20))
        painter.eraseRect(self.rect())

        center = self.mm_to_pixel(0, 0)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 2))
        painter.drawLine(center[0], center[1], center[0] + 80, center[1])
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0), 2))
        painter.drawLine(center[0], center[1], center[0], center[1] - 80)

    def sync_all_children(self):
        for c in self.findChildren(QtGui.QWidget):
            if hasattr(c, 'sync'):  c.sync()

    def resizeEvent(self, event):
        self.update()
        self.sync_all_children()

    def scatter_points(self, n):
        for i in range(n):
            pt = Point('p%i' % i, random.uniform(-10, 10), random.uniform(-10, 10))
            ctrl = PointControl(self, pt)
            e = Editor(ctrl)
            ctrl.editor = e
            ctrl.raise_()

    def make_circle(self):
        c = Circle('c', 1, 1, 4)
        ctrl = CircleControl(self, c)
        e = Editor(ctrl)
        ctrl.editor = e
        ctrl.raise_()

    def mm_to_pixel(self, x=None, y=None):
        """ Converts an x,y position in mm into a pixel coordinate.
        """
        if x is not None:
            x = int((x - self.center.x()) * self.scale + self.size().width()/2)
        if y is not None:
            y = int((self.center.y() - y) * self.scale + self.size().height()/2)

        if x is not None and y is not None:     return x, y
        elif x is not None:                     return x
        elif y is not None:                     return y

    def pixel_to_mm(self, x=None, y=None):
        """ Converts a pixel location into an x,y coordinate.
        """
        if x is not None:
            x =  (x - self.width()/2) / self.scale + self.center.x()
        if y is not None:
            y = -((y - self.height()/2) / self.scale - self.center.y())
        if x is not None and y is not None:     return x, y
        elif x is not None:                     return x
        elif y is not None:                     return y

    def find_input(self, pos):
        """ Hunts through all Editor panels to find one with
            a connection.Input control at the given position, returning
            None otherwise.
        """
        for c in self.findChildren(Editor):
            i = c.find_input(pos)
            if i is not None:   return i
        return None

################################################################################

from node.point import Point
from control.point import PointControl

from node.circle import Circle
from control.circle import CircleControl

from ui.editor import Editor