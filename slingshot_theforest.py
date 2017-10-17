import arcade
from model_theforest import Grape_config, Banana_config, Meat_config, Slingshot_config
from sprite_theforest import Grape_sprite, Banana_sprite, Meat_sprite, Slingshot_sprite, SlingshotHand_sprite
from setting_theforest import Mouse_C
from random import randint

SCREEN_WIDTH = 1910
SCREEN_HEIGHT = 900

class Slingshot_fruit:
    def __init__(self):
        self.background = arcade.load_texture("images/bg.jpg")
        self.mouse = Mouse_C()
        self.slingshot_C = Slingshot_config(327, 400, self.mouse)
        self.slingshot_S = Slingshot_sprite(self.slingshot_C)
        self.slingshotHand_S = SlingshotHand_sprite(self.slingshot_C)
        self.fruit_C = self.random_fruit()
        self.fruit_S = self.Get_sprite(self.fruit_C)
        self.map = None
    def draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        '''__shoot part__'''
        self.slingshot_S.draw_line_R()
        self.slingshot_S.draw()
        self.fruit_S.draw()
        self.slingshot_S.draw_line_L()
        self.slingshotHand_S.draw()
        '''__Debug__'''
        #self.fruit_C.debug()
    def update(self):
        '''__Control part__'''
        ###########_startSpecial_###########
        if(self.fruit_C.tag == "grape"):
            if self.mouse.click and self.fruit_C.canSpecial and self.mouse.shooting:
                self.fruit_C.special_skill()
        if(self.fruit_C.tag == "banana"):
            if self.mouse.click and self.fruit_C.canSpecial and self.mouse.shooting:
                self.fruit_C.special_skill()
                self.fruit_C.clicked = True
            if not(self.mouse.click) and self.fruit_C.clicked:
                self.fruit_C.canSpecial = False
                self.fruit_C.stop_special()
        ############_endSpecial_############
        if self.mouse.aimming:
            self.fruit_C.aim()
        if self.mouse.shooting:
            self.fruit_C.shoot()        
        '''__Sprite update__'''
        self.slingshot_S.update()
        self.slingshotHand_S.update()
        self.fruit_S.update()
        '''__Auto function__'''
        if self.fruit_C.sprite_ResetOnoutScreen(SCREEN_WIDTH,SCREEN_HEIGHT):
            self.fruit_C = self.random_fruit()
            self.fruit_S = self.Get_sprite(self.fruit_C)
            self.map.fruit = self.fruit_C
            self.mouse.reset_mouse()
            self.map.score -= 10
    def on_mouse_motion(self, x, y):
        self.mouse.x = x
        self.mouse.y = y
        circular_equation = (x - self.fruit_C.centerX)**2
        circular_equation += (y - self.fruit_C.centerY)**2
        if circular_equation <=  self.fruit_C.caught_radian**2: # r^2
            #print("inside")
            self.mouse.canCaught = True
        else:
            self.mouse.canCaught = False
            #print("outinside")
    def on_mouse_press(self, button):
        if button == arcade.MOUSE_BUTTON_LEFT and (not self.mouse.shooting) and self.mouse.canCaught:
            self.mouse.aimming = True
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse.click = True
    def on_mouse_release(self, button):
        if button == arcade.MOUSE_BUTTON_LEFT and self.mouse.aimming:
            self.mouse.shooting = True
            self.mouse.aimming = False
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse.click = False
    def sync(self, map):
        self.map = map
    def random_fruit(self):
        num = randint(1,3)
        if num == 1:
            return Grape_config(self.slingshot_C)
        elif num == 2:
            return Banana_config(self.slingshot_C)
        else:
            return Meat_config(self.slingshot_C)
    def Get_sprite(self, model):
        if model.tag == "grape":
            return Grape_sprite(model)
        elif model.tag == "banana":
            return Banana_sprite(model)
        else:
            return Meat_sprite(model)