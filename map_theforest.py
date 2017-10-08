from model_theforest import Shoothill_config, Ground_config, Grass_config
from sprite_theforest import Shoothill_sprite, Ground_sprite, Grass_sprite
from random import randint

RANGE_SPAW = 8
MAX_HIGHT_HILL = 5

class Map_F:
    def __init__(self,width,height):
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
    def draw(self):
        self.shoothill_S.draw()
        for hill in self.mapRandom_S:
            hill.draw()
        for box in self.mapFixBox_S:
            box.draw()
    def update(self):
        self.shoothill_S.update()
        for hill in self.mapRandom_S:
            hill.update()
        for box in self.mapFixBox_S:
            box.update()
    def Ylevel(self, y):
        return 107 + (71*y)
    def YGrass(self, y):
        return 106 + (71*y)
    def canDragonSpawn(self):
        for i in range(1, RANGE_SPAW):
            if self.height_Random[self.ground_Random[i]] == self.height_Random[self.ground_Random[i-1]]:
                return True
        return False

        