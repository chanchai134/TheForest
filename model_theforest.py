import math
class Model_F:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

class Shoot_F(Model_F):
    def __init__(self, width, height, x, y, accelerate, velocity, gravity, angle):
        super().__init__(width, height, x, y)
        self.accelerate = accelerate
        self.velocity = velocity
        self.gravity = gravity
        self.angle = angle
    def shoot(self):
        self.x += 1

class Grape_F(Shoot_F):
    def __init__(self, width, height, x, y, accelerate, velocity, gravity, angle):
        super().__init__(width, height, x, y, accelerate, velocity, gravity, angle)

        