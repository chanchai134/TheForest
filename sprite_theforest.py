import arcade
class Sprite_F(arcade.Sprite):
    def __init__(self, scr, model_theforest):
        super().__init__(scr)
        self.model = model_theforest
        self.sprite = arcade.Sprite(scr)
    def update(self):
        self.set_position(self.model.x, self.model.y)
    def draw(self):
        super().draw()