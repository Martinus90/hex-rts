# cos
import sys
import math
import pygame as pg
import inspect
from os import path
from hexo import *
from settings import *
from sprites import *
from tilemap import *
from loading import *
from languages import *


class Game:
    """
    Main game class
    """
    def __init__(self, player=1, map_name="", save_name=""):
        """
        Construct of new game

        :param screen: Main game screen, take value WIDTH and HEIGHT from settings.py
        :param clock: Initiation in-game clock
        :param map_name: Map name
        :param language: Initialization of game language via Language.py file
        :param variables: Setting all starting variables
        :param pause: In-game pause
        :param all "-ing": Variables containing current selected object
        :param window_display: If true then selecting is unavailable
        :param drag*: Variable used to move windows
        :param territory_visible: Display "owner" layer 
        :param nations: list with all nations
        :param players: list with all contenders
        :param types: list with all units types
        :param new_info_text: list with new info text to display
        """
        inspect.isclass(NB_Button)
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.map_name = map_name
        self.load_data()
        self.load_save("maps/" + save_name + ".txt")
        self.language = Language()
        self.timer = 0
        self.quarter = 0
        self.hour = 0
        self.day = 1
        self.start_day = 1
        self.idn = 1
        self.week = 1
        self.start_week = 1
        self.season = 0
        self.start_season = 0
        self.year = 1980
        self.start_year = 1980
        self.speed = GAME_SPEED
        self.pause = False
        self.selecting = None
        self.resourcing = None
        self.uniting = None
        self.building = None
        self.window_display = False
        self.dragging = False
        self.dragged = None
        self.multi_task = False
        self.territory_visible = False
        self.s_drag = pg.Vector2
        self.nations = []
        self.players = []
        self.types = []
        self.new_info_text = []

    def load_data(self):
        """
        Loading data function 

        :param game_folder: main folder path
        :param img_folder: image folder path
        :param gui_folder: graphical user interface folder path
        :param map_folder: map folder path
        :param myfont: contain game font
        :param layout: contain layout of hexagonal grid select position
        :param other var: loading all data
        :param map: loading game map
        """
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "images")
        gui_folder = path.join(game_folder, "gui")
        map_folder = path.join(game_folder, "maps")
        self.myfont = pg.font.Font(FONT_NAME, 24)
        self.layout = Layout(layout_pointy, Point(36.9, 32.0), Point(0.0, 0.0))

        if 1 == 1:  # rolling loading images

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
                self.image.blit(
                    self.stability_img.copy(),
                    (0, 0),
                    (0, a * STABILITY_SIZE[1], STABILITY_SIZE[0], STABILITY_SIZE[1]),
                )
                self.stability.append(self.image)

            self.construction_img = pg.image.load(
                path.join(img_folder, CONSTRUCTION_IMG)
            )
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
            self.light_industry_plant_img = pg.image.load(
                path.join(img_folder, LIGHT_INDUSTRY_PLANT_IMG)
            )
            self.heavy_industry_plant_img = pg.image.load(
                path.join(img_folder, HEAVY_INDUSTRY_PLANT_IMG)
            )
            self.chemical_plant_img = pg.image.load(
                path.join(img_folder, CHEMICAL_PLANT_IMG)
            )
            self.high_tech_plant_img = pg.image.load(
                path.join(img_folder, HIGH_TECH_PLANT_IMG)
            )
            self.mechanical_plant_img = pg.image.load(
                path.join(img_folder, MECHANICAL_PLANT_IMG)
            )
            self.armament_plant_img = pg.image.load(
                path.join(img_folder, ARMAMENT_PLANT_IMG)
            )
            self.aviation_plant_img = pg.image.load(
                path.join(img_folder, AVIATION_PLANT_IMG)
            )
            self.shipyard_img = pg.image.load(path.join(img_folder, SHIPYARD_IMG))

            self.x_img = pg.image.load(path.join(gui_folder, X_IMG))
            self.window_img = pg.image.load(path.join(gui_folder, WINDOW_IMG))
            self.o_window_img = pg.image.load(path.join(gui_folder, O_WINDOW_IMG))
            self.o_window_img.blit(
                pg.font.Font(FONT_NAME, 24).render("Open", False, LIGHTGREY), (2, 4)
            )
            self.button_1_img = pg.image.load(path.join(gui_folder, O_WINDOW_IMG))
            self.elect_yes_img = pg.image.load(path.join(gui_folder, ELECT_YES))
            self.elect_yes_img.set_colorkey(VIOLET)
            self.elect_no_img = pg.image.load(path.join(gui_folder, ELECT_NO))
            self.elect_no_img.set_colorkey(VIOLET)

            self.yes_img = pg.image.load(path.join(gui_folder, YES_IMG))
            self.no_img = pg.image.load(path.join(gui_folder, NO_IMG))

        self.map = TiledMap(
            self, path.join(map_folder, self.map_name + ".tmx")
        )  # test / test2 / default

        # side 0 is always neutral / side 1 is always player / other side are variable
        # self.side_0 = "Neutral"
        # self.side_1 = "Player"
        # self.side_2 = "Enemy"

    def load_save(self, save_file):
        """
        Loading data from save.txt

        :param save_file: name of file
        :param saved_data: containg all lines of save_file
        """
        self.save_file = save_file
        self.saved_data = []
        with open(self.save_file, "r") as reader:
            # Read & print the first 5 characters of the line 5 times
            all_lines = reader.readlines()
            for a in all_lines:
                # print(a[-1])
                if "\n" in a:
                    b = a[:-1]
                    self.saved_data.append(b)
                else:
                    self.saved_data.append(a)

    def new(self):
        """
        Creating new game

        :param all_sprites: this and other; used to initialize sprites groups
        :param texts: contain all menu text variables
        :param nations: adding all nations / class from loading.py
        :param players: adding all players / class Contender from loading.py
        :param diplomacy: adding game diplomacy / class from loading.py
        :param int_politics: adding game internal politics / class from loading.py
        :param event_list: adding game events / class from loading.py
        :param trade: adding game trade / class from loading.py
        
        Initialize few loops to convert "list" to 
        "object" like resource, building, unit
        """
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
        self.nations.append(Nation(self, name="Grenaly"))
        self.nations.append(Nation(self, name="Kitayce"))



        for a in range(len(self.nations)):
            self.nations[a].id_num = a

        # first on the list is always neutral, second is player, 3+ are others / to change color just change side
        self.player = Player(self, 0, 0, 1)
        self.players.append(
            Contender(
                self,
                name="Neutral",
                nation=0,
                player=False,
                side=0,
                exc_rt=10.0,
                money=0,
                global_money=2000,
                reputation=0,
                stability=2,
                pop_tax=10,
                build_tax=10,
                reserve=100,
            )
        )
        self.players.append(
            Contender(
                self,
                name="Sovenya",
                nation=0,
                player=True,
                side=1,
                exc_rt=10.0,
                money=10000,
                global_money=10000,
                reputation=0,
                stability=2,
                pop_tax=10,
                build_tax=10,
                reserve=100,
            )
        )
        self.players.append(
            Contender(
                self,
                name="Nebohray",
                nation=1,
                player=False,
                side=2,
                exc_rt=10.0,
                money=10000,
                global_money=0,
                reputation=0,
                stability=2,
                pop_tax=3,
                build_tax=10,
                reserve=100,
            )
        )
        self.players.append(
            Contender(
                self,
                name="Sovenyan Rebels",
                nation=0,
                player=False,
                side=11,
                exc_rt=10.0,
                money=10000,
                global_money=0,
                reputation=0,
                stability=2,
                pop_tax=3,
                build_tax=10,
                reserve=100,
            )
        )
        self.players.append(
            Contender(
                self,
                name="Nebohray Rebels",
                nation=1,
                player=False,
                side=12,
                exc_rt=10.0,
                money=10000,
                global_money=0,
                reputation=0,
                stability=2,
                pop_tax=3,
                build_tax=10,
                reserve=100,
            )
        )
        self.players.append(
            Contender(
                self,
                name="Grenals",
                nation=2,
                player=False,
                side=3,
                exc_rt=10.0,
                money=100,
                global_money=0,
                reputation=0,
                stability=2,
                pop_tax=3,
                build_tax=10,
                reserve=100,
            )
        )
        self.players.append(
            Contender(
                self,
                name="Kitaycan",
                nation=3,
                player=False,
                side=4,
                exc_rt=10.0,
                money=100,
                global_money=0,
                reputation=0,
                stability=2,
                pop_tax=3,
                build_tax=10,
                reserve=100,
            )
        )
        for a in range(len(self.players)):
            self.players[a].id_num = a

        self.diplomacy = Diplomacy(self)
        self.diplomacy.window.show_relations()
        self.int_politics = Int_Politics(self)
        self.event_list = Event_List(
            self,
            [
                [50, "event_name", "here_event_properties"]
            ],
        )


        #initialising trade
        self.trade = Trade(self)

        # creating unit types
        if 1 == 1:
            # infantry
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[0],
                    typ=0,
                    s_normal=4,
                    s_water=200,
                    s_mountain=6,
                    s_coast=4,
                    s_river=12,
                    s_no_fuel=20,
                    money_usage=2,
                    max_men=79,
                    max_art=0,
                    max_truck=0,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=25,
                    min_art=0,
                    min_truck=0,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # armored
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[1],
                    typ=1,
                    s_normal=2,
                    s_water=200,
                    s_mountain=12,
                    s_coast=4,
                    s_river=12,
                    s_no_fuel=40,
                    money_usage=2,
                    max_men=30,
                    max_art=0,
                    max_truck=0,
                    max_apc=0,
                    max_tank=6,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=15,
                    min_art=0,
                    min_truck=0,
                    min_apc=0,
                    min_tank=3,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # artillery
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[2],
                    typ=2,
                    s_normal=2,
                    s_water=200,
                    s_mountain=12,
                    s_coast=4,
                    s_river=12,
                    s_no_fuel=20,
                    money_usage=2,
                    max_men=35,
                    max_art=6,
                    max_truck=7,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=20,
                    min_art=3,
                    min_truck=4,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # mechanized
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[3],
                    typ=3,
                    s_normal=2,
                    s_water=200,
                    s_mountain=12,
                    s_coast=4,
                    s_river=12,
                    s_no_fuel=40,
                    money_usage=2,
                    max_men=99,
                    max_art=0,
                    max_truck=0,
                    max_apc=9,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=55,
                    min_art=0,
                    min_truck=0,
                    min_apc=5,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # reconnaissance
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[4],
                    typ=4,
                    s_normal=2,
                    s_water=200,
                    s_mountain=8,
                    s_coast=3,
                    s_river=8,
                    s_no_fuel=20,
                    money_usage=2,
                    max_men=99,
                    max_art=0,
                    max_truck=4,
                    max_apc=4,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=55,
                    min_art=0,
                    min_truck=2,
                    min_apc=2,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # motorized
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[5],
                    typ=5,
                    s_normal=2,
                    s_water=200,
                    s_mountain=12,
                    s_coast=4,
                    s_river=12,
                    s_no_fuel=20,
                    money_usage=2,
                    max_men=99,
                    max_art=0,
                    max_truck=9,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=55,
                    min_art=0,
                    min_truck=5,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # other
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[6],
                    typ=6,
                    s_normal=4,
                    s_water=200,
                    s_mountain=6,
                    s_coast=4,
                    s_river=12,
                    s_no_fuel=20,
                    money_usage=1,
                    max_men=79,
                    max_art=0,
                    max_truck=0,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=25,
                    min_art=0,
                    min_truck=0,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # logistic
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[7],
                    typ=7,
                    s_normal=2,
                    s_water=200,
                    s_mountain=12,
                    s_coast=4,
                    s_river=12,
                    s_no_fuel=20,
                    money_usage=2,
                    max_men=45,
                    max_art=0,
                    max_truck=20,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=15,
                    min_art=0,
                    min_truck=5,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # headquaters
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[8],
                    typ=8,
                    s_normal=2,
                    s_water=200,
                    s_mountain=12,
                    s_coast=4,
                    s_river=12,
                    s_no_fuel=20,
                    money_usage=2,
                    max_men=30,
                    max_art=0,
                    max_truck=5,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=24,
                    min_art=0,
                    min_truck=4,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # helicopters
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[9],
                    typ=9,
                    s_normal=2,
                    s_water=2,
                    s_mountain=2,
                    s_coast=2,
                    s_river=2,
                    s_no_fuel=40,
                    money_usage=10,
                    max_men=9,
                    max_art=0,
                    max_truck=0,
                    max_apc=0,
                    max_tank=0,
                    max_heli=3,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=3,
                    min_art=0,
                    min_truck=0,
                    min_apc=0,
                    min_tank=0,
                    min_heli=1,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # aircraft
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[10],
                    typ=10,
                    s_normal=1,
                    s_water=1,
                    s_mountain=1,
                    s_coast=1,
                    s_river=1,
                    s_no_fuel=40,
                    money_usage=20,
                    max_men=9,
                    max_art=0,
                    max_truck=0,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=3,
                    max_rocket_truck=0,
                    min_men=3,
                    min_art=0,
                    min_truck=0,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=1,
                    min_rocket_truck=0,
                )
            )

            # need to do
            # AA anti-aircraft
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[11],
                    typ=11,
                    s_normal=3,
                    s_water=200,
                    s_mountain=12,
                    s_coast=5,
                    s_river=12,
                    s_no_fuel=40,
                    money_usage=2,
                    max_men=30,
                    max_art=0,
                    max_truck=3,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=3,
                    min_men=12,
                    min_art=0,
                    min_truck=1,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=1,
                )
            )

            # anti-armor
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[12],
                    typ=12,
                    s_normal=2,
                    s_water=200,
                    s_mountain=12,
                    s_coast=4,
                    s_river=12,
                    s_no_fuel=20,
                    money_usage=2,
                    max_men=35,
                    max_art=6,
                    max_truck=7,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=20,
                    min_art=3,
                    min_truck=4,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

            # rocket
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[13],
                    typ=13,
                    s_normal=2,
                    s_water=200,
                    s_mountain=12,
                    s_coast=5,
                    s_river=12,
                    s_no_fuel=40,
                    money_usage=5,
                    max_men=30,
                    max_art=0,
                    max_truck=4,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=6,
                    min_men=16,
                    min_art=0,
                    min_truck=2,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=2,
                )
            )

            # engineering
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[14],
                    typ=14,
                    s_normal=2,
                    s_water=200,
                    s_mountain=10,
                    s_coast=4,
                    s_river=12,
                    s_no_fuel=40,
                    money_usage=3,
                    max_men=40,
                    max_art=0,
                    max_truck=8,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=20,
                    min_art=0,
                    min_truck=4,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )
            # volunteers
            self.types.append(
                Unit_Type(
                    self,
                    name=self.language.UNIT_TYPE[15],
                    typ=15,
                    s_normal=5,
                    s_water=200,
                    s_mountain=8,
                    s_coast=5,
                    s_river=16,
                    s_no_fuel=20,
                    money_usage=1,
                    max_men=35,
                    max_art=0,
                    max_truck=0,
                    max_apc=0,
                    max_tank=0,
                    max_heli=0,
                    max_aircraft=0,
                    max_rocket_truck=0,
                    min_men=15,
                    min_art=0,
                    min_truck=0,
                    min_apc=0,
                    min_tank=0,
                    min_heli=0,
                    min_aircraft=0,
                    min_rocket_truck=0,
                )
            )

        #making map
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        #getting grids neighbors
        for grid in self.map.grids:
            grid.get_neighbors(self.map)
            grid.get_owner()

        # print(self.map.grids)
        self.menu = Menu(self)  # .make_menu()
        self.menu2 = self.menu.make_menu()
        self.menu_rect = self.menu2.get_rect()

        # here load all data from save file
        SCENARIO_INFO = False
        SCENARIO_DIPLOMACY = False
        SCENARIO_EVENTS = False
        SCENARIO_RESOURCES = False
        SCENARIO_BUILDINGS = False
        SCENARIO_UNITS = False

        for line in self.saved_data:
            n_line = []
            nn_line = []
            nnn_line = []
            nnnn_line = []

            if SCENARIO_INFO == True:
                if line != "END":
                    self.new_info_text.append(line)
                if line == "END":
                    self.event_list.scenario.new_text_to_display(self.new_info_text)
                    SCENARIO_INFO = False

            if SCENARIO_DIPLOMACY == True:
                if line != "END":
                    n_line = list(line.split(","))
                    for n in n_line:
                        if "/" in n:
                            nn_line.append(list(n.split("/")))
                        else:
                            nn_line.append(n)
                    for nn in nn_line:
                        if nn[0] == "*":
                            nnn_line.append(int(nn[1:]))
                        else:
                            if nn == "False":
                                nnn_line.append(False)
                            elif nn == "True":
                                nnn_line.append(True)
                            else:
                                nnn_line.append(nn)
                    self.diplomacy.relations[nnn_line[0]][nnn_line[1]][nnn_line[2]] = nnn_line[3]
                if line == "END":
                    SCENARIO_DIPLOMACY = False

            if SCENARIO_EVENTS == True:
                if line != "END":
                    n_line = list(line.split(","))
                    for n in n_line:
                        if "/" in n:
                            nn_line.append(list(n.split("/")))
                        else:
                            nn_line.append(n)
                    for nn in nn_line:
                        if type(nn) == list:
                            f = []
                            for e in nn:
                                if "&" in e:
                                    f.append(list(e.split("&")))
                                else:
                                    f.append(e)
                            nnn_line.append(f)
                        else:
                            nnn_line.append(nn)

                    for nnn in nnn_line:
                        if type(nnn) != list:
                            if nnn[0] == "*":
                                nnnn_line.append(int(nnn[1:]))
                            elif nnn[0] == "^":
                                nnnn_line.append(float(nnn[1:]))
                            else:
                                nnnn_line.append(nnn)
                        else:
                            f = []
                            for a in nnn:
                                if a[0] == "*":
                                    f.append(int(a[1:]))
                                elif a[0] == "^":
                                    f.append(float(a[1:]))
                                else:
                                    g = []
                                    if type(a) == list:
                                        for b in a:
                                            if b[0] == "*":
                                                g.append(int(b[1:]))
                                            elif b[0] == "^":
                                                g.append(float(b[1:]))
                                            else:
                                                print(b)
                                                g.append(b)
                                        f.append(g)
                                    else:
                                        f.append(a)
                            nnnn_line.append(f)
                    if len(nnnn_line) == 3:
                        self.event_list.add_event(
                            [nnnn_line[0], nnnn_line[1], nnnn_line[2]]
                        )
                    elif len(nnnn_line) == 4:
                        self.event_list.add_event(
                            [nnnn_line[0], nnnn_line[1], nnnn_line[2], nnnn_line[3]]
                        )
                    elif len(nnnn_line) == 5:
                        self.event_list.add_event(
                            [
                                nnnn_line[0],
                                nnnn_line[1],
                                nnnn_line[2],
                                nnnn_line[3],
                                nnnn_line[4],
                            ]
                        )
                if line == "END":
                    SCENARIO_EVENTS = False

            if SCENARIO_RESOURCES == True:
                if line != "END":
                    n_line = list(line.split(","))
                    for n in n_line:
                        if "/" in n:
                            nn_line.append(list(n.split("/")))
                        else:
                            nn_line.append(n)
                    for nn in nn_line:
                        if nn[0] == "*":
                            nnn_line.append(int(nn[1:]))
                        else:
                            nnn_line.append(nn)
                    lista = []
                    for nnn in nnn_line:
                        lista.append(nnn)
                    self.map.resources.append(lista)
                if line == "END":
                    SCENARIO_RESOURCES = False

            if SCENARIO_BUILDINGS == True:
                if line != "END":
                    n_line = list(line.split(","))
                    for n in n_line:
                        if "/" in n:
                            nn_line.append(list(n.split("/")))
                        else:
                            nn_line.append(n)
                    for nn in nn_line:
                        if nn[0] == "*" or nn == "":
                            nnn_line.append(int(nn[1:]))
                        else:
                            nnn_line.append(nn)
                    lista = []
                    for nnn in nnn_line:
                        lista.append(nnn)
                    self.map.buildings.append(lista)
                if line == "END":
                    SCENARIO_BUILDINGS = False

            if SCENARIO_UNITS == True:
                if line != "END":
                    n_line = list(line.split(","))
                    for n in n_line:
                        if "/" in n:
                            nn_line.append(list(n.split("/")))
                        else:
                            nn_line.append(n)
                    for nn in nn_line:
                        if nn[0] == "*" or nn == "":
                            nnn_line.append(int(nn[1:]))
                        else:
                            nnn_line.append(nn)
                    lista = []
                    for nnn in nnn_line:
                        lista.append(nnn)
                    self.map.units.append(lista)
                if line == "END":
                    SCENARIO_UNITS = False

            if line == "SCENARIO_INFO":
                SCENARIO_INFO = True
            if line == "SCENARIO_DIPLOMACY":
                SCENARIO_DIPLOMACY = True
            if line == "SCENARIO_EVENTS":
                SCENARIO_EVENTS = True
            if line == "SCENARIO_RESOURCES":
                SCENARIO_RESOURCES = True
            if line == "SCENARIO_BUILDINGS":
                SCENARIO_BUILDINGS = True
            if line == "SCENARIO_UNITS":
                SCENARIO_UNITS = True

        #creating resources objects from list
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

        #creating buildings objects from list
        for b in self.map.buildings:
            if b[2] == "CONSTRUCTION":
                CONSTRUCTION(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8])
            elif b[2] == "VILLAGE":
                VILLAGE(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11], b[12])
            elif b[2] == "CITY":
                CITY(self,b[0],b[1],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10],b[11],b[12])
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
                RAFINERY(self, b[0], b[1], b[3], b[4], b[5], b[6], b[7], b[8], b[9])
            elif b[2] == "POWER_PLANT":
                POWER_PLANT(self, b[0], b[1], b[3], b[4], b[5])
            elif b[2] == "LIGHT_INDUSTRY_PLANT":
                LIGHT_INDUSTRY_PLANT(self,b[0],b[1],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10],b[11],b[12],b[13])
            elif b[2] == "HEAVY_INDUSTRY_PLANT":
                HEAVY_INDUSTRY_PLANT(self,b[0],b[1],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10],b[11],b[12],b[13],b[14])
            elif b[2] == "CHEMICAL_PLANT":
                CHEMICAL_PLANT(self,b[0],b[1],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10])
            elif b[2] == "HIGH_TECH_PLANT":
                HIGH_TECH_PLANT(self,b[0],b[1],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10])
            elif b[2] == "MECHANICAL_PLANT":
                MECHANICAL_PLANT(self,b[0],b[1],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10],b[11],b[12])
            elif b[2] == "ARMAMENT_PLANT":
                ARMAMENT_PLANT(self,b[0],b[1],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10],b[11],b[12],b[13])
            elif b[2] == "AVIATION_PLANT":
                AVIATION_PLANT(self,b[0],b[1],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10],b[11],b[12],b[13],b[14],b[15],b[16])

        #creating units objects from list
        for u in self.map.units:
            Unit(self,u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8],u[9],
                u[10],u[11],u[12],u[13],u[14],u[15],u[16],u[17],u[18],
                u[19],u[20],u[21],u[22],u[23],u[24],u[25])

        for b in range(len(self.players)):
            self.players[b].recalculate_all()

        self.camera = Camera(self.map.width, self.map.height)

    #adding new construction site on map
    def adding_building(self, variable):
        """
        Function that add construction, placed by player
        :param variable: int refer to position in list, which contain all correct buildings class names
        :param zeros: new construction at begining have zero needed recources
        """
        CONSTRUCTION(
            self,
            self.selecting.col,
            self.selecting.row,
            BUILDING_LIST[variable],
            self.player.side,
            0,
            0,
            0,
            0,
        )

    def adding_unit(self, x, y, loyalty, nationality, owner, typ, unit_name, men):
        Unit(self, x=x, y=y, loyalty=loyalty, nationality=nationality, 
            owner=owner, typ=typ, unit_name=unit_name, men=men)

    #converting construction site to building if finished
    def build(self, construction):
        """
        Function initialized by CONSTRUCTION if finished
        del CONSTRUCTION and place building
        """
        a = construction
        
        if a.what == "VILLAGE":
            construction.kill()
            VILLAGE(self, a.x, a.y, a.owner.id_num, "New village", 
            a.owner.nation.id_num)
               
        elif a.what == "CITY":
            construction.kill()
            CITY(self, a.x, a.y, a.owner.id_num, "New city",
            a.owner.nation.id_num)
            
        elif a.what == "HARBOR":
            construction.kill()
            HARBOR(self, a.x, a.y, a.owner.id_num)

        elif a.what == "AIRPORT":
            construction.kill()
            AIRPORT(self, a.x, a.y, a.owner.id_num)

        elif a.what == "WAREHOUSE":
            construction.kill()
            WAREHOUSE(self, a.x, a.y, a.owner.id_num)

        elif a.what == "BARRACK":
            construction.kill()
            BARRACK(self, a.x, a.y, a.owner.id_num)

        elif a.what == "MINE":
            construction.kill()
            MINE(self, a.x, a.y, a.owner.id_num)

        elif a.what == "SMELTER":
            construction.kill()
            SMELTER(self, a.x, a.y, a.owner.id_num)

        elif a.what == "OIL_WELL":
            construction.kill()
            OIL_WELL(self, a.x, a.y, a.owner.id_num)
        
        elif a.what == "RAFINERY":
            construction.kill()
            RAFINERY(self, a.x, a.y, a.owner.id_num)

        elif a.what == "POWER_PLANT":
            construction.kill()
            POWER_PLANT(self, a.x, a.y, a.owner.id_num)

        elif a.what == "LIGHT_INDUSTRY_PLANT":
            construction.kill()
            LIGHT_INDUSTRY_PLANT(self, a.x, a.y, a.owner.id_num)

        elif a.what == "HEAVY_INDUSTRY_PLANT":
            construction.kill()
            HEAVY_INDUSTRY_PLANT(self, a.x, a.y, a.owner.id_num)

        elif a.what == "CHEMICAL_PLANT":
            construction.kill()
            CHEMICAL_PLANT(self, a.x, a.y, a.owner.id_num)

        elif a.what == "HIGH_TECH_PLANT":
            construction.kill()
            HIGH_TECH_PLANT(self, a.x, a.y, a.owner.id_num)

        elif a.what == "MECHANICAL_PLANT":
            construction.kill()
            MECHANICAL_PLANT(self, a.x, a.y, a.owner.id_num)

        elif a.what == "ARMAMENT_PLANT":
            construction.kill()
            ARMAMENT_PLANT(self, a.x, a.y, a.owner.id_num)

        elif a.what == "AVIATION_PLANT":
            construction.kill()
            AVIATION_PLANT(self, a.x, a.y, a.owner.id_num)

    def time(self):
        """
        Function with in-game data and time
        convert hour "24" to "0" and other
        also call all units, buildings ... dayil / weekly ... funcitons
        """
        if self.timer > 1:  # def 1
            self.timer -= 1
            self.quarter += 1
            for unit in self.units:
                unit.do()
            for res in self.resources:
                res.do()
            for building in self.buildings:
                building.do()

        if self.quarter > 3:  # def 3
            self.quarter -= 4
            self.hour += 1
            for cont in self.players:
                cont.hourly()
            for unit in self.units:
                unit.hourly()
            for building in self.buildings:
                building.hourly()
        if self.hour > 23:  # def 23
            self.hour -= 24
            self.day += 1
            self.idn = (
                self.day
                + ((self.week - 1) * 7)
                + (self.season * 91)
                + ((self.year - 1980) * 364)
            )
            
            for res in self.resources:
                res.daily()
            for building in self.buildings:
                building.daily()
            for unit in self.units:
                unit.daily()
            for cont in self.players:
                cont.daily()
            self.int_politics.dayli()
            self.diplomacy.dayli()
            self.trade.dayli()
            self.trade.window.dayli()
            self.event_list.dayli()
        if self.day > 7:  # def 7
            self.day -= 7
            self.week += 1
            for building in self.buildings:
                building.weekly()
            for unit in self.units:
                unit.weekly()
            for player in self.players:
                player.weekly()
            self.int_politics.update_window_value()
            self.diplomacy.update_window_value()
        if self.week > 13:  # 13
            self.week -= 13
            self.season += 1
            for res in self.resources:
                res.seasonly()
            for building in self.buildings:
                building.seasonly()
        if self.season > 3:  # def 3
            self.season -= 4
            self.year += 1

    def mouse(self):
        """
        Fuction give new mouse real and grid position
        """
        # if pg.mouse.get_pos() >=
        nowy2 = hex_round(
            pixel_to_hex(
                self.layout,
                pg.Vector2(pg.mouse.get_pos())
                - pg.Vector2(self.camera.x, self.camera.y),
            )
        )
        self.mouse_pos = roffset_from_cube(-1, nowy2)

    def run(self):
        """
        In game loop, call function update, events, draw
        game loop - set self.playing = False to end the game
        self.pause in-game pause
        """

        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 2000
            if self.pause == False:
                self.timer += self.dt * self.speed
            self.update()
            self.events()
            self.draw()

    def select(self, select_new):
        """
        Function called after mouse click.
        Select grid, resource, unit, building
        """
        for grid in self.map.grids:
            if (grid.col == self.mouse_pos.col) and (grid.row == self.mouse_pos.row):
                self.selecting = grid
                self.menu.terrain1[0] = (
                    "X: " + str(self.selecting.col) + ", Y: " + str(self.selecting.row)
                )
                self.menu.terrain2[0] = str(self.selecting.terrain)
                self.selecting.get_near_resources()

        for r in self.resources:
            if (r.col == self.mouse_pos.col) and (r.row == self.mouse_pos.row):
                self.resourcing = r
                self.menu.terrain3[0] = (
                    self.resourcing.name + " " + str(self.resourcing.value)
                )
                break
            else:
                self.resourcing = None
                self.menu.terrain3[0] = ""

        for u in self.units:
            
            if (
                (u.col == self.mouse_pos.col)
                and (u.row == self.mouse_pos.row)
                and (u.owner.player == True)
            ):
                # print("Tak tu jest jednostka")
                self.uniting = u
                self.uniting.check_grid()
                self.menu.unit1[0] = self.uniting.description[0]
                self.menu.unit2[0] = self.uniting.description[1]
                self.menu.unit3[0] = self.uniting.description[2]
                self.menu.unit4[0] = self.uniting.description[3]
                self.menu.unit5[0] = self.uniting.description[4]
                self.menu.unit6[0] = self.uniting.description[5]
                self.menu.unit7[0] = self.uniting.description[6]
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
            if (
                (b.col == self.mouse_pos.col)
                and (b.row == self.mouse_pos.row)
                and (b.owner.player == True)
            ):
                self.building = b
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
        """
        Deselect grid, resource, unit, building
        """
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
        self.menu.unit4[0] = ""
        self.menu.unit5[0] = ""
        self.menu.unit6[0] = ""
        self.menu.unit7[0] = ""
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

        for w in self.windows:
            if w.visible == True:
                w.visible = False

    def quit(self):
        """
        Quit game
        """
        # pg.quit()
        sys.exit()

    def update(self):
        """
        Function update all variables, and call objects update functions
        Also update menu texts
        """
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
            self.menu.terrain3[0] = (
                self.resourcing.name + " " + str(self.resourcing.value)
            )
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
            self.menu.building11[0] = self.building.description[10]
            self.menu.building12[0] = self.building.description[11]
            self.menu.building13[0] = self.building.description[12]

        if self.uniting != None:
            self.menu.unit1[0] = self.uniting.description[0]
            self.menu.unit2[0] = self.uniting.description[1]
            self.menu.unit3[0] = self.uniting.description[2]
            self.menu.unit4[0] = self.uniting.description[3]
            self.menu.unit5[0] = self.uniting.description[4]
            self.menu.unit6[0] = self.uniting.description[5]
            self.menu.unit7[0] = self.uniting.description[6]

    def conv_idn_to_data(self, id_numb):
        """
        Functions convert int to specific game date
        """
        a = id_numb
        repeat = True
        returnig_date = [0, 1, 0, 0]
        while repeat == True:
            if a > 364:
                returnig_date[3] += 1
                a -= 364
            else:
                if a > 91:
                    returnig_date[2] += 1
                    a -= 91
                else:
                    if a > 7:
                        returnig_date[1] += 1
                        a -= 7
                    else:
                        returnig_date[0] = a
                        repeat = False
        returnig_date[3] = str(self.start_year + returnig_date[3])
        returnig_date[2] = self.language.SEASONS[returnig_date[2]]
        returnig_date[1] = self.language.DISPLAY_GUI[2] + str(returnig_date[1])
        returnig_date[0] = self.language.DISPLAY_GUI[3] + str(returnig_date[0])
        return (
            returnig_date[1]
            + returnig_date[0]
            + ", "
            + returnig_date[2]
            + ", "
            + returnig_date[3]
        )

    def draw(self):
        """
        Function that draw all sprites on game screen
        """
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        if self.territory_visible == True:
            self.screen.blit(self.map.surface2, self.camera.apply_rect(self.map_rect))

        #for sprite in self.all_sprites:
        #    self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.resources:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.buildings:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.units:
            self.screen.blit(sprite.image, self.camera.apply(sprite))


        self.screen.blit(self.menu2, (0, 0))

        # draw top bar
        self.screen.blit(self.players[self.player.side].image, (5, -2))
        if self.players[self.player.side].stability >= 75:
            self.screen.blit(
                self.stability[0], (4, 23)
            )
        elif self.players[self.player.side].stability < 75 and self.players[self.player.side].stability >= 25:
            self.screen.blit(
                self.stability[1], (4, 23)
            )
        elif self.players[self.player.side].stability < 25 and self.players[self.player.side].stability >= -25:
            self.screen.blit(
                self.stability[2], (4, 23)
            )
        elif self.players[self.player.side].stability < -25 and self.players[self.player.side].stability >= -75:
            self.screen.blit(
                self.stability[3], (4, 23)
            )
        else:
            self.screen.blit(
                self.stability[4], (4, 23)
            )

        self.screen.blit(self.players[self.player.side].image, (312, 0))
        self.screen.blit(self.money_img, (310, 30))
        self.screen.blit(self.global_img, (463, 8))
        self.screen.blit(self.money_img, (460, 30))

        #drawing electricity status image
        if self.players[self.player.side].electricity == True:

            self.screen.blit(self.elect_yes_img, (23, 23))
        else:
            self.screen.blit(self.elect_no_img, (23, 23))

        #drawing all menu buttons
        for x in self.menu.buttons:
            self.screen.blit(x.image, x.pos)

        #drawing top status of currency exchange rate 
        for a in range(len(self.players) - 1):
            #max 5 players
            if a < 5:
                self.screen.blit(
                    self.players[a + 1].image, (TOP_BAR_DISTANS + (a * TOP_BAR_STEP), -6)
                )
                self.screen.blit(
                    self.exchange_img, (TOP_BAR_DISTANS + (a * TOP_BAR_STEP), 14)
                )
                self.screen.blit(
                    self.global_img, (TOP_BAR_DISTANS + 3 + (a * TOP_BAR_STEP), 34)
                )

                self.screen.blit(
                    pg.font.Font(FONT_NAME, FONT_SIZE).render(
                        str(self.players[a + 1].exc_rt), False, LIGHTGREY
                    ),
                    (TOP_BAR_DISTANS + 20 + (a * TOP_BAR_STEP), 17),
                )

        #displaing text on menu
        for text in self.texts:
            self.screen.blit(
                pg.font.Font(FONT_NAME, text[1]).render(text[0], False, text[2]),
                text[3],
            )


        if self.selecting != None:
            self.screen.blit(
                self.map.tmxdata.images[self.selecting.gid],
                (WIDTH - MENU_RIGHT[0] + 10, 140),
            )
            if self.building == None and self.selecting.owner == self.player.side:
                self.screen.blit(
                    self.menu.new_building_button.image,
                    self.menu.new_building_button.pos,
                )

        if self.resourcing != None:
            self.screen.blit(self.resourcing.image, (WIDTH - MENU_RIGHT[0] + 10, 140))

        if self.building != None:
            self.screen.blit(
                self.building.owner.image, (WIDTH - MENU_RIGHT[0] + 10, 412)
            )
            self.screen.blit(self.building.image, (WIDTH - MENU_RIGHT[0] + 0, 435))
            if self.building.name != self.language.BUILDINGS1[0]:
                self.screen.blit(self.building.button.image, self.building.button.pos)
                if self.building.window.visible == True:
                    self.screen.blit(
                        self.building.window.image, self.building.window.pos
                    )
            # if self.building.what == None:
            #    language.BUILDINGS1[0]

        if self.uniting != None:
            self.screen.blit(self.uniting.owner.image, (WIDTH - MENU_RIGHT[0] + 5, 222))
            self.screen.blit(
                self.uniting.unit_typ.image, (WIDTH - MENU_RIGHT[0] - 5, 248)
            )
            self.screen.blit(self.uniting.button.image, self.uniting.button.pos)
            if self.uniting.window.visible == True:
                self.screen.blit(self.uniting.window.image, self.uniting.window.pos)
                # for var in self.uniting.window.variables:

        for window in self.unit_windows:
            if window.visible == True:
                self.screen.blit(window.image, window.pos)
                for button in window.buttons:
                    window.image.blit(button.image, button.pos)
                if 1 == 1:  # rolling display unit variables
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.men) + " / " + str(window.thing.max_men),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 38),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.supply)
                            + " / "
                            + str(window.thing.max_supply),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 58),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.uniforms)
                            + " / "
                            + str(window.thing.max_uniforms),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 78),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.fuel) + " / " + str(window.thing.max_fuel),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 98),
                    )

                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.light_ammo)
                            + " / "
                            + str(window.thing.max_light_ammo),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 138),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.heavy_ammo)
                            + " / "
                            + str(window.thing.max_heavy_ammo),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 158),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.rockets)
                            + " / "
                            + str(window.thing.max_rockets),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 178),
                    )

                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.rifle)
                            + " / "
                            + str(window.thing.max_rifle),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 218),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.artilleries)
                            + " / "
                            + str(window.thing.max_artilleries),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 238),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.truck)
                            + " / "
                            + str(window.thing.max_truck),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 258),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.apc) + " / " + str(window.thing.max_apc),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 278),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.tank) + " / " + str(window.thing.max_tank),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 298),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.heli) + " / " + str(window.thing.max_heli),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 318),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.aircraft)
                            + " / "
                            + str(window.thing.max_aircraft),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 338),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.rocket_truck)
                            + " / "
                            + str(window.thing.max_rocket_truck),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 358),
                    )
                    #upkeep cost
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.DESCRIPTION[12]
                            + str(window.thing.weekly_cost),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 378),
                    )
                    #max transporting
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.DESCRIPTION[13]
                            + str(window.thing.max_transport),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 10, window.pos[1] + 398),
                    )
                    #current transporting
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.DESCRIPTION[14] + str(window.thing.current_transport),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 220, window.pos[1] + 378),
                    )
                    #diplaying list of current transporting things
                    if len(window.thing.transporting) > 0:
                        keys = window.thing.transporting.keys()
                        posy = 0
                        for key in keys:
                            if posy < 80:
                                self.screen.blit(
                                    pg.font.Font(FONT_NAME, FONT_SIZE).render(
                                        key + ": " + str(window.thing.transporting[key]),
                                        False,
                                        LIGHTGREY,
                                    ),
                                    (window.pos[0] + 210, window.pos[1] + 398 + posy),
                                )
                            elif posy == 80:
                                self.screen.blit(
                                    pg.font.Font(FONT_NAME, FONT_SIZE).render(
                                        "... ... ...",
                                        False,
                                        LIGHTGREY,
                                    ),
                                    (window.pos[0] + 210, window.pos[1] + 398 + posy),
                                )
                            posy += 20

                    self.screen.blit(
                        window.thing.owner.image,
                        (window.pos[0] + 270, window.pos[1] + 30),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            window.thing.owner.name + " / " + window.thing.nationality.name, False, LIGHTGREY
                        ),
                        (window.pos[0] + 300, window.pos[1] + 38),
                    )
                    self.screen.blit(
                        window.thing.unit_typ.image,
                        (window.pos[0] + 260, window.pos[1] + 56),
                    )
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.thing.unit_typ.name, False, LIGHTGREY),
                        (window.pos[0] + 300, window.pos[1] + 58),)
                        
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            window.thing.print_mobilized(), False, LIGHTGREY
                        ),
                        (window.pos[0] + 270, window.pos[1] + 80),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.DESCRIPTION[2]
                            + ": "
                            + str(window.thing.combat_ability)
                            + "/"
                            + str(window.thing.combat_ability_max),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 270, window.pos[1] + 96),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.DESCRIPTION[0]
                            + ": "
                            + str(window.thing.experience),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 270, window.pos[1] + 117),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.DESCRIPTION[7]
                            + ": "
                            + str(window.thing.tiredness)
                            + "/"
                            + str(window.thing.tiredness_max),
                            False,
                            LIGHTGREY,
                        ),
                        (window.pos[0] + 270, window.pos[1] + 133),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            window.thing.task, False, LIGHTGREY
                        ),
                        (window.pos[0] + 270, window.pos[1] + 153),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.GUI[14] + str(window.thing.loyalty), False, LIGHTGREY
                        ),
                        (window.pos[0] + 270, window.pos[1] + 173),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.fuel_usage), False, YELLOW
                        ),
                        (window.pos[0] + 510, window.pos[1] + 60),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.GUI[12] + " " + return_bool(window.thing.conditions["starving"]), False, LIGHTGREY
                        ),
                        (window.pos[0] + 510, window.pos[1] + 220),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.GUI[13] + " " + return_bool(window.thing.conditions["run_away"]), False, LIGHTGREY
                        ),
                        (window.pos[0] + 510, window.pos[1] + 240),
                    )
                    y = 0
                    for t in window.thing.order_list:
                        if y <= 100:
                            self.screen.blit(
                                pg.font.Font(FONT_NAME, FONT_SIZE).render(

                                    t[0] + ": " + str(t[1][0]) + " " + str(t[1][1]), False, LIGHTGREY
                                ),
                                (window.pos[0] + 270, window.pos[1] + 240 + y),
                            )
                            y += 20
                        else:
                            self.screen.blit(
                            pg.font.Font(FONT_NAME, FONT_SIZE).render(

                                "... ... ...", False, LIGHTGREY
                            ),
                            (window.pos[0] + 270, window.pos[1] + 240 + y),
                        )
                            break

                    #printing new task option or change task option
                    if window.selected_order == 0:
                        self.screen.blit(
                            pg.font.Font(FONT_NAME, FONT_SIZE).render(
                                self.language.INFO_TEXTS[10], False, LIGHTGREY
                            ),
                            (window.pos[0] + 450, window.pos[1] + 340),
                        )
                    else:
                        self.screen.blit(
                            pg.font.Font(FONT_NAME, FONT_SIZE).render(
                                self.language.INFO_TEXTS[12] + str(window.selected_order), False, LIGHTGREY
                            ),
                            (window.pos[0] + 450, window.pos[1] + 340),
                        )


                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.NEW_TASKS[window.new_task_properties[0]], False, LIGHTGREY
                        ),
                        (window.pos[0] + 520, window.pos[1] + 360),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.new_task_properties[2]), False, LIGHTGREY
                        ),
                        (window.pos[0] + 520, window.pos[1] + 380),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.new_task_properties[3]), False, LIGHTGREY
                        ),
                        (window.pos[0] + 520, window.pos[1] + 400),
                    )


        for window in self.building_windows:
            if window.visible == True:
                self.screen.blit(window.image, window.pos)
                for button in window.buttons:
                    window.image.blit(button.image, button.pos)
                for t in window.texts:
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(t[0], False, t[2]),
                        (window.pos[0] + t[3][0], window.pos[1] + t[3][1]),
                    )

                # if 1 == 1: #rolling display building variables
                e = 0
                f = 0
                if window.thing.name != self.language.BUILDINGS1[6]:
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.GUI[4], False, LIGHTGREY
                        ),
                        (window.pos[0] + 10, window.pos[1] + 80 + (e * 20)),
                    )
                else:
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.DESCRIPTION[3], False, LIGHTGREY
                        ),
                        (window.pos[0] + 10, window.pos[1] + 80 + (e * 20)),
                    )

                self.screen.blit(
                    pg.font.Font(FONT_NAME, FONT_SIZE).render(
                        self.language.GUI[8], False, LIGHTGREY
                    ),
                    (window.pos[0] + 350, window.pos[1] + 40),
                )
                self.screen.blit(
                    pg.font.Font(FONT_NAME, FONT_SIZE).render(
                        self.language.GUI[10], False, LIGHTGREY
                    ),
                    (window.pos[0] + 560, window.pos[1] + 10),
                )

                if window.thing.owner.electricity == True:
                    self.screen.blit(
                        self.elect_yes_img, (window.pos[0] + 670, window.pos[1] + 7)
                    )
                else:
                    self.screen.blit(
                        self.elect_no_img, (window.pos[0] + 670, window.pos[1] + 7)
                    )

                for v in window.variables:

                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(v, False, LIGHTGREY),
                        (window.pos[0] + 10 + f, window.pos[1] + 100 + (e * 20)),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.storage[v]), False, LIGHTGREY
                        ),
                        (window.pos[0] + 110 + f, window.pos[1] + 100 + (e * 20)),
                    )
                    e += 1
                    if e > 18:
                        e = 0
                        f += 160
                if len(window.thing.orders) > 0:
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            window.thing.orders[0][0], False, LIGHTGREY
                        ),
                        (window.pos[0] + 300, window.pos[1] + 60),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.orders[0][1]), False, LIGHTGREY
                        ),
                        (window.pos[0] + 420, window.pos[1] + 60),
                    )

                if len(window.thing.orders) > 1:
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            window.thing.orders[1][0], False, LIGHTGREY
                        ),
                        (window.pos[0] + 300, window.pos[1] + 80),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.orders[1][1]), False, LIGHTGREY
                        ),
                        (window.pos[0] + 420, window.pos[1] + 80),
                    )

                if len(window.thing.orders) > 2:
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            window.thing.orders[2][0], False, LIGHTGREY
                        ),
                        (window.pos[0] + 300, window.pos[1] + 100),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.orders[2][1]), False, LIGHTGREY
                        ),
                        (window.pos[0] + 420, window.pos[1] + 100),
                    )

                if len(window.thing.orders) > 3:
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.GUI[9], False, LIGHTGREY
                        ),
                        (window.pos[0] + 300, window.pos[1] + 140),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(len(window.thing.orders)), False, LIGHTGREY
                        ),
                        (window.pos[0] + 420, window.pos[1] + 140),
                    )

                if (
                    window.thing.name == self.language.BUILDINGS1[1]
                    or window.thing.name == self.language.BUILDINGS1[2]
                ):
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.GUI[7], False, LIGHTGREY
                        ),
                        (window.pos[0] + 550, window.pos[1] + 40),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            "/ " + window.thing.nationality.name, False, LIGHTGREY
                        ),
                        (window.pos[0] + 320, window.pos[1] + 8),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            str(window.thing.population), False, LIGHTGREY
                        ),
                        (window.pos[0] + 550, window.pos[1] + 60),
                    )
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            self.language.GUI[14] +
                            str(window.thing.loyalty), False, LIGHTGREY
                        ),
                        (window.pos[0] + 550, window.pos[1] + 100),
                    )

        for window in self.menu_windows:
            if window.visible == True:
                self.screen.blit(window.image, window.pos)
                for button in window.buttons:
                    window.image.blit(button.image, button.pos)
                for variable in window.variables:
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            "$ " + str(variable[0]), False, variable[2]
                        ),
                        (
                            window.pos[0] + variable[3][0],
                            window.pos[1] + variable[3][1],
                        ),
                    )
                for res in window.resources:
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(
                            res[0], False, res[2]
                        ),
                        (window.pos[0] + res[3][0], window.pos[1] + res[3][1]),
                    )
                for t in window.texts:
                    self.screen.blit(
                        pg.font.Font(FONT_NAME, FONT_SIZE).render(t[0], False, t[2]),
                        (window.pos[0] + t[3][0], window.pos[1] + t[3][1]),
                    )

        pg.display.flip()

    def events(self):
        """
        All game events like mouse move and click, press keyboard keys
        """
        # pg.display.set_caption(str(self.timer))
        self.menu.position[0] = (
            str(self.language.DISPLAY_GUI[0])
            + str(self.mouse_pos.col)
            + " "
            + str(self.mouse_pos.row)
        )
        self.menu.time[0] = (
            str(self.language.DISPLAY_GUI[1])
            + str(self.hour)
            + ":"
            + f"{int(self.quarter * 15):02d}"
        )
        self.menu.speed[0] = str(
            self.language.DISPLAY_GUI[4]
            if self.pause == True
            else self.language.DISPLAY_GUI[5] + str(self.speed)
        )
        self.menu.data1[0] = (
            str(self.language.DISPLAY_GUI[2])
            + str(self.week)
            + self.language.DISPLAY_GUI[3]
            + str(self.day)
        )
        self.menu.data2[0] = (
            str(self.language.SEASONS[self.season]) + " " + str(self.year)
        )

        # qwx, qwy = pg.mouse.get_pos()
        # print(qwx, qwy)
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.deselect()
                    self.window_display = False
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.player.move(dx=-1)
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.player.move(dx=1)
                elif event.key == pg.K_UP or event.key == pg.K_w:
                    self.player.move(dy=-1)
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.move(dy=1)
                elif event.key == pg.K_e:
                    self.player.x = 12
                    self.player.y = 12
                elif event.key == pg.K_m:
                    self.territory_visible = not self.territory_visible
                elif (event.key == pg.K_KP_PLUS) or (event.key == pg.K_PLUS):  # plus key
                    if self.speed < 32:
                        self.speed = self.speed * 2
                elif (event.key == pg.K_KP_MINUS) or (event.key == pg.K_MINUS):  # minus key
                    if self.speed >= 2:
                        self.speed = self.speed / 2
                elif event.key == pg.K_PAUSE or event.key == pg.K_SPACE:
                    self.pause = not self.pause
                elif event.key == pg.K_LSHIFT:
                    self.multi_task = True
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_LSHIFT:
                    self.multi_task = False



            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for window in self.windows:
                        if (
                            window.rect.collidepoint(pg.mouse.get_pos())
                            and window.visible == True
                        ):
                            self.s_drag = pg.mouse.get_pos()
                            self.dragging = True
                            self.dragged = window
                            break

            if event.type == pg.MOUSEMOTION:
                if self.dragging == True:
                    self.dragged.pos[0] = self.dragged.pos[0] + (
                        pg.mouse.get_pos()[0] - self.s_drag[0]
                    )
                    self.dragged.pos[1] = self.dragged.pos[1] + (
                        pg.mouse.get_pos()[1] - self.s_drag[1]
                    )
                    self.s_drag = pg.mouse.get_pos()

            if event.type == pg.MOUSEBUTTONUP:
                # print(event.button)
                self.dragging = False
                self.dragged = None

                for a in self.menu.buttons:
                    a.check_col(pg.mouse.get_pos())

                if pg.mouse.get_pos()[0] < (WIDTH - MENU_RIGHT[0]):
                    if event.button == 1:
                        if self.window_display == False:
                            self.select(True)
                        # elif self.window_display == True:
                        for window in self.windows:
                            if window.visible == True:
                                for button in window.buttons:
                                    button.check_col(pg.mouse.get_pos())
                                    # print(pg.mouse.get_pos())

                    if event.button == 3:
                        if self.uniting != None:
                            if self.multi_task == False:
                                self.uniting.stop()
                                self.uniting.order_list = []
                                self.uniting.order_list.append(["go_to",self.mouse_pos])
                                
                            else:
                                self.uniting.order_list.append(["go_to",self.mouse_pos])

                if pg.mouse.get_pos()[0] > (WIDTH - MENU_RIGHT[0]):
                    if event.button == 1:
                        # print(self.selecting.building)
                        if self.uniting:
                            self.uniting.button.check_col(pg.mouse.get_pos())
                            # print(self.uniting.button.rect)
                            # print(pg.mouse.get_pos())
                        if self.building:
                            if self.building.window != None:
                                self.building.button.check_col(pg.mouse.get_pos())
                            # print(self.building.button.rect)
                            # print(pg.mouse.get_pos())

                        # if self.building == None:
                if self.building == None and self.selecting != None:
                    if self.selecting.owner == self.player.side:
                        self.menu.new_building_button.check_col(pg.mouse.get_pos())           

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game(player=1, map_name="default", save_name="save1")
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
