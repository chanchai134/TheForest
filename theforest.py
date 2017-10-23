import arcade
from map_theforest import Map_F
from slingshot_theforest import Slingshot_fruit
from score_theforeset import Score_F
from home_theforest import Home_F

SCREEN_WIDTH = 1910
SCREEN_HEIGHT = 900

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.status = "home"
        self.control_fruit = Slingshot_fruit()
        self.map = Map_F(SCREEN_WIDTH, SCREEN_HEIGHT, self.control_fruit)
        self.control_fruit.sync(self.map)
        self.scoreboard = Score_F(self.map, self.control_fruit.mouse)
        self.home = Home_F(self.control_fruit.mouse)
    def on_mouse_motion(self, x, y, dx, dy):
        self.control_fruit.on_mouse_motion(x,y)
    def on_mouse_press(self, x, y, button, modifiers):
        #print("(x,y) = ("+str(x)+","+str(y)+")")
        self.control_fruit.on_mouse_press(button)
    def on_mouse_release(self, x, y, button,modifiers):
        self.control_fruit.on_mouse_release(button)
    def on_draw(self):
        arcade.start_render()
        if self.status == "game":
            self.control_fruit.draw()
            self.map.draw()
            self.map.draw_text()
            self.map.draw_animal()
        elif self.status == "scoreboard":
            self.control_fruit.draw()
            self.map.draw()
            self.scoreboard.draw()
        else:
            self.home.draw()
    def update(self, delta_time):
        if self.status == "game":
            self.control_fruit.update()
            self.map.update()
            if not self.map.animal_C:
                self.status = "scoreboard"
                self.control_fruit.mouse.shooting = True
        elif self.status == "scoreboard":
            self.scoreboard.update()
            if self.scoreboard.status == "change":
                self.status = "home"
                self.control_fruit = Slingshot_fruit()
                self.map = Map_F(SCREEN_WIDTH, SCREEN_HEIGHT, self.control_fruit)
                self.control_fruit.sync(self.map)
                self.scoreboard = Score_F(self.map, self.control_fruit.mouse)
                self.home = Home_F(self.control_fruit.mouse)
        else:
            self.home.update()
            if self.home.status == "change":
                self.status = "game"
if __name__ == '__main__':
    runGame = GameWindow(SCREEN_WIDTH,SCREEN_HEIGHT,"TheForest")
    arcade.set_window(runGame)
    arcade.run()