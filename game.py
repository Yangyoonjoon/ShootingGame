from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal, QObject
from PyQt5.QtGui import QPainter
from threading import Thread
import time
import random

# 적군 클래스
class Enemy:
    def __init__(self, r, d, s):
        self.r = r
        # 방향 0:Left, 1:Up, 2:Right, 3:Down
        self.dir = d
        self.size = s

class Game(QObject):

    # 시그널 생성
    update_signal = pyqtSignal()

    def __init__(self, w):
        super().__init__()

        self.parent = w
        self.rect = w.rect()

        # 아군
        pt = self.rect.center()
        size = 30
        self.my = QRectF(pt.x()-size/2, pt.y()-size/2, size, size)

        # 적군
        self.e = []
        

        # 이동
        self.L = False
        self.R = False
        self.U = False
        self.D = False

        # 시그널 처리
        self.update_signal.connect(self.parent.update)

        # 쓰레드 생성
        self.t = Thread(target=self.threadFunc)
        self.bRun = True
        self.t.start()

    def draw(self, qp):
        # 아군 그리기
        qp.drawRect(self.my)

        # 적군 그리기
        for e in self.e:
            qp.drawRect(e.r)

    def keyDown(self, key):
        if key == Qt.Key_Left:
            self.L = True
        elif key == Qt.Key_Right:
            self.R = True
        elif key == Qt.Key_Up:
            self.U = True
        elif key == Qt.Key_Down:
            self.D = True

    def keyUp(self, key):
        if key == Qt.Key_Left:
            self.L = False
        elif key == Qt.Key_Right:
            self.R = False
        elif key == Qt.Key_Up:
            self.U = False
        elif key == Qt.Key_Down:
            self.D = False

    def threadFunc(self):
        sp = 5
        gap = 5
        # 적군 사이즈
        esize = 50

        while self.bRun:
            # 아군 이동 처리
            if self.L and self.my.left() > self.rect.left() + gap:
                self.my.adjust(-sp, 0, -sp, 0)
            if self.R and self.my.right() < self.rect.right() - gap:
                self.my.adjust(sp, 0, sp, 0)
            if self.U and self.my.top() > self.rect.top() + gap:
                self.my.adjust(0, -sp, 0, -sp)
            if self.D and self.my.bottom() < self.rect.bottom() - gap:
                self.my.adjust(0, sp, 0, sp)

            # 적군 생성
            r = random.randint(1, 100)
            if r == 1:
                # 방향 0:Left, 1:Up, 2:Right, 3:Down
                d = 0 #random.randint(0, 3)
                x = self.rect.left()
                y = random.randint(0, self.rect.bottom() - esize)
                rect = QRectF(x, y, esize, esize)
                e = Enemy(rect, d , esize)

                self.e.append(e)


            time.sleep(0.01)
            self.update_signal.emit()