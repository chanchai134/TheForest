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
    def draw_line_R(self, open_draw, shoot_x, shoot_y, end_x, end_y):
        if open_draw:
            arcade.draw_line(shoot_x + 21, shoot_y -3 , end_x, end_y, ROPE_COLOR, 5)
    def draw_line_L(self, open_draw, shoot_x, shoot_y, end_x, end_y):
        if open_draw:
            arcade.draw_line(shoot_x -38 , shoot_y -13 , end_x, end_y, ROPE_COLOR, 5)

class Hand_sprite(Sprite_F):
    def __init__(self, scr, model_theforest):
        super().__init__(scr, model_theforest)
    def update(self):
        if self.model.mouse_hold:
            self.set_position(self.model.mouse_x, self.model.mouse_y)
            self._set_angle(self.model.getAngle_degree())
    def draw(self):
        if self.model.mouse_hold:
            super().draw()