import arcade
from sprite_theforest import Logo_sprite, Click_sprite

SCREEN_WIDTH = 1910
SCREEN_HEIGHT = 900

class Home_F:
    def __init__(self, mouse):
        self.background = arcade.load_texture("images/bg.jpg")
        self.mouse = mouse
        self.logo = Logo_sprite()
        self.click = Click_sprite()
        self.status = "not"
    def draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.logo.draw()
        self.click.draw()
    def update(self):
        if 635 < self.mouse.x and self.mouse.x < 1275 and 266 < self.mouse.y and self.mouse.y < 494 and self.mouse.click:
            self.status = "change"