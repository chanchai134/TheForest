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
        self.slingshot_setting = model_theforest.Slingshot_F(80,182,350,150)
        self.slingshot_sprite = sprite_theforest.Slingshot_sprite("images/slingshot.png",self.slingshot_setting)
        self.grape_setting = model_theforest.Grape_F(68,91,100,300,6,GRAVITY,45)
        self.grape_sprite = sprite_theforest.Sprite_F("images/grape.png",self.grape_setting)
    def on_mouse_press(self, x, y, button, modifiers):
        print("(x,y) = ("+str(x)+","+str(y)+")")
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_hold = True
            self.mouse_x = x
            self.mouse_y = y
    def on_mouse_release(self, x, y, button,modifiers):
        #print("(x,y) = ("+str(x)+","+str(y)+")")
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_hold = False
    def on_draw(self):
        arcade.start_render()
        arcade.draw_line(270, 495, 300, 450, arcade.color.BLACK, 3)
        self.grape_sprite.draw()
        arcade.draw_line(270, 495, 300, 450, arcade.color.WOOD_BROWN, 3)
        self.slingshot_sprite.draw()
    def update(self, delta_time):
        #print(self.mouse_hold)
        self.grape_setting.shoot()
        self.grape_sprite.update()
        self.slingshot_sprite.update()
    
if __name__ == '__main__':
    runGame = GameWindow(SCREEN_WIDTH,SCREEN_HEIGHT,"TheForest")
    arcade.set_window(runGame)
    arcade.run()