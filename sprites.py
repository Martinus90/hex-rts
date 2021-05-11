import pygame as pg
import loading as ld
import inspect
from hexo import *
from settings import *
from queue import PriorityQueue

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, side):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.plr_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.side = side

    def move(self, dx=0, dy=0):
        self.x += dx# * TILESIZE[0]
        self.y += dy# * TILESIZE[1]

    def update(self):
        #self.get_keys()
        self.rect.x = (self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2) - TILESIZE[0]/2
        self.rect.y = (self.y * TILESIZE[1]) - TILESIZE[0]/2
        #self.rect.topleft = (self.x, self.y)

class Grid(pg.sprite.Sprite):
    def __init__(self, game, x, y, terrain, idnr, gid, owner=None):
        self.groups = game.grids
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.terrain = terrain
        self.gid = gid
        self.owner = owner

        self.x = x
        self.y = y
        self.id = idnr
        self.neighbors = []
        self.resource = None
        self.near_resources = []
        self.building = None
        

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self) #self.hex = Hex(?,?,?)

        self.q, self.r, self.s = self.hex

    def get_neighbors(self, map):
        #print("Hex")
        #print(self.id)
        #print("neighbors:")
        for i in range(6):
            #print(hex_id(-1, hex_neighbor(self.hex, i), width))
            if hex_neighbor(self.hex, i) in map.grid_list:
                new_neighbor = hex_neighbor(self.hex, i)
                n = hex_id(-1, hex_neighbor(self.hex, i), map.tmxdata.width)
                self.neighbors.append(self.game.map.grids[n])
            else:
                pass 

    def get_near_resources(self):
        self.near_resources = []
        for n in self.neighbors:
            if n.resource != None:
                self.near_resources.append(n.resource)

    def get_hex(self):
        return self.hex

    def get_pos(self):
        return self.x, self.y

