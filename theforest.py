import arcade
import model_theforest
import sprite_theforest

SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 700
GRAVITY = 0.35

class GameWindow(arcade.Window):
    def __init__(self, width, height,title):
        super().__init__(width, height,title)
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.mouse_hold = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.shoot_enable = None
        self.mouse_enable = True
        self.slingshot_setting = model_theforest.Slingshot_F(80,182,350,150,0,70)
        self.slingshot_sprite = sprite_theforest.Slingshot_sprite("images/slingshot.png",self.slingshot_setting)
        self.hand_sprite = sprite_theforest.Hand_sprite("images/hand.png",self.slingshot_setting)
        self.grape_setting = model_theforest.Grape_F(75,91,350,220,GRAVITY)
        self.grape_sprite = sprite_theforest.Sprite_F("images/grape.png",self.grape_setting)
    def on_mouse_motion(self, x, y, dx, dy):
        #print("(x,y) = ("+str(x)+","+str(y)+")")
        self.mouse_x = x
        self.mouse_y = y
    def on_mouse_press(self, x, y, button, modifiers):
        print("(x,y) = ("+str(x)+","+str(y)+")")
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_hold = True
    def on_mouse_release(self, x, y, button,modifiers):
        #print("(x,y) = ("+str(x)+","+str(y)+")")
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_hold = False
            self.shoot_enable = True
    def on_draw(self):
        arcade.start_render()
        if self.mouse_enable:
            self.slingshot_sprite.draw_line_R(self.slingshot_setting.mouse_hold,
                                            self.slingshot_setting.shoot_x, 
                                            self.slingshot_setting.shoot_y, 
                                            self.slingshot_setting.mouse_x, 
                                            self.slingshot_setting.mouse_y)
        self.slingshot_sprite.draw()
        self.grape_sprite.draw()
        if self.mouse_enable:
            self.slingshot_sprite.draw_line_L(self.slingshot_setting.mouse_hold,
                                            self.slingshot_setting.shoot_x, 
                                            self.slingshot_setting.shoot_y, 
                                            self.slingshot_setting.mouse_x, 
                                            self.slingshot_setting.mouse_y)
        self.hand_sprite.draw()
    def update(self, delta_time):
        #print(self.mouse_hold)
        #print("(x,y) = ("+str(self.grape_setting.x)+","+str(self.grape_setting.y)+")")
        if self.slingshot_setting.mouse_hold:
            self.grape_setting.x = self.slingshot_setting.mouse_x
            self.grape_setting.y = self.slingshot_setting.mouse_y
        if self.shoot_enable:
            self.grape_setting.setup_shoot(self.slingshot_setting.getVelocity(),self.slingshot_setting.getAngle_radian())
            self.grape_setting.shoot()
            self.mouse_enable = False
        self.grape_sprite.update()
        self.slingshot_sprite.update()
        self.slingshot_setting.updateMouse(self.mouse_x, self.mouse_y, self.mouse_hold)
        self.hand_sprite.update()
        ''' Out Screen Edge '''
        if self.grape_setting.isOutScreen(SCREEN_WIDTH,SCREEN_HEIGHT):
            self.shoot_enable = False
            self.mouse_enable = True
           
if __name__ == '__main__':
    runGame = GameWindow(SCREEN_WIDTH,SCREEN_HEIGHT,"TheForest")
    arcade.set_window(runGame)
    arcade.run()