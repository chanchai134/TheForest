import arcade
import math
from random import randint

GRAVITY = 0.35

class Model_config:
    def __init__(self, x, y, tag):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.tag = tag

class Slingshot_config(Model_config):
    def __init__(self, x, y, mouse):
        super().__init__(x, y, "slingshot")
        self.shoot_x = self.x
        self.shoot_y = self.y + 103
        self.mouse = mouse
    def getAngle_radian(self):
        return math.atan2(self.shoot_y-self.mouse.y ,self.shoot_x-self.mouse.x)
    def getAngle_degree(self):
        return (math.atan2(self.shoot_y-self.mouse.y ,self.shoot_x-self.mouse.x)*180)/math.pi
    def getVelocity(self):
        return math.sqrt(math.pow(self.shoot_y-self.mouse.y ,2) + math.pow(self.shoot_x-self.mouse.x,2))/12

class Shoot_config(Model_config): #all sprite that can shoot
    def __init__(self, Slingshot, caught_radian, ate_radian, centerMarginX, centerMarginY, tag):
        super().__init__(Slingshot.shoot_x, Slingshot.shoot_y, tag)
        self.gravity = (-1)*GRAVITY
        self.angle = None
        self.velocity_x = None
        self.velocity_y_pre = None
        self.velocity_y_post = None
        self.shiff_distance_y = 0
        self.slingshot = Slingshot
        '''__outlineCheck__'''
        self.caught_radian = caught_radian
        self.ate_radian = ate_radian
        self.centerMarginX = centerMarginX
        self.centerMarginY = centerMarginY  
        self.centerX = Slingshot.shoot_x + self.centerMarginX
        self.centerY = Slingshot.shoot_y + self.centerMarginY
        self.start_centerX = Slingshot.shoot_x + self.centerMarginX
        self.start_centerY = Slingshot.shoot_y + self.centerMarginY
    def aim(self):
        self.x = self.slingshot.mouse.x
        self.y = self.slingshot.mouse.y
        self.centerX = self.slingshot.mouse.x + self.centerMarginX
        self.centerY = self.slingshot.mouse.y + self.centerMarginY
        self.angle = self.slingshot.getAngle_radian()
        self.velocity_x_start = self.slingshot.getVelocity()*math.cos(self.angle)
        self.velocity_x = self.slingshot.getVelocity()*math.cos(self.angle)
        self.velocity_y_pre = self.slingshot.getVelocity()*math.sin(self.angle)
        self.velocity_y_post = self.slingshot.getVelocity()*math.sin(self.angle) + self.gravity
    def shoot(self):
        self.shiff_distance_y = math.pow(self.velocity_y_post,2)-math.pow(self.velocity_y_pre,2)
        self.shiff_distance_y /= 2*self.gravity
        self.velocity_y_pre += self.gravity
        self.velocity_y_post += self.gravity
        self.x += self.velocity_x
        self.y += self.shiff_distance_y
        self.centerX += self.velocity_x
        self.centerY += self.shiff_distance_y
    def sprite_ResetOnoutScreen(self, screen_width, screen_height):
        if self.x > screen_width or self.x < 0 or self.y < 0:
            return True
        return False
    def debug(self):
        arcade.draw_circle_outline(self.centerX, self.centerY, self.caught_radian, arcade.color.BLACK)
        arcade.draw_circle_outline(self.centerX, self.centerY, self.ate_radian, arcade.color.BLACK)

class Grape_config(Shoot_config):
    def __init__(self, Slingshot):
        super().__init__(Slingshot, 35, 25, 0 ,-10, "grape")
        self.canSpecial = True
    def special_skill(self):
        self.velocity_x = 0
        self.velocity_y_pre += 5*self.gravity
        self.velocity_y_post += 5*self.gravity

