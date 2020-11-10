# 방어막 클래스
class Shield:
    def __init__(self, r):
        self.r = r
        self.die = False
        self.life = 4
        
# 총알 클래스
class Bullet:
    def __init__(self, r, d):
        self.r = r
        self.die = False
        self.dir = d

# 흔적 클래스
class Trace:
    def __init__(self, r, x, y):
        self.r = r
        self.die = False
        self.x = x
        self.y = y

# 폭탄, 폭탄 범위, 폭발 클래스
class Bomb:
    def __init__(self, r):
        self.r = r
        self.die = False