class Resource(pg.sprite.Sprite):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[0]
        self.image = self.game.resource_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 0
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        #print(self.grid_id)
        self.game.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

    def do(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        pass

    def seasons(self):
        pass

class Tree(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[1]
        self.image = self.game.tree_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 3
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

    def daily(self):
        self.value += 1

class Grain(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[2]
        self.image = self.game.grain_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 0
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class Oil(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[3]
        self.image = self.game.oil_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 0
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class Iron(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[4]
        self.image = self.game.iron_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 1
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class Coal(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[5]
        self.image = self.game.coal_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 1
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class Calcium(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[6]
        self.image = self.game.calcium_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 1
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class Silicon(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[7]
        self.image = self.game.silicon_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 1
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class Cotton(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[8]
        self.image = self.game.cotton_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 0
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class Rubber(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[9]
        self.image = self.game.rubber_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 3
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class Bauxite(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[10]
        self.image = self.game.bauxite_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 1
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class Uranium(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[11]
        self.image = self.game.uranium_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 1
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class Water(Resource):
    def __init__(self, game, x, y, value):
        self.groups = game.all_sprites, game.resources
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = game.language.RESOURCES[12]
        self.image = self.game.water_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.value = value
        self.off_road_value = 0
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

class CONSTRUCTION(pg.sprite.Sprite):
    def __init__(self, game, x, y, what, owner, wood=0, cement=0, steel=0, progress=0):
        self.groups = game.all_sprites, game.buildings#, game.grids[]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.what = what
        self.owner = self.game.players[owner]

        self.name = game.language.BUILDINGS1[0]
        self.image = self.game.construction_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * (TILESIZE[0] / 2)
        self.rect.y = self.y * TILESIZE[1]
        self.storage = {}
        
        self.side = self.owner.side
        self.grid = self.game.map.grids[self.col + self.row * self.game.map.tmxdata.height]
        self.grid.building = self
        self.materials = {'wood':wood, 'cement':cement, 'steel':steel}
        self.fullmaterials = {}
        self.cost = globals()[self.what.upper()+"_COST"]
        self.fullcost = sum(self.cost.values())
        self.fullmaterials = sum(self.materials.values())
        self.progress = progress
        self.description = [self.owner.name, self.name, self.what, self.print_progress(), "", "", "","","",""]

        #self.screen.blit(self.building.owner.image, (WIDTH - MENU_RIGHT[0]+10, 412))

        #self.description[4] = ""
        #for m in self.materials.items():
        #    self.description[4] += str(m[0]) + ": " + str(m[1]) + ", "

        #self.description[4] = 
        #print(self.materials['wood'])

        self.description[4] = self.game.language.RES1[0] + ": " + str(self.materials['wood']) + "/" + str(self.cost['wood'])
        self.description[5] = self.game.language.RES1[2] + ": " + str(self.materials['cement']) + "/" + str(self.cost['cement'])
        self.description[6] = self.game.language.RES1[5] + ": " + str(self.materials['steel']) + "/" + str(self.cost['steel'])

        self.description[5] = ""
        for c in self.cost.items():
            self.description[5] += str(c[0]) + ": " + str(c[1]) + ", "
        
    def print_progress(self):
        return "Progress: " + str(self.progress) + " / " + str(self.fullcost)
        
    def construction(self, value):
        if (self.fullmaterials - self.progress) >= value:
            self.progress += value
        else:
            self.progress += (self.fullmaterials - self.progress)

    def hourly(self):
        pass

    def daily(self):
        if self.progress >= self.fullmaterials:
            print("Koniec budowy.")
            if self.game.building == self:
                self.game.building = None
            #test
            self.game.build(self)

    def update(self):
        self.fullmaterials = sum(self.materials.values())

        self.description[3] = self.print_progress()#str(self.progress)
        self.description[4] = ""
        self.description[5] = ""
        self.description[6] = ""
        for m in self.materials.items():
            self.description[4] += m[0].title() + ": " + str(m[1]) + ", "
        if not self.materials:
            self.description[4] = "None"
        #for c in self.cost.items():
        #    self.description[5] += c[0].title() + ": " + str(c[1]) + ", "

        self.description[4] = self.game.language.RES1[0] + ": " + str(self.materials['wood']) + "/" + str(self.cost['wood'])
        self.description[5] = self.game.language.RES1[2] + ": " + str(self.materials['cement']) + "/" + str(self.cost['cement'])
        self.description[6] = self.game.language.RES1[5] + ": " + str(self.materials['steel']) + "/" + str(self.cost['steel'])

class SETTLEMENT(pg.sprite.Sprite):
    def __init__(self, game, x, y, owner, name, nationality, population):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.resource_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.owner = owner

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]
        self.storage = {}


        self.name = name
        self.population = name
        self.side = self.owner.side
        self.grid = self.game.map.grids[self.col + self.row * self.game.map.tmxdata.height]
        self.grid.building = self

    def hourly(self):
        pass

    def daily(self):
        pass

class VILLAGE(SETTLEMENT):
    def __init__(self, game, x, y, owner=0, name="New", nationality=0, population=0, food=0, wood=0):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = name
        self.nationality = self.game.nations[nationality]
        self.population = population

        self.image = self.game.village_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {'food': food, 'wood': wood}
        self.grid_with_res = []
        self.sum_res = []

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[self.col + self.row * self.game.map.tmxdata.height]
        self.grid.building = self
        self.description = [self.owner.name, self.name, "Pop: " + str(self.population), self.game.language.GUI[0], self.game.language.RESOURCES[2] + ":", self.game.language.RESOURCES[1] + ":","","","",""]
        #here near resources 
        self.resources_near_building()

    def resources_near_building(self):
        self.grid_with_res = []
        self.sum_res = []
        self.sum_res.append(0)
        self.game.map.grids[self.hexid].get_near_resources()
        if self.game.map.grids[self.hexid].resource != None:
            if self.game.map.grids[self.hexid].resource.name == self.game.language.RESOURCES[2]:
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[0] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[2]:
                    self.grid_with_res.append(a)
                    self.sum_res[0] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if self.game.map.grids[self.hexid].resource.name == self.game.language.RESOURCES[1]:
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[1] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[1]:
                    self.grid_with_res.append(a)
                    self.sum_res[1] += a.resource.value

        self.description[4] = self.game.language.RESOURCES[2] + ": " + str(self.sum_res[0])
        self.description[5] = self.game.language.RESOURCES[1] + ": " + str(self.sum_res[1])
        
    def hourly(self):
        pass
    
    def daily(self):
        e = round(self.population / (50), 2)
        self.resources_near_building()
        for d in self.grid_with_res:
            if d.resource.value > e:
                if d.resource.name == self.game.language.RESOURCES[2]:  #food
                    self.storage['food'] += e
                    d.resource.value -= e
                if d.resource.name == self.game.language.RESOURCES[2]:  #food
                    self.storage['food'] += e
                    d.resource.value -= e

class BUILDING(pg.sprite.Sprite):
    def __init__(self, game, x, y, owner):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]

        self.name = game.language.BUILDINGS1[0]
        self.image = self.game.resource_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        self.storage = {}

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[self.col + self.row * self.game.map.tmxdata.height]
        self.grid.building = self
        self.description = [self.owner.name, self.name, "", "", "", "", "","","",""]

    def hourly(self):
        pass

    def daily(self):
        pass

class OIL_WELL(BUILDING):
    def __init__(self, game, x, y, owner, oil=0):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[9]

        self.image = self.game.oil_well_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {'oil': oil}
        self.grid_with_res = []
        self.sum_res = 0

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[self.col + self.row * self.game.map.tmxdata.height]
        self.grid.building = self
        self.description = [self.owner.name, self.name, "", self.game.language.GUI[0], self.game.language.RESOURCES[3] + ": ","","","","",""]
        #here near resources 
        self.resources_near_building()

    def resources_near_building(self):
        self.grid_with_res = []
        self.sum_res = 0
        self.game.map.grids[self.hexid].get_near_resources()
        if self.game.map.grids[self.hexid].resource != None:
            if self.game.map.grids[self.hexid].resource.name == self.game.language.RESOURCES[3]:
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[3]:
                    self.grid_with_res.append(a)
                    self.sum_res += a.resource.value

        self.description[4] = self.game.language.RESOURCES[3] + ": " + str(self.sum_res)
        
    def hourly(self):
        pass

    def daily(self):
        pass
        #(round(self.men * 3 / 20, 2))

class MINE(BUILDING):
    def __init__(self, game, x, y, owner=0, iron=0, coal=0, calcium=0, silicon=0, bauxite=0, uranium=0):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[7]

        self.image = self.game.mine_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {'iron': iron, 'coal': coal, 'calcium': calcium, 'silicon': silicon, 'bauxite': bauxite, 'uranium': uranium}
        self.grid_with_res = []
        self.sum_res = 0

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[self.col + self.row * self.game.map.tmxdata.height]
        self.grid.building = self
        self.description = [self.owner.name, self.name, "", self.game.language.GUI[0], "","","","","",""]
        #here near resources 
        self.resources_near_building()

    def resources_near_building(self):
        self.grid_with_res = []
        self.sum_res = []
        self.sum_res.append(0)
        self.game.map.grids[self.hexid].get_near_resources()
        if self.game.map.grids[self.hexid].resource != None:
            if self.game.map.grids[self.hexid].resource.name == self.game.language.RESOURCES[4]:
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[0] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[4]:
                    self.grid_with_res.append(a)
                    self.sum_res[0] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if self.game.map.grids[self.hexid].resource.name == self.game.language.RESOURCES[5]:
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[1] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[5]:
                    self.grid_with_res.append(a)
                    self.sum_res[1] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if self.game.map.grids[self.hexid].resource.name == self.game.language.RESOURCES[6]:
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[2] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[6]:
                    self.grid_with_res.append(a)
                    self.sum_res[2] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if self.game.map.grids[self.hexid].resource.name == self.game.language.RESOURCES[7]:
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[3] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[7]:
                    self.grid_with_res.append(a)
                    self.sum_res[3] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if self.game.map.grids[self.hexid].resource.name == self.game.language.RESOURCES[10]:
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[4] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[10]:
                    self.grid_with_res.append(a)
                    self.sum_res[4] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if self.game.map.grids[self.hexid].resource.name == self.game.language.RESOURCES[11]:
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[5] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[11]:
                    self.grid_with_res.append(a)
                    self.sum_res[5] += a.resource.value

        self.description[4] = self.game.language.RESOURCES[4] + ": " + str(self.sum_res[0])
        self.description[5] = self.game.language.RESOURCES[5] + ": " + str(self.sum_res[1])
        self.description[6] = self.game.language.RESOURCES[6] + ": " + str(self.sum_res[2])
        self.description[7] = self.game.language.RESOURCES[7] + ": " + str(self.sum_res[3])
        self.description[8] = self.game.language.RESOURCES[10] + ": " + str(self.sum_res[4])
        self.description[9] = self.game.language.RESOURCES[11] + ": " + str(self.sum_res[5])
        
    def hourly(self):
        pass

    def daily(self):
        pass
        #(round(self.men * 3 / 20, 2))

class RAFINERY(BUILDING):
    def __init__(self, game, x, y, owner=0, oil=0, fuel=0, calcium=0, cement=0, coal=0):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[10]

        self.image = self.game.rafinery_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {'oil': oil, 'fuel': fuel, 'calcium': calcium, 'cement': cement, 'coal': coal}

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[self.col + self.row * self.game.map.tmxdata.height]
        self.grid.building = self
        self.description = [self.owner.name, self.name, "", self.game.language.GUI[4], "","","","","",""]
        #here near resources 

        self.description[4] = self.game.language.RES1[10] + ": " + str(self.storage['oil'])
        self.description[5] = self.game.language.RES1[11] + ": " + str(self.storage['fuel'])
        self.description[6] = self.game.language.RES1[16] + ": " + str(self.storage['calcium'])
        self.description[7] = self.game.language.RES1[2] + ": " + str(self.storage['cement'])
        self.description[8] = self.game.language.RES1[4] + ": " + str(self.storage['coal'])
        
    def hourly(self):
        e = round(100 / (50), 2)
        if self.storage['oil'] > e:
            self.storage['oil'] -= e
            self.storage['fuel'] += (e * 2)
        if self.storage['calcium'] > e:
            self.storage['calcium'] -= e
            self.storage['cement'] += (e * 2)

        self.description[4] = self.game.language.RES1[10] + ": " + str(self.storage['oil'])
        self.description[5] = self.game.language.RES1[11] + ": " + str(self.storage['fuel'])
        self.description[6] = self.game.language.RES1[16] + ": " + str(self.storage['calcium'])
        self.description[7] = self.game.language.RES1[2] + ": " + str(self.storage['cement'])
        self.description[8] = self.game.language.RES1[4] + ": " + str(self.storage['coal'])        
        
    def daily(self):
        pass
        #(round(self.men * 3 / 20, 2))


class Unit(pg.sprite.Sprite):
    def __init__(self, game, x, y, owner, typ, unit_name, brigade, regiment, battalion, company, men, supply, uniforms, fuel, light_ammo, heavy_ammo, rockets, rifle, art, truck, apc, tank, heli, aircraft):
        self.groups = game.all_sprites, game.units
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.side = self.owner.side
        self.unit_typ = self.game.types[typ]
        self.typ = self.unit_typ.typ
        self.unit_name = unit_name
        self.brigade = brigade
        self.regiment = regiment
        self.battalion = battalion
        self.company = company
        self.state = {"mobilized": True, "training": False, "refill_equipment": False, "refill_crew": False, "building": False, "patroling": False, "engage": False}

        self.mobilized = True
        self.training = False
        self.refill_equipment = False
        self.refill_crew = False
        self.building = False

        self.combat_ability = 20
        self.combat_ability_max = 20
        self.experience = 0
        self.tiredness = 0
        self.tiredness_max = 20
        self.task = self.game.language.COMMANDS[0]
        
        self.men = men
        self.supply = supply
        self.uniforms = uniforms
        self.fuel = fuel

        self.light_ammo = light_ammo
        self.heavy_ammo = heavy_ammo
        self.rockets = rockets
        
        self.rifle = rifle
        self.art = art
        self.truck = truck
        self.apc = apc
        self.tank = tank
        self.heli = heli
        self.aircraft = aircraft

        self.visible = True
        self.pos = [50, 50]
        self.window = ld.Unit_Window(self, self.game, [100, 100], (500, 400), DARKGREY, self.unit_name + self.game.language.UNIT_STRU_SHORT[0] + str(self.brigade) + self.game.language.UNIT_STRU_SHORT[1] + str(self.regiment) + self.game.language.UNIT_STRU_SHORT[2] + str(self.battalion) + self.game.language.UNIT_STRU_SHORT[3] + str(self.company), 16, LIGHTGREY, (35, 10), 2)

        self.button = ld.OU_Button(self, self.game, pos=[WIDTH - MENU_RIGHT[0]+130, 230], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK) 
        
        
        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)

        self.image = pg.Surface((TILESIZE[0], TILESIZE[0]))
        self.image.fill(VIOLET)
        self.image.set_colorkey(VIOLET)

        #white / red / blue / green /yellow / lime / orange / grey / purple / brown / and other flag from onwers
        self.image.blit(self.owner.image, FLAG_OFFSET)

        #infantry / panc / arty / mech / recon / mot / other / support / heli / air / antiair / antipanc / engin / rocket
        #self.img_typ = self.image.blit(self.game.units_img.copy(), UNIT_OFFSET, (0, self.typ*UNIT_SIZE[1], UNIT_SIZE[0], UNIT_SIZE[1]))
        self.image.blit(self.unit_typ.image, UNIT_OFFSET)

        self.step_to = None
        self.go_to = None
        self.path = None
        self.return_to = None
        self.doing = 0.0
        self.last_step_cost = 0
        self.step_cost = 0

        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILESIZE[0] - self.y % 2 * TILESIZE[0] / 2 #+ FLAG_OFFSET[0]
        self.rect.y = self.y * TILESIZE[1] #+ FLAG_OFFSET[1]

        #self.description = [self.owner.name, self.unit_typ.name, self.task, str(self.men), self.game.language.DESCRIPTION[0] + ": " + str(self.experience), "Sixth"]
        self.description = [self.owner.name, 
                            self.unit_typ.name, 
                            self.print_mobilized(), 
                            self.game.language.DESCRIPTION[2] + ": " + str(self.combat_ability), 
                            self.game.language.DESCRIPTION[0] + ": " + str(self.experience), 
                            self.game.language.DESCRIPTION[7] + ": " + str(self.tiredness) + "/" + str(self.tiredness_max),
                            self.task]

    #def print_side(self):
    #    return self.owner.name
    def print_mobilized(self):
        if self.state["mobilized"] == True:
            return self.game.language.DESCRIPTION[1] + ": " + self.game.language.BASIC[2]
        else:
            return self.game.language.DESCRIPTION[1] + ": " + self.game.language.BASIC[3]
    #def print_typ(self):
    #    return self.unit_typ.name
        #if self.typ == 0:
        #    return self.game.typ_0
        #elif self.typ == 1:
        #    return self.game.typ_1
            
    def terrain_cost(self, grid_id):
        global c
        global t

        t = self.game.map.grids[grid_id].terrain

        #if self.typ == 0 and self.fuel >= self.unit_typ.fuel_usage:
        if self.fuel >= self.unit_typ.fuel_usage:
            t = self.game.map.grids[grid_id].terrain
            if t == self.game.language.TERRAIN[0]:
                c = self.unit_typ.s_normal
            elif t == self.game.language.TERRAIN[1]:
                c = self.unit_typ.s_normal
            elif t == self.game.language.TERRAIN[2]:
                c = self.unit_typ.s_water
            elif t == self.game.language.TERRAIN[3]:
                c = self.unit_typ.s_mountain
            elif t == self.game.language.TERRAIN[4]:
                c = self.unit_typ.s_coast
            elif t == self.game.language.TERRAIN[5]:
                c = self.unit_typ.s_river
            elif t == self.game.language.TERRAIN[6]:
                c = self.unit_typ.s_normal
        else:
            c = 20
        #return int(c)
        return c #self.unit_typ.move_cost(t)

    def add_materials(self):
        pass

    def check_grid(self):
        if self.game.map.grids[self.col + self.row * self.game.map.tmxdata.height].building != None:
            print("There is building")
        else:
            print("There is clear area to build something.")

    def stop(self):
        self.go_to = None
        self.step_to = None
        self.frontier = PriorityQueue()
        self.came_from = dict()
        self.cost_so_far = dict()
        self.doing = 0
        self.path = []
        self.step_cost = 0
        self.last_step_cost = 0
        
    def make_path(self, go_to):
        self.go_to = go_to
        if self.state["patroling"] == True:
            self.return_to = roffset_to_cube(-1, self)
        else:
            self.return_to = None
        self.step_to = None
        self.frontier = PriorityQueue()
        self.frontier.put((0, self.hexid))
        self.came_from = dict()
        self.cost_so_far = dict()
        self.came_from[self.hexid] = None
        self.cost_so_far[self.hexid] = 0
        self.doing = 0.0
        self.path = []
        self.step_cost = 0
        self.last_step_cost = 0
        

        while not self.frontier.empty():
            self.current = self.frontier.get()
            for next in self.game.map.grids[self.current[1]].neighbors:
                for a in self.game.resources:
                    if a.grid_id == next.id:
                        additional = a.off_road_value
                        break
                    else:
                        additional = 0

                self.new_cost = self.cost_so_far[self.current[1]] + ((self.terrain_cost(self.current[1]) + self.terrain_cost(next.id))) / 2 + additional
                #self.terrain_cost(next.id)
                if next.id not in self.cost_so_far or self.new_cost < self.cost_so_far[next.id]:
                    self.cost_so_far[next.id] = self.new_cost
                    self.priority = self.new_cost
                    self.frontier.put((self.priority, next.id))
                    self.came_from[next.id] = self.current[1]
            if self.current[1] == hex_id(OFFSET, self.go_to, self.game.map.tmxdata.width):
                break

        self.current = hex_id(OFFSET, self.go_to, self.game.map.tmxdata.width)
        self.path = []
        while self.current != self.hexid: 
            self.path.append(self.current)
            self.current = self.came_from[self.current]
        #self.path.append(self.hexid) # optional
        #self.path.reverse() # optional
        print("Start:")
        print(self.hexid)
        print("Path:")
        print(self.path)
        print("Full move cost:")
        for p in self.path:
            print(self.cost_so_far[p])
            break
        print(" ")

    def do(self):
        if self.go_to != None:
            print(self.doing)
            if self.go_to == self.hex:
                print("Na miejscu")
                if self.state["patroling"] == True and self.return_to != None:
                    self.make_path(self.return_to)
                else:
                    self.stop()
                    self.task = self.game.language.COMMANDS[0]
            else:    
                if self.step_to == None:
                    if len(self.path) != 0:
                        self.step_to = self.path.pop()
                        self.step_cost = self.cost_so_far[self.step_to] - self.last_step_cost
                    else:
                        print("Teoretycznie nie powinno do tego dojść / test")
                        print("Koniec drogi")
                        self.stop()

                if self.step_to != None:
                    self.task = self.game.language.COMMANDS[1] + str(roffset_from_cube(-1, self.go_to)[0]) + ", " + str(roffset_from_cube(-1, self.go_to)[1])       
                    if self.fuel < self.unit_typ.fuel_usage:
                        #moving without fuel
                        if self.doing >= self.step_cost:
                            self.doing = self.doing - self.step_cost
                            self.hex = self.game.map.grids[self.step_to].hex
                            print("No fuel / Moving slowly")
                            #self.task = self.game.language.COMMANDS[1] + str(roffset_from_cube(-1, self.go_to)[0]) + ", " + str(roffset_from_cube(-1, self.go_to)[1])
                            print(self.step_to)
                            print("Koszt:")
                            print(self.step_cost)
                            print(" ")
                            self.last_step_cost = self.cost_so_far[self.step_to]
                            self.step_to = None
                    else:
                        if self.doing >= self.step_cost:
                            self.doing = self.doing - self.step_cost
                            self.hex = self.game.map.grids[self.step_to].hex
                            print("Kroczek w stronę:")
                            #self.task = self.game.language.COMMANDS[1] + str(roffset_from_cube(-1, self.go_to)[0]) + ", " + str(roffset_from_cube(-1, self.go_to)[1])
                            print(self.step_to)
                            print("Koszt:")
                            print(self.step_cost)
                            print(" ")
                            self.last_step_cost = self.cost_so_far[self.step_to]
                            self.step_to = None
            self.doing += 1
            if self.fuel > 0:
                self.fuel = self.fuel - self.unit_typ.fuel_usage
                if self.fuel < self.unit_typ.fuel_usage:
                    self.stop()
                    self.fuel = 0
            else:
                self.fuel = 0
        else:
            self.doing = 0
            self.task = self.game.language.COMMANDS[0]

        if self.state["training"] == True:
                self.combat_ability = 5
                self.task = self.game.language.COMMANDS[2]
        
        if self.state['mobilized'] == True:
            if self.state['building'] == True:
                self.combat_ability_max = 15
            else:
                self.combat_ability_max = 25
        else:
            self.combat_ability_max = 5

    def refill_eq(self):
        if self.game.map.grids[self.hexid].building != None:
            print('Tu jest jakiś budynek. Sprawdź czy możesz się uzupełnić.')
            a = self.game.map.grids[self.hexid].building
            if 'fuel' in a.storage.keys() and a.owner == self.owner:
            #if a.storage['fuel']
                print("Tu jest paliwo do zatankowania.")
                if a.storage['fuel'] > 100:
                    a.storage['fuel'] -= 100
                    self.fuel += 100
            else:
                print("Nie ma tu paliwa.")
        else:
            print("Nie ma budynku.")

    def hourly(self):
        if self.state['refill_equipment'] == True:
            self.refill_eq()
        

        if self.state['mobilized'] == True and self.state["training"] == False:
            if self.combat_ability < self.combat_ability_max:
                self.combat_ability += 1
            elif self.combat_ability > self.combat_ability_max:
                self.combat_ability = self.combat_ability_max

        if self.state["mobilized"] == True and self.state["training"] == True:
            if self.experience < 100:
                self.experience += 0.1
        elif self.state["mobilized"] == True and self.state["training"] == False and self.state["building"] == True:
            if self.game.map.grids[self.hexid].building != None:
                if self.unit_typ == 14:
                    self.game.map.grids[self.hexid].building.construction(round(self.men * 3 / 20, 2))
                else:
                    self.game.map.grids[self.hexid].building.construction(round(self.men / 20, 2))

    def daily(self):
        pass

    def update(self): 
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.col, self.row = roffset_from_cube(OFFSET, self.hex)
        self.x = self.col
        self.y = self.row

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2 #+ FLAG_OFFSET[0]
        self.rect.y = self.y * TILESIZE[1] #+ FLAG_OFFSET[1]

        self.description = [self.owner.name, 
                            self.unit_typ.name, 
                            self.print_mobilized(), 
                            self.game.language.DESCRIPTION[2] + ": " + str(self.combat_ability) + "/" + str(self.combat_ability_max), 
                            self.game.language.DESCRIPTION[0] + ": " + str(self.experience), 
                            self.game.language.DESCRIPTION[7] + ": " + str(self.tiredness) + "/" + str(self.tiredness_max),
                            self.task,]

        