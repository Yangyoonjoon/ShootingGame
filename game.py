from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont
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
        self.die = False
        self.col =  QColor(255,0,0)
        self.type = 0

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
        self.hp = 10

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
        # 창 크기
        self.rect = self.parent.rect()

        # 적군 그리기
        for e in self.e:
            b = QBrush(e.col)
            qp.setBrush(b)
            qp.drawRect(e.r)

        # 아군 그리기
        b = QBrush(QColor(0,0,0))
        qp.setBrush(b)
        qp.drawRect(self.my)
        p = QPen(QColor(255,255,255), 1, Qt.SolidLine)
        qp.setPen(p)
        f = QFont('궁서체', 15)
        f.setBold(True)
        qp.setFont(f)
        qp.drawText(self.my, Qt.AlignCenter, str(self.hp))

    def keyDown(self, key):
        if key == Qt.Key_Left or key == Qt.Key_A:
            self.L = True
        elif key == Qt.Key_Right or key == Qt.Key_D:
            self.R = True
        elif key == Qt.Key_Up or key == Qt.Key_W:
            self.U = True
        elif key == Qt.Key_Down or key == Qt.Key_S:
            self.D = True

    def keyUp(self, key):
        if key == Qt.Key_Left or key == Qt.Key_A:
            self.L = False
        elif key == Qt.Key_Right or key == Qt.Key_D:
            self.R = False
        elif key == Qt.Key_Up or key == Qt.Key_W:
            self.U = False
        elif key == Qt.Key_Down or key == Qt.Key_S:
            self.D = False

    def threadFunc(self):
        sp = 4
        esp = 2
        gap = 5
        # 적군 사이즈
        esize = 30

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
            if r >= 1 and r <= 10:
                # 방향 0:Left, 1:Up, 2:Right, 3:Down
                d = random.randint(0, 3)
                if d == 0:
                    x = self.rect.left() - esize
                    y = random.randint(0, self.rect.bottom() - esize)
                elif d == 1:
                    x = random.randint(0, self.rect.width() - esize)
                    y = self.rect.top() - esize
                elif d == 2:
                    x = self.rect.right()
                    y = random.randint(0, self.rect.bottom() - esize)
                else:
                    x = random.randint(0, self.rect.width() - esize)
                    y = self.rect.bottom()

                rect = QRectF(x, y, esize, esize)
                e = Enemy(rect, d , esize)

                self.e.append(e)

            # 적군 이동 처리 & 삭제
            for e in self.e:
                # 적군과 나의 충돌
                if self.my.intersects(e.r):
                    e.die = True
                    self.hp -= 1
                    continue

                # 방향 0:Left, 1:Up, 2:Right, 3:Down
                if e.dir == 0:
                    if e.r.left() > self.rect.right():
                        e.die = True
                    else:
                        e.r.adjust(esp, 0, esp, 0)
                elif e.dir == 1:
                    if e.r.top() > self.rect.bottom():
                        e.die = True
                    else:
                        e.r.adjust(0, esp, 0, esp)
                elif e.dir == 2:
                    if e.r.right() < self.rect.left():
                        e.die = True
                    else:
                        e.r.adjust(-esp, 0, -esp, 0)
                else:
                    if e.r.bottom() < self.rect.top():
                        e.die = True
                    else:
                        e.r.adjust(0, -esp, 0, -esp)

            # 적군 삭제
            self.e = [e for e in self.e if e.die == False]
            #print(len(self.e))


            time.sleep(0.01)
            self.update_signal.emit()