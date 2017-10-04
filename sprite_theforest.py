import arcade
ROPE_COLOR = (217,180,138)
class Sprite_F(arcade.Sprite):
    def __init__(self, scr, model_theforest):
        super().__init__(scr)
        self.model = model_theforest
        self.sprite = arcade.Sprite(scr)
    def update(self):
        self.set_position(self.model.x, self.model.y)
    def draw(self):
        super().draw()
class Slingshot_sprite(Sprite_F):
    def __init__(self, scr, model_theforest):
        super().__init__(scr, model_theforest)
    def draw_line(self, open_draw, start_x, start_y, end_x, end_y):
        if open_draw:
            arcade.draw_line(start_x, start_y, end_x, end_y, ROPE_COLOR, 4)