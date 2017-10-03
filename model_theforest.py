import math
class Model_F:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

class Shoot_F(Model_F):
    def __init__(self, width, height, x, y, velocity, gravity, angle):
        super().__init__(width, height, x, y)
        self.gravity = (-1)*gravity
        self.angle = (angle*math.pi)/180
        self.velocity_x = velocity*math.cos(self.angle)
        self.velocity_y_pre = velocity*math.sin(self.angle)
        self.velocity_y_post = velocity*math.sin(self.angle) + self.gravity
    def shoot(self):
        shiff_distance_y = math.pow(self.velocity_y_post,2)-math.pow(self.velocity_y_pre,2)
        shiff_distance_y /= 2*self.gravity
        self.velocity_y_pre += self.gravity
        self.velocity_y_post += self.gravity
        self.x += self.velocity_x
        self.y += shiff_distance_y

class Grape_F(Shoot_F):
    def __init__(self, width, height, x, y, velocity, gravity, angle):
        super().__init__(width, height, x, y, velocity, gravity, angle)

        