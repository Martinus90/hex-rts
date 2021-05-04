import pygame as pg
#import pytmx
from pytmx.util_pygame import load_pygame
from settings import *
from sprites import *
import math

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE[0]
        self.height = self.tileheight * TILESIZE[1]

class TiledMap:
    def __init__(self, game, filename):
        tm = load_pygame(filename, pixelalpha = True, load_all_tiles = True, allow_duplicate_names = True)
        self.game = game
        self.width = tm.width * tm.tilewidth + tm.tilewidth / 2
        self.height = tm.height * tm.tileheight * 48 / 64 + tm.tileheight / 2
        self.listtiles = [z for z in tm.gidmap]
        self.tmxdata = tm
        self.id = 0
        #print(self.tmxdata.width)

        self.grids = []
        self.grid_list = []
        self.resources = []
        self.trees = []
        self.units = []
        self.buildings = []
        self.cereals = []
        self.oil_filds = []

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        mg = self.tmxdata.map_gid
        re = self.tmxdata.register_gid
        #print(self.tmxdata.images)
        for layer in self.tmxdata.visible_layers:
            if layer.name == "layer1": 
                for x, y, gid in layer:
                    po = re(gid)
                    #print(x, y, self.listtiles[int(gid - 1)], self.id)
                    tile = ti(gid)
                    
                    #self.grids.append([x, y, self.get_terrain(self.listtiles[int(gid - 1)]), self.id])
                    self.grids.append(Grid(self.game, x, y, self.get_terrain(self.listtiles[int(gid - 1)]), self.id, gid))
                    self.grid_list.append(Hex(x - (y - 1 * (y & 1)) // 2, y, -(x - (y - 1 * (y & 1)) // 2) - y))
                    #self.grids.append([x, y, self.listtiles[int(gid - 1)], self.id])

                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth + (y&1) * self.tmxdata.tilewidth / 2, y * self.tmxdata.tileheight / TILESIZE[0] * TILESIZE[1]))
                    self.id += 1

        for grp in self.tmxdata.objectgroups:
            for obj in grp:
                if obj.name == "tree":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"tree",obj.properties['value']])
                elif obj.name == "grain":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"grain",obj.properties['value']])
                elif obj.name == "oil":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"oil",obj.properties['value']])
                elif obj.name == "iron":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"iron",obj.properties['value']])
                elif obj.name == "coal":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"coal",obj.properties['value']])
                elif obj.name == "calcium":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"calcium",obj.properties['value']])
                elif obj.name == "silicon":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"silicon",obj.properties['value']])
                elif obj.name == "cotton":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"cotton",obj.properties['value']])
                elif obj.name == "rubber":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"rubber",obj.properties['value']])
                elif obj.name == "bauxite":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"bauxite",obj.properties['value']])
                elif obj.name == "uranium":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"uranium",obj.properties['value']])
                elif obj.name == "water":
                    self.resources.append([math.floor(obj.x/64),math.floor(obj.y/48),"water",obj.properties['value']])


                if obj.name == "unit":
                    self.units.append([math.floor(obj.x/64),#0
                    math.floor(obj.y/48),
                    obj.properties['1_1_owner'],
                    obj.properties['1_1_typ'],
                    obj.properties['1_1_unit_name'],
                    obj.properties['1_2_1_brigade'],
                    obj.properties['1_2_2_regiment'],
                    obj.properties['1_2_3_battalion'],
                    obj.properties['1_2_4_company'],#8

                    obj.properties['2_1_men'],
                    obj.properties['2_2_supply'],
                    obj.properties['2_3_uniforms'],
                    obj.properties['2_4_fuel'],

                    obj.properties['3_1_light_ammo'],
                    obj.properties['3_2_heavy_ammo'],
                    obj.properties['3_3_rockets'],

                    obj.properties['4_1_rifle'],
                    obj.properties['4_2_art'],
                    obj.properties['4_3_truck'],
                    obj.properties['4_4_apc'],
                    obj.properties['4_5_tank'],
                    obj.properties['4_6_heli'],
                    obj.properties['4_7_aircraft'],
                    
                    #22
                    
                    
                    ])

                if obj.name == "building":
                    self.buildings.append([math.floor(obj.x/64),math.floor(obj.y/48),obj.properties['typ'],obj.properties['what'],obj.properties['owner']])

        #self.grid_list = set(self.grid_list)

    def get_terrain(self, a):
        b = ""
        if a in TERRAIN_GRASS:
            b = self.game.language.TERRAIN[0]
        if a in TERRAIN_DESSERT:
            b = self.game.language.TERRAIN[1]
        if a in TERRAIN_SEE:
            b = self.game.language.TERRAIN[2]
        if a in TERRAIN_MOUNTAIN:
            b = self.game.language.TERRAIN[3]
        if a in TERRAIN_COAST:
            b = self.game.language.TERRAIN[4]
        if a in TERRAIN_RIVER:
            b = self.game.language.TERRAIN[5]
        if a in TERRAIN_FORD:
            b = self.game.language.TERRAIN[6]
        return b

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

    def make_objects(self):
        pass

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft-pg.Vector2(TILESIZE[0]/2,TILESIZE[0]/2))

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft-pg.Vector2(TILESIZE[0]/2,TILESIZE[0]/2))

    def update(self, target):
        self.x = -target.rect.x + int(WIDTH / 2)
        self.y = -target.rect.y + int(HEIGHT / 2)
        self.camera = pg.Rect(self.x, self.y, self.width, self.height)