class Banana_config(Shoot_config):
    def __init__(self, Slingshot):
        super().__init__(Slingshot, 40, 30, -4 ,-9, "banana")
        self.canSpecial = True
        self.clicked = False
        self.freeze_y_pre = None
        self.freeze_y_post = None
        self.freeze_is_start = False
        self.freeze_is_end = False
    def special_skill(self):
        self.velocity_x = self.velocity_x_start + 20
        self.y -= self.shiff_distance_y
        self.centerY -= self.shiff_distance_y
        if not(self.freeze_is_start):
            self.freeze_y_pre = self.velocity_y_pre
            self.freeze_y_post = self.velocity_y_post
            self.freeze_is_start = True
    def stop_special(self):
        if not(self.freeze_is_end):
            self.velocity_x = self.velocity_x_start
            self.velocity_y_pre = self.freeze_y_pre - self.gravity
            self.velocity_y_post = self.freeze_y_post - self.gravity
            self.freeze_is_end = True
            self.canSpecial = False

class Meat_config(Shoot_config):
    def __init__(self, Slingshot):
        super().__init__(Slingshot, 45, 35, -3 ,-7, "meat")

class Eat_config(Model_config):
    def __init__(self, x, y, eat_radian, centerMarginX, centerMarginY, tag):
        super().__init__(x, y, tag)
        self.centerMarginX = centerMarginX
        self.centerMarginY = centerMarginY
        self.centerX = x + self.centerMarginX
        self.centerY = y + self.centerMarginY
        self.eat_radian = eat_radian
    def update_random(self, SCREEN_WIDTH, SCREEN_HEIGHT):        
        self.x = randint(0,SCREEN_WIDTH)
        self.y = randint(0,SCREEN_HEIGHT)
        self.centerX = self.x + self.centerMarginX
        self.centerY = self.y + self.centerMarginY
    def isHit(self, model):
        diff_equation = (self.centerX-model.centerX)**2
        diff_equation += (self.centerY-model.centerY)**2
        diff_equation = math.sqrt(diff_equation)
        if diff_equation <= (self.eat_radian + model.ate_radian):
            return True
        else:
            return False
    def debug(self):
        arcade.draw_circle_outline(self.centerX, self.centerY, self.eat_radian, arcade.color.BLACK)

class Worm_config(Eat_config):
    def __init__(self, x, y):
        super().__init__(x, y, 30, -20, 0 , "worm")

class Monkey_config(Eat_config):
    def __init__(self, x, y):
        super().__init__(x, y, 40, -10, 20, "monkey")

class Dragon_config(Eat_config):
    def __init__(self, x, y):
        super().__init__(x, y, 60, -68, -50, "dragon")

class Shoothill_config(Model_config):
    def __init__(self, x, y):
        super().__init__(x, y, "hill")

class Ground_config(Model_config):
    def __init__(self, x, y):
        super().__init__(x, y, "ground")
    def isHit(self, model):
        X_equation = self.x-35
        temp = (model.caught_radian - X_equation + model.centerX)*(model.caught_radian + X_equation - model.centerX)
        if temp > 0:
            y1 = math.sqrt(temp) + model.centerY
            y2 = ((-1)*math.sqrt(temp)) + model.centerY
            if (y1 > (self.y-35) and y1 < (self.y+35)) or (y2 > (self.y-35) and y2 < (self.y+35)):
                return True    

class Grass_config(Model_config):
    def __init__(self, x, y):
        super().__init__(x, y, "grass")
    def isHit(self, model):
        X_equation = self.x-35
        temp = (model.caught_radian - X_equation + model.centerX)*(model.caught_radian + X_equation - model.centerX)
        if temp > 0:
            y1 = math.sqrt(temp) + model.centerY
            y2 = ((-1)*math.sqrt(temp)) + model.centerY
            if (y1 > (self.y-35) and y1 < (self.y+35)) or (y2 > (self.y-35) and y2 < (self.y+35)):
                return True
        Y_equation = self.y+35
        temp = (model.caught_radian - Y_equation + model.centerY)*(model.caught_radian + Y_equation - model.centerY)
        if temp > 0:
            x1 = math.sqrt(temp) + model.centerX
            x2 = ((-1)*math.sqrt(temp)) + model.centerX
            if (x1 > (self.x-35) and x1 < (self.x+35)) or (x2 > (self.x-35) and x2 < (self.x+35)):
                return True
        return False  