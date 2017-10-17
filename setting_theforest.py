class Mouse_C:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.aimming = False
        self.shooting = False
        self.canCaught = False
        self.click = False
    def reset_mouse(self):
        self.aimming = False
        self.shooting = False
        self.canCaught = False