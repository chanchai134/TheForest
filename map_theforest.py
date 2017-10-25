from model_theforest import Shoothill_config, Ground_config, Grass_config, Worm_config, Monkey_config, Dragon_config
from sprite_theforest import Shoothill_sprite, Ground_sprite, Grass_sprite, Worm_sprite, Monkey_sprite, Dragon_sprite
from random import randint
import arcade

RANGE_SPAW = 8
MAX_HIGHT_HILL = 5 

class Map_F:
    def __init__(self, width, height, world):
        self.width = width
        self.height = height
        self.shoothill_C = Shoothill_config(249,141)
        self.shoothill_S = Shoothill_sprite(self.shoothill_C)
        self.ground_Random = [] #couple(x1,x2)
        self.height_Random = {} #key = couple
        self.mapFixBox_C = []
        self.mapFixBox_S = []
        self.mapRandom_C = []
        self.mapRandom_S = []
        self.animal_C = []
        self.animal_S = []
        self.fruit = world.fruit_C
        self.world = world
        self.score = 0
        self.bonus = 0
        self.score_text = arcade.create_text("Score : "+str(self.score), arcade.color.BLACK, 50)
        self.bonus_text = arcade.create_text("Bonus : "+str(self.bonus), arcade.color.BLACK, 50)
        self.hint_text = arcade.create_text("Some food have special skill. Let click or hold to try it.", arcade.color.BLACK, 20)
        self.hint2_text = arcade.create_text("Some food that make animal like will give a bonus.", arcade.color.BLACK, 20)
        '''__Map Generator__'''
        start_x = 533
        ground_x = [start_x]
        while start_x + 35 < width:
            start_x += 71
            ground_x.append(start_x)
        ground_xRandom = []
        #Base
        for x in ground_x[-((RANGE_SPAW*2) + 1): -1]:
            ground_xRandom.append(x)
            self.mapFixBox_C.append(Ground_config(x, 107))
            self.mapFixBox_S.append(Ground_sprite(self.mapFixBox_C[-1]))
        for x in ground_x[: -((RANGE_SPAW*2) + 1)]:
            self.mapFixBox_C.append(Grass_config(x, 106))
            self.mapFixBox_S.append(Grass_sprite(self.mapFixBox_C[-1]))
        self.mapFixBox_C.append(Grass_config(ground_x[-1], 106))
        self.mapFixBox_S.append(Grass_sprite(self.mapFixBox_C[-1]))
        for x in ground_x:
            self.mapFixBox_C.append(Ground_config(x, 36))
            self.mapFixBox_S.append(Ground_sprite(self.mapFixBox_C[-1]))
        for i in range(0, len(ground_xRandom), 2):
            self.ground_Random.append((ground_xRandom[i], ground_xRandom[i+1]))
        #HillRandoms
        for i in self.ground_Random:
            self.height_Random[i] = randint(1,MAX_HIGHT_HILL)
        if not(self.canDragonSpawn()):
            index_temp = randint(2,RANGE_SPAW)-1
            self.height_Random[self.ground_Random[index_temp]] = self.height_Random[self.ground_Random[index_temp-1]]
        for x1, x2 in self.ground_Random:
            self.mapRandom_C.append(Grass_config(x1, self.YGrass(self.height_Random[(x1,x2)])))
            self.mapRandom_C.append(Grass_config(x2, self.YGrass(self.height_Random[(x1,x2)])))
            self.mapRandom_S.append(Grass_sprite(self.mapRandom_C[-1]))            
            self.mapRandom_S.append(Grass_sprite(self.mapRandom_C[-2]))
            for i in range(self.height_Random[(x1,x2)]-1, 0, -1):
                self.mapRandom_C.append(Ground_config(x1, self.Ylevel(i)))
                self.mapRandom_C.append(Ground_config(x2, self.Ylevel(i)))
                self.mapRandom_S.append(Ground_sprite(self.mapRandom_C[-1]))
                self.mapRandom_S.append(Ground_sprite(self.mapRandom_C[-2]))
        #Generate Monster
        i = 0
        while i < len(self.ground_Random):
            y = self.Ylevel(self.height_Random[self.ground_Random[i]])
            yN = 0
            xCenter = (self.ground_Random[i][0] + self.ground_Random[i][1])/2
            if i != len(self.ground_Random)-1:
                yN = self.Ylevel(self.height_Random[self.ground_Random[i+1]])
            if y == yN :
                animal_No = randint(1,3)
                if animal_No != 3:
                    animal_No = randint(1,3)
                if animal_No != 3:
                    animal_No = randint(1,3)
                if animal_No == 1:
                    xCenter = (self.ground_Random[i][0] + self.ground_Random[i][1])/2
                    self.animal_C.append(Worm_config(xCenter, y + 90))   
                    self.animal_S.append(Worm_sprite(self.animal_C[-1]))
                    i += 1
                elif animal_No == 2:
                    xCenter = (self.ground_Random[i][0] + self.ground_Random[i][1])/2
                    self.animal_C.append(Monkey_config(xCenter, y + 100))   
                    self.animal_S.append(Monkey_sprite(self.animal_C[-1]))
                    i += 1
                else :
                    xCenter = (self.ground_Random[i][1] + self.ground_Random[i+1][0])/2
                    self.animal_C.append(Dragon_config(xCenter, y + 150))   
                    self.animal_S.append(Dragon_sprite(self.animal_C[-1]))
                    i += 2
            else :
                animal_No = randint(1,2)
                xCenter = (self.ground_Random[i][0] + self.ground_Random[i][1])/2
                if animal_No == 1:
                    self.animal_C.append(Worm_config(xCenter, y + 90))   
                    self.animal_S.append(Worm_sprite(self.animal_C[-1]))
                elif animal_No == 2:
                    self.animal_C.append(Monkey_config(xCenter, y + 100))   
                    self.animal_S.append(Monkey_sprite(self.animal_C[-1]))
                i += 1
    def draw(self):
        self.shoothill_S.draw()
        for hill in self.mapRandom_S:
            hill.draw()
        for box in self.mapFixBox_S:
            box.draw()
    def draw_animal(self):
        for animal in self.animal_S:
            animal.draw()
    def draw_text(self):
        arcade.render_text(self.score_text, 1550, 800)
        arcade.render_text(self.bonus_text, 1550, 720)
        arcade.render_text(self.hint_text, 685, 60)
        arcade.render_text(self.hint2_text, 700, 25)
    def update(self):
        self.shoothill_S.update()
        for hill in self.mapRandom_S:
            hill.update()
        for box in self.mapFixBox_S:
            box.update()
        for animal in self.animal_S:
            animal.update()
            if animal.model.isHit(self.fruit):
                if animal.model.tag == "dragon":
                    self.score += 90
                else:
                    self.score += 50
                if animal.model.tag == "dragon" and self.fruit.tag == "meat":
                    self.bonus += 10
                elif animal.model.tag == "monkey" and self.fruit.tag == "banana":
                    self.bonus += 10
                elif animal.model.tag == "worm" and self.fruit.tag == "grape":
                    self.bonus += 10
                self.animal_C.remove(animal.model)
                self.animal_S.remove(animal)
                self.world.fruit_C = self.world.random_fruit()
                self.world.fruit_S = self.world.Get_sprite(self.world.fruit_C)
                self.fruit = self.world.fruit_C     
                self.world.mouse.reset_mouse()
        if self.shoothill_C.isHit(self.fruit):
            self.world.fruit_C = self.world.random_fruit()
            self.world.fruit_S = self.world.Get_sprite(self.world.fruit_C)
            self.fruit = self.world.fruit_C
            self.world.mouse.reset_mouse()
            self.score -= 10
        for box in self.mapRandom_C:
            if box.isHit(self.fruit):
                self.world.fruit_C = self.world.random_fruit()
                self.world.fruit_S = self.world.Get_sprite(self.world.fruit_C)
                self.fruit = self.world.fruit_C
                self.world.mouse.reset_mouse()
                self.score -= 10
        for box in self.mapFixBox_C:
            if box.isHit(self.fruit):
                self.world.fruit_C = self.world.random_fruit()
                self.world.fruit_S = self.world.Get_sprite(self.world.fruit_C)
                self.fruit = self.world.fruit_C
                self.world.mouse.reset_mouse()
                self.score -= 10 
        self.score_text = arcade.create_text("Score : "+str(self.score), arcade.color.BLACK, 50)
        self.bonus_text = arcade.create_text("Bonus : "+str(self.bonus), arcade.color.BLACK, 50)
    def debug(self):
        for animal in self.animal_C:
            animal.debug()
    def Ylevel(self, y):
        return 107 + (71*y)
    def YGrass(self, y):
        return 106 + (71*y)
    def canDragonSpawn(self):
        for i in range(1, RANGE_SPAW):
            if self.height_Random[self.ground_Random[i]] == self.height_Random[self.ground_Random[i-1]]:
                return True
        return False