import pygame as pg

# import pytmx
from pytmx.util_pygame import load_pygame
from settings import *
from sprites import *
import math


class Map:
    """
    IDK
    """
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE[0]
        self.height = self.tileheight * TILESIZE[1]


class TiledMap:
    """
    Map class, loading map: -tiles, -units, -resources, -buildings
    """
    def __init__(self, game, filename):
        """
        Construct of map

        :param game: refer to main game
        :param filename: map name
        """
        tm = load_pygame(
            filename, pixelalpha=True, load_all_tiles=True, allow_duplicate_names=True
        )
        self.game = game
        self.width = tm.width * tm.tilewidth + tm.tilewidth / 2
        self.height = tm.height * tm.tileheight * 48 / 64 + tm.tileheight / 2
        self.listtiles = [z for z in tm.gidmap]
        self.tmxdata = tm
        self.id = 0
        self.surface1 = pg.Surface((self.width, self.height))
        self.surface2 = pg.Surface((self.width, self.height))
        pg.draw.rect(self.surface2, VIOLET, (0, 0, self.width, self.height))
        self.surface2.set_colorkey(VIOLET)
        # print(self.tmxdata.width)

        self.grids = []
        self.grid_list = []
        self.resources = []
        self.trees = []
        self.units = []
        self.buildings = []
        self.cereals = []
        self.oil_filds = []

    def render(self, surface):
        """
        Load and render map graphic, load data from map file (units, res, buildings)
        """
        ti = self.tmxdata.get_tile_image_by_gid
        mg = self.tmxdata.map_gid
        re = self.tmxdata.register_gid
        # print(self.tmxdata.images)
        for layer in self.tmxdata.visible_layers:
            if layer.name == "layer1":
                for x, y, gid in layer:
                    po = re(gid)
                    # print(x, y, self.listtiles[int(gid - 1)], self.id)
                    tile = ti(gid)

                    # self.grids.append([x, y, self.get_terrain(self.listtiles[int(gid - 1)]), self.id])
                    self.grids.append(
                        Grid(
                            self.game,
                            x,
                            y,
                            self.get_terrain(self.listtiles[int(gid - 1)]),
                            self.id,
                            gid,
                        )
                    )
                    self.grid_list.append(
                        Hex(
                            x - (y - 1 * (y & 1)) // 2,
                            y,
                            -(x - (y - 1 * (y & 1)) // 2) - y,
                        )
                    )
                    # self.grids.append([x, y, self.listtiles[int(gid - 1)], self.id])

                    if tile:
                        surface.blit(
                            tile,
                            (
                                x * self.tmxdata.tilewidth
                                + (y & 1) * self.tmxdata.tilewidth / 2,
                                y * self.tmxdata.tileheight / TILESIZE[0] * TILESIZE[1],
                            ),
                        )
                    self.id += 1

            if layer.name == "layer3":
                for x, y, gid in layer:
                    tile = ti(gid)
                    # print(x, y, gid, tile)
                    # print(self.listtiles[int(gid - 1)])

                    if tile != None:
                        self.surface2.blit(
                            tile,
                            (
                                x * self.tmxdata.tilewidth
                                + (y & 1) * self.tmxdata.tilewidth / 2,
                                y * self.tmxdata.tileheight / TILESIZE[0] * TILESIZE[1],
                            ),
                        )

                        self.grids[(x + (y * self.tmxdata.width))].owner = int(
                            self.listtiles[int(gid - 1)] - 321
                        )

        self.surface2.set_colorkey(VIOLET)

        for grp in self.tmxdata.objectgroups:
            for obj in grp:
                if obj.name == "tree":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "tree",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "grain":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "grain",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "oil":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "oil",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "iron":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "iron",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "coal":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "coal",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "calcium":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "calcium",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "silicon":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "silicon",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "cotton":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "cotton",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "rubber":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "rubber",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "bauxite":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "bauxite",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "uranium":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "uranium",
                            obj.properties["value"],
                        ]
                    )
                elif obj.name == "water":
                    self.resources.append(
                        [
                            math.floor(obj.x / 64),
                            math.floor(obj.y / 48),
                            "water",
                            obj.properties["value"],
                        ]
                    )

                if obj.name == "unit":
                    self.units.append(
                        [
                            math.floor(obj.x / 64),  # 0
                            math.floor(obj.y / 48),
                            obj.properties["1_1_loyalty"],
                            obj.properties["1_1_nationality"],
                            obj.properties["1_1_owner"],
                            obj.properties["1_1_typ"],
                            obj.properties["1_1_unit_name"],
                            obj.properties["1_2_1_brigade"],
                            obj.properties["1_2_2_regiment"],
                            obj.properties["1_2_3_battalion"],
                            obj.properties["1_2_4_company"],  # 8
                            obj.properties["2_1_men"],
                            obj.properties["2_2_supply"],
                            obj.properties["2_3_uniforms"],
                            obj.properties["2_4_fuel"],
                            obj.properties["3_1_light_ammo"],
                            obj.properties["3_2_heavy_ammo"],
                            obj.properties["3_3_rockets"],
                            obj.properties["4_1_rifle"],
                            obj.properties["4_2_art"],
                            obj.properties["4_3_truck"],
                            obj.properties["4_4_apc"],
                            obj.properties["4_5_tank"],
                            obj.properties["4_6_heli"],
                            obj.properties["4_7_aircraft"],
                            obj.properties["4_8_rocket_truck"]
                            # 22
                        ]
                    )

                if obj.name == "building":
                    if obj.properties["typ"] == "CONSTRUCTION":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["what"],
                                obj.properties["owner"],
                                obj.properties["wood"],
                                obj.properties["cement"],
                                obj.properties["steel"],
                                obj.properties["progress"],
                            ]
                        )
                    elif obj.properties["typ"] == "VILLAGE":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["name"],
                                obj.properties["nationality"],
                                obj.properties["population"],
                                obj.properties["prosperity"],
                                obj.properties["food"],
                                obj.properties["wood"],
                                obj.properties["cotton"],
                                obj.properties["rubber"],
                                obj.properties["loyalty"],
                            ]
                        )
                    elif obj.properties["typ"] == "CITY":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["name"],
                                obj.properties["nationality"],
                                obj.properties["population"],
                                obj.properties["prosperity"],
                                obj.properties["food"],
                                obj.properties["textiles"],
                                obj.properties["furniture"],
                                obj.properties["electronics"],
                                obj.properties["loyalty"],
                            ]
                        )

                    elif (
                        obj.properties["typ"] == "HARBOR"
                        or obj.properties["typ"] == "AIRPORT"
                        or obj.properties["typ"] == "WAREHOUSE"
                    ):
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                [
                                    obj.properties["1_1_wood"],
                                    obj.properties["1_2_food"],
                                    obj.properties["1_3_cement"],
                                    obj.properties["1_4_iron_ore"],
                                    obj.properties["1_5_coal"],
                                    obj.properties["1_6_steel"],
                                    obj.properties["1_7_water"],
                                    obj.properties["1_8_tools"],
                                    obj.properties["1_9_parts"],
                                    obj.properties["2_1_aluminum"],
                                    obj.properties["2_2_oil"],
                                    obj.properties["2_3_fuel"],
                                    obj.properties["2_4_plastic"],
                                    obj.properties["2_5_chem_comp"],
                                    obj.properties["2_6_fertilizer"],
                                    obj.properties["2_7_silicon"],
                                    obj.properties["2_8_calcium"],
                                    obj.properties["2_9_electronics"],
                                    obj.properties["3_1_cotton"],
                                    obj.properties["3_2_textiles"],
                                    obj.properties["3_3_rubber"],
                                    obj.properties["3_4_bauxite"],
                                    obj.properties["3_5_furniture"],
                                    obj.properties["3_6_civ_mach"],
                                    obj.properties["3_7_elec_comp"],
                                ],
                                [
                                    obj.properties["4_1_supply"],
                                    obj.properties["4_2_uniforms"],
                                    obj.properties["4_3_fuel"],
                                    obj.properties["4_4_light_ammo"],
                                    obj.properties["4_5_heavy_ammo"],
                                    obj.properties["4_6_rockets"],
                                    obj.properties["4_7_rifle"],
                                    obj.properties["4_8_artilleries"],
                                    obj.properties["4_9_truck"],
                                    obj.properties["5_1_apc"],
                                    obj.properties["5_2_tank"],
                                    obj.properties["5_3_heli"],
                                    obj.properties["5_4_aircraft"],
                                ],
                            ]
                        )
                    elif obj.properties["typ"] == "BARRACK":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["cadets"],
                                obj.properties["graduates"],
                            ]
                        )

                    elif obj.properties["typ"] == "MINE":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["iron"],
                                obj.properties["coal"],
                                obj.properties["calcium"],
                                obj.properties["silicon"],
                                obj.properties["bauxite"],
                                obj.properties["uranium"],
                            ]
                        )
                    elif obj.properties["typ"] == "SMELTER":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["iron"],
                                obj.properties["coal"],
                                obj.properties["steel"],
                                obj.properties["bauxite"],
                                obj.properties["aluminum"],
                            ]
                        )
                    elif obj.properties["typ"] == "OIL_WELL":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["oil"],
                            ]
                        )
                    elif obj.properties["typ"] == "RAFINERY":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["oil"],
                                obj.properties["fuel"],
                                obj.properties["calcium"],
                                obj.properties["cement"],
                                obj.properties["coal"],
                            ]
                        )
                    elif obj.properties["typ"] == "POWER_PLANT":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["oil"],
                                obj.properties["coal"],
                            ]
                        )
                    elif obj.properties["typ"] == "LIGHT_INDUSTRY_PLANT":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["steel"],
                                obj.properties["food"],
                                obj.properties["supply"],
                                obj.properties["wood"],
                                obj.properties["furniture"],
                                obj.properties["cotton"],
                                obj.properties["textiles"],
                                obj.properties["uniforms"],
                            ]
                        )
                    elif obj.properties["typ"] == "HEAVY_INDUSTRY_PLANT":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["steel"],
                                obj.properties["aluminum"],
                                obj.properties["plastic"],
                                obj.properties["parts"],
                                obj.properties["tools"],
                                obj.properties["civ_mach"],
                                obj.properties["rifle"],
                            ]
                        )
                    elif obj.properties["typ"] == "CHEMICAL_PLANT":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["oil"],
                                obj.properties["plastic"],
                                obj.properties["chem_comp"],
                                obj.properties["textiles"],
                                obj.properties["fertilizer"],
                            ]
                        )
                    elif obj.properties["typ"] == "HIGH_TECH_PLANT":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["steel"],
                                obj.properties["aluminum"],
                                obj.properties["plastic"],
                                obj.properties["chem_comp"],
                                obj.properties["silicon"],
                                obj.properties["electronics"],
                                obj.properties["elec_comp"],
                            ]
                        )
                    elif obj.properties["typ"] == "MECHANICAL_PLANT":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["steel"],
                                obj.properties["rubber"],
                                obj.properties["parts"],
                                obj.properties["tools"],
                                obj.properties["textiles"],
                                obj.properties["electronics"],
                                obj.properties["truck"],
                                obj.properties["apc"],
                            ]
                        )
                    elif obj.properties["typ"] == "ARMAMENT_PLANT":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["steel"],
                                obj.properties["rubber"],
                                obj.properties["plastic"],
                                obj.properties["parts"],
                                obj.properties["electronics"],
                                obj.properties["rifle"],
                                obj.properties["artilleries"],
                                obj.properties["tank"],
                            ]
                        )
                    elif obj.properties["typ"] == "AVIATION_PLANT":
                        self.buildings.append(
                            [
                                math.floor(obj.x / 64),
                                math.floor(obj.y / 48),
                                obj.properties["typ"],
                                obj.properties["owner"],
                                obj.properties["aluminum"],
                                obj.properties["rubber"],
                                obj.properties["plastic"],
                                obj.properties["parts"],
                                obj.properties["electronics"],
                                obj.properties["rockets"],
                                obj.properties["helicopters"],
                                obj.properties["aircraft"],
                            ]
                        )

        # self.grid_list = set(self.grid_list)

    def new_owner(self, owner, coord):
        """
        Function uset to generate new tiles ownership

        :param owner: new owner
        :param coord: coordinate of tile. They are convertet do tile id
        """
        self.surface2.blit(
            self.game.players[owner].color,
            (
                coord[0] * self.tmxdata.tilewidth
                + (coord[1] & 1) * self.tmxdata.tilewidth / 2,
                coord[1] * self.tmxdata.tileheight / TILESIZE[0] * TILESIZE[1],
            ),
        )

    def get_terrain(self, a):
        """
        Function return corect tile typ name
        """
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
        """
        Function used to generate tile map surface
        """
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

    def update_map_owning(self):
        pass

    def make_objects(self):
        pass


class Camera:
    """
    Object contain position of camera. This position is used later to display map
    """
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def apply(self, entity):
        return entity.rect.move(
            self.camera.topleft - pg.Vector2(TILESIZE[0] / 2, TILESIZE[0] / 2)
        )

    def apply_rect(self, rect):
        return rect.move(
            self.camera.topleft - pg.Vector2(TILESIZE[0] / 2, TILESIZE[0] / 2)
        )

    def update(self, target):
        self.x = -target.rect.x + int(WIDTH / 2)
        self.y = -target.rect.y + int(HEIGHT / 2)
        self.camera = pg.Rect(self.x, self.y, self.width, self.height)
