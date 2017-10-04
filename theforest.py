import arcade
from model_theforest import Grape_config, Slingshot_config
from sprite_theforest import Grape_sprite, Slingshot_sprite, SlingshotHand_sprite

SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 700

class GameWindow(arcade.Window):
    def __init__(self, width, height,title):
        super().__init__(width, height,title)
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.mouse_hold = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.shoot_enable = None
        self.mouse_enable = True
        self.slingshot_C = Slingshot_config(350,150)
        self.slingshot_S = Slingshot_sprite(self.slingshot_C)
        self.slingshotHand_S = SlingshotHand_sprite(self.slingshot_C)
        self.grape_C = Grape_config(self.slingshot_C)
        self.grape_S = Grape_sprite(self.grape_C)
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
    def on_mouse_press(self, x, y, button, modifiers):
        print("(x,y) = ("+str(x)+","+str(y)+")")
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_hold = True
    def on_mouse_release(self, x, y, button,modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_hold = False
            self.shoot_enable = True
    def on_draw(self):
        arcade.start_render()
        if self.mouse_enable:
            self.slingshot_S.draw_line_R()
        self.slingshot_S.draw()
        self.grape_S.draw()
        if self.mouse_enable:
            self.slingshot_S.draw_line_L()
        self.slingshotHand_S.draw()
    def update(self, delta_time):
        #print("(x,y) = ("+str(self.grape_C.x)+","+str(self.grape_C.y)+")")
        if self.slingshot_C.mouse_hold:
            self.grape_C.x = self.slingshot_C.mouse_x
            self.grape_C.y = self.slingshot_C.mouse_y
        if self.shoot_enable:
            self.grape_C.setup_shoot(self.slingshot_C.getVelocity(),self.slingshot_C.getAngle_radian())
            self.grape_C.shoot()
            self.mouse_enable = False
        self.grape_S.update()
        self.slingshot_S.update()
        self.slingshot_C.updateMouse(self.mouse_x, self.mouse_y, self.mouse_hold)
        self.slingshotHand_S.update()
        ''' Out Screen Edge '''
        if self.grape_C.isOutScreen(SCREEN_WIDTH,SCREEN_HEIGHT):
            self.shoot_enable = False
            self.mouse_enable = True
           
if __name__ == '__main__':
    runGame = GameWindow(SCREEN_WIDTH,SCREEN_HEIGHT,"TheForest")
    arcade.set_window(runGame)
    arcade.run()