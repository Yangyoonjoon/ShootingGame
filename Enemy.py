# 적군 클래스
class Enemy:
    def __init__(self, r, d, s, c, t):
        self.r = r
        # 방향 0:Left, 1:Up, 2:Right, 3:Down
        self.dir = d
        self.size = s
        self.die = False
        self.col =  c
        # 타입 0:적군, 1:hp회복, 2:모든 적군 삭제
        self.type = t
