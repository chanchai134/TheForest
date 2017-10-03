import arcade
import model_theforest
import sprite_theforest

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
GRAVITY = 0.05

class GameWindow(arcade.Window):
    def __init__(self, width, height,title):
        super().__init__(width, height,title)
        arcade.set_background_color(arcade.color.BLACK)
    grape_setting = model_theforest.Grape_F(68,91,100,300,6,GRAVITY,45)
    grape_sprite = sprite_theforest.Sprite_F("images/grape.png",grape_setting)
    def on_draw(self):
        arcade.start_render()
        self.grape_sprite.draw()
    def update(self, delta):
        self.grape_setting.shoot()
        self.grape_sprite.update()

if __name__ == '__main__':
    runGame = GameWindow(SCREEN_WIDTH,SCREEN_HEIGHT,"TheForest")
    arcade.set_window(runGame)
    arcade.run()