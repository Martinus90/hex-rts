import sys
import math

import pygame as pg
from os import path
from hexo import *
from settings import *
from sprites import *
from tilemap import *
from loading import *
from languages import *

class Game:
    def __init__(self, player=1):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.language = Language()
        self.timer = 0
        self.quarter = 0
        self.hour = 0
        self.day = 1
        self.idn = 0
        self.week = 1
        self.season = 0
        self.year = 1980
        self.speed = GAME_SPEED
        self.pause = False
        self.selecting = None
        self.resourcing = None
        self.uniting = None
        self.building = None
        self.window_display = False
        self.dragging = False
        self.dragged = None
        self.territory_visible = False
        self.s_drag = pg.Vector2
        self.nations = []
        self.players = []
        self.types = []

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        gui_folder = path.join(game_folder, 'gui')
        map_folder = path.join(game_folder, 'maps')
        self.myfont = pg.font.Font(FONT_NAME, 24)
        self.layout = Layout(layout_pointy, Point(36.9, 32.0), Point(0.0, 0.0))

        if 1 == 1: #rolling loading images

            self.plr_img = pg.image.load(path.join(img_folder, PLAYER_IMG))
            self.flags_img = pg.image.load(path.join(img_folder, FLAGS_IMG))
            self.units_img = pg.image.load(path.join(img_folder, UNITS_IMG))
            self.colors_img = pg.image.load(path.join(img_folder, COLOR_GRIDS))
            self.colors_img.set_colorkey(VIOLET)
            self.resource_img = pg.image.load(path.join(img_folder, RESOURCE_IMG))
            self.tree_img = pg.image.load(path.join(img_folder, TREE_IMG))
            self.grain_img = pg.image.load(path.join(img_folder, GRAIN_IMG))
            self.oil_img = pg.image.load(path.join(img_folder, OIL_IMG))
            self.iron_img = pg.image.load(path.join(img_folder, IRON_IMG))
            self.coal_img = pg.image.load(path.join(img_folder, COAL_IMG))
            self.calcium_img = pg.image.load(path.join(img_folder, CALCIUM_IMG))
            self.silicon_img = pg.image.load(path.join(img_folder, SILICON_IMG))
            self.cotton_img = pg.image.load(path.join(img_folder, COTTON_IMG))
            self.rubber_img = pg.image.load(path.join(img_folder, RUBBER_IMG))
            self.bauxite_img = pg.image.load(path.join(img_folder, BAUXITE_IMG))
            self.uranium_img = pg.image.load(path.join(img_folder, URANIUM_IMG))
            self.water_img = pg.image.load(path.join(img_folder, WATER_IMG))

            self.money_img = pg.image.load(path.join(img_folder, MONEY_IMG))
            self.global_img = pg.image.load(path.join(img_folder, GLOBAL_IMG))
            self.global_img.set_colorkey(VIOLET)
            self.exchange_img = pg.image.load(path.join(img_folder, EXCHANGE_IMG))
            self.exchange_img.set_colorkey(VIOLET)
            self.reputation_img = pg.image.load(path.join(gui_folder, REPUTATION_IMG))
            self.reputation_img.set_colorkey(VIOLET)
            self.stability_img = pg.image.load(path.join(gui_folder, STABILITY_IMG))
            self.stability_img.set_colorkey(VIOLET)
            self.stability = []
            for a in range(5):
                self.image = pg.Surface(STABILITY_SIZE)
                self.image.fill(VIOLET)
                self.image.set_colorkey(VIOLET)
                self.image.blit(self.stability_img.copy(),(0, 0), (0, a*STABILITY_SIZE[1], STABILITY_SIZE[0], STABILITY_SIZE[1]))
                self.stability.append(self.image)

            self.construction_img = pg.image.load(path.join(img_folder, CONSTRUCTION_IMG))
            self.village_img = pg.image.load(path.join(img_folder, VILLAGE_IMG))
            self.city_img = pg.image.load(path.join(img_folder, CITY_IMG))
            self.harbor_img = pg.image.load(path.join(img_folder, HARBOR_IMG))
            self.airport_img = pg.image.load(path.join(img_folder, AIRPORT_IMG))
            self.warehouse_img = pg.image.load(path.join(img_folder, WAREHOUSE_IMG))
            self.barrack_img = pg.image.load(path.join(img_folder, BARRACK_IMG))
            self.mine_img = pg.image.load(path.join(img_folder, MINE_IMG))
            self.smelter_img = pg.image.load(path.join(img_folder, SMELTER_IMG))
            self.oil_well_img = pg.image.load(path.join(img_folder, OIL_WELL_IMG))
            self.rafinery_img = pg.image.load(path.join(img_folder, RAFINERY_IMG))
            self.power_plant_img = pg.image.load(path.join(img_folder, POWER_PLANT_IMG))
            self.light_industry_plant_img = pg.image.load(path.join(img_folder, LIGHT_INDUSTRY_PLANT_IMG))
            self.heavy_industry_plant_img = pg.image.load(path.join(img_folder, HEAVY_INDUSTRY_PLANT_IMG))
            self.chemical_plant_img = pg.image.load(path.join(img_folder, CHEMICAL_PLANT_IMG))
            self.high_tech_plant_img = pg.image.load(path.join(img_folder, HIGH_TECH_PLANT_IMG))
            self.mechanical_plant_img = pg.image.load(path.join(img_folder, MECHANICAL_PLANT_IMG))
            self.armament_plant_img = pg.image.load(path.join(img_folder, ARMAMENT_PLANT_IMG))
            self.aviation_plant_img = pg.image.load(path.join(img_folder, AVIATION_PLANT_IMG))
            self.shipyard_img = pg.image.load(path.join(img_folder, SHIPYARD_IMG))

            self.x_img = pg.image.load(path.join(gui_folder, X_IMG))
            self.window_img = pg.image.load(path.join(gui_folder, WINDOW_IMG))
            self.o_window_img = pg.image.load(path.join(gui_folder, O_WINDOW_IMG))
            self.o_window_img.blit(pg.font.Font(FONT_NAME, 24).render("Open", False, LIGHTGREY), (2,4))
            self.button_1_img = pg.image.load(path.join(gui_folder, O_WINDOW_IMG))
            self.elect_yes_img = pg.image.load(path.join(gui_folder, ELECT_YES))
            self.elect_yes_img.set_colorkey(VIOLET)
            self.elect_no_img = pg.image.load(path.join(gui_folder, ELECT_NO))
            self.elect_no_img.set_colorkey(VIOLET)

            self.yes_img = pg.image.load(path.join(gui_folder, YES_IMG))
            self.no_img = pg.image.load(path.join(gui_folder, NO_IMG))

        self.map = TiledMap(self, path.join(map_folder, 'default.tmx'))#test / test2 / default
        
        #side 0 is always neutral / side 1 is always player / other side are variable
        #self.side_0 = "Neutral" 
        #self.side_1 = "Player"
        #self.side_2 = "Enemy"

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.grids = pg.sprite.Group()
        self.resources = pg.sprite.Group()
        self.menus = pg.sprite.Group()
        self.windows = pg.sprite.Group()
        self.unit_windows = pg.sprite.Group()
        self.building_windows = pg.sprite.Group()
        self.menu_windows = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        self.settlements = pg.sprite.Group()
        self.buildings = pg.sprite.Group()
        self.units = pg.sprite.Group()
        self.texts = []

        self.nations.append(Nation(self, name="Sovenyan"))
        self.nations.append(Nation(self, name="Nebohracy"))

        #first on the list is always neutral, second is player, 3+ are others / to change color just change side
        self.player = Player(self, 0, 0, 1)
        self.players.append(Contender(self, name="Neutral", nation=0, player=False, side=0, exc_rt=1.0, money=0, global_money=0, reputation=0, stability=0, tax=3))
        self.players.append(Contender(self, name="Sovenya", nation=0, player=True, side=1, exc_rt=1.0, money=10000, global_money=0, reputation=0, stability=0, tax=3))
        self.players.append(Contender(self, name="Nebohray", nation=1, player=False, side=2, exc_rt=1.0, money=10000, global_money=0, reputation=0, stability=0, tax=3))
        self.players.append(Contender(self, name="Sovenyan Rebels", nation=0, player=False, side=3.0, exc_rt=1.0, money=10000, global_money=0, reputation=0, stability=0, tax=3))
        self.players.append(Contender(self, name="hj6u654", nation=1, player=False, side=4, exc_rt=1.0, money=10000, global_money=0, reputation=0, stability=0, tax=3))

        self.diplomacy = Diplomacy(self)
        self.event_list = Event_List(self, [[5, "event_name", 'here_event_properties'], [7, "event_name2", "here_event_properies2"]])
        self.event_list.add_event([7, "event_name", "Event 3"])


        
        self.trade = Trade(self)
        self.players[1].relations[2][2] = False
        self.players[2].relations[1][2] = False

            #unit types
        #infantry
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[0], typ=0, s_normal=4, s_water=100, s_mountain=6, s_coast=4, s_river=12, s_no_fuel=20, money_usage=2, max_men=79, max_art=0, max_truck=0, max_apc=0, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #armored
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[1], typ=1, s_normal=2, s_water=100, s_mountain=12, s_coast=4, s_river=12, s_no_fuel=40, money_usage=2, max_men=20, max_art=0, max_truck=0, max_apc=0, max_tank=4, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #artillery
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[2], typ=2, s_normal=2, s_water=100, s_mountain=12, s_coast=4, s_river=12, s_no_fuel=20, money_usage=2, max_men=25, max_art=4, max_truck=4, max_apc=0, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #mechanized
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[3], typ=3, s_normal=2, s_water=100, s_mountain=12, s_coast=4, s_river=12, s_no_fuel=40, money_usage=2, max_men=99, max_art=0, max_truck=0, max_apc=9, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #reconnaissance
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[4], typ=4, s_normal=2, s_water=100, s_mountain=8, s_coast=3, s_river=8, s_no_fuel=20, money_usage=2, max_men=99, max_art=0, max_truck=4, max_apc=4, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #motorized
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[5], typ=5, s_normal=2, s_water=100, s_mountain=12, s_coast=4, s_river=12, s_no_fuel=20, money_usage=2, max_men=99, max_art=0, max_truck=9, max_apc=0, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #other
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[6], typ=6, s_normal=4, s_water=100, s_mountain=6, s_coast=4, s_river=12, s_no_fuel=20, money_usage=1, max_men=79, max_art=0, max_truck=0, max_apc=0, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #logistic
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[7], typ=7, s_normal=2, s_water=100, s_mountain=12, s_coast=4, s_river=12, s_no_fuel=20, money_usage=2, max_men=64, max_art=0, max_truck=20, max_apc=0, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #headquaters
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[8], typ=8, s_normal=2, s_water=100, s_mountain=12, s_coast=4, s_river=12, s_no_fuel=20, money_usage=2, max_men=30, max_art=0, max_truck=5, max_apc=0, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #helicopters
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[9], typ=9, s_normal=2, s_water=2, s_mountain=2, s_coast=2, s_river=2, s_no_fuel=40, money_usage=10, max_men=6, max_art=0, max_truck=0, max_apc=0, max_tank=0, max_heli=3, max_aircraft=0, max_rocket_truck=0))
        
        #aircraft
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[10], typ=10, s_normal=1, s_water=1, s_mountain=1, s_coast=1, s_river=1, s_no_fuel=40, money_usage=20, max_men=6, max_art=0, max_truck=0, max_apc=0, max_tank=0, max_heli=0, max_aircraft=3, max_rocket_truck=0))
        
        #need to do 

        #AA anti-aircraft
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[11], typ=11, s_normal=3, s_water=100, s_mountain=12, s_coast=5, s_river=12, s_no_fuel=40, money_usage=2, max_men=25, max_art=0, max_truck=5, max_apc=0, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #anti-armor
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[12], typ=12, s_normal=2, s_water=100, s_mountain=12, s_coast=4, s_river=12, s_no_fuel=20, money_usage=2, max_men=25, max_art=0, max_truck=5, max_apc=0, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #rocket
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[13], typ=13, s_normal=2, s_water=100, s_mountain=12, s_coast=5, s_river=12, s_no_fuel=40, money_usage=5, max_men=25, max_art=0, max_truck=5, max_apc=0, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))
        
        #engineering
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[14], typ=14, s_normal=2, s_water=100, s_mountain=10, s_coast=4, s_river=12, s_no_fuel=40, money_usage=3, max_men=25, max_art=0, max_truck=5, max_apc=0, max_tank=0, max_heli=0, max_aircraft=0, max_rocket_truck=0))


        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        
        for grid in self.map.grids:
            grid.get_neighbors(self.map)

        #print(self.map.grids)
        self.menu = Menu(self)#.make_menu()
        self.menu2 = self.menu.make_menu()
        self.menu_rect = self.menu2.get_rect()

        for r in self.map.resources:
            if r[2] == "tree":
                Tree(self, r[0], r[1], r[3])
            elif r[2] == "grain":
                Grain(self, r[0], r[1], r[3])
            elif r[2] == "oil":
                Oil(self, r[0], r[1], r[3])
            elif r[2] == "iron":
                Iron(self, r[0], r[1], r[3])
            elif r[2] == "coal":
                Coal(self, r[0], r[1], r[3])
            elif r[2] == "calcium":
                Calcium(self, r[0], r[1], r[3])
            elif r[2] == "silicon":
                Silicon(self, r[0], r[1], r[3])
            elif r[2] == "cotton":
                Cotton(self, r[0], r[1], r[3])
            elif r[2] == "rubber":
                Rubber(self, r[0], r[1], r[3])
            elif r[2] == "bauxite":
                Bauxite(self, r[0], r[1], r[3])
            elif r[2] == "uranium":
                Uranium(self, r[0], r[1], r[3])
            elif r[2] == "water":
                Water(self, r[0], r[1], r[3])

        for b in self.map.buildings:
            if b[2] == "CONSTRUCTION":
                CONSTRUCTION(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8])
            elif b[2] == "VILLAGE":
                VILLAGE(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9])
            elif b[2] == "CITY":
                CITY(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11])
            elif b[2] == "HARBOR":
                HARBOR(self, b[0], b[1], b[3], b[4], b[5])
            elif b[2] == "AIRPORT":
                AIRPORT(self, b[0], b[1], b[3], b[4], b[5])
            elif b[2] == "WAREHOUSE":
                WAREHOUSE(self, b[0], b[1], b[3], b[4], b[5])
            elif b[2] == "BARRACK":
                BARRACK(self, b[0], b[1], b[3], b[4], b[5])

            elif b[2] == "MINE":
                MINE(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9])
            elif b[2] == "SMELTER":
                SMELTER(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8])
            elif b[2] == "OIL_WELL":
                OIL_WELL(self, b[0], b[1], b[3], b[4])
            elif b[2] == "RAFINERY":
                RAFINERY(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8])
            elif b[2] == "POWER_PLANT":
                POWER_PLANT(self, b[0], b[1], b[3], b[4], b[5])
            elif b[2] == "LIGHT_INDUSTRY_PLANT":
                LIGHT_INDUSTRY_PLANT(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11])
            elif b[2] == "HEAVY_INDUSTRY_PLANT":
                HEAVY_INDUSTRY_PLANT(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10])
            elif b[2] == "CHEMICAL_PLANT":
                CHEMICAL_PLANT(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8])
            elif b[2] == "HIGH_TECH_PLANT":
                HIGH_TECH_PLANT(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10])
            elif b[2] == "MECHANICAL_PLANT":
                MECHANICAL_PLANT(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11])
            elif b[2] == "ARMAMENT_PLANT":
                ARMAMENT_PLANT(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11])
            elif b[2] == "AVIATION_PLANT":
                AVIATION_PLANT(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11])
            

        for u in self.map.units:
            Unit(self, u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8], u[9], u[10], u[11], u[12], u[13], u[14], u[15], u[16], u[17], u[18], u[19], u[20], u[21], u[22], u[23], u[24])

        
        self.camera = Camera(self.map.width, self.map.height)

    def adding_building(self, variable):
        CONSTRUCTION(self, self.selecting.col, self.selecting.row, BUILDING_LIST[variable], self.player.side, 0, 0, 0, 0)

    def build(self, construction):
        if construction.what == OIL_WELL:
            a = construction
            del construction
            OIL_WELL(self, a.x, a.y, a.owner)

    def time(self):
        if self.timer > 1: #def 1
            self.timer -= 1
            self.quarter += 1
            for unit in self.units:
                unit.do()
            for res in self.resources:
                res.do()
            for building in self.buildings:
                building.do()

        if self.quarter > 3: #def 3
            self.quarter -= 4
            self.hour += 1
            for cont in self.players:
                cont.hourly()
            for unit in self.units:
                unit.hourly()
            for building in self.buildings:
                building.hourly()
        if self.hour > 23: #def 23
            self.hour -= 24
            self.day += 1
            self.idn = (self.day + (
                                    (self.week - 1) * 7) + (
                                    self.season * 91) + (
                                    (self.year - 1980) * 364))


            for res in self.resources:
                res.daily()
            for building in self.buildings:
                building.daily()
            for unit in self.units:
                unit.daily()
            self.diplomacy.dayli()
            self.menu.trade_window.dayli()
            self.trade.dayli()
            self.event_list.dayli()
        if self.day > 7: #def 7
            self.day -= 7
            self.week += 1
            for building in self.buildings:
                building.weekly()
        if self.week > 13: #13
            self.week -= 13
            self.season += 1
            for res in self.resources:
                res.seasonly()
            for building in self.buildings:
                building.seasonly()
        if self.season > 3: #def 3
            self.season -= 4
            self.year += 1

    def mouse(self):
        #if pg.mouse.get_pos() >=
        nowy2 = hex_round(pixel_to_hex(self.layout, pg.Vector2(pg.mouse.get_pos()) - pg.Vector2(self.camera.x , self.camera.y)))
        self.mouse_pos = roffset_from_cube(-1, nowy2)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            if self.pause == False:
                self.timer += self.dt * self.speed
            self.update()
            self.events()
            self.draw()

    def select(self, select_new):
        for grid in self.map.grids:
            if (grid.col == self.mouse_pos.col) and (grid.row == self.mouse_pos.row):
                self.selecting = grid
                self.menu.terrain1[0] = "X: " + str(self.selecting.col) + ", Y: " + str(self.selecting.row)
                self.menu.terrain2[0] = str(self.selecting.terrain)
                self.selecting.get_near_resources()
                print(self.selecting.owner)

        for r in self.resources:
            if (r.col == self.mouse_pos.col) and (r.row == self.mouse_pos.row):
                self.resourcing = r
                self.menu.terrain3[0] = self.resourcing.name + " " + str(self.resourcing.value)
                break
            else:
                self.resourcing = None
                self.menu.terrain3[0] = ""

        for u in self.units:
            if (u.col == self.mouse_pos.col) and (u.row == self.mouse_pos.row) and (u.owner.player == True):
                #print("Tak tu jest jednostka")
                self.uniting = u
                self.uniting.check_grid()
                self.menu.unit1[0] = self.uniting.description[0]
                self.menu.unit2[0] = self.uniting.description[1]
                self.menu.unit3[0] = self.uniting.description[2]
                self.menu.unit4[0] = self.uniting.description[3]
                self.menu.unit5[0] = self.uniting.description[4]
                self.menu.unit6[0] = self.uniting.description[5]
                self.menu.unit7[0] = self.uniting.description[6]
                print("Unit typ:")
                print(self.uniting.unit_typ.name)
                print(self.uniting.unit_typ.equipment)
                break
            else:
                self.uniting = None
                self.menu.unit1[0] = ""
                self.menu.unit2[0] = ""
                self.menu.unit3[0] = ""
                self.menu.unit4[0] = ""
                self.menu.unit5[0] = ""
                self.menu.unit6[0] = ""
                self.menu.unit7[0] = ""

        for b in self.buildings:
            #print("First")
            #print(str(b.col) + " / " + str(self.mouse_pos.col))
            #print("Second")
            #print(str(b.row) + " / " + str(self.mouse_pos.row))
            if (b.col == self.mouse_pos.col) and (b.row == self.mouse_pos.row) and (b.owner.player == True):
                print("Selected")
                self.building = b
                print(self.building)
                self.menu.building1[0] = self.building.description[0]
                self.menu.building2[0] = self.building.description[1]
                self.menu.building3[0] = self.building.description[2]
                self.menu.building4[0] = self.building.description[3]
                self.menu.building5[0] = self.building.description[4]
                self.menu.building6[0] = self.building.description[5]
                self.menu.building7[0] = self.building.description[6]
                self.menu.building8[0] = self.building.description[7]
                self.menu.building9[0] = self.building.description[8]
                self.menu.building10[0] = self.building.description[9]
                self.menu.building11[0] = self.building.description[10]
                self.menu.building12[0] = self.building.description[11]
                self.menu.building13[0] = self.building.description[12]

                break
            else:
                self.building = None
                self.menu.building1[0] = ""
                self.menu.building2[0] = ""
                self.menu.building3[0] = ""
                self.menu.building4[0] = ""
                self.menu.building5[0] = ""
                self.menu.building6[0] = ""
                self.menu.building7[0] = ""
                self.menu.building8[0] = ""
                self.menu.building9[0] = ""
                self.menu.building10[0] = ""
                self.menu.building11[0] = ""
                self.menu.building12[0] = ""
                self.menu.building13[0] = ""

    def deselect(self):
        self.selecting = None
        self.resourcing = None
        self.uniting = None
        self.building = None
        self.menu.terrain1[0] = ""
        self.menu.terrain2[0] = ""
        self.menu.terrain3[0] = ""
        self.menu.unit1[0] = ""
        self.menu.unit2[0] = ""
        self.menu.unit3[0] = ""
        self.menu.building1[0] = ""
        self.menu.building2[0] = ""
        self.menu.building3[0] = ""

    def quit(self):
        #pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        self.menu.update()
        self.windows.update()
        self.buttons.update()
        # update mouse pos & time
        self.mouse()
        self.time()
        if self.resourcing != None:
            self.menu.terrain3[0] = self.resourcing.name + " " + str(self.resourcing.value)
        if self.building != None:
            self.menu.building1[0] = self.building.description[0]
            self.menu.building2[0] = self.building.description[1]
            self.menu.building3[0] = self.building.description[2]
            self.menu.building4[0] = self.building.description[3]
            self.menu.building5[0] = self.building.description[4]
            self.menu.building6[0] = self.building.description[5]
            self.menu.building7[0] = self.building.description[6]
            self.menu.building8[0] = self.building.description[7]
            self.menu.building9[0] = self.building.description[8]
            self.menu.building10[0] = self.building.description[9]
        if self.uniting != None:
            self.menu.unit1[0] = self.uniting.description[0]
            self.menu.unit2[0] = self.uniting.description[1]
            self.menu.unit3[0] = self.uniting.description[2]
            self.menu.unit4[0] = self.uniting.description[3]
            self.menu.unit5[0] = self.uniting.description[4]
            self.menu.unit6[0] = self.uniting.description[5]
            self.menu.unit7[0] = self.uniting.description[6]


                

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        if self.territory_visible == True:
            self.screen.blit(self.map.surface2, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            #if (self.player.x - 8 < sprite.x < self.player.x + 8) and (self.player.y - 8 < sprite.y < self.player.y + 8):
                #print(sprite.x, sprite.y, sprite.z)
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            #self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.screen.blit(self.menu2, (0, 0))

        #draw top bar
        self.screen.blit(self.players[self.player.side].image, (5, -2))
        self.screen.blit(self.stability[self.players[self.player.side].stability], (4, 23))

        self.screen.blit(self.players[self.player.side].image, (312, 0))
        self.screen.blit(self.money_img, (310, 30))
        self.screen.blit(self.global_img, (463, 8))
        self.screen.blit(self.money_img, (460, 30))

        #print("HERE")
        #print(self.players[self.player.side].electricity)
        if self.players[self.player.side].electricity == True:
            
            self.screen.blit(self.elect_yes_img, (23, 23))
        else:
            self.screen.blit(self.elect_no_img, (23, 23))

        #print(self.menu.buttons)
        #for b in self.menu.buttons:
        #    self.screen.blit(b.image, b.pos)
        self.screen.blit(self.menu.buttons[1].image, self.menu.buttons[1].pos)


        for a in range(len(self.players)-1):
            self.screen.blit(self.players[a+1].image, (TOP_BAR_DISTANS + (a * TOP_BAR_STEP), -6))
            self.screen.blit(self.exchange_img, (TOP_BAR_DISTANS + (a * TOP_BAR_STEP), 14))
            self.screen.blit(self.global_img, (TOP_BAR_DISTANS+3 + (a * TOP_BAR_STEP), 34))

            self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(self.players[a+1].exc_rt), False, LIGHTGREY), (TOP_BAR_DISTANS+20 + (a * TOP_BAR_STEP), 17))
        

        for text in self.texts:
            self.screen.blit(pg.font.Font(FONT_NAME, text[1]).render(text[0], False, text[2]), text[3])

        
        if self.selecting != None:
            self.screen.blit(self.map.tmxdata.images[self.selecting.gid], (WIDTH - MENU_RIGHT[0]+10, 140))
            if self.building == None:
                #self.screen.blit(self.building.image, (WIDTH - MENU_RIGHT[0]+0, 435))
                #print("Empty place to build something")
                self.screen.blit(self.menu.new_building_button.image, self.menu.new_building_button.pos)
            else:
                #print("There is a building")
                pass

        if self.resourcing != None:
            self.screen.blit(self.resourcing.image, (WIDTH - MENU_RIGHT[0]+10, 140))

        if self.building != None:
            self.screen.blit(self.building.owner.image, (WIDTH - MENU_RIGHT[0]+10, 412))
            self.screen.blit(self.building.image, (WIDTH - MENU_RIGHT[0]+0, 435))
            if self.building.name != self.language.BUILDINGS1[0]:
                self.screen.blit(self.building.button.image, self.building.button.pos)
                if self.building.window.visible == True:
                    self.screen.blit(self.building.window.image, self.building.window.pos)
            #if self.building.what == None:
            #    language.BUILDINGS1[0]
            
        if self.uniting != None:
            self.screen.blit(self.uniting.owner.image, (WIDTH - MENU_RIGHT[0]+5, 222))
            self.screen.blit(self.uniting.unit_typ.image, (WIDTH - MENU_RIGHT[0]-5, 248))
            self.screen.blit(self.uniting.button.image, self.uniting.button.pos)
            if self.uniting.window.visible == True:
                self.screen.blit(self.uniting.window.image, self.uniting.window.pos)
                #for var in self.uniting.window.variables:

        for window in self.unit_windows:
            if window.visible == True:
                self.screen.blit(window.image, window.pos)
                for button in window.buttons:
                    window.image.blit(button.image, button.pos)
                if 1 == 1: #rolling display unit variables
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.men) + " / " + str(window.thing.max_men), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 38))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.supply) + " / " + str(window.thing.max_supply), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 58))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.uniforms) + " / " + str(window.thing.max_uniforms), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 78))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.fuel) + " / " + str(window.thing.max_fuel), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 98))
                    
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.light_ammo) + " / " + str(window.thing.max_light_ammo), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 138))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.heavy_ammo) + " / " + str(window.thing.max_heavy_ammo), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 158))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.rockets) + " / " + str(window.thing.max_rockets), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 178))
                    
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.rifle) + " / " + str(window.thing.max_rifle), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 218))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.artilleries) + " / " + str(window.thing.max_artilleries), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 238))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.truck) + " / " + str(window.thing.max_truck), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 258))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.apc) + " / " + str(window.thing.max_apc), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 278))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.tank) + " / " + str(window.thing.max_tank), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 298))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.heli) + " / " + str(window.thing.max_heli), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 318))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.aircraft) + " / " + str(window.thing.max_aircraft), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 338))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.rocket_truck) + " / " + str(window.thing.max_rocket_truck), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 358))


                    self.screen.blit(self.uniting.owner.image, (window.pos[0] + 270, window.pos[1] + 30))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.thing.owner.name, False, LIGHTGREY), (window.pos[0] + 300, window.pos[1] + 38))
                    self.screen.blit(self.uniting.unit_typ.image, (window.pos[0] + 260, window.pos[1] + 56))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.thing.unit_typ.name, False, LIGHTGREY), (window.pos[0] + 300, window.pos[1] + 58))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.thing.print_mobilized(), False, LIGHTGREY), (window.pos[0] + 270, window.pos[1] + 80))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.DESCRIPTION[2] + ": " + str(window.thing.combat_ability) + "/" + str(window.thing.combat_ability_max), False, LIGHTGREY), (window.pos[0] + 270, window.pos[1] + 96))
                    
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.DESCRIPTION[0] + ": " + str(window.thing.experience), False, LIGHTGREY), (window.pos[0] + 270, window.pos[1] + 117))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.DESCRIPTION[7] + ": " + str(window.thing.tiredness) + "/" + str(window.thing.tiredness_max), False, LIGHTGREY), (window.pos[0] + 270, window.pos[1] + 133))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.thing.task, False, LIGHTGREY), (window.pos[0] + 270, window.pos[1] + 153))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.fuel_usage), False, YELLOW), (window.pos[0] + 510, window.pos[1] + 40))


        for window in self.building_windows:
            if window.visible == True:
                self.screen.blit(window.image, window.pos)
                for button in window.buttons:
                    window.image.blit(button.image, button.pos)
                for t in window.texts:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(t[0], False, t[2]), (window.pos[0] + t[3][0], window.pos[1] + t[3][1]))
                
                #if 1 == 1: #rolling display building variables
                e = 0
                f = 0
                if window.thing.name != self.language.BUILDINGS1[6]:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.GUI[4], False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 80 + (e * 20)))
                else:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.DESCRIPTION[3], False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 80 + (e * 20)))
                
                self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.GUI[8], False, LIGHTGREY), (window.pos[0] + 350, window.pos[1] + 40))
                self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.GUI[10], False, LIGHTGREY), (window.pos[0] + 580, window.pos[1] + 10))
                
                if window.thing.owner.electricity == True:
                    self.screen.blit(self.elect_yes_img, (window.pos[0] + 670, window.pos[1] + 7))
                else:
                    self.screen.blit(self.elect_no_img, (window.pos[0] + 670, window.pos[1] + 7))
                
                for v in window.variables:
                    
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(v, False, LIGHTGREY), (window.pos[0] + 10 + f, window.pos[1] + 100 + (e * 20)))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.storage[v]), False, LIGHTGREY), (window.pos[0] + 110 + f, window.pos[1] + 100 + (e * 20)))
                    e += 1
                    if e > 18:
                        e = 0
                        f += 160
                if len(window.thing.orders) > 0:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.thing.orders[0][0], False, LIGHTGREY), (window.pos[0] + 300, window.pos[1] + 60))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.orders[0][1]), False, LIGHTGREY), (window.pos[0] + 420, window.pos[1] + 60))
                    
                if len(window.thing.orders) > 1:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.thing.orders[1][0], False, LIGHTGREY), (window.pos[0] + 300, window.pos[1] + 80))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.orders[1][1]), False, LIGHTGREY), (window.pos[0] + 420, window.pos[1] + 80))
                    
                if len(window.thing.orders) > 2:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.thing.orders[2][0], False, LIGHTGREY), (window.pos[0] + 300, window.pos[1] + 100))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.orders[2][1]), False, LIGHTGREY), (window.pos[0] + 420, window.pos[1] + 100))

                if len(window.thing.orders) > 3:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.GUI[9], False, LIGHTGREY), (window.pos[0] + 300, window.pos[1] + 140))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(len(window.thing.orders)), False, LIGHTGREY), (window.pos[0] + 420, window.pos[1] + 140))
                    

                if window.thing.name == self.language.BUILDINGS1[1] or window.thing.name == self.language.BUILDINGS1[2]:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.GUI[7], False, LIGHTGREY), (window.pos[0] + 550, window.pos[1] + 40))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render("/ " + window.thing.nationality.name, False, LIGHTGREY), (window.pos[0] + 320, window.pos[1] + 8))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.thing.population), False, LIGHTGREY), (window.pos[0] + 550, window.pos[1] + 60))
                    


        for window in self.menu_windows:
            if window.visible == True:
                self.screen.blit(window.image, window.pos)
                for button in window.buttons:
                    window.image.blit(button.image, button.pos)
                for variable in window.variables:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render("$ " + str(variable[0]), False, variable[2]), (window.pos[0] + variable[3][0], window.pos[1] + variable[3][1]))
                for res in window.resources:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(res[0], False, res[2]), (window.pos[0] + res[3][0], window.pos[1] + res[3][1]))
                for t in window.texts:
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(t[0], False, t[2]), (window.pos[0] + t[3][0], window.pos[1] + t[3][1]))
                

 

        pg.display.flip()


    def events(self):
        #pg.display.set_caption(str(self.timer))
        self.menu.position[0] = str(self.language.DISPLAY_GUI[0]) + str(self.mouse_pos.col) + " " + str(self.mouse_pos.row)
        self.menu.time[0] = str(self.language.DISPLAY_GUI[1]) + str(self.hour) + ":" + f"{int(self.quarter * 15):02d}"
        self.menu.speed[0] = str(self.language.DISPLAY_GUI[4] if self.pause == True else self.language.DISPLAY_GUI[5] + str(self.speed))
        self.menu.data1[0] = str(self.language.DISPLAY_GUI[2]) + str(self.week) + self.language.DISPLAY_GUI[3] + str(self.day)
        self.menu.data2[0] = str(self.language.SEASONS[self.season]) + " " + str(self.year)

        #qwx, qwy = pg.mouse.get_pos()
        #print(qwx, qwy)
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                print(event.key)
                if event.key == pg.K_ESCAPE:
                    self.deselect()
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.player.move(dx = -1)
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.player.move(dx = 1)
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.player.move(dy = -1)
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.move(dy = 1)
                if event.key == pg.K_e:
                    self.player.x = 12
                    self.player.y = 12
                if event.key == pg.K_r:
                    self.players[self.player.side].stability += 1 
                if event.key == pg.K_t:
                    print(self.building)
                    print(self.building.materials)
                    
                    print(self.building.cost)
                    print("Cheat")
                    self.building.materials = self.building.cost
                    print(self.building.materials)
                    
                if event.key == pg.K_m:
                    self.territory_visible = not self.territory_visible
                    print(self.territory_visible)
                if (event.key == 61) or (event.key == 270): #plus key
                    if self.speed < 32:
                        self.speed = self.speed * 2
                    #print(self.speed)
                if (event.key == 45) or (event.key == 269): #minus key
                    if self.speed >= 2:
                        self.speed = self.speed / 2
                    #print(self.speed)
                if event.key == pg.K_PAUSE or event.key == 32:
                    self.pause = not self.pause
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for window in self.windows:
                        if window.rect.collidepoint(pg.mouse.get_pos()) and window.visible == True:
                            self.s_drag = pg.mouse.get_pos()
                            self.dragging = True
                            self.dragged = window
                            break

            if event.type == pg.MOUSEMOTION:
                if self.dragging == True:
                    self.dragged.pos[0] = self.dragged.pos[0] + (pg.mouse.get_pos()[0] - self.s_drag[0])
                    self.dragged.pos[1] = self.dragged.pos[1] + (pg.mouse.get_pos()[1] - self.s_drag[1])
                    self.s_drag = pg.mouse.get_pos()

            
            if event.type == pg.MOUSEBUTTONUP:
                #print(event.button)
                self.dragging = False

                if pg.mouse.get_pos()[0] < (WIDTH - MENU_RIGHT[0]):
                    if event.button == 1:
                        if self.window_display == False:
                            self.select(True)
                        elif self.window_display == True:
                            for window in self.windows:
                                if window.visible == True:
                                    for button in window.buttons:
                                        button.check_col(pg.mouse.get_pos())
                                        #print(pg.mouse.get_pos())

                    if event.button == 3:
                        if self.uniting != None:
                            #print("To tu")
                            #self.uniting.go_to = roffset_to_cube(OFFSET, self.mouse_pos)
                            self.uniting.stop()
                            self.uniting.make_path(roffset_to_cube(OFFSET, self.mouse_pos))
                            #self.uniting.col = self.mouse_pos.col

                if pg.mouse.get_pos()[0] > (WIDTH - MENU_RIGHT[0]):
                    if event.button == 1:
                        #print(self.selecting.building)
                        if self.uniting: 
                            self.uniting.button.check_col(pg.mouse.get_pos())
                            print(self.uniting.button.rect)
                            print(pg.mouse.get_pos())
                        if self.building: 
                            self.building.button.check_col(pg.mouse.get_pos())
                            print(self.building.button.rect)
                            print(pg.mouse.get_pos())

                        if self.building == None:
                            for a in self.menu.buttons:
                                #print(self.menu.buttons)
                                a.check_col(pg.mouse.get_pos())
                        


    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()