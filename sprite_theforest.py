import arcade

SCREEN_WIDTH = 1910
SCREEN_HEIGHT = 900
ROPE_COLOR = (217,180,138)

class Sprite_sprite(arcade.Sprite):
    def __init__(self, scr, model_theforest):
        super().__init__(scr)
        self.model = model_theforest
    def update(self):
        self.set_position(self.model.x, self.model.y)
    def draw(self):
        super().draw()

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

class Grape_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/grape.png", model_theforest)

class Banana_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/banana.png", model_theforest)

class Meat_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/meat.png", model_theforest)

class Worm_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/worm.png", model_theforest)

class Monkey_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/monkey.png", model_theforest)

class Dragon_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/dragon.png", model_theforest)

class Shoothill_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/shoothill.png", model_theforest)

class Ground_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/ground.png", model_theforest)

class Grass_sprite(Sprite_sprite):
    def __init__(self, model_theforest):
        super().__init__("images/grass.png", model_theforest)

class Score_sprite(arcade.Sprite):
    def __init__(self):
        super().__init__("images/score.png")
        self.center_x = SCREEN_WIDTH//2
        self.center_y = SCREEN_HEIGHT//2

class Win_sprite(arcade.Sprite):
    def __init__(self):
        super().__init__("images/win.png")
        self.center_x = SCREEN_WIDTH//2
        self.center_y = SCREEN_HEIGHT//2 + 240

class Lose_sprite(arcade.Sprite):
    def __init__(self):
        super().__init__("images/lose.png")
        self.center_x = SCREEN_WIDTH//2
        self.center_y = SCREEN_HEIGHT//2 + 240

class Click_sprite(arcade.Sprite):
    def __init__(self):
        super().__init__("images/click.png")
        self.center_x = SCREEN_WIDTH//2
        self.center_y = SCREEN_HEIGHT//2 - 70

class Logo_sprite(arcade.Sprite):
    def __init__(self):
        super().__init__("images/theforest.png")
        self.center_x = SCREEN_WIDTH//2
        self.center_y = SCREEN_HEIGHT//2 + 250