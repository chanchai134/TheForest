import arcade

ROPE_COLOR = (217,180,138)

class Sprite_sprite(arcade.Sprite):
    def __init__(self, scr, model_theforest):
        super().__init__(scr)
        self.model = model_theforest
        self.sprite = arcade.Sprite(scr)
    def update(self):
        self.set_position(self.model.x, self.model.y)
    def draw(self):
        super().draw()

class Grape_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/grape.png", model_theforest)

class Slingshot_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/slingshot.png", model_theforest)
    def draw_line_R(self):
        if self.model.mouse.aimming :
            arcade.draw_line(self.model.shoot_x + 21,
                            self.model.shoot_y -3 ,
                            self.model.mouse.x,
                            self.model.mouse.y,
                            ROPE_COLOR,
                            5)
    def draw_line_L(self):
        if self.model.mouse.aimming :
            arcade.draw_line(self.model.shoot_x -38,
                            self.model.shoot_y -13 ,
                            self.model.mouse.x,
                            self.model.mouse.y,
                            ROPE_COLOR,
                            5)

class SlingshotHand_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/hand.png", model_theforest)
    def update(self):
        if self.model.mouse.aimming :
            self.set_position(self.model.mouse.x, self.model.mouse.y)
            self._set_angle(self.model.getAngle_degree())
    def draw(self):
        if self.model.mouse.aimming :
            super().draw()