import pygame as pg
import loading as ld
import inspect
from hexo import *
from settings import *
from queue import PriorityQueue
import random


class Player(pg.sprite.Sprite):
    """
    Player class. Contain his side (position of player in players list in game)
    """
    def __init__(self, game, x, y, side):
        """
        Initalise of player

        :param game: refer to game main object
        :param x: x position of camera
        :param y: y position of camera
        :param side: position of player in game contender list
        """
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
        """
        Camera move function
        :param dx: move in x / horizontally
        :param dy: move in y / vertically
        """
        self.x += dx # * TILESIZE[0]
        self.y += dy # * TILESIZE[1]

    def update(self):
        # self.get_keys()
        self.rect.x = (self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2) - TILESIZE[
            0
        ] / 2
        self.rect.y = (self.y * TILESIZE[1]) - TILESIZE[0] / 2
        # self.rect.topleft = (self.x, self.y)


class Grid(pg.sprite.Sprite):
    """
    Basic tile in game
    """
    def __init__(self, game, x, y, terrain, idnr, gid, owner=None):
        """
        Initialising of new tile
        :param game: refer to game main object
        :param x: x coordinate of tile
        :param y: y coordinate of tile
        :param terrain: terrain typ in tile
        :param idnr: identification number of tile
        :param gid: graphic id
        :param owner: owner of tile
        """
        self.groups = game.grids
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.terrain = terrain
        self.gid = gid
        self.owner = owner
        self.owner_side = None

        self.x = x
        self.y = y
        self.id = idnr
        self.neighbors = []
        self.resource = None
        self.near_resources = []
        self.building = None

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)  # self.hex = Hex(?,?,?)

        self.q, self.r, self.s = self.hex

    def get_owner(self):
        o = self.owner
        for p in self.game.players:
            if p.side == o:
                self.owner_side = 0
                self.owner = p.id_num

    def get_neighbors(self, map):
        """
        Function used after loading full map, and all tiles.
        Use to put all tile neighbor in tile neighbors list
        """
        for i in range(6):
            if hex_neighbor(self.hex, i) in map.grid_list:
                new_neighbor = hex_neighbor(self.hex, i)
                n = hex_id(-1, hex_neighbor(self.hex, i), map.tmxdata.width)
                self.neighbors.append(self.game.map.grids[n])
            else:
                pass

    def get_near_resources(self):
        """
        Function used to get info of resources in nearby tiles
        """
        self.near_resources = []
        for n in self.neighbors:
            if n.resource != None:
                self.near_resources.append(n.resource)

    def get_hex(self):
        """
        Function return Hex of grid/tile
        """
        return self.hex

    def get_pos(self):
        """
        Function return X and Y position of grid/tile
        """
        return self.x, self.y


class Resource(pg.sprite.Sprite):
    """
    Base class, used to make other resources
    """
    def __init__(self, game, x, y, value):
        """
        Init
        :param game: refer to game main object
        :param x: x pos
        :param y: y pos
        :param value: quantity of resource
        """
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
        self.game.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

    def do(self):
        """
        Periodic function, used in lower "unit" of time
        """
        pass

    def daily(self):
        """
        Periodic function, used dayli
        """
        pass

    def weekly(self):
        """
        Periodic function, used weekly
        """
        pass

    def seasonly(self):
        """
        Periodic function, used seasonly
        """
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
        if self.game.season < 3 and self.value < 5000:  # 3 == winter
            self.value += 50

    def seasonly(self):
        pass


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
        self.growth = 0
        self.off_road_value = 0
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

    def daily(self):
        if self.game.season < 2:  # 0 and 1 // spring and summer
            self.growth += 1000

    def seasonly(self):
        if self.game.season == 0:  # spring
            pass
        if self.game.season == 1:  # summer
            self.value += self.growth
            self.growth = 0
        if self.game.season == 2:  # autumn
            self.value += self.growth
            self.growth = 0
        if self.game.season == 3:
            self.value = 0


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
        self.growth = 0
        self.off_road_value = 0
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

    def daily(self):
        if self.game.season < 2:  # 0 and 1 // spring and summer
            self.growth += 1000

    def seasonly(self):
        if self.game.season == 0:  # spring
            pass
        if self.game.season == 1:  # summer
            self.value += self.growth
            self.growth = 0
        if self.game.season == 2:  # autumn
            self.value += self.growth
            self.growth = 0
        if self.game.season == 3:
            self.value = 0


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
        self.growth = 0
        self.off_road_value = 3
        self.grid_id = self.x + self.y * self.game.map.tmxdata.width
        self.game.map.grids[self.grid_id].resource = self

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)

        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

    def daily(self):
        if self.game.season < 3:  # 0 and 1 // spring and summer
            self.growth += 1000

    def seasonly(self):
        if self.game.season == 0:  # spring
            pass
        if self.game.season == 1:  # summer
            self.value += self.growth
            self.growth = 0
        if self.game.season == 2:  # autumn
            self.value += self.growth
            self.growth = 0
        if self.game.season == 3:
            self.value = 0


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

    def daily(self):
        if self.value < 2000:
            self.value += 100


class CONSTRUCTION(pg.sprite.Sprite):
    """

    """
    def __init__(self, game, x, y, what, owner, wood=0, cement=0, steel=0, progress=0):
        self.groups = game.all_sprites, game.buildings  # , game.grids[]
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
        self.orders = []
        self.window = None

    

        self.upkeep = UPKEEP_BUILDING["construction"]
        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.storage = {"wood": wood, "cement": cement, "steel": steel}
        self.fullmaterials = {}
        self.cost = globals()[self.what.upper() + "_COST"]
        self.fullcost = sum(self.cost.values())
        self.fullmaterials = sum(self.storage.values())
        self.progress = progress
        self.description = [
            self.owner.name,
            self.name,
            self.what,
            self.print_progress(),
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]

        # self.screen.blit(self.building.owner.image, (WIDTH - MENU_RIGHT[0]+10, 412))

        # self.description[4] = ""
        # for m in self.materials.items():
        #    self.description[4] += str(m[0]) + ": " + str(m[1]) + ", "

        # self.description[4] =
        # print(self.materials['wood'])

        self.description[4] = (
            self.game.language.RES1[0]
            + ": "
            + str(self.storage["wood"])
            + "/"
            + str(self.cost["wood"])
        )
        self.description[5] = (
            self.game.language.RES1[2]
            + ": "
            + str(self.storage["cement"])
            + "/"
            + str(self.cost["cement"])
        )
        self.description[6] = (
            self.game.language.RES1[5]
            + ": "
            + str(self.storage["steel"])
            + "/"
            + str(self.cost["steel"])
        )

        self.description[5] = ""
        for c in self.cost.items():
            self.description[5] += str(c[0]) + ": " + str(c[1]) + ", "

    def print_progress(self):
        return "Progress: " + str(self.progress) + " / " + str(self.fullcost)

    def construction(self, value):
        if (self.fullmaterials - self.progress) >= value:
            self.progress += value
        else:
            self.progress += self.fullmaterials - self.progress

    def do(self):
        pass

    def hourly(self):
        if self.progress >= self.fullcost:
            if self.game.building == self:
                self.game.deselect()
            self.game.build(self)

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def seasonly(self):
        pass

    def change_owner(self, new_owner):
        self.owner = self.game.players[new_owner]
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))

        if self.window != None:
            b = pg.Surface((150, 30))
            pg.draw.rect(b, self.window.color, (0, 0, 150, 30))
            self.game.map.grids[self.hexid].building.window.image.blit(
            b, (200, 5)
            )
            self.window.image.blit(pg.font.Font(FONT_NAME, 
            self.window.textsize).render(
            self.owner.name, False, self.window.textcolor
            ),
            (245, 10),
            )
            self.window.image.blit(
            self.owner.image, (220, 0)
            )
            self.window.image.blit(
            self.image, (0, 25)
            )
        self.update()

    def update(self):
        self.fullmaterials = sum(self.storage.values())

        self.description[3] = self.print_progress()  # str(self.progress)
        self.description[4] = ""
        self.description[5] = ""
        self.description[6] = ""
        for m in self.storage.items():
            self.description[4] += m[0].title() + ": " + str(m[1]) + ", "
        if not self.storage:
            self.description[4] = "None"
        # for c in self.cost.items():
        #    self.description[5] += c[0].title() + ": " + str(c[1]) + ", "

        self.description[4] = (
            self.game.language.RES1[0]
            + ": "
            + str(self.storage["wood"])
            + "/"
            + str(self.cost["wood"])
        )
        self.description[5] = (
            self.game.language.RES1[2]
            + ": "
            + str(self.storage["cement"])
            + "/"
            + str(self.cost["cement"])
        )
        self.description[6] = (
            self.game.language.RES1[5]
            + ": "
            + str(self.storage["steel"])
            + "/"
            + str(self.cost["steel"])
        )


class SETTLEMENT(pg.sprite.Sprite):
    def __init__(
        self, game, x, y, owner, name, nationality=0, population=0, prosperity=0, loyalty=20
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.resource_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = self.game.language.BUILDINGS1[1]
        self.settlement_name = name
        self.nationality = self.game.nations[nationality]
        self.population = population
        self.prosperity = prosperity
        self.state = {"food": True, "wood": True}
        self.orders = []
        self.loyalty = loyalty

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]
        self.storage = {}
        self.window = None

        self.upkeep = 0
        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self

        self.description = ["", "", "", "", "", "", "", "", "", "", "", "", ""]

    def do(self):
        pass

    def hourly(self):
        pass

    def daily(self):
        if self.nationality == self.owner.nation:
            self.loyalty += LOYALTY_DAYLI_GAIN
            if self.loyalty > 100:
                self.loyalty = 100

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

        #people pay taxes to settlement
        self.owner.money += self.population * self.owner.pop_tax

    def seasonly(self):
        pass

    def change_owner(self, new_owner):
        self.owner = self.game.players[new_owner]
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.loyalty = 30

        if self.window != None:
            b = pg.Surface((150, 30))
            pg.draw.rect(b, self.window.color, (0, 0, 150, 30))
            self.game.map.grids[self.hexid].building.window.image.blit(
            b, (200, 5)
            )
            self.window.image.blit(pg.font.Font(FONT_NAME, 
            self.window.textsize).render(
            self.owner.name, False, self.window.textcolor
            ),
            (245, 10),
            )
            self.window.image.blit(
            self.owner.image, (220, 0)
            )
            self.window.image.blit(
            self.image, (0, 25)
            )
        self.update()


    def update(self):
        self.description = ["", "", "", "", "", "", "", "", "", "", "", "", ""]


