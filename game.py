from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont
from threading import Thread
import time
import random
from PyQt5.QtWidgets import QInputDialog

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

class Mine:
    def __init__(self, r):
        self.r = r
        self.die = False

class Game(QObject):

    # 시그널 생성
    update_signal = pyqtSignal()
    gameover_signal = pyqtSignal()

    def __init__(self, w):
        super().__init__()

        self.parent = w
        self.rect = w.rect()

        # 아군
        pt = self.rect.center()
        size = 30
        self.my = QRectF(pt.x()-size/2, pt.y()-size/2, size, size)
        self.hp = 10

        # 게임 난이도 조절
        label = ('상', '중', '하')
        item = QInputDialog.getItem(self.parent, '게임 시작', '난이도 설정', label, 0, False)

        if item[1]:
            pass
        else:
            self.hp = 0

        # 지뢰
        self.mine = []

        # 지뢰 쿨타임
        self.c = True
        self.ct = 300

        # 적군
        self.e = []

        # 이동
        self.L = False
        self.R = False
        self.U = False
        self.D = False

        # 시그널 처리
        self.update_signal.connect(self.parent.update)
        self.gameover_signal.connect(self.parent.gameOver)

        # 쓰레드 생성
        self.t = Thread(target=self.threadFunc)
        self.bRun = True
        self.t.start()

    def draw(self, qp):
        # 안티 엘리어싱
        qp.setRenderHint(QPainter.Antialiasing)

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

        # 지뢰 그리기
        b = QBrush(QColor(0, 0, 0, 128))
        qp.setBrush(b)
        for m in self.mine:
            qp.drawEllipse(m.r)

        # 지뢰 쿨타임 표시
        p = QPen(QColor(0,0,0), 1, Qt.SolidLine)
        qp.setPen(p)
        f = format(self.ct/100, '0.2f')
        txt = f'쿨타임:{f}초'
        qp.drawText(self.rect, Qt.AlignTop|Qt.AlignLeft, txt)

    def keyDown(self, key):
        if key == Qt.Key_Left or key == Qt.Key_A:
            self.L = True
        elif key == Qt.Key_Right or key == Qt.Key_D:
            self.R = True
        elif key == Qt.Key_Up or key == Qt.Key_W:
            self.U = True
        elif key == Qt.Key_Down or key == Qt.Key_S:
            self.D = True
                        
        # 지뢰 생성
        if key == Qt.Key_Space and self.c:
            size = 100
            pt = self.my.center()
            x = pt.x() - size/2
            y = pt.y() - size/2
            rect = QRectF(x, y, size, size)
            self.mine.append(Mine(rect))
            self.c = False

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
            if r >= 1 and r <= 5:
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

                bNext = False
                for m in self.mine:
                    if m.r.intersects(e.r):
                        m.die = True
                        e.die = True
                        bNext = True
                        break

                if bNext:
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

            # 지뢰 삭제
            self.mine = [m for m in self.mine if m.die == False]

            # 지뢰 쿨타임
            if self.c == False:
                self.ct -= 1

            if self.ct <= 0:
                self.c = True
                self.ct = 300

            # 게임 종료 (hp <= 0)
            if self.hp <= 0:
                self.gameover_signal.emit()
                break


            time.sleep(0.01)
            self.update_signal.emit()