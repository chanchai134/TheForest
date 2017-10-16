import arcade
from model_theforest import Grape_config, Slingshot_config
from sprite_theforest import Grape_sprite, Slingshot_sprite, SlingshotHand_sprite
from setting_theforest import Mouse_C
from map_theforest import Map_F

SCREEN_WIDTH = 1910
SCREEN_HEIGHT = 900

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.background = arcade.load_texture("images/bg.jpg")
        self.mouse = Mouse_C()
        self.slingshot_C = Slingshot_config(327, 400, self.mouse)
        self.slingshot_S = Slingshot_sprite(self.slingshot_C)
        self.slingshotHand_S = SlingshotHand_sprite(self.slingshot_C)
        self.grape_C = Grape_config(self.slingshot_C)
        self.grape_S = Grape_sprite(self.grape_C)
        self.map = Map_F(SCREEN_WIDTH, SCREEN_HEIGHT, self.grape_C)
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.x = x
        self.mouse.y = y
        circular_equation = (x - self.grape_C.centerX)**2
        circular_equation += (y - self.grape_C.centerY)**2
        if circular_equation <=  self.grape_C.caught_radian**2: # r^2
            #print("inside")
            self.mouse.canCaught = True
        else:
            self.mouse.canCaught = False
            #print("outinside")
    def on_mouse_press(self, x, y, button, modifiers):
        #print("(x,y) = ("+str(x)+","+str(y)+")")
        if button == arcade.MOUSE_BUTTON_LEFT and (not self.mouse.shooting) and self.mouse.canCaught:
            self.mouse.aimming = True
    def on_mouse_release(self, x, y, button,modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.mouse.aimming:
            self.mouse.shooting = True
            self.mouse.aimming = False
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        '''__shoot part__'''
        self.slingshot_S.draw_line_R()
        self.slingshot_S.draw()
        self.grape_S.draw()
        self.slingshot_S.draw_line_L()
        self.slingshotHand_S.draw()
        '''__Map part__'''
        self.map.draw()
        '''__Debug__'''
        self.grape_C.debug()
    def update(self, delta_time):
        '''__Map part__'''
        self.map.update()
        '''__Control part__'''
        if self.mouse.aimming:
            self.grape_C.aim()
        if self.mouse.shooting:
            self.grape_C.shoot()
        '''__Auto function__'''
        self.grape_C.sprite_ResetOnoutScreen(SCREEN_WIDTH,SCREEN_HEIGHT)
        #print("(x,y) = ("+str(self.grape_C.x)+","+str(self.grape_C.y)+")")
        '''__Sprite update__'''
        self.slingshot_S.update()
        self.slingshotHand_S.update()
        self.grape_S.update()
           
if __name__ == '__main__':
    runGame = GameWindow(SCREEN_WIDTH,SCREEN_HEIGHT,"TheForest")
    arcade.set_window(runGame)
    arcade.run()