class VILLAGE(SETTLEMENT):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        name="New",
        nationality=0,
        population=0,
        prosperity=1,
        food=0,
        wood=0,
        cotton=0,
        rubber=0,
        loyalty=30
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = self.game.language.BUILDINGS1[1]
        self.settlement_name = name
        self.nationality = self.game.nations[nationality]
        self.population = population
        self.prosperity = prosperity
        self.state = {"food": True, "wood": True, "cotton": False, "rubber": False}
        self.orders = []
        self.loyalty = loyalty

        self.image = self.game.village_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {"food": food, "wood": wood, "cotton": cotton, "rubber": rubber}
        self.grid_with_res = []
        self.sum_res = []
        self.food_source = False

        self.upkeep = UPKEEP_BUILDING["village"]
        self.window = ld.Building_Window(
            self,
            self.game,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.window.buttons.append(
            ld.Function_Button(
                self.game,
                self.window,
                pos=(450, 450),
                text=self.game.language.DECISIONS[2],
                function="grant_money",
            )
        )
        self.window.buttons.append(
            ld.Function_Button(
                self.game,
                self.window,
                pos=(550, 450),
                text=self.game.language.DECISIONS[4],
                function="calling_up",
            )
        )

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            self.settlement_name,
            "Pop: " + str(self.population),
            self.game.language.GUI[0],
            self.game.language.RESOURCES[2] + ":",
            self.game.language.RESOURCES[1] + ":",
            self.game.language.RESOURCES[8] + ":",
            self.game.language.RESOURCES[9] + ":",
            self.game.language.GUI[14] + str(self.loyalty),
            self.game.language.GUI[16] + str(self.prosperity),
            "",
            "",
        ]
        # here near resources
        self.resources_near_building()

    def resources_near_building(self):
        self.grid_with_res = []
        self.sum_res = []
        self.sum_res.append(0)
        self.game.map.grids[self.hexid].get_near_resources()
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[2]
            ):
                self.food_source = True
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[0] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[2]:
                    self.food_source = True
                    self.grid_with_res.append(a)
                    self.sum_res[0] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[1]
            ):
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[1] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[1]:
                    self.grid_with_res.append(a)
                    self.sum_res[1] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[8]
            ):
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[2] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[8]:
                    self.grid_with_res.append(a)
                    self.sum_res[2] += a.resource.value
        
        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[9]
            ):
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[3] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[9]:
                    self.grid_with_res.append(a)
                    self.sum_res[3] += a.resource.value

        self.description[5] = (
            self.game.language.RESOURCES[2] + ": " + str(self.sum_res[0])
        )
        self.description[6] = (
            self.game.language.RESOURCES[1] + ": " + str(self.sum_res[1])
        )
        self.description[7] = (
            self.game.language.RESOURCES[8] + ": " + str(self.sum_res[2])
        )
        self.description[8] = (
            self.game.language.RESOURCES[9] + ": " + str(self.sum_res[3])
        )

    def rebeling(self):
        enemy = None
        for p in self.game.players:
            if p.name != self.owner.name and p.nation.name == self.nationality.name:
                enemy = p.id_num
        
        if enemy == None:
            enemy = 0

        g = [self.grid.id]
        for a in self.grid.neighbors:
            g.append(a.id)

        self.game.event_list.get_control_over_grids(enemy, g, False)


    def do(self):
        pass

    def hourly(self):
        jobs = 0
        for aa in self.all_jobs:
            if self.state[aa] == True:
                jobs += 1

        if jobs > 0:
            e = int(self.population / jobs)
            self.resources_near_building()
            for d in self.grid_with_res:
                if d.resource.value > e:
                    if d.resource.name == self.game.language.RESOURCES[2]:  # food
                        if self.state["food"] == True:
                            self.storage["food"] += e
                            d.resource.value -= e
                    if d.resource.name == self.game.language.RESOURCES[1]:  # food
                        if self.state["wood"] == True:
                            self.storage["wood"] += e
                            d.resource.value -= e
                    if d.resource.name == self.game.language.RESOURCES[8]:  # cotton
                        if self.state["cotton"] == True:
                            self.storage["cotton"] += e
                            d.resource.value -= e
                    if d.resource.name == self.game.language.RESOURCES[9]:  # cotton
                        if self.state["rubber"] == True:
                            self.storage["rubber"] += e
                            d.resource.value -= e

    def daily(self):
        #check near resources for food
        self.resources_near_building()
        if self.food_source == False:
            for g in self.grid.neighbors:
                if g.terrain == self.game.language.TERRAIN[0] and g.resource == None and g.building == None:
                    g.resource = Grain(self.game, g.x, g.y, 0)
                    self.food_source = True
                    break

        if self.nationality == self.owner.nation:
            self.loyalty += LOYALTY_DAYLI_GAIN

        if self.storage["food"] >= self.population:
            self.storage["food"] -= self.population
        else:
            if self.prosperity >= 1:
                self.prosperity -= 1
            self.loyalty -= 1
        
        if self.owner.stability < -50:
            self.loyalty -= 1
        elif self.owner.stability > 50:
            self.loyalty += 1

        
        if self.loyalty > 100:
            self.loyalty = 100

        a = random.randint(1,30)
        if self.loyalty < a:
            self.rebeling()
        
    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

        #people pay taxes to settlement
        self.owner.money += round(self.population * self.owner.pop_tax / 10, 2)
        self.population += int(self.population * self.prosperity / 100)
        if self.population > 200:
            self.population = 200
        if self.storage["food"] >= self.population:
            if self.prosperity <= 1:
                self.prosperity += 1

    def seasonly(self):
        print("seasonly village " + self.settlement_name)
        print("prosperity: " + str(self.prosperity))
        print("population" + str(self.population))
        print("   ")

    def update(self):
        self.description = [
            self.owner.name,
            self.name,
            self.settlement_name,
            "Pop: " + str(self.population),
            self.game.language.GUI[0],
            self.game.language.RESOURCES[2] + ":",
            self.game.language.RESOURCES[1] + ":",
            self.game.language.RESOURCES[8] + ":",
            self.game.language.RESOURCES[9] + ":",
            self.game.language.GUI[14] + str(self.loyalty),
            self.game.language.GUI[16] + str(self.prosperity),
            "",
            "",
        ]
        self.description[5] = (
            self.game.language.RESOURCES[2] + ": " + str(self.sum_res[0])
        )
        self.description[6] = (
            self.game.language.RESOURCES[1] + ": " + str(self.sum_res[1])
        )
        self.description[7] = (
            self.game.language.RESOURCES[8] + ": " + str(self.sum_res[2])
        )
        self.description[8] = (
            self.game.language.RESOURCES[9] + ": " + str(self.sum_res[3])
        )


class CITY(SETTLEMENT):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        name="New",
        nationality=0,
        population=0,
        prosperity=1,
        food=0,
        textiles=0,
        furniture=0,
        electronics=0,
        loyalty=30
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = self.game.language.BUILDINGS1[2]
        self.settlement_name = name
        self.nationality = self.game.nations[nationality]
        self.population = population
        self.prosperity = prosperity
        self.state = {}
        self.orders = []
        self.loyalty = loyalty

        self.image = self.game.city_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "food": food,
            "textiles": textiles,
            "furniture": furniture,
            "electronics": electronics,
        }
        self.grid_with_res = []
        self.sum_res = []

        self.upkeep = UPKEEP_BUILDING["city"]
        self.window = ld.Building_Window(
            self,
            self.game,
            #[300, 200],
            #(700, 500),
            #DARKGREY,
            #"",
            #16,
            #LIGHTGREY,
            #(35, 10),
            #2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        self.window.buttons.append(
            ld.Function_Button(
                self.game,
                self.window,
                pos=(510, 460),
                text=self.game.language.DECISIONS[2],
                function="grant_money",
            )
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        # self.all_jobs = self.state.keys()
        # b = 0
        # for a in self.all_jobs:
        #    self.window.image.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.game.language.GUI[6], False, LIGHTGREY), (180, 40))
        #    self.window.image.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY), (180, 60 + (b * 20)))
        #    self.window.buttons.append(ld.Switch_Button(self.game, self.window, pos=[160,60 + (b * 20)], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable=a))
        #    b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            self.settlement_name,
            "Pop: " + str(self.population),
            self.game.language.GUI[14] + str(self.loyalty),
            self.game.language.GUI[16] + str(self.prosperity),
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here near resources

    def rebeling(self):
        enemy = None
        print(" - - - ")
        print("Owner:")
        print(self.owner.name)
        print(self.owner.nation.name)
        for p in self.game.players:
            if p.name != self.owner.name and p.nation.name == self.owner.nation.name:
                enemy = p.id_num
            
        if enemy == None:
            enemy = 0

        g = [self.grid.id]
        for a in self.grid.neighbors:
            g.append(a.id)

        self.game.event_list.get_control_over_grids(enemy, g, False)

    def do(self):
        pass

    def hourly(self):
        pass

    def daily(self):
        if self.nationality == self.owner.nation:
            self.loyalty += LOYALTY_DAYLI_GAIN

        if self.storage["food"] >= self.population:
            self.storage["food"] -= self.population
            self.loyalty += 1
        else:
            if self.prosperity >= 1:
                self.prosperity -= 1
            self.loyalty -= 1

        if self.owner.stability < -50:
            self.loyalty -= 1
        elif self.owner.stability > 50:
            self.loyalty += 1

        if self.loyalty > 100:
            self.loyalty = 100

        a = random.randint(1,30)
        if self.loyalty < a:
            self.rebeling()

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

        #people pay taxes to settlement
        self.owner.money += round(self.population * self.owner.pop_tax / 10, 2)
                          

        self.population += int(
            self.population * self.prosperity / 100
        )

        a = 1 + (self.population // 100)
        if self.storage["electronics"] >= 1 * a:  # electronics give prosperity to max 6
            self.storage["electronics"] -= 1 * a
            if self.prosperity <= 5:
                self.prosperity += 1
        else:
            if self.prosperity >= 1:
                self.prosperity -= 1

        if self.storage["furniture"] >= 5 * a:  # furniture give prosperity to max 4
            self.storage["furniture"] -= 5 * a
            if self.prosperity <= 3:
                self.prosperity += 1
        else:
            if self.prosperity >= 1:
                self.prosperity -= 1

        if self.storage["textiles"] >= 10 * a:  # textiles give prosperity to max 2
            self.storage["textiles"] -= 10 * a
            if self.prosperity <= 1:
                self.prosperity += 1
        else:
            if self.prosperity >= 1:
                self.prosperity -= 1

    def seasonly(self):
        print("seasonly city " + self.settlement_name)
        print("prosperity: " + str(self.prosperity))
        print("population" + str(self.population))
        print("   ")

    def update(self):
        self.description = [
            self.owner.name,
            self.name,
            self.settlement_name,
            "Pop: " + str(self.population),
            self.game.language.GUI[0],
            self.game.language.GUI[14] + str(self.loyalty),
            self.game.language.GUI[16] + str(self.prosperity),
            "",
            "",
            "",
            "",
            "",
            "",
        ]


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
        self.orders = []

        self.upkeep = 0
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]

    def do(self):
        pass

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def seasonly(self):
        pass

    def change_owner(self, new_owner):
        self.owner = self.game.players[new_owner]
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))

        if self.window != None:
            b = pg.Surface((150, 30))
            pg.draw.rect(b, self.window.color, (0, 0, 150, 30))
            self.game.map.grids[self.hexid].building.window.image.blit(
            b, (200, 5)
            )
            self.window.image.blit(pg.font.Font(FONT_NAME, 
            self.window.textsize).render(
            self.owner.name, False, self.window.textcolor
            ),
            (245, 10),
            )
            self.window.image.blit(
            self.owner.image, (220, 0)
            )
            self.window.image.blit(
            self.image, (0, 25)
            )
        self.update()

    def update(self):
        self.description = [
            self.owner.name,
            self.name,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]


