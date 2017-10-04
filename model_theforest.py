import math

GRAVITY = 0.35

class Model_config:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y

class Shoot_config(Model_config):
    def __init__(self, width, height, x, y, gravity):
        super().__init__(width, height, x, y)
        self.gravity = (-1)*gravity
        self.angle = None
        self.velocity_x = None #enable setup_shoot method
        self.velocity_y_pre = None
        self.velocity_y_post = None
        self.shiff_distance_y = None
    def setup_shoot(self, velocity, angle):
        if self.velocity_x == None:
            self.angle = angle
            self.velocity_x = velocity*math.cos(self.angle)
            self.velocity_y_pre = velocity*math.sin(self.angle)
            self.velocity_y_post = velocity*math.sin(self.angle) + self.gravity
    def shoot(self):
        self.shiff_distance_y = math.pow(self.velocity_y_post,2)-math.pow(self.velocity_y_pre,2)
        self.shiff_distance_y /= 2*self.gravity
        self.velocity_y_pre += self.gravity
        self.velocity_y_post += self.gravity
        self.x += self.velocity_x
        self.y += self.shiff_distance_y
    def isOutScreen(self, screen_width, screen_height):
        if self.x > screen_width or self.x < 0 or self.y > screen_height or self.y < 0 :
            self.x = self.start_x
            self.y = self.start_y
            self.velocity_x = None #enable setup_shoot method
            return True
        return False

class Grape_config(Shoot_config):
    def __init__(self, ModelReference):
        super().__init__(75, 91, ModelReference.shoot_x, ModelReference.shoot_y, GRAVITY)
    

class Slingshot_config(Model_config):
    def __init__(self, x, y):
        super().__init__(80, 248, x, y)
        self.shoot_x = self.x
        self.shoot_y = self.y + 103
        self.mouse_hold = None
        self.mouse_x = None
        self.mouse_y = None
    def updateMouse(self ,mouse_x, mouse_y, mouse_hold):
        self.mouse_hold = mouse_hold
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
    def getAngle_radian(self):
        return math.atan2(self.shoot_y-self.mouse_y ,self.shoot_x-self.mouse_x)
    def getAngle_degree(self):
        return (math.atan2(self.shoot_y-self.mouse_y ,self.shoot_x-self.mouse_x)*180)/math.pi
    def getVelocity(self):
        return math.sqrt(math.pow(self.shoot_y-self.mouse_y ,2) + math.pow(self.shoot_x-self.mouse_x,2))/12