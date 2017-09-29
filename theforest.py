import arcade
import library

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class GameWindow(arcade.Window):

    def __init__(self, width, height,title):
        super().__init__(width, height,title)
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        arcade.start_render()
    
#    def update(self, delta):

if __name__ == '__main__':
    runGame = GameWindow(SCREEN_WIDTH,SCREEN_HEIGHT,"TheForest")
    arcade.set_window(runGame)
    arcade.run()