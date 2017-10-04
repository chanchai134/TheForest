import math
class Model_F:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

class Shoot_F(Model_F):
    def __init__(self, width, height, x, y, gravity):
        super().__init__(width, height, x, y)
        self.gravity = (-1)*gravity
        self.angle = None
        self.velocity_x = None
        self.velocity_y_pre = None
        self.velocity_y_post = None
    def setup_shoot(self, velocity, angle):
        if self.angle == None:
            self.angle = angle
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
    def __init__(self, width, height, x, y, gravity):
        super().__init__(width, height, x, y, gravity)
    

class Slingshot_F(Model_F):
    def __init__(self, width, height, x, y, shoot_x_shiff, shoot_y_shiff):
        super().__init__(width, height, x, y)
        self.shoot_x = self.x + shoot_x_shiff
        self.shoot_y = self.y + shoot_y_shiff
        self.mouse_hold = None
        self.mouse_x = None
        self.mouse_y = None
    def updateMouse(self ,mouse_x, mouse_y, mouse_hold):
        self.mouse_hold = mouse_hold
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
    def getAngle(self):
        return math.atan2(self.shoot_y-self.mouse_y ,self.shoot_x-self.mouse_x)
