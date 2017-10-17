import arcade
from map_theforest import Map_F
from slingshot_theforest import Slingshot_fruit

SCREEN_WIDTH = 1910
SCREEN_HEIGHT = 900

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.control_fruit = Slingshot_fruit()
        self.map = Map_F(SCREEN_WIDTH, SCREEN_HEIGHT, self.control_fruit)
        self.control_fruit.sync(self.map)
        self.score_text = arcade.create_text("Score : "+str(self.map.score), arcade.color.BLACK, 50)
    def on_mouse_motion(self, x, y, dx, dy):
        self.control_fruit.on_mouse_motion(x,y)
    def on_mouse_press(self, x, y, button, modifiers):
        #print("(x,y) = ("+str(x)+","+str(y)+")")
        self.control_fruit.on_mouse_press(button)
    def on_mouse_release(self, x, y, button,modifiers):
        self.control_fruit.on_mouse_release(button)
    def on_draw(self):
        arcade.start_render()
        self.control_fruit.draw()
        self.map.draw()
        arcade.render_text(self.score_text, 1550, 800)
    def update(self, delta_time):
        self.control_fruit.update()
        self.map.update()        
        self.score_text = arcade.create_text("Score : "+str(self.map.score), arcade.color.BLACK, 50)

if __name__ == '__main__':
    runGame = GameWindow(SCREEN_WIDTH,SCREEN_HEIGHT,"TheForest")
    arcade.set_window(runGame)
    arcade.run()