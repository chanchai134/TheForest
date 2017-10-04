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
class Slingshot_sprite(Sprite_F):
    def __init__(self, scr, model_theforest):
        super().__init__(scr, model_theforest)
        self.mouse_hold = None
        self.mouse_x = None
        self.mouse_y = None
    def updateMouse(self ,mouse_x, mouse_y, mouse_hold):
        self.mouse_hold = mouse_x
        self.mouse_x = mouse_y
        self.mouse_y = mouse_hold
    def update(self):
        super().update()
    def draw(self):
        super().draw()