class HARBOR(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        res1=[0, 0, 0, 0, 0,
            0, 0, 0, 0, 0,
            0, 0, 0, 0, 0,
            0, 0, 0, 0, 0,
            0, 0, 0, 0, 0,
        ],
        res2=[0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 
            0, 0, 0],
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[3]
        self.state = {}
        self.orders = []

        self.image = self.game.harbor_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {}
        c = 0
        for a in RES1_LIST:
            b = a.lower()
            self.storage[b] = res1[c]
            c += 1
            # print(b)
        c = 0
        for a in RES2_LIST:
            b = a.lower()
            if b != "fuel":
                self.storage[b] = res2[c]
            c += 1
            # print(b)

        self.upkeep = UPKEEP_BUILDING["harbor"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here near resources

    def do(self):
        pass

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class AIRPORT(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        res1=[
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
        res2=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[4]
        self.state = {}
        self.orders = []

        self.image = self.game.airport_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {}
        c = 0
        for a in RES1_LIST:
            b = a.lower()
            self.storage[b] = res1[c]
            c += 1
            # print(b)
        c = 0
        for a in RES2_LIST:
            b = a.lower()
            if b != "fuel":
                self.storage[b] = res2[c]
            c += 1
            # print(b)

        self.upkeep = UPKEEP_BUILDING["airport"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here near resources

    def do(self):
        pass

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class WAREHOUSE(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        res1=[
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
        res2=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[5]
        self.state = {}
        self.orders = []

        self.image = self.game.warehouse_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {}
        c = 0
        for a in RES1_LIST:
            b = a.lower()
            self.storage[b] = res1[c]
            c += 1
            # print(b)
        c = 0
        for a in RES2_LIST:
            b = a.lower()
            if b != "fuel":
                self.storage[b] = res2[c]
            c += 1
            # print(b)

        self.upkeep = UPKEEP_BUILDING["warehouse"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here near resources

    def do(self):
        pass

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class BARRACK(BUILDING):
    def __init__(self, game, x, y, owner=0, cadets=0, graduates=0):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[6]
        self.state = {}
        self.orders = []
        self.new_unit_typ = 0

        self.image = self.game.barrack_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {"cadets": cadets, "graduates": graduates}

        self.upkeep = UPKEEP_BUILDING["barrack"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )
        self.window.buttons.append(
            ld.Function_Button(
                self.game,
                self.window,
                pos=(10, 460),
                text=self.game.language.BASIC[4],
                function="func_prev_unit",
            )
        )
        self.window.buttons.append(
            ld.Function_Button(
                self.game,
                self.window,
                pos=(140, 460),
                text=self.game.language.BASIC[9],
                function="func_new_unit",
            )
        )
        self.window.buttons.append(
            ld.Function_Button(
                self.game,
                self.window,
                pos=(240, 460),
                text=self.game.language.BASIC[5],
                function="func_next_unit",
            )
        )
        self.window.texts.append(
            [self.game.language.UNIT_TYPE[self.new_unit_typ], 16, RED, (10, 140)]
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here near resources

    def do(self):
        pass

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class MINE(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        iron=0,
        coal=0,
        calcium=0,
        silicon=0,
        bauxite=0,
        uranium=0,
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[7]
        self.state = {
            "iron": True,
            "coal": True,
            "calcium": True,
            "silicon": True,
            "bauxite": True,
            "uranium": True,
        }
        self.orders = []

        self.image = self.game.mine_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "iron": iron,
            "coal": coal,
            "calcium": calcium,
            "silicon": silicon,
            "bauxite": bauxite,
            "uranium": uranium,
        }
        self.grid_with_res = []
        self.sum_res = 0

        self.upkeep = UPKEEP_BUILDING["mine"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[0],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here near resources
        self.resources_near_building()

    def resources_near_building(self):
        self.grid_with_res = []
        self.sum_res = []
        self.sum_res.append(0)
        self.game.map.grids[self.hexid].get_near_resources()
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[4]
            ):
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[0] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[4]:
                    self.grid_with_res.append(a)
                    self.sum_res[0] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[5]
            ):
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[1] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[5]:
                    self.grid_with_res.append(a)
                    self.sum_res[1] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[6]
            ):
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[2] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[6]:
                    self.grid_with_res.append(a)
                    self.sum_res[2] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[7]
            ):
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[3] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[7]:
                    self.grid_with_res.append(a)
                    self.sum_res[3] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[10]
            ):
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[4] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[10]:
                    self.grid_with_res.append(a)
                    self.sum_res[4] += a.resource.value

        self.sum_res.append(0)
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[11]
            ):
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res[5] += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[11]:
                    self.grid_with_res.append(a)
                    self.sum_res[5] += a.resource.value

        self.description[4] = (
            self.game.language.RESOURCES[4] + ": " + str(self.sum_res[0])
        )
        self.description[5] = (
            self.game.language.RESOURCES[5] + ": " + str(self.sum_res[1])
        )
        self.description[6] = (
            self.game.language.RESOURCES[6] + ": " + str(self.sum_res[2])
        )
        self.description[7] = (
            self.game.language.RESOURCES[7] + ": " + str(self.sum_res[3])
        )
        self.description[8] = (
            self.game.language.RESOURCES[10] + ": " + str(self.sum_res[4])
        )
        self.description[9] = (
            self.game.language.RESOURCES[11] + ": " + str(self.sum_res[5])
        )

    def do(self):
        jobs = 0
        for aa in self.all_jobs:
            if self.state[aa] == True:
                jobs += 1

        if jobs > 0:
            if self.owner.electricity == False:
                e = int(12 / jobs)
            else:
                e = int(60 / jobs)
            self.resources_near_building()
            #mining resources
            for d in self.grid_with_res:
                if d.resource.value > e:
                    if d.resource.name == self.game.language.RESOURCES[4]:
                        if self.state["iron"] == True:
                            self.storage["iron"] += e
                            d.resource.value -= e
                    elif d.resource.name == self.game.language.RESOURCES[5]:
                        if self.state["coal"] == True:
                            self.storage["coal"] += e
                            d.resource.value -= e
                    elif d.resource.name == self.game.language.RESOURCES[6]:
                        if self.state["calcium"] == True:
                            self.storage["calcium"] += e
                            d.resource.value -= e
                    elif d.resource.name == self.game.language.RESOURCES[7]:
                        if self.state["silicon"] == True:
                            self.storage["silicon"] += e
                            d.resource.value -= e
                    elif d.resource.name == self.game.language.RESOURCES[10]:
                        if self.state["bauxite"] == True:
                            self.storage["bauxite"] += e
                            d.resource.value -= e
                    elif d.resource.name == self.game.language.RESOURCES[11]:
                        if self.state["uranium"] == True:
                            self.storage["uranium"] += e
                            d.resource.value -= e


    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class SMELTER(BUILDING):
    def __init__(
        self, game, x, y, owner=0, iron=0, coal=0, steel=0, bauxite=0, aluminum=0
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[8]
        self.state = {"steel": False, "aluminum": False}
        self.orders = []

        self.image = self.game.smelter_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "iron": iron,
            "coal": coal,
            "steel": steel,
            "bauxite": bauxite,
            "aluminum": aluminum,
        }

        self.upkeep = UPKEEP_BUILDING["smelter"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here near resources

        self.description[4] = (
            self.game.language.RES1[3] + ": " + str(self.storage["iron"])
        )
        self.description[5] = (
            self.game.language.RES1[4] + ": " + str(self.storage["coal"])
        )
        self.description[6] = (
            self.game.language.RES1[5] + ": " + str(self.storage["steel"])
        )
        self.description[7] = (
            self.game.language.RES1[21] + ": " + str(self.storage["bauxite"])
        )
        self.description[8] = (
            self.game.language.RES1[9] + ": " + str(self.storage["aluminum"])
        )

    def do(self):
        jobs = 0
        for aa in self.all_jobs:
            if self.state[aa] == True:
                jobs += 1

        if jobs > 0 and self.owner.electricity == True:
            e = int(60 / jobs)

            #steel production/casting
            if (
                self.storage["iron"] >= STEEL_COST["iron"] * e
                and self.storage["coal"] >= STEEL_COST["coal"] * e
                and self.state["steel"] == True
                ):
                    self.storage["iron"] -= STEEL_COST["iron"] * e
                    self.storage["coal"] -= STEEL_COST["coal"] * e
                    self.storage["steel"] += STEEL_COST["output"] * e

            #aluminum production/casting
            if self.storage["bauxite"] >= ALUMINUM_COST["bauxite"] * e and self.state["aluminum"] == True:
                self.storage["bauxite"] -= ALUMINUM_COST["bauxite"] * e
                self.storage["aluminum"] += ALUMINUM_COST["output"] * e

        self.description[4] = (
            self.game.language.RES1[3] + ": " + str(self.storage["iron"])
        )
        self.description[5] = (
            self.game.language.RES1[4] + ": " + str(self.storage["coal"])
        )
        self.description[6] = (
            self.game.language.RES1[5] + ": " + str(self.storage["steel"])
        )
        self.description[7] = (
            self.game.language.RES1[21] + ": " + str(self.storage["bauxite"])
        )
        self.description[8] = (
            self.game.language.RES1[9] + ": " + str(self.storage["aluminum"])
        )

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
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
        self.state = {"oil": True}
        self.orders = []

        self.image = self.game.oil_well_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {"oil": oil}
        self.grid_with_res = []
        self.sum_res = 0

        self.upkeep = UPKEEP_BUILDING["oil_well"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[0],
            self.game.language.RESOURCES[3] + ": ",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here near resources
        self.resources_near_building()

    def resources_near_building(self):
        self.grid_with_res = []
        self.sum_res = 0
        self.game.map.grids[self.hexid].get_near_resources()
        if self.game.map.grids[self.hexid].resource != None:
            if (
                self.game.map.grids[self.hexid].resource.name
                == self.game.language.RESOURCES[3]
            ):
                self.grid_with_res.append(self.game.map.grids[self.hexid])
                self.sum_res += self.game.map.grids[self.hexid].resource.value
        for a in self.game.map.grids[self.hexid].neighbors:
            if a.resource != None:
                if a.resource.name == self.game.language.RESOURCES[3]:
                    self.grid_with_res.append(a)
                    self.sum_res += a.resource.value

        self.description[4] = self.game.language.RESOURCES[3] + ": " + str(self.sum_res)

    def do(self):
        jobs = 0
        for aa in self.all_jobs:
            if self.state[aa] == True:
                jobs += 1

        if jobs > 0:
            if self.owner.electricity == False:
                e = int(12 / jobs)
            else:
                e = int(60 / jobs)

            self.resources_near_building()
            for d in self.grid_with_res:
                if d.resource.value > e:
                    if d.resource.name == self.game.language.RESOURCES[3]:  # food
                        if self.state["oil"] == True:
                            self.storage["oil"] += e
                            d.resource.value -= e

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[0],
            self.game.language.RESOURCES[3] + ": ",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        self.description[4] = self.game.language.RESOURCES[3] + ": " + str(self.sum_res)


class RAFINERY(BUILDING):
    def __init__(self, game, x, y, owner=0, oil=0, fuel=0, rubber=0, calcium=0, cement=0, coal=0):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[10]
        self.state = {"fuel": False, "cement": False, "rubber": False}
        self.orders = []

        self.image = self.game.rafinery_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "oil": oil,
            "fuel": fuel,
            "rubber": rubber,
            "calcium": calcium,
            "coal": coal,
            "cement": cement,
        }

        self.upkeep = UPKEEP_BUILDING["rafinery"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here near resources

        self.description[4] = (
            self.game.language.RES1[11] + ": " + str(self.storage["fuel"])
        )
        self.description[5] = (
            self.game.language.RES1[2] + ": " + str(self.storage["cement"])
        )
        self.description[6] = (
            self.game.language.RES1[20] + ": " + str(self.storage["rubber"])
        )


    def do(self):
        jobs = 0
        for aa in self.all_jobs:
            if self.state[aa] == True:
                jobs += 1

        if jobs > 0:
            if self.owner.electricity == False:
                e = int(12 / jobs)
            else:
                e = int(60 / jobs)

            #fuel
            if self.storage["oil"] >= FUEL_COST["oil"] * e and self.state["fuel"] == True:
                self.storage["oil"] -= FUEL_COST["oil"] * e
                self.storage["fuel"] += FUEL_COST["output"] * e

            #sythetic rubber
            if self.storage["oil"] >= SYNTHETIC_RUBBER_COST["oil"] * e and self.state["rubber"] == True:
                self.storage["oil"] -= SYNTHETIC_RUBBER_COST["oil"] * e
                self.storage["rubber"] += SYNTHETIC_RUBBER_COST["output"] * e

            #cement
            if (self.storage["calcium"] >= CEMENT_COST["calcium"] * e
                and self.storage["coal"] >= CEMENT_COST["coal"]
                and self.state["cement"] == True
                ):
                    self.storage["calcium"] -= CEMENT_COST["calcium"] * e
                    self.storage["coal"] -= CEMENT_COST["coal"]
                    self.storage["cement"] += CEMENT_COST["output"] * e

        self.description[4] = (
            self.game.language.RES1[11] + ": " + str(self.storage["fuel"])
        )
        self.description[5] = (
            self.game.language.RES1[2] + ": " + str(self.storage["cement"])
        )
        self.description[6] = (
            self.game.language.RES1[20] + ": " + str(self.storage["rubber"])
        )

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class POWER_PLANT(BUILDING):
    def __init__(self, game, x, y, owner=0, oil=0, coal=0):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[11]
        self.state = {"oil": False, "coal": False}
        self.working = False

        self.image = self.game.power_plant_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {"oil": oil, "coal": coal}
        self.orders = []

        self.upkeep = UPKEEP_BUILDING["power_plant"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here near resources

        self.description[4] = (
            self.game.language.RES1[10] + ": " + str(self.storage["oil"])
        )
        self.description[5] = (
            self.game.language.RES1[4] + ": " + str(self.storage["coal"])
        )

    def do(self):
        self.working = False
        jobs = 0
        for aa in self.all_jobs:
            if self.state[aa] == True:
                jobs += 1

        if jobs > 0:
            e = int(6 / jobs)
            if self.storage["oil"] >= e and self.state["oil"] == True:
                self.storage["oil"] -= e
                self.working = True
            if self.storage["coal"] >= e and self.state["coal"] == True:
                self.storage["coal"] -= e
                self.working = True
        self.description[4] = (
            self.game.language.RES1[10] + ": " + str(self.storage["oil"])
        )
        self.description[5] = (
            self.game.language.RES1[4] + ": " + str(self.storage["coal"])
        )

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class LIGHT_INDUSTRY_PLANT(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        steel=0,
        food=0,
        supply=0,
        wood=0,
        furniture=0,
        cotton=0,
        textiles=0,
        uniforms=0,
        chem_comp=0,
        light_ammo=0,
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[12]
        self.state = {
            "supply": False,
            "furniture": False,
            "textiles": False,
            "uniforms": False,
            "light_ammo": False,
        }
        self.orders = []

        self.image = self.game.light_industry_plant_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "steel": steel,
            "food": food,
            "supply": supply,
            "wood": wood,
            "furniture": furniture,
            "cotton": cotton,
            "textiles": textiles,
            "uniforms": uniforms,
            "chem_comp": chem_comp,
            "light_ammo": light_ammo,
        }

        self.upkeep = UPKEEP_BUILDING["light_industry_plant"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here resources

        self.description[4] = (
            self.game.language.RES2[0] + ": " + str(self.storage["supply"])
        )
        self.description[5] = (
            self.game.language.RES1[22] + ": " + str(self.storage["furniture"])
        )
        self.description[6] = (
            self.game.language.RES1[19] + ": " + str(self.storage["textiles"])
        )
        self.description[7] = (
            self.game.language.RES2[1] + ": " + str(self.storage["uniforms"])
        )
        self.description[8] = (
            self.game.language.RES2[3] + ": " + str(self.storage["light_ammo"])
        )

    def do(self):
        jobs = 0
        for aa in self.all_jobs:
            if self.state[aa] == True:
                jobs += 1

        if jobs > 0:
            if self.owner.electricity == False:
                e = int(12 / jobs)
            else:
                e = int(60 / jobs)

            #supply
            if (self.storage["steel"] >= e * SUPPLY_COST["steel"]
                and self.storage["food"] >= e * SUPPLY_COST["food"]
                and self.state["supply"] == True
                ):
                self.storage["steel"] -= e * SUPPLY_COST["steel"]
                self.storage["food"] -= e * SUPPLY_COST["food"]
                self.storage["supply"] += e * SUPPLY_COST["output"]

            #furniture    
            if self.storage["wood"] >= e * FURNITURE_COST["wood"] and self.state["furniture"] == True:
                self.storage["wood"] -= e * FURNITURE_COST["wood"]
                self.storage["furniture"] += e * FURNITURE_COST["output"]

            #textiles
            if self.storage["cotton"] >= e * TEXTILES_COST["cotton"] and self.state["textiles"] == True:
                self.storage["cotton"] -= e * TEXTILES_COST["cotton"]
                self.storage["textiles"] += e * TEXTILES_COST["output"]

            #uniforms
            if self.storage["textiles"] >= e * UNIFORMS_COST["textiles"] and self.state["uniforms"] == True:
                self.storage["textiles"] -= e * UNIFORMS_COST["textiles"]
                self.storage["uniforms"] += e * UNIFORMS_COST["output"]

            #light_ammo
            if self.storage["steel"] >= e * LIGHT_AMMO_COST["steel"] and self.storage["textiles"] >= e * LIGHT_AMMO_COST["textiles"] and self.storage["chem_comp"] >= e * LIGHT_AMMO_COST["chem_comp"] and self.state["light_ammo"] == True:
                self.storage["steel"] -= e * LIGHT_AMMO_COST["steel"]
                self.storage["textiles"] -= e * LIGHT_AMMO_COST["textiles"]
                self.storage["chem_comp"] -= e * LIGHT_AMMO_COST["chem_comp"]
                self.storage["light_ammo"] += e * LIGHT_AMMO_COST["output"]

        self.description[4] = (
            self.game.language.RES2[0] + ": " + str(self.storage["supply"])
        )
        self.description[5] = (
            self.game.language.RES1[22] + ": " + str(self.storage["furniture"])
        )
        self.description[6] = (
            self.game.language.RES1[19] + ": " + str(self.storage["textiles"])
        )
        self.description[7] = (
            self.game.language.RES2[1] + ": " + str(self.storage["uniforms"])
        )
        self.description[8] = (
            self.game.language.RES2[3] + ": " + str(self.storage["light_ammo"])
        )

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class HEAVY_INDUSTRY_PLANT(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        steel=0,
        aluminum=0,
        plastic=0,
        parts=0,
        tools=0,
        civ_mach=0,
        rifle=0,
        chem_comp=0,
        textiles=0,
        light_ammo=0,
        heavy_ammo=0,
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[13]
        self.state = {"parts": False, "tools": False, "civ_mach": False, "rifle": False, "light_ammo": False, "heavy_ammo": False}
        self.orders = []

        self.image = self.game.heavy_industry_plant_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "steel": steel,
            "aluminum": aluminum,
            "plastic": plastic,
            "parts": parts,
            "tools": tools,
            "civ_mach": civ_mach,
            "rifle": rifle,
            "chem_comp": chem_comp,
            "textiles": textiles,
            "light_ammo": light_ammo,
            "heavy_ammo": heavy_ammo,
        }

        self.upkeep = UPKEEP_BUILDING["heavy_industry_plant"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here resources
        self.description[4] = (
            self.game.language.RES1[8] + ": " + str(self.storage["parts"])
        )
        self.description[5] = (
            self.game.language.RES1[7] + ": " + str(self.storage["tools"])
        )
        self.description[6] = (
            self.game.language.RES1[23] + ": " + str(self.storage["civ_mach"])
        )
        self.description[7] = (
            self.game.language.RES2[6] + ": " + str(self.storage["rifle"])
        )
        self.description[8] = (
            self.game.language.RES2[3] + ": " + str(self.storage["light_ammo"])
        )
        self.description[9] = (
            self.game.language.RES2[4] + ": " + str(self.storage["heavy_ammo"])
        )

    def do(self):
        jobs = 0
        for aa in self.all_jobs:
            if self.state[aa] == True:
                jobs += 1

        if jobs > 0:
            if self.owner.electricity == False:
                e = int(12 / jobs)
            else:
                e = int(60 / jobs)

            #civ_mach
            if (
                self.storage["steel"] >= CIV_MACH_COST["steel"]
                and self.storage["aluminum"] >= CIV_MACH_COST["aluminum"]
                and self.storage["plastic"] >= CIV_MACH_COST["plastic"]
                and self.storage["parts"] >= CIV_MACH_COST["parts"]
                and self.state["civ_mach"] == True
                ):
                self.storage["steel"] -= CIV_MACH_COST["steel"]
                self.storage["aluminum"] -= CIV_MACH_COST["aluminum"]
                self.storage["plastic"] -= CIV_MACH_COST["plastic"]
                self.storage["parts"] -= CIV_MACH_COST["parts"]
                self.orders.append(["civ_mach", CIV_MACH_COST["time"]])

            #parts
            if (
                self.storage["steel"] >= PARTS_COST["steel"]
                and self.storage["aluminum"] >= PARTS_COST["aluminum"]
                and self.state["parts"] == True
                ):
                self.storage["steel"] -= PARTS_COST["steel"]
                self.storage["aluminum"] -= PARTS_COST["aluminum"]
                self.storage["parts"] += PARTS_COST["output"]
            
            #tools
            if (
                self.storage["steel"] >= TOOL_COST["steel"]
                and self.storage["plastic"] >= TOOL_COST["plastic"]
                and self.state["tools"] == True
                ):
                self.storage["steel"] -= TOOL_COST["steel"]
                self.storage["plastic"] -= TOOL_COST["plastic"]
                self.storage["tools"] += TOOL_COST["output"]

            #rifle
            if (
                self.storage["steel"] >= RIFLE_COST["steel"]
                and self.storage["plastic"] >= RIFLE_COST["plastic"]
                and self.state["rifle"] == True
                ):
                self.storage["steel"] -= RIFLE_COST["steel"]
                self.storage["plastic"] -= RIFLE_COST["plastic"]
                self.orders.append(["rifle", RIFLE_COST["time"]])

            #light_ammo
            if self.storage["steel"] >= e * LIGHT_AMMO_COST["steel"] and self.storage["textiles"] >= e * LIGHT_AMMO_COST["textiles"] and self.storage["chem_comp"] >= e * LIGHT_AMMO_COST["chem_comp"] and self.state["light_ammo"] == True:
                self.storage["steel"] -= e * LIGHT_AMMO_COST["steel"]
                self.storage["textiles"] -= e * LIGHT_AMMO_COST["textiles"]
                self.storage["chem_comp"] -= e * LIGHT_AMMO_COST["chem_comp"]
                self.storage["light_ammo"] += e * LIGHT_AMMO_COST["output"]

            #heavy_ammo
            if self.storage["steel"] >= e * HEAVY_AMMO_COST["steel"] and self.storage["plastic"] >= e * HEAVY_AMMO_COST["plastic"] and self.storage["chem_comp"] >= e * HEAVY_AMMO_COST["chem_comp"] and self.state["heavy_ammo"] == True:
                self.storage["steel"] -= e * HEAVY_AMMO_COST["steel"]
                self.storage["plastic"] -= e * HEAVY_AMMO_COST["plastic"]
                self.storage["chem_comp"] -= e * HEAVY_AMMO_COST["chem_comp"]
                self.orders.append(["heavy_ammo", HEAVY_AMMO_COST["time"]])
                #self.storage["heavy_ammo"] += e * HEAVY_AMMO_COST["output"]



        if self.owner.electricity == True:
            if len(self.orders) > 0:
                self.orders[0][1] = (
                    self.orders[0][1] - (1 + self.storage["civ_mach"])
                )  # 2 temporaly, normaly would be number of civilian machines
                if self.orders[0][1] <= 0:
                    self.storage[self.orders[0][0]] += 1
                    del self.orders[0]

        self.description[4] = (
            self.game.language.RES1[8] + ": " + str(self.storage["parts"])
        )
        self.description[5] = (
            self.game.language.RES1[7] + ": " + str(self.storage["tools"])
        )
        self.description[6] = (
            self.game.language.RES1[23] + ": " + str(self.storage["civ_mach"])
        )
        self.description[7] = (
            self.game.language.RES2[6] + ": " + str(self.storage["rifle"])
        )
        self.description[8] = (
            self.game.language.RES2[3] + ": " + str(self.storage["light_ammo"])
        )
        self.description[9] = (
            self.game.language.RES2[4] + ": " + str(self.storage["heavy_ammo"])
        )

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class CHEMICAL_PLANT(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        oil=0,
        plastic=0,
        chem_comp=0,
        textiles=0,
        calcium=0,
        fertilizer=0,
        steel=0,
        light_ammo=0,
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[14]
        self.state = {
            "plastic": False,
            "chem_comp": False,
            "textiles": False,
            "fertilizer": False,
            "light_ammo": False,
        }
        self.orders = []

        self.image = self.game.chemical_plant_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "oil": oil,
            "plastic": plastic,
            "chem_comp": chem_comp,
            "textiles": textiles,
            "calcium": calcium,
            "fertilizer": fertilizer,
            "steel": steel,
            "light_ammo": light_ammo,
        }

        self.upkeep = UPKEEP_BUILDING["chemical_plant"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here resources

        self.description[4] = (
            self.game.language.RES1[12] + ": " + str(self.storage["plastic"])
        )
        self.description[5] = (
            self.game.language.RES1[13] + ": " + str(self.storage["chem_comp"])
        )
        self.description[6] = (
            self.game.language.RES1[19] + ": " + str(self.storage["textiles"])
        )
        self.description[7] = (
            self.game.language.RES1[14] + ": " + str(self.storage["fertilizer"])
        )
        self.description[8] = (
            self.game.language.RES2[3] + ": " + str(self.storage["light_ammo"])
        )

    def do(self):
        jobs = 0
        for aa in self.all_jobs:
            if self.state[aa] == True:
                jobs += 1

        if jobs > 0:
            if self.owner.electricity == False:
                e = int(12 / jobs)
            else:
                e = int(60 / jobs)

            #plastic
            if (
                self.storage["oil"] >= PLASTIC_COST["oil"]
                and self.state["plastic"] == True
                ):
                self.storage["oil"] -= PLASTIC_COST["oil"]
                self.storage["plastic"] += PLASTIC_COST["output"]
            
            #chem_comp
            if (
                self.storage["oil"] >= CHEM_COMP_COST["oil"]
                and self.state["chem_comp"] == True
                ):
                self.storage["oil"] -= CHEM_COMP_COST["oil"]
                self.storage["chem_comp"] += CHEM_COMP_COST["output"]
            
            #textiles
            if (
                self.storage["plastic"] >= PET_TEXTILES_COST["plastic"]
                and self.state["textiles"] == True
                ):
                self.storage["plastic"] -= PET_TEXTILES_COST["plastic"]
                self.storage["textiles"] += PET_TEXTILES_COST["output"]
            
            #fertilizer
            if (
                self.storage["calcium"] >= FERTILIZER_COST["calcium"]
                and self.storage["chem_comp"] >= FERTILIZER_COST["chem_comp"]
                and self.state["fertilizer"] == True
                ):
                self.storage["calcium"] -= FERTILIZER_COST["calcium"]
                self.storage["chem_comp"] -= FERTILIZER_COST["chem_comp"]
                self.storage["fertilizer"] += FERTILIZER_COST["output"]

            #light_ammo
            if (self.storage["steel"] >= e * LIGHT_AMMO_COST["steel"] 
                and self.storage["textiles"] >= e * LIGHT_AMMO_COST["textiles"] 
                and self.storage["chem_comp"] >= e * LIGHT_AMMO_COST["chem_comp"] 
                and self.state["light_ammo"] == True):
                self.storage["steel"] -= e * LIGHT_AMMO_COST["steel"]
                self.storage["textiles"] -= e * LIGHT_AMMO_COST["textiles"]
                self.storage["chem_comp"] -= e * LIGHT_AMMO_COST["chem_comp"]
                self.storage["light_ammo"] += e * LIGHT_AMMO_COST["output"]

        self.description[4] = (
            self.game.language.RES1[12] + ": " + str(self.storage["plastic"])
        )
        self.description[5] = (
            self.game.language.RES1[13] + ": " + str(self.storage["chem_comp"])
        )
        self.description[6] = (
            self.game.language.RES1[19] + ": " + str(self.storage["textiles"])
        )
        self.description[7] = (
            self.game.language.RES1[14] + ": " + str(self.storage["fertilizer"])
        )
        self.description[8] = (
            self.game.language.RES2[3] + ": " + str(self.storage["light_ammo"])
        )

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class HIGH_TECH_PLANT(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        steel=0,
        aluminum=0,
        plastic=0,
        chem_comp=0,
        silicon=0,
        electronics=0,
        elec_comp=0,
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[15]
        self.state = {"elec_comp": False, "electronics": False}
        self.orders = []

        self.image = self.game.high_tech_plant_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "steel": steel,
            "aluminum": aluminum,
            "plastic": plastic,
            "chem_comp": chem_comp,
            "silicon": silicon,
            "elec_comp": elec_comp,
            "electronics": electronics,
        }

        self.upkeep = UPKEEP_BUILDING["high_tech_plant"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here resources

        self.description[4] = (
            self.game.language.RES1[24] + ": " + str(self.storage["elec_comp"])
        )
        self.description[5] = (
            self.game.language.RES1[17] + ": " + str(self.storage["electronics"])
        )

    def do(self):
        jobs = 0
        for aa in self.all_jobs:
            if self.state[aa] == True:
                jobs += 1

        if jobs > 0:
            if self.owner.electricity == True:

                #elec_comp
                if (
                    self.storage["aluminum"] >= ELEC_COMP_COST["aluminum"]
                    and self.storage["chem_comp"] >= ELEC_COMP_COST["chem_comp"]
                    and self.storage["silicon"] >= ELEC_COMP_COST["silicon"]
                    and self.state["elec_comp"] == True
                    ):
                    self.storage["aluminum"] -= ELEC_COMP_COST["aluminum"]
                    self.storage["chem_comp"] -= ELEC_COMP_COST["chem_comp"]
                    self.storage["silicon"] -= ELEC_COMP_COST["silicon"]
                    self.storage["elec_comp"] += ELEC_COMP_COST["output"]

                #electronics
                if (
                    self.storage["steel"] >= ELECTRONICS_COST["steel"]
                    and self.storage["plastic"] >= ELECTRONICS_COST["plastic"]
                    and self.storage["elec_comp"] >= ELECTRONICS_COST["elec_comp"]
                    and self.state["electronics"] == True
                    ):
                    self.storage["steel"] -= ELECTRONICS_COST["steel"]
                    self.storage["plastic"] -= ELECTRONICS_COST["plastic"]
                    self.storage["elec_comp"] -= ELECTRONICS_COST["elec_comp"]
                    self.storage["electronics"] += ELECTRONICS_COST["output"]

        self.description[4] = (
            self.game.language.RES1[24] + ": " + str(self.storage["elec_comp"])
        )
        self.description[5] = (
            self.game.language.RES1[17] + ": " + str(self.storage["electronics"])
        )

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class MECHANICAL_PLANT(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        steel=0,
        rubber=0,
        plastic=0,
        parts=0,
        tools=0,
        textiles=0,
        electronics=0,
        rifle=0,
        truck=0,
        apc=0,
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[16]
        self.state = {"rifle": False, "truck": False, "apc": False}
        self.orders = []

        self.image = self.game.mechanical_plant_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "steel": steel,
            "rubber": rubber,
            "plastic": plastic,
            "parts": parts,
            "tools": tools,
            "textiles": textiles,
            "electronics": electronics,
            "rifle": rifle,
            "truck": truck,
            "apc": apc,
        }

        self.upkeep = UPKEEP_BUILDING["mechanical_plant"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here resources

        self.description[4] = (
            self.game.language.RES2[6] + ": " + str(self.storage["rifle"])
        )
        self.description[5] = (
            self.game.language.RES2[8] + ": " + str(self.storage["truck"])
        )
        self.description[6] = (
            self.game.language.RES2[9] + ": " + str(self.storage["apc"])
        )

    def do(self):

        #rifle
        if (
            self.storage["steel"] >= RIFLE_COST["steel"]
            and self.storage["plastic"] >= RIFLE_COST["plastic"]
            and self.state["rifle"] == True
            ):
            self.storage["steel"] -= RIFLE_COST["steel"]
            self.storage["plastic"] -= RIFLE_COST["plastic"]
            self.orders.append(["rifle", RIFLE_COST["time"]])

        #truck
        if (
            self.storage["steel"] >= TRUCK_COST["steel"]
            and self.storage["rubber"] >= TRUCK_COST["rubber"]
            and self.storage["parts"] >= TRUCK_COST["parts"]
            and self.storage["tools"] >= TRUCK_COST["tools"]
            and self.storage["textiles"] >= TRUCK_COST["textiles"]
            and self.storage["electronics"] >= TRUCK_COST["electronics"]
            and self.state["truck"] == True
            ):
            self.storage["steel"] -= TRUCK_COST["steel"]
            self.storage["rubber"] -= TRUCK_COST["rubber"]
            self.storage["parts"] -= TRUCK_COST["parts"]
            self.storage["tools"] -= TRUCK_COST["tools"]
            self.storage["textiles"] -= TRUCK_COST["textiles"]
            self.storage["electronics"] -= TRUCK_COST["electronics"]
            self.orders.append(["truck", TRUCK_COST["time"]])
        
        #apc
        if (
            self.storage["steel"] >= APC_COST["steel"]
            and self.storage["rubber"] >= APC_COST["rubber"]
            and self.storage["parts"] >= APC_COST["parts"]
            and self.storage["tools"] >= APC_COST["tools"]
            and self.storage["textiles"] >= APC_COST["textiles"]
            and self.storage["electronics"] >= APC_COST["electronics"]
            and self.state["apc"] == True
            ):
            self.storage["steel"] -= APC_COST["steel"]
            self.storage["rubber"] -= APC_COST["rubber"]
            self.storage["parts"] -= APC_COST["parts"]
            self.storage["tools"] -= APC_COST["tools"]
            self.storage["textiles"] -= APC_COST["textiles"]
            self.storage["electronics"] -= APC_COST["electronics"]
            self.orders.append(["apc", APC_COST["time"]])

        if self.owner.electricity == True:
            if len(self.orders) > 0:
                self.orders[0][1] = (
                    self.orders[0][1] - 2
                )  # 2 temporaly, normaly would be number of civilian machines in factory
                if self.orders[0][1] <= 0:
                    self.storage[self.orders[0][0]] += 1
                    del self.orders[0]

        self.description[4] = (
            self.game.language.RES2[6] + ": " + str(self.storage["rifle"])
        )
        self.description[5] = (
            self.game.language.RES2[8] + ": " + str(self.storage["truck"])
        )
        self.description[6] = (
            self.game.language.RES2[9] + ": " + str(self.storage["apc"])
        )

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class ARMAMENT_PLANT(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        steel=0,
        rubber=0,
        plastic=0,
        parts=0,
        tools=0,
        textiles=0,
        electronics=0,
        rifle=0,
        truck=0,
        artilleries=0,
        tank=0,
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[17]
        self.state = {"rifle": False, "artilleries": False, "truck": False, "tank": False}
        self.orders = []

        self.image = self.game.armament_plant_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "steel": steel,
            "rubber": rubber,
            "plastic": plastic,
            "parts": parts,
            "tools": tools,
            "textiles": textiles,
            "electronics": electronics,
            "rifle": rifle,
            "artilleries": artilleries,
            "truck": truck,
            "tank": tank,
        }

        self.upkeep = UPKEEP_BUILDING["armament_plant"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here resources
        
        self.description[4] = (
            self.game.language.RES2[6] + ": " + str(self.storage["rifle"])
        )
        self.description[5] = (
            self.game.language.RES2[7] + ": " + str(self.storage["artilleries"])
        )
        self.description[6] = (
            self.game.language.RES2[8] + ": " + str(self.storage["truck"])
        )
        self.description[7] = (
            self.game.language.RES2[10] + ": " + str(self.storage["tank"])
        )

    def do(self):

        #rifle
        if (
            self.storage["steel"] >= RIFLE_COST["steel"]
            and self.storage["plastic"] >= RIFLE_COST["plastic"]
            and self.state["rifle"] == True
            ):
            self.storage["steel"] -= RIFLE_COST["steel"]
            self.storage["plastic"] -= RIFLE_COST["plastic"]
            self.orders.append(["rifle", RIFLE_COST["time"]])

        #artilleries
        if (
            self.storage["steel"] >= ARTILLERIES_COST["steel"]
            and self.storage["rubber"] >= ARTILLERIES_COST["rubber"]
            and self.storage["parts"] >= ARTILLERIES_COST["parts"]
            and self.storage["electronics"] >= ARTILLERIES_COST["electronics"]
            and self.state["artilleries"] == True
            ):
            self.storage["steel"] -= ARTILLERIES_COST["steel"]
            self.storage["rubber"] -= ARTILLERIES_COST["rubber"]
            self.storage["parts"] -= ARTILLERIES_COST["parts"]
            self.storage["electronics"] -= ARTILLERIES_COST["electronics"]
            self.orders.append(["artilleries", ARTILLERIES_COST["time"]])
        
        #truck
        if (
            self.storage["steel"] >= TRUCK_COST["steel"]
            and self.storage["rubber"] >= TRUCK_COST["rubber"]
            and self.storage["parts"] >= TRUCK_COST["parts"]
            and self.storage["tools"] >= TRUCK_COST["tools"]
            and self.storage["textiles"] >= TRUCK_COST["textiles"]
            and self.storage["electronics"] >= TRUCK_COST["electronics"]
            and self.state["truck"] == True
            ):
            self.storage["steel"] -= TRUCK_COST["steel"]
            self.storage["rubber"] -= TRUCK_COST["rubber"]
            self.storage["parts"] -= TRUCK_COST["parts"]
            self.storage["tools"] -= TRUCK_COST["tools"]
            self.storage["textiles"] -= TRUCK_COST["textiles"]
            self.storage["electronics"] -= TRUCK_COST["electronics"]
            self.orders.append(["truck", TRUCK_COST["time"]])
        
        #tank
        if (
            self.storage["steel"] >= TANK_COST["steel"]
            and self.storage["rubber"] >= TANK_COST["rubber"]
            and self.storage["parts"] >= TANK_COST["parts"]
            and self.storage["electronics"] >= TANK_COST["electronics"]
            and self.state["tank"] == True
            ):
            self.storage["steel"] -= TANK_COST["steel"]
            self.storage["rubber"] -= TANK_COST["rubber"]
            self.storage["parts"] -= TANK_COST["parts"]
            self.storage["electronics"] -= TANK_COST["electronics"]
            self.orders.append(["tank", TANK_COST["time"]])
        
        if self.owner.electricity == True:
            if len(self.orders) > 0:
                self.orders[0][1] = (
                    self.orders[0][1] - 2
                )  # 2 temporaly, normaly would be number of civilian machines
                if self.orders[0][1] <= 0:
                    self.storage[self.orders[0][0]] += 1
                    del self.orders[0]

        self.description[4] = (
            self.game.language.RES2[6] + ": " + str(self.storage["rifle"])
        )
        self.description[5] = (
            self.game.language.RES2[7] + ": " + str(self.storage["artilleries"])
        )
        self.description[6] = (
            self.game.language.RES2[8] + ": " + str(self.storage["truck"])
        )
        self.description[7] = (
            self.game.language.RES2[10] + ": " + str(self.storage["tank"])
        )

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class AVIATION_PLANT(BUILDING):
    def __init__(
        self,
        game,
        x,
        y,
        owner=0,
        steel=0,
        aluminum=0,
        textiles=0,
        rubber=0,
        plastic=0,
        parts=0,
        tools=0,
        elec_comp=0,
        chem_comp=0,
        light_ammo=0,
        rockets=0,
        helicopters=0,
        aircraft=0,
        
    ):
        self.groups = game.all_sprites, game.buildings
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.owner = self.game.players[owner]
        self.name = game.language.BUILDINGS1[17]
        self.state = {"light_ammo": False, "rockets": False, "helicopters": False, "aircraft": False}
        self.orders = []

        self.image = self.game.aviation_plant_img.copy()
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, (44, 10))
        self.rect = self.image.get_rect()
        self.storage = {
            "steel": steel,
            "aluminum": aluminum,
            "textiles": textiles,
            "rubber": rubber,
            "plastic": plastic,
            "parts": parts,
            "tools": tools,
            "elec_comp": elec_comp,
            "chem_comp": chem_comp,
            "light_ammo": light_ammo,
            "rockets": rockets,
            "helicopters": helicopters,
            "aircraft": aircraft,
        }

        self.upkeep = UPKEEP_BUILDING["aviation_plant"]
        self.window = ld.Building_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            "",
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )
        self.button = ld.OB_Button(
            self,
            self.game,
        )

        g = self.storage.keys()
        for a in g:
            self.window.variables.append(a)
        self.all_jobs = self.state.keys()
        b = 0
        for a in self.all_jobs:
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(
                    self.game.language.GUI[6], False, LIGHTGREY
                ),
                (180, 40),
            )
            self.window.image.blit(
                pg.font.Font(FONT_NAME, FONT_SIZE).render(a, False, LIGHTGREY),
                (180, 60 + (b * 20)),
            )
            self.window.buttons.append(
                ld.Switch_Button(
                    self.game,
                    self.window,
                    pos=[160, 60 + (b * 20)],
                    size=(20, 20),
                    color=LIGHTGREY,
                    text="X",
                    textsize=10,
                    textcolor=BLACK,
                    variable=a,
                )
            )
            b += 1

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.rect.x = self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        self.rect.y = self.y * TILESIZE[1]

        self.side = self.owner.side
        self.grid = self.game.map.grids[
            self.col + self.row * self.game.map.tmxdata.height
        ]
        self.grid.building = self
        self.description = [
            self.owner.name,
            self.name,
            "",
            self.game.language.GUI[4],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        # here resources

        self.description[4] = (
            self.game.language.RES2[3] + ": " + str(self.storage["light_ammo"])
        )
        self.description[5] = (
            self.game.language.RES2[5] + ": " + str(self.storage["rockets"])
        )
        self.description[6] = (
            self.game.language.RES2[11] + ": " + str(self.storage["helicopters"])
        )
        self.description[7] = (
            self.game.language.RES2[12] + ": " + str(self.storage["aircraft"])
        )

    def do(self):

        #light_ammo
        if (self.storage["steel"] >= LIGHT_AMMO_COST["steel"] 
            and self.storage["textiles"] >= LIGHT_AMMO_COST["textiles"] 
            and self.storage["chem_comp"] >= LIGHT_AMMO_COST["chem_comp"] 
            and self.state["light_ammo"] == True):
            self.storage["steel"] -= LIGHT_AMMO_COST["steel"]
            self.storage["textiles"] -= LIGHT_AMMO_COST["textiles"]
            self.storage["chem_comp"] -= LIGHT_AMMO_COST["chem_comp"]
            self.storage["light_ammo"] += LIGHT_AMMO_COST["output"]

        #rockets
        if (
            self.storage["aluminum"] >= ROCKETS_COST["aluminum"]
            and self.storage["chem_comp"] >= ROCKETS_COST["chem_comp"]
            and self.storage["plastic"] >= ROCKETS_COST["plastic"]
            and self.storage["parts"] >= ROCKETS_COST["parts"]
            and self.state["rockets"] == True
            ):
            self.storage["aluminum"] -= ROCKETS_COST["aluminum"]
            self.storage["chem_comp"] -= ROCKETS_COST["chem_comp"]
            self.storage["plastic"] -= ROCKETS_COST["plastic"]
            self.storage["parts"] -= ROCKETS_COST["parts"]
            self.orders.append(["rockets", ROCKETS_COST["time"]])

        #helicopters
        if (
            self.storage["aluminum"] >= HELICOPTERS_COST["aluminum"]
            and self.storage["rubber"] >= HELICOPTERS_COST["rubber"]
            and self.storage["parts"] >= HELICOPTERS_COST["parts"]
            and self.storage["tools"] >= HELICOPTERS_COST["tools"]
            and self.storage["elec_comp"] >= HELICOPTERS_COST["elec_comp"]
            and self.state["helicopters"] == True
            ):
            self.storage["aluminum"] -= HELICOPTERS_COST["aluminum"]
            self.storage["rubber"] -= HELICOPTERS_COST["rubber"]
            self.storage["parts"] -= HELICOPTERS_COST["parts"]
            self.storage["tools"] -= HELICOPTERS_COST["tools"]
            self.storage["elec_comp"] -= HELICOPTERS_COST["elec_comp"]
            self.orders.append(["helicopters", HELICOPTERS_COST["time"]])

        #aircraft
        if (
            self.storage["aluminum"] >= AIRCRAFT_COST["aluminum"]
            and self.storage["rubber"] >= AIRCRAFT_COST["rubber"]
            and self.storage["parts"] >= AIRCRAFT_COST["parts"]
            and self.storage["tools"] >= AIRCRAFT_COST["tools"]
            and self.storage["elec_comp"] >= AIRCRAFT_COST["elec_comp"]
            and self.state["aircraft"] == True
            ):
            self.storage["aluminum"] -= AIRCRAFT_COST["aluminum"]
            self.storage["rubber"] -= AIRCRAFT_COST["rubber"]
            self.storage["parts"] -= AIRCRAFT_COST["parts"]
            self.storage["tools"] -= AIRCRAFT_COST["tools"]
            self.storage["elec_comp"] -= AIRCRAFT_COST["elec_comp"]
            self.orders.append(["aircraft", AIRCRAFT_COST["time"]])
        
        
        if self.owner.electricity == True:
            if len(self.orders) > 0:
                self.orders[0][1] = (
                    self.orders[0][1] - 2
                )  # 2 temporaly, normaly would be number of civilian machines
                if self.orders[0][1] <= 0:
                    self.storage[self.orders[0][0]] += 1
                    del self.orders[0]


        self.description[4] = (
            self.game.language.RES2[3] + ": " + str(self.storage["light_ammo"])
        )
        self.description[5] = (
            self.game.language.RES2[5] + ": " + str(self.storage["rockets"])
        )
        self.description[6] = (
            self.game.language.RES2[11] + ": " + str(self.storage["helicopters"])
        )
        self.description[7] = (
            self.game.language.RES2[12] + ": " + str(self.storage["aircraft"])
        )

    def hourly(self):
        pass

    def daily(self):
        pass

    def weekly(self):
        #paying for maintanance building
        self.owner.money -= self.upkeep
        #paying money for land owner
        if self.grid.owner != None:
            if self.owner.id_num != self.grid.owner:
                self.owner.global_money -= self.game.players[self.grid.owner].build_tax
                self.game.players[self.grid.owner].global_money += self.game.players[self.grid.owner].build_tax

    def update(self):
        pass


class Unit(pg.sprite.Sprite):
    def __init__(
        self,
        game,
        x,
        y,
        loyalty=30,
        nationality=0,
        owner=0,
        typ=0,
        unit_name="Volunteers",
        brigade=0,
        regiment=0,
        battalion=0,
        company=0,
        men=0,
        supply=0,
        uniforms=0,
        fuel=0,
        light_ammo=0,
        heavy_ammo=0,
        rockets=0,
        rifle=0,
        art=0,
        truck=0,
        apc=0,
        tank=0,
        heli=0,
        aircraft=0,
        rocket_truck=0,
    ):

        self.groups = game.all_sprites, game.units
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.x = x
        self.y = y
        self.loyalty = loyalty
        self.nationality = self.game.nations[nationality]
        self.owner = self.game.players[owner]
        self.side = self.owner.side
        self.unit_typ = self.game.types[typ]
        self.typ = self.unit_typ.typ
        self.unit_name = unit_name
        self.unit_id = len(self.game.units)
        self.brigade = brigade
        self.regiment = regiment
        self.battalion = battalion
        self.company = company
        self.state = {
            "mobilized": True,
            "training": False,
            "building": False,
            "repeat": False,
            "engage": True,
            "conquest": False,
        }
        self.conditions = {
            "starving": False,
            "run_away": False
        }

        self.mobilized = True
        self.training = False
        #self.refill_equipment = False
        #self.refill_crew = False
        self.building = False

        self.order_list = []
        self.transporting = {}

        self.combat_ability = 20
        self.combat_ability_max = 20
        self.experience = 0
        self.tiredness = 0
        self.tiredness_max = 20
        self.fuel_usage = 0
        self.weekly_cost = 0
        self.max_transport = 0
        self.current_transport = 0
        self.task = self.game.language.COMMANDS[0]

        self.men = men
        self.max_men = self.unit_typ.max_men
        self.supply = supply
        self.max_supply = self.men * MEN_MAX_SUPPLY
        self.uniforms = uniforms
        self.max_uniforms = self.men

        self.fuel = fuel
        self.light_ammo = light_ammo
        self.heavy_ammo = heavy_ammo
        self.rockets = rockets

        self.rifle = rifle
        self.max_rifle = self.max_men
        self.artilleries = art
        self.max_artilleries = self.unit_typ.max_art
        self.truck = truck
        self.max_truck = self.unit_typ.max_truck
        self.rocket_truck = rocket_truck
        self.max_rocket_truck = self.unit_typ.max_rocket_truck
        self.apc = apc
        self.max_apc = self.unit_typ.max_apc
        self.tank = tank
        self.max_tank = self.unit_typ.max_tank
        self.heli = heli
        self.max_heli = self.unit_typ.max_heli
        self.aircraft = aircraft
        self.max_aircraft = self.unit_typ.max_aircraft

        self.max_fuel = (
            (self.truck * TRUCK_FUEL_CAP)
            + (self.apc * APC_FUEL_CAP)
            + (self.tank * TANK_FUEL_CAP)
            + (self.heli * HELI_FUEL_CAP)
            + (self.aircraft * AIRCRAFT_FUEL_CAP)
            + (self.rocket_truck * ROCKET_TRUCK_FUEL_CAP)
        )
        self.fuel_usage_calc()
        self.transporting_calc()
        self.max_light_ammo = 0
        self.max_light_ammo += (
            self.men * 5 + self.apc * 200 + self.tank * 100 + self.heli * 100
        )
        self.max_heavy_ammo = 0
        self.max_heavy_ammo += (
            self.tank * 30 + self.heli * 6 + self.aircraft * 12
        )
        self.max_rockets = 0
        self.max_rockets += self.heli * 6 + self.aircraft * 12 + self.rocket_truck * 40 

        self.visible = True
        self.pos = [50, 50]
        self.window = ld.Unit_Window(
            self,
            self.game,
            [300, 200],
            (700, 500),
            DARKGREY,
            self.unit_name
            + self.game.language.UNIT_STRU_SHORT[0]
            + str(self.brigade)
            + self.game.language.UNIT_STRU_SHORT[1]
            + str(self.regiment)
            + self.game.language.UNIT_STRU_SHORT[2]
            + str(self.battalion)
            + self.game.language.UNIT_STRU_SHORT[3]
            + str(self.company),
            16,
            LIGHTGREY,
            (35, 10),
            2,
        )

        self.button = ld.OU_Button(
            self,
            self.game,
        )

        self.col = x
        self.row = y
        self.hex = roffset_to_cube(-1, self)
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)

        self.image = pg.Surface((TILESIZE[0], TILESIZE[0]))
        self.image.fill(VIOLET)
        self.image.set_colorkey(VIOLET)

        # white / red / blue / green /yellow / lime / orange / grey / purple / brown / and other flag from onwers
        self.image.blit(self.owner.image, FLAG_OFFSET)

        # infantry / panc / arty / mech / recon / mot / other / support / heli / air / antiair / antipanc / engin / rocket
        # self.img_typ = self.image.blit(self.game.units_img.copy(), UNIT_OFFSET, (0, self.typ*UNIT_SIZE[1], UNIT_SIZE[0], UNIT_SIZE[1]))
        self.image.blit(self.unit_typ.image, UNIT_OFFSET)

        self.step_to = None
        self.to_do = None
        self.go_to = None
        self.path = None
        self.return_to = None
        self.doing = 0.0
        self.last_step_cost = 0
        self.step_cost = 0

        self.rect = self.image.get_rect()
        self.rect.x = (
            self.x * TILESIZE[0] - self.y % 2 * TILESIZE[0] / 2
        )  # + FLAG_OFFSET[0]
        self.rect.y = self.y * TILESIZE[1]  # + FLAG_OFFSET[1]

        # self.description = [self.owner.name, self.unit_typ.name, self.task, str(self.men), self.game.language.DESCRIPTION[0] + ": " + str(self.experience), "Sixth"]
        self.description = [
            self.owner.name,
            self.unit_typ.name,
            self.print_mobilized(),
            self.game.language.DESCRIPTION[2] + ": " + str(self.combat_ability),
            self.game.language.DESCRIPTION[0] + ": " + str(self.experience),
            self.game.language.DESCRIPTION[7]
            + ": "
            + str(self.tiredness)
            + "/"
            + str(self.tiredness_max),
            self.task,
        ]

    def fuel_usage_calc(self):
        self.fuel_usage = 0
        self.fuel_usage += TRUCK_FUEL_USAGE * self.truck
        self.fuel_usage += ROCKET_TRUCK_FUEL_USAGE * self.rocket_truck
        self.fuel_usage += APC_FUEL_USAGE * self.apc
        self.fuel_usage += TANK_FUEL_USAGE * self.tank
        self.fuel_usage += HELI_FUEL_USAGE * self.heli
        self.fuel_usage += AIRCRAFT_FUEL_USAGE * self.aircraft

    def transporting_calc(self):
        self.current_transport = 0
        for a in self.transporting.values():
            self.current_transport += a
        self.max_transport = 0
        self.max_transport = (
            (self.men * MEN_TRANSPORT_CAP)
            + (self.truck * TRUCK_TRANSPORT_CAP)
            + (self.apc * APC_TRANSPORT_CAP)
            + (self.tank * TANK_TRANSPORT_CAP)
            + (self.heli * HELI_TRANSPORT_CAP)
            + (self.aircraft * AIRCRAFT_TRANSPORT_CAP)
            + (self.rocket_truck * ROCKET_TRANSPORT_CAP)
        )

    def print_mobilized(self):
        if self.state["mobilized"] == True:
            return (
                self.game.language.DESCRIPTION[1] + ": " + self.game.language.BASIC[2]
            )
        else:
            return (
                self.game.language.DESCRIPTION[1] + ": " + self.game.language.BASIC[3]
            )

    def concquering(self):
        if self.state["conquest"] == True and self.conditions["run_away"] == False:
            if self.game.map.grids[self.hexid].owner != None:
                a = self.game.map.grids[self.hexid].owner
                b = self.owner.id_num
                # if False, that mean in war with grid/hex owner
                if self.game.diplomacy.relations[a][b][2] == False:  
                    self.game.map.grids[self.hexid].owner = self.owner.id_num
                    self.game.map.new_owner(
                        self.owner.id_num, roffset_from_cube(-1, self.hex)
                    )
                    if self.game.map.grids[self.hexid].building != None:
                        c = self.game.map.grids[self.hexid].building.owner.id_num
                        #if False, then mean in war with building owner
                        if self.game.diplomacy.relations[c][b][2] == False:  
                            self.game.map.grids[self.hexid].building.change_owner(self.owner.id_num)
                            self.owner.recalculate_all()
                else:
                    #if owner is not ally to then decrease relations
                    if self.game.diplomacy.relations[a][b][4] == False:
                        self.game.diplomacy.relations[a][b][0] -= 1
            else:
                self.game.map.grids[self.hexid].owner = self.owner.id_num
                self.game.map.new_owner(
                    self.owner.id_num, roffset_from_cube(-1, self.hex)
                )

    def terrain_cost(self, grid_id):
        global c
        global t

        t = self.game.map.grids[grid_id].terrain

        # if self.typ == 0 and self.fuel >= self.unit_typ.fuel_usage:
        if self.fuel >= self.fuel_usage:
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
            t = self.game.map.grids[grid_id].terrain
            if t == self.game.language.TERRAIN[0]:
                c = self.unit_typ.s_normal + self.unit_typ.s_no_fuel
            elif t == self.game.language.TERRAIN[1]:
                c = self.unit_typ.s_normal + self.unit_typ.s_no_fuel
            elif t == self.game.language.TERRAIN[2]:
                c = self.unit_typ.s_water + self.unit_typ.s_no_fuel
            elif t == self.game.language.TERRAIN[3]:
                c = self.unit_typ.s_mountain + self.unit_typ.s_no_fuel
            elif t == self.game.language.TERRAIN[4]:
                c = self.unit_typ.s_coast + self.unit_typ.s_no_fuel
            elif t == self.game.language.TERRAIN[5]:
                c = self.unit_typ.s_river + self.unit_typ.s_no_fuel
            elif t == self.game.language.TERRAIN[6]:
                c = self.unit_typ.s_normal + self.unit_typ.s_no_fuel
        # return int(c)
        return c  # self.unit_typ.move_cost(t)

    def check_grid(self):
        pass
        # if self.game.map.grids[self.col + self.row * self.game.map.tmxdata.height].building != None:
        # print("There is building")
        # else:
        # print("There is clear area to build something.")

    def stop(self):
        self.to_do = None
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
        self.go_to = roffset_to_cube(OFFSET, go_to)
        if self.state["repeat"] == True:
            self.return_to = roffset_to_cube(OFFSET, self)
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

                self.new_cost = (
                    self.cost_so_far[self.current[1]]
                    + (
                        (
                            self.terrain_cost(self.current[1])
                            + self.terrain_cost(next.id)
                        )
                    )
                    / 2
                    + additional
                )
                # self.terrain_cost(next.id)
                if (
                    next.id not in self.cost_so_far
                    or self.new_cost < self.cost_so_far[next.id]
                ):
                    self.cost_so_far[next.id] = self.new_cost
                    self.priority = self.new_cost
                    self.frontier.put((self.priority, next.id))
                    self.came_from[next.id] = self.current[1]
            if self.current[1] == hex_id(
                OFFSET, self.go_to, self.game.map.tmxdata.width
            ):
                break

        self.current = hex_id(OFFSET, self.go_to, self.game.map.tmxdata.width)
        self.path = []
        while self.current != self.hexid:
            self.path.append(self.current)
            self.current = self.came_from[self.current]

    def do(self):
        if len(self.order_list) > 0:#selecting task to do if not empty
            if self.to_do == None:#selecting task to do if not selected
                self.to_do = self.order_list[0]
                if self.to_do[0] == "go_to":
                    self.make_path(self.to_do[1])
                elif self.to_do[0] == "wait_time":
                    pass
                elif self.to_do[0] == "pick_up":
                    pass
                elif self.to_do[0] == "leave":
                    pass
                elif self.to_do[0] == "refill_eq":
                    pass
                elif self.to_do[0] == "refill_cr":
                    pass
                elif self.to_do[0] == "reorganize":
                    pass

        if self.to_do != None:#doing selected task
            if self.to_do[0] == "go_to":
                self.moving()
                self.task = self.game.language.COMMANDS[1] + str(self.x) + "/" + str(self.y)
            elif self.to_do[0] == "wait_time":
                self.wait_time()
                self.task = self.game.language.COMMANDS[0]
            elif self.to_do[0] == "pick_up":
                self.pick_up_goods(self.to_do[1][0], self.to_do[1][1])
                self.task = self.game.language.COMMANDS[5]
            elif self.to_do[0] == "leave":
                self.leave_goods(self.to_do[1][0], self.to_do[1][1])
                self.task = self.game.language.COMMANDS[6]
            elif self.to_do[0] == "refill_eq":
                self.refill_eq()
                self.task = self.game.language.COMMANDS[7]
            elif self.to_do[0] == "refill_cr":
                self.refill_cr()
                self.task = self.game.language.COMMANDS[8]
            elif self.to_do[0] == "reorganize":
                self.reorganize()
                self.task = self.game.language.COMMANDS[9]



            self.doing += 1
        else:
            #if not going / just stand
            self.doing = 0
            self.task = self.game.language.COMMANDS[0]

            if self.state["training"] == True:
                self.combat_ability = 5
                self.task = self.game.language.COMMANDS[2]

            if self.state["mobilized"] == True:
                if self.state["building"] == True:
                    self.combat_ability_max = 15
                else:
                    self.combat_ability_max = 25
            else:
                self.combat_ability_max = 5


    def refill_eq(self):
        f = None
        for u in self.game.units:
            #check if another unit is on same hex
            if u.unit_id != self.unit_id and u.hex == self.hex:
                if u.task == self.game.language.COMMANDS[0]:
                    f = u
            #if not then refill eq from transporting goods
            else:
                f = self
        if f != None:
            for d in self.unit_typ.equipment:
            #refill from transporting unit
                if d in f.transporting.keys() and f.owner == self.owner:
                    b = f.transporting[d]
                    c = 0
                    e = 0
                    if d == "supply":
                        c = self.max_supply - self.supply
                    elif d == "uniforms":
                        c = self.max_uniforms - self.uniforms
                    elif d == "fuel":
                        c = self.max_fuel - self.fuel
                    elif d == "light_ammo":
                        c = self.max_light_ammo - self.light_ammo
                    elif d == "heavy_ammo":
                        c = self.max_heavy_ammo - self.heavy_ammo
                    elif d == "rockets":
                        c = self.max_rockets - self.rockets
                    elif d == "rifle":
                        c = self.max_rifle - self.rifle
                    elif d == "artilleries":
                        c = self.max_artilleries - self.artilleries
                    elif d == "truck":
                        c = self.max_truck - self.truck
                        e = self.max_rocket_truck - self.rocket_truck
                    elif d == "apc":
                        c = self.max_apc - self.apc
                    elif d == "tank":
                        c = self.max_tank - self.tank
                    elif d == "rifle":
                        c = self.max_rifle - self.rifle
                    elif d == "heli":
                        c = self.max_heli - self.heli
                    elif d == "aircraft":
                        c = self.max_aircraft - self.aircraft

                    if b < c:
                        f.transporting[d] -= b
                        if d == "supply":
                            self.supply += b
                        elif d == "uniforms":
                            self.uniforms += b
                        elif d == "fuel":
                            self.fuel += b
                        elif d == "light_ammo":
                            self.light_ammo += b
                        elif d == "heavy_ammo":
                            self.heavy_ammo += b
                        elif d == "rockets":
                            self.rockets += b
                        elif d == "rifle":
                            self.rifle += b
                        elif d == "artilleries":
                            self.artilleries += b
                        elif d == "truck":
                            self.truck += b
                        elif d == "apc":
                            self.apc += b
                        elif d == "tank":
                            self.tank += b
                        elif d == "heli":
                            self.heli += b
                        elif d == "aircraft":
                            self.aircraft += b

                    else:
                        f.transporting[d] -= c
                        if d == "supply":
                            self.supply += c
                        if d == "uniforms":
                            self.uniforms += c
                        if d == "fuel":
                            self.fuel += c
                        if d == "light_ammo":
                            self.light_ammo += c
                        if d == "heavy_ammo":
                            self.heavy_ammo += c
                        if d == "rockets":
                            self.rockets += c
                        if d == "rifle":
                            self.rifle += c
                        if d == "artilleries":
                            self.artilleries += c
                        if d == "truck":
                            self.truck += c
                        if d == "apc":
                            self.apc += c
                        if d == "tank":
                            self.tank += c
                        if d == "heli":
                            self.heli += c
                        if d == "aircraft":
                            self.aircraft += c

                    if c == 0 and e > 0:
                        if b < e:
                            f.transporting[d] -= b
                            if d == "truck":
                                self.rocket_truck += b
                        else:
                            f.transporting[d] -= e
                            if d == "truck":
                                self.rocket_truck += e

                    self.fuel_usage_calc()
                    self.transporting_calc()
                    self.calculate_cost()

        if self.game.map.grids[self.hexid].building != None:
            a = self.game.map.grids[self.hexid].building
            for d in self.unit_typ.equipment:
                #refill from storage in building
                if d in a.storage.keys() and a.owner == self.owner:
                    if a.storage[d] > 100:
                        b = 100
                    else:
                        b = a.storage[d]
                    c = 0
                    e = 0
                    if d == "supply":
                        c = self.max_supply - self.supply
                    elif d == "uniforms":
                        c = self.max_uniforms - self.uniforms
                    elif d == "fuel":
                        c = self.max_fuel - self.fuel
                    elif d == "light_ammo":
                        c = self.max_light_ammo - self.light_ammo
                    elif d == "heavy_ammo":
                        c = self.max_heavy_ammo - self.heavy_ammo
                    elif d == "rockets":
                        c = self.max_rockets - self.rockets
                    elif d == "rifle":
                        c = self.max_rifle - self.rifle
                    elif d == "artilleries":
                        c = self.max_artilleries - self.artilleries
                    elif d == "truck":
                        c = self.max_truck - self.truck
                        e = self.max_rocket_truck - self.rocket_truck
                    elif d == "apc":
                        c = self.max_apc - self.apc
                    elif d == "tank":
                        c = self.max_tank - self.tank
                    elif d == "rifle":
                        c = self.max_rifle - self.rifle
                    elif d == "heli":
                        c = self.max_heli - self.heli
                    elif d == "aircraft":
                        c = self.max_aircraft - self.aircraft

                    if b < c:
                        a.storage[d] -= b
                        if d == "supply":
                            self.supply += b
                        elif d == "uniforms":
                            self.uniforms += b
                        elif d == "fuel":
                            self.fuel += b
                        elif d == "light_ammo":
                            self.light_ammo += b
                        elif d == "heavy_ammo":
                            self.heavy_ammo += b
                        elif d == "rockets":
                            self.rockets += b
                        elif d == "rifle":
                            self.rifle += b
                        elif d == "artilleries":
                            self.artilleries += b
                        elif d == "truck":
                            self.truck += b
                        elif d == "apc":
                            self.apc += b
                        elif d == "tank":
                            self.tank += b
                        elif d == "heli":
                            self.heli += b
                        elif d == "aircraft":
                            self.aircraft += b

                    else:
                        a.storage[d] -= c
                        if d == "supply":
                            self.supply += c
                        if d == "uniforms":
                            self.uniforms += c
                        if d == "fuel":
                            self.fuel += c
                        if d == "light_ammo":
                            self.light_ammo += c
                        if d == "heavy_ammo":
                            self.heavy_ammo += c
                        if d == "rockets":
                            self.rockets += c
                        if d == "rifle":
                            self.rifle += c
                        if d == "artilleries":
                            self.artilleries += c
                        if d == "truck":
                            self.truck += c
                        if d == "apc":
                            self.apc += c
                        if d == "tank":
                            self.tank += c
                        if d == "heli":
                            self.heli += c
                        if d == "aircraft":
                            self.aircraft += c

                    if c == 0 and e > 0:
                        if b < e:
                            a.storage[d] -= b
                            if d == "truck":
                                self.rocket_truck += b

                        else:
                            a.storage[d] -= e
                            if d == "truck":
                                self.rocket_truck += e

                    self.fuel_usage_calc()
                    self.transporting_calc()
                    self.calculate_cost()
            
        if self.to_do[1][0] <= self.doing:
            if self.state["repeat"] == True:
                self.order_list.append(self.to_do)
            self.stop()
            self.to_do = None
            del self.order_list[0]
            self.doing = 0
                

    def refill_cr(self):
        if self.game.map.grids[self.hexid].building != None:
            a = self.game.map.grids[self.hexid].building
            if (
                a.name == self.game.language.BUILDINGS1[1]
                or a.name == self.game.language.BUILDINGS1[2]
            ):
                if a.owner.name == self.owner.name and a.nationality.name == self.nationality.name:
                    # if a.storage['fuel']
                    if a.population > 20:
                        b = 4
                        c = self.max_men - self.men
                        if b < c:
                            a.population -= b
                            self.men += b
                            if self.experience >= 1:
                                self.experience -= 1
                                self.experience = round(self.experience, 2)
                        else:
                            a.population -= c
                            self.men += c
                            if self.experience >= 1:
                                self.experience -= 1
                                self.experience = round(self.experience, 2)
                    self.calculate_cost()
                    self.transporting_calc()

        if self.to_do[1][0] <= self.doing:
            if self.state["repeat"] == True:
                self.order_list.append(self.to_do)
            self.stop()
            self.to_do = None
            del self.order_list[0]
            self.doing = 0


    def moving(self):
        if self.go_to != None:
            if self.go_to == self.hex:#rewrite
                if self.state["repeat"] == True:
                    self.order_list.append(self.to_do)
                self.stop()
                self.to_do = None
                del self.order_list[0]
            else:
                if self.step_to == None:
                    if len(self.path) != 0:
                        self.step_to = self.path.pop()
                        self.step_cost = (
                            self.cost_so_far[self.step_to] - self.last_step_cost
                        )
                    else:
                        self.stop()

                if self.step_to != None:
                    self.task = (
                        self.game.language.COMMANDS[1]
                        + str(roffset_from_cube(-1, self.go_to)[0])
                        + ", "
                        + str(roffset_from_cube(-1, self.go_to)[1])
                    )
                    if self.fuel < self.fuel_usage:
                        # moving without fuel
                        if self.doing >= self.step_cost:

                            #self.doing = self.doing - self.step_cost

                            self.hex = self.game.map.grids[self.step_to].hex
                            self.hexid = hex_id(
                                OFFSET, self.hex, self.game.map.tmxdata.width
                            )
                            self.last_step_cost = self.cost_so_far[self.step_to]
                            self.step_to = None
                            self.concquering()
                            self.doing = 0
                    else:
                        if self.doing >= self.step_cost:
                            #self.doing = self.doing - self.step_cost
                            self.hex = self.game.map.grids[self.step_to].hex
                            self.hexid = hex_id(
                                OFFSET, self.hex, self.game.map.tmxdata.width
                            )
                            self.last_step_cost = self.cost_so_far[self.step_to]
                            self.step_to = None
                            self.concquering()
                            self.doing = 0
            if self.fuel > 0:
                self.fuel = self.fuel - self.fuel_usage
                if self.fuel < self.fuel_usage:
                    self.stop()
                    self.fuel = 0
            else:
                self.fuel = 0


    def wait_time(self):
        if self.to_do[1][0] <= self.doing:
            if self.state["repeat"] == True:
                self.order_list.append(self.to_do)
            self.stop()
            self.to_do = None
            del self.order_list[0]
            self.doing = 0


    def pick_up_goods(self, goods, quantity):
        self.transporting_calc()
        a = quantity
        b = self.max_transport - self.current_transport
        if quantity == 0:
            a = 3000
        if a > b:
            a = b

        if self.game.map.grids[self.hexid].building != None and a != 0:
            if self.game.map.grids[self.hexid].building.owner.name == self.owner.name:
                #check if specific goods are in building
                if goods in self.game.map.grids[self.hexid].building.storage:
                    c = self.game.map.grids[self.hexid].building.storage[goods]
                    if not goods in self.transporting:
                        self.transporting[goods] = 0
                    if c >= a:
                        self.transporting[goods] += a
                        self.game.map.grids[self.hexid].building.storage[goods] -= a
                        if self.state["repeat"] == True:
                            self.order_list.append(self.to_do)
                        self.stop()
                        self.to_do = None
                        del self.order_list[0]
                        self.doing = 0
                        self.transporting_calc()
                    else:
                        self.transporting[goods] += c
                        self.game.map.grids[self.hexid].building.storage[goods] -= c
                        if self.state["repeat"] == True:
                            self.order_list.append(self.to_do)
                        self.stop()
                        self.to_do = None
                        del self.order_list[0]
                        self.doing = 0
                        self.transporting_calc()
                else:
                    self.game.event_list.show_new_info([self.game.language.INFO_TEXTS[20], "Pos: " + str(self.x) + "/" + str(self.y)])
            else:
                self.game.event_list.show_new_info([self.game.language.INFO_TEXTS[21], "Pos: " + str(self.x) + "/" + str(self.y)])
        else:
            if a == 0:
                self.game.event_list.show_new_info([self.game.language.INFO_TEXTS[23], "Pos: " + str(self.x) + "/" + str(self.y)])
            else:
                self.game.event_list.show_new_info([self.game.language.INFO_TEXTS[22], "Pos: " + str(self.x) + "/" + str(self.y)])

                        
    def leave_goods(self, goods, quantity):
        a = quantity
        #if 0 or more then transporting, then leave all goods
        if goods in self.transporting: 
            if quantity == 0 or a > self.transporting[goods]:
                a = self.transporting[goods]
        if self.game.map.grids[self.hexid].building != None:
            if self.game.map.grids[self.hexid].building.owner.name == self.owner.name:
                #check if specific goods are in building
                if goods in self.game.map.grids[self.hexid].building.storage:
                    if goods in self.transporting:
                        if self.transporting[goods] >= a:
                            self.transporting[goods] -= a
                            self.game.map.grids[self.hexid].building.storage[goods] += a
                            if self.state["repeat"] == True:
                                self.order_list.append(self.to_do)
                            self.stop()
                            self.to_do = None
                            del self.order_list[0]
                            self.doing = 0
                            self.transporting_calc()
                        #del transporting goods from list if there is 0
                        if self.transporting[goods] == 0:
                            self.transporting.pop(goods)
                else:
                    self.game.event_list.show_new_info([self.game.language.INFO_TEXTS[20], "Pos: " + str(self.x) + "/" + str(self.y)])
            else:
                self.game.event_list.show_new_info([self.game.language.INFO_TEXTS[21], "Pos: " + str(self.x) + "/" + str(self.y)])
        else:
            self.game.event_list.show_new_info([self.game.language.INFO_TEXTS[22], "Pos: " + str(self.x) + "/" + str(self.y)])


    def reorganize(self):
        #supply
        if self.supply > self.max_supply:
            a = self.supply - self.max_supply
            self.supply -= a
            if "supply" not in self.transporting:
                self.transporting["supply"] = 0
            self.transporting["supply"] += a
        #uniforms
        if self.uniforms > self.max_uniforms:
            a = self.uniforms - self.max_uniforms
            self.uniforms -= a
            if "uniforms" not in self.transporting:
                self.transporting["uniforms"] = 0
            self.transporting["uniforms"] += a
        #fuel
        if self.fuel > self.max_fuel:
            a = self.fuel - self.max_fuel
            self.fuel -= a
            if "fuel" not in self.transporting:
                self.transporting["fuel"] = 0
            self.transporting["fuel"] += a
        #



        #repeat and del order
        if self.state["repeat"] == True:
            self.order_list.append(self.to_do)
        self.stop()
        self.to_do = None
        del self.order_list[0]
        self.doing = 0


    def change_owner(self, new_owner):
        self.owner = self.game.players[new_owner]

        self.image = pg.Surface((TILESIZE[0], TILESIZE[0]))
        self.image.fill(VIOLET)
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.owner.image, FLAG_OFFSET)
        self.image.blit(self.unit_typ.image, UNIT_OFFSET)
        self.loyalty = 30
        self.window.hide()


    def hourly(self):
        if (self.state["mobilized"] == True 
            and self.state["training"] == False 
            and self.conditions["starving"] == False 
            and self.conditions["run_away"] == False 
            and self.go_to == None):
            if self.combat_ability < self.combat_ability_max:
                self.combat_ability += 1
            elif self.combat_ability > self.combat_ability_max:
                self.combat_ability = self.combat_ability_max

        if self.state["mobilized"] == True and self.state["training"] == True and self.go_to == None:
            if self.experience < 100:
                self.experience += 0.1
                self.experience = round(self.experience, 2)
        elif (
            self.state["mobilized"] == True
            and self.state["training"] == False
            and self.state["building"] == True
            and self.go_to == None
        ):
            if self.game.map.grids[self.hexid].building != None:
                if self.game.map.grids[self.hexid].building.name == self.game.language.BUILDINGS1[0]:
                    if self.unit_typ == 14:
                        self.game.map.grids[self.hexid].building.construction(
                            round(self.men * 3 / 20, 2)
                        )
                    else:
                        self.game.map.grids[self.hexid].building.construction(
                            round(self.men / 20, 2)
                        )

    def daily(self):
        self.supply -= self.men
        if self.supply <= 0:
            self.conditions["starving"] = True
            self.supply = 0
            self.loyalty -= 1
        else:
            self.conditions["starving"] = False
        
        if self.owner.money < 0:
            self.loyalty -= 1

        if self.nationality == self.owner.nation:
            self.loyalty += 1

    def weekly(self):
        self.calculate_cost()
        self.owner.money -= self.weekly_cost

    def calculate_cost(self):
        self.weekly_cost = 0
        if self.state["mobilized"] == True:
            self.weekly_cost += self.men
        else:
            self.weekly_cost += int(self.men / 2)
        self.weekly_cost += self.truck * UPKEEP_TRUCK
        self.weekly_cost += self.apc * UPKEEP_APC
        self.weekly_cost += self.tank * UPKEEP_TANK
        self.weekly_cost += self.heli * UPKEEP_HELI
        self.weekly_cost += self.aircraft * UPKEEP_AIRCRAFT
        self.weekly_cost += self.rocket_truck * UPKEEP_ROCKET_TRUCK

    def update(self):
        self.hexid = hex_id(OFFSET, self.hex, self.game.map.tmxdata.width)
        self.col, self.row = roffset_from_cube(OFFSET, self.hex)
        self.x = self.col
        self.y = self.row

        self.rect.x = (
            self.x * TILESIZE[0] + self.y % 2 * TILESIZE[0] / 2
        )  # + FLAG_OFFSET[0]
        self.rect.y = self.y * TILESIZE[1]  # + FLAG_OFFSET[1]

        self.description = [
            self.owner.name,
            self.unit_typ.name,
            self.print_mobilized(),
            self.game.language.DESCRIPTION[2]
            + ": "
            + str(self.combat_ability)
            + "/"
            + str(self.combat_ability_max),
            self.game.language.DESCRIPTION[0] + ": " + str(self.experience),
            self.game.language.DESCRIPTION[7]
            + ": "
            + str(self.tiredness)
            + "/"
            + str(self.tiredness_max),
            self.task,
        ]
