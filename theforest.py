import arcade
import model_theforest
import sprite_theforest

SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 700
GRAVITY = 0.05

class GameWindow(arcade.Window):
    def __init__(self, width, height,title):
        super().__init__(width, height,title)
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.mouse_hold = None
        self.mouse_x = None
        self.mouse_y = None
        self.slingshot_setting = model_theforest.Slingshot_F(80,182,350,150,0,70)
        self.slingshot_sprite = sprite_theforest.Slingshot_sprite("images/slingshot.png",self.slingshot_setting)
        self.grape_setting = model_theforest.Grape_F(75,91,350,220,6,GRAVITY,45)
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
    def on_draw(self):
        arcade.start_render()
        self.slingshot_sprite.draw_line_R(self.slingshot_setting.mouse_hold,
                                        self.slingshot_setting.shoot_x, 
                                        self.slingshot_setting.shoot_y, 
                                        self.slingshot_setting.mouse_x, 
                                        self.slingshot_setting.mouse_y)
        self.slingshot_sprite.draw()
        self.grape_sprite.draw()
        self.slingshot_sprite.draw_line_L(self.slingshot_setting.mouse_hold,
                                        self.slingshot_setting.shoot_x, 
                                        self.slingshot_setting.shoot_y, 
                                        self.slingshot_setting.mouse_x, 
                                        self.slingshot_setting.mouse_y)
    def update(self, delta_time):
        #print(self.mouse_hold)
        self.grape_setting.shoot()
        self.grape_sprite.update()
        self.slingshot_sprite.update()
        self.slingshot_setting.updateMouse(self.mouse_x, self.mouse_y, self.mouse_hold)
           
if __name__ == '__main__':
    runGame = GameWindow(SCREEN_WIDTH,SCREEN_HEIGHT,"TheForest")
    arcade.set_window(runGame)
    arcade.run()