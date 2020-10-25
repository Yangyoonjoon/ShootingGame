from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont
from threading import Thread
import time
import random
from PyQt5.QtWidgets import QInputDialog

# 적군 클래스
class Enemy:
    def __init__(self, r, d, s, c, t):
        self.r = r
        # 방향 0:Left, 1:Up, 2:Right, 3:Down
        self.dir = d
        self.size = s
        self.die = False
        self.col =  c
        # 타입 0:적군, 1:hp회복
        self.type = t

class Mine:
    def __init__(self, r):
        self.r = r
        self.die = False

class Bullet:
    def __init__(self, r, d):
        self.r = r
        self.die = False
        self.dir = d

class Game(QObject):

    # 시그널 생성
    update_signal = pyqtSignal()
    gameover_signal = pyqtSignal()

    def __init__(self, w):
        super().__init__()

        self.parent = w
        self.rect = w.rect()

        # 점수
        self.score = 0

        # 에너지
        self.energy = 0

        # 궁극기
        self.ultimate = False

        # 궁극기 효과 지속 시간
        self.ultimateC = True
        self.ultimateCt = 500

        # 아군
        pt = self.rect.center()
        size = 30
        self.my = QRectF(pt.x()-size/2, pt.y()-size/2, size, size)
        self.hp = 10

        # 지뢰
        self.mine = []

        # 지뢰 쿨타임
        self.mineC = True
        self.mineCt = 300

        # 총알
        self.bullet = []

        # 적군
        self.e = []
        # 적군 속도
        self.esp = 2

        # 이동
        self.L = False
        self.R = False
        self.U = False
        self.D = False

        # 마지막으로 누른 이동 버튼
        # 방향 0:Left, 1:Up, 2:Right, 3:Down
        self.key = 1

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
        f = QFont('돋움체', 15)
        f.setBold(True)
        qp.setFont(f)
        qp.drawText(self.my, Qt.AlignCenter, str(self.hp))

        # 지뢰 그리기
        b = QBrush(QColor(0, 0, 0, 128))
        qp.setBrush(b)
        for m in self.mine:
            qp.drawEllipse(m.r)

        # 점수 & 지뢰 쿨타임 & 총알 개수 표시
        p = QPen(QColor(0,0,0), 1, Qt.SolidLine)
        qp.setPen(p)
        f = format(self.mineCt/100, '0.2f')
        txt = f'점수:{self.score} \n쿨타임:{f}초 \n총알 개수:{10 - len(self.bullet)}'
        qp.drawText(self.rect, Qt.AlignTop|Qt.AlignLeft, txt)

        # 에너지 & 궁극기 남은 시간 표시
        if self.ultimateC == False:
            f = format(self.ultimateCt/100, '0.2f')
            txt = f'궁극기 남은 시간:{f}'
        else:
            txt = f'에너지:{self.energy}/50'
        qp.drawText(self.rect, Qt.AlignTop|Qt.AlignRight, txt)

        # 총알 그리기
        # 궁극기 사용 가능시 총알 색상이 노란색으로 변함
        if self.energy >= 50:
            b = QBrush(QColor(255, 255, 0))
            qp.setBrush(b)
        else:
            b = QBrush(QColor(0, 0, 0))
            qp.setBrush(b)
        for bullet in self.bullet:
            qp.drawEllipse(bullet.r)

    def keyDown(self, key):
        if key == Qt.Key_Left or key == Qt.Key_A:
            self.L = True
            self.key = 0
        elif key == Qt.Key_Right or key == Qt.Key_D:
            self.R = True
            self.key = 2
        elif key == Qt.Key_Up or key == Qt.Key_W:
            self.U = True
            self.key = 1
        elif key == Qt.Key_Down or key == Qt.Key_S:
            self.D = True
            self.key = 3
                        
        # 지뢰 생성
        if (key == Qt.Key_H or key == Qt.Key_K) and self.mineC:
            size = 100
            pt = self.my.center()
            x = pt.x() - size/2
            y = pt.y() - size/2
            rect = QRectF(x, y, size, size)
            self.mine.append(Mine(rect))
            self.mineC = False

        # 총알 생성
        if key == Qt.Key_J and len(self.bullet) <= 10:
            size = 5
            pt = self.my.center()
            rect = QRectF(pt.x(), pt.y(), size, size)
            dir = self.key
            self.bullet.append(Bullet(rect, dir))

        # 궁극기 사용
        if key == Qt.Key_Space:
            self.ultimate = True

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
        while self.bRun:
            # 아군 속도
            sp = 4
            # 적군 속도
            esp = self.esp
            #총알 속도
            bsp = 5
            # 적군 사이즈
            esize = 30

            gap = 5

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

                t = random.randint(1, 100)
                if t <= 3:
                    t = 1
                    c = QColor(0,0,255)
                else:
                    t = 0
                    c = QColor(255,0,0)
                rect = QRectF(x, y, esize, esize)
                e = Enemy(rect, d , esize, c, t)

                self.e.append(e)

            # 총알 이동
            # 방향 0:Left, 1:Up, 2:Right, 3:Down
            for b in self.bullet:
                if b.dir == 0:
                    if b.r.right() < self.rect.left():
                        b.die = True
                    else:
                        b.r.adjust(-bsp, 0, -bsp, 0)
                elif b.dir == 1:
                    if b.r.bottom() < self.rect.top():
                        b.die = True
                    else:
                        b.r.adjust(0, -bsp, 0, -bsp)
                elif b.dir == 2:
                    if b.r.left() > self.rect.right():
                        b.die = True
                    else:
                        b.r.adjust(bsp, 0, bsp, 0)
                else:
                    if b.r.top() > self.rect.bottom():
                        b.die = True
                    else:
                        b.r.adjust(0, bsp, 0, bsp)

            # 궁극기
            if self.energy >= 50 and self.ultimate == True:
                self.energy -= 50
                self.esp = 0.5
                self.ultimateC = False
                self.ultimate = False

            # 궁극기 효과 지속
            if self.ultimateC == False:
                self.ultimateCt -= 1

            if self.ultimateCt <= 0:
                self.ultimateC = True
                self.ultimateCt = 500
                self.esp = 2

            # 적군의 이동 및 충돌 처리
            for e in self.e:
                # 적군과 나의 충돌
                if self.my.intersects(e.r):
                    e.die = True
                    if e.type == 0:
                        self.hp -= 1
                    else:
                        if self.hp < 10:
                            self.hp += 1
                    continue

                # 지뢰와 적군의 충돌
                bNext = False
                for m in self.mine:
                    if m.r.intersects(e.r) and e.type == 0:
                        m.die = True
                        e.die = True
                        bNext = True
                        break

                if bNext:
                    continue

                # 총알과 적군의 충돌
                for bullet in self.bullet:
                    if bullet.r.intersects(e.r) and e.type == 0:
                        bullet.die = True
                        e.die = True
                        self.score += 1
                        if self.energy < 50 and self.ultimateC == True:
                            self.energy += 1

                # 적군 이동 처리 및 벽과 충돌 처리
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
            if self.mineC == False:
                self.mineCt -= 1

            if self.mineCt <= 0:
                self.mineC = True
                self.mineCt = 300

            # 총알 삭제
            self.bullet = [bullet for bullet in self.bullet if bullet.die == False]

            # 게임 종료 (hp <= 0)
            if self.hp <= 0:
                self.gameover_signal.emit()
                break

            time.sleep(0.01)
            self.update_signal.emit()