from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
import sys
from game import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.game = Game(self)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        if hasattr(self, 'game'):
            self.game.draw(qp)
        qp.end()

    def keyPressEvent(self, e):
        self.game.keyDown(e.key())
        if e.key() == Qt.Key_Escape:
            self.close()

    def keyReleaseEvent(self, e):
        self.game.keyUp(e.key())

    def closeEvent(self, e):
        self.game.bRun = False

    def gameOver(self):
        result = QMessageBox.information(self, '게임 종료', '한 판 더 하시겠습니까?', QMessageBox.Yes|QMessageBox.No)

        if result == QMessageBox.Yes:
            del(self.game)
            self.game = Game(self)
        else:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
