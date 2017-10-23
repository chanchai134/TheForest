import arcade
from sprite_theforest import Score_sprite, Win_sprite, Lose_sprite

class Score_F:
    def __init__(self, mapP, mouse):
        self.score_BG = Score_sprite()
        self.show = Win_sprite()
        self.map = mapP
        self.mouse = mouse
        self.score_text = arcade.create_text("Score", arcade.color.BLACK, 50)
        self.bonus_text = arcade.create_text("Bonus", arcade.color.BLACK, 50)
        self.total_text = arcade.create_text("Total Score", arcade.color.BLACK, 50)
        self.score_num = arcade.create_text(str(self.map.score), arcade.color.BLACK, 50)
        self.bonus_num = arcade.create_text(str(self.map.bonus), arcade.color.BLACK, 50)
        self.total_num = arcade.create_text(str(self.map.score + self.map.bonus), arcade.color.BLACK, 50)
        self.status = "not"
    def draw(self):
        self.score_BG.draw()
        self.show.draw()
        arcade.render_text(self.score_text,630, 535)
        arcade.render_text(self.bonus_text,630, 415)
        arcade.render_text(self.total_text,630, 295)
        arcade.render_text(self.score_num,1200, 535)
        arcade.render_text(self.bonus_num,1200, 415)
        arcade.render_text(self.total_num,1200, 295)
    def update(self):
        self.score_num = arcade.create_text(str(self.map.score), arcade.color.BLACK, 50)
        self.bonus_num = arcade.create_text(str(self.map.bonus), arcade.color.BLACK, 50)
        self.total_num = arcade.create_text(str(self.map.score + self.map.bonus), arcade.color.BLACK, 50)
        if self.map.score + self.map.bonus < 1:
            self.show = Lose_sprite()
        else:
            self.show = Win_sprite()
        if 822 < self.mouse.x and self.mouse.x < 1090 and 150 < self.mouse.y and self.mouse.y < 227 and self.mouse.click:
            self.status = "change"