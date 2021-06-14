import pygame as pg
from settings import *
from languages import *
from sprites import *
from random import randint
from random import choice
import matplotlib.pyplot as plt
from queue import PriorityQueue


class Event_List(pg.sprite.Sprite):
    def __init__(self, game, events=[]):
        self.game = game
        self.events = events
        self.queue = PriorityQueue()
        for e in range(len(self.events)):
            self.queue.put((self.events[e][0], e))
        self.check = None

        self.window = Decision_Window(
            self.game,
            size=(500, 500),
            color=DARKGREY,
            text="Decision window",
            textpos=(150, 10),
            border_size=3,
            available=True,
            decisions=[],
        )
        self.scenario = Info_Window(
            self.game,
            size=(500, 500),
            text="Scenario Window",
            textpos=(150, 10),
            border_size=3,
            display_text=[],
            visible=False,
        )
        self.info = Info_Window(
            self.game,
            size=(500, 500),
            text="Info Window",
            textpos=(150, 10),
            border_size=3,
            display_text=[],
            visible=False,
        )

        # self.frontier.put((0, self.hexid))

    def add_event(self, event):
        self.queue.put((event[0], len(self.events)))
        self.events.append(event)

    def add_to_building(self, building, what, quantity):
        building.storage[what] += quantity

    def add_money_to_player(self, player, quantity):
        self.game.players[player].global_money += quantity

    def gain_stability(self, player, gain):
        self.game.players[player].stability -= gain

    def strengthen_the_currency(self, player, value):
        self.game.players[player].exc_rt = self.game.players[player].exc_rt * value
        self.game.players[player].exc_rt = round(self.game.players[player].exc_rt, 4)

    def show_new_info(self, info):
        self.info.new_text_to_display(info)
        self.info.show()

    def new_decisions(self, deci, option, text):
        self.window.decisions = []
        for a in range(len(deci)):
            self.window.decisions.append(deci[a])
        self.window.scripts = []
        for b in range(len(option)):
            self.window.scripts.append(option[b])
        self.window.texts = []
        for c in range(len(text)):
            self.window.texts.append([text[c], 16, LIGHTGREY, (10, 45 + (c * 20))])

        self.window.generate_wbat()
        self.open_decision_window()

    def switch(self, var):
        if var[0] == "add_to_building":
            self.add_to_building(var[1], var[2], var[3])
        elif var[0] == "add_money_to_player":
            self.add_money_to_player(var[1], var[2])
        elif var[0] == "gain_stability":
            self.gain_stability(var[1], var[2])
        elif var[0] == "strengthen_the_currency":
            self.strengthen_the_currency(var[1], var[2])

    def open_decision_window(self):
        self.window.show()

    def dayli(self):
        print(self.game.idn)  # identification date number
        if not self.queue.empty():
            self.check = self.queue.get()
        if self.check != None:
            if self.check[0] == self.game.idn:
                c = self.events[self.check[1]]
                if c[1] == "add_to_building":
                    print("Items go to building")
                    self.add_to_building(c[2], c[3], c[4])
                elif c[1] == "new_decision":
                    print("Decyzja")
                    self.new_decisions(c[2], c[3], c[4])
                elif c[1] == "show_new_info":
                    print("Info")
                    self.show_new_info(c[2])

                self.check = None
                self.dayli()
            else:
                print("none event")
                self.queue.put((self.check[0], self.check[1]))
        self.check = None


class Politics(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.window = Politics_Window(
            self.game,
            pos=[100, 100],
            text="Internal and external policy",
        )
    
    def update_window_value(self):
        self.window.update_politics()

    def dayli(self):
        #calculate of country global reputation
        for d in range(len(self.game.diplomacy.relations)):
            #print("Player")
            #print(d)
            gr_change = 0
            for r in self.game.diplomacy.relations[d]:
                #print(r)
                if r[2] == False:
                    gr_change -= 2
                if r[3] == True:
                    gr_change += 1
            self.game.players[d].reputation_change(gr_change)
        self.update_window_value()

                
class Diplomacy(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.relations = []
        for p in self.game.players:
            s = []
            for o in self.game.players:
                if p == o:
                    r = 200
                    t = True
                    a = True
                elif p.nation == o.nation:
                    r = randint(40, 60)
                    t = False
                    a = False
                else:
                    r = randint(-20, 20)
                    t = False
                    a = False
                # 0 side, 1 relations, 2 peace, 3 trade, 4 ally
                s.append(
                    [o.side, r, True, t, a, self.game.idn, self.game.idn, self.game.idn]
                )
            self.relations.append(s)
        self.window = Diplomacy_Window(
            self.game,
            pos=[100, 100],
            size=(900, 700),
            color=DARKGREY,
            text="Diplomacy Window",
            textsize=15,
            textcolor=LIGHTGREY,
            textpos=(150, 10),
            border_size=3,
            visible=False,
        )

    def refresh_players(self):
        self.players = self.game.players

    def update_window_value(self):
        self.window.show_relations()
        self.window.update_dip_info()

    def adding_new_player(self):
        pass

    def dayli(self):
        #calculate country relations
        for p in self.relations:  # p is each player
            print("Player")
            for r in p:  # r is each players relation
                print(r)
                if r[2] == False:  # is at war with
                    if r[1] > -200:
                        r[1] -= 1
                if r[3] == True:  # have trade agreement
                    if r[1] < 0:
                        r[1] += 1
                if r[4] == True:
                    if r[1] < 100:
                        r[1] += 1
        self.update_window_value()
                # 0 side, 1 relations, 2 peace, 3 trade, 4 ally


class Trade(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.resource_exchange_rate1 = [
            4,
            3,
            3,
            2,
            2,  # "Wood", "Food", "Cement", "Iron Ore", "Coal",
            5,
            1,
            10,
            10,
            5,  #    "Steel":5, "Water":1, "Tools":10, "Parts":10, "Aluminum":5,
            2,
            3,
            2,
            3,
            1,  #      "Oil":2, "Fuel":3, "Plastic":2, "Chemical Compounds":3, "Fertilizer":1,
            1,
            1,
            20,
            1,
            2,  #     "Silicon":1, "Calcium":1, "Electronics":20, "Cotton":1, "Textiles":2,
            1,
            1,
            5,
            30,
            5,
        ]  #       "Rubber":1, "Bauxite":1, "Furniture":5, "Civilian Machines":30, "Electronic Comp.":3
        self.resource_exchange_rate2 = [
            4,  #    "Supply":4,
            3,
            3,
            2,
            4,
            30,  #    "Uniforms":3, "Fuel":3, "Light Ammo":2, "Heavy Ammo":4, "Rockets":30,
            8,
            40,
            100,
            200,
            300,  #    "Rifle":8, "Artilleries":40, "Truck":100, "APC":200, "Tank":300,
            500,
            1000,
        ]  #    "Helicopters":500, "Aircrafts":1000
        # self.resource_rating = [4,3,3,2,2, #"Wood", "Food", "Cement", "Iron Ore", "Coal",
        # 5,1,10,10,5,#    "Steel":5, "Water":1, "Tools":10, "Parts":10, "Aluminum":5,
        # 2,3,2,3,1,#      "Oil":2, "Fuel":3, "Plastic":2, "Chemical Compounds":3, "Fertilizer":1,
        # 1,1,20,1,2,#     "Silicon":1, "Calcium":1, "Electronics":20, "Cotton":1, "Textiles":2,
        # 1,1,5,30,5]
        self.state = {}
        for a in self.game.language.RES1:
            self.state[a] = False
        for b in self.game.language.RES2:
            self.state[b] = False
        self.price_history1 = []  # 1 = base resources
        self.price_history2 = []
        self.price_history_date = []
        for c in range(len(self.resource_exchange_rate1)):
            self.price_history1.append([])
            self.price_history1[c].append(self.resource_exchange_rate1[c])
        for d in range(len(self.resource_exchange_rate2)):
            self.price_history2.append([])
            self.price_history2[d].append(self.resource_exchange_rate2[d])
        # self.price_history1.append(self.resource_exchange_rate1)
        # self.price_history2.append(self.resource_exchange_rate2)
        self.price_history_date.append(
            self.game.day
            + ((self.game.week - 1) * 7)
            + (self.game.season * 91)
            + ((self.game.year - 1980) * 364)
        )
        self.handle = []
        # self.label = []

    def rating(
        self, value
    ):  # convert int rating to color 1=fall/red 2=stable/grey 3=rising/green
        if value == 1:
            return DARKRED
        elif value == 2:
            return LIGHTGREY
        elif value == 3:
            return DARKGREEN

    def dayli(self):
        for a in range(len(self.resource_exchange_rate1)):
            # for a in self.game.menu.trade_window.variables:
            c = self.game.menu.trade_window.variables
            b = randint(1, 3)
            c[a][2] = self.rating(b)
            if c[a][0] > 0 and c[a][0] < 10:
                c[a][0] -= (2 - b) / 10
            if c[a][0] >= 10 and c[a][0] < 200:
                c[a][0] -= 2 - b
            if c[a][0] >= 200:  # and a[0] < 1000:
                c[a][0] -= (2 - b) * 10
            c[a][0] = round(c[a][0], 2)
            self.resource_exchange_rate1[a] = c[a][0]
        for a in range(len(self.resource_exchange_rate2)):
            # for a in self.game.menu.trade_window.variables:
            c = self.game.menu.trade_window.variables
            b = randint(1, 3)
            c[a + 25][2] = self.rating(b)
            if c[a + 25][0] > 0 and c[a + 25][0] < 10:
                c[a + 25][0] -= (2 - b) / 10
            if c[a + 25][0] >= 10 and c[a + 25][0] < 200:
                c[a + 25][0] -= 2 - b
            if c[a + 25][0] >= 200:  # and a[0] < 1000:
                c[a + 25][0] -= (2 - b) * 10
            c[a + 25][0] = round(c[a + 25][0], 2)
            self.resource_exchange_rate2[a] = c[a + 25][0]
        for c in range(len(self.resource_exchange_rate1)):
            self.price_history1[c].append(self.resource_exchange_rate1[c])
        for d in range(len(self.resource_exchange_rate2)):
            self.price_history2[d].append(self.resource_exchange_rate2[d])
        # self.price_history1.append(self.resource_exchange_rate1)
        # self.price_history2.append(self.resource_exchange_rate2)
        self.price_history_date.append(
            self.game.day
            + ((self.game.week - 1) * 7)
            + (self.game.season * 13)
            + ((self.game.year - 1980) * 364)
        )
        if self.game.menu.trade_window.visible == True:
            self.game.menu.trade_window.update_trade_quantity()

    def show_graph(self, which=0):
        if which == 0:
            plt.style.use("dark_background")
            self.handle = []
            # self.label = []
            for a in range(len(self.game.language.RES1)):
                if self.state[self.game.language.RES1[a]] == True:
                    self.handle.append(
                        plt.plot(
                            self.price_history_date,
                            self.price_history1[a],
                            color=ctts(choice(ALL_COLORS)),
                            label=str(self.game.language.RES1[a]),
                        )
                    )
                    # self.label.append(str(self.game.language.RES1[a]))

            for a in range(len(self.game.language.RES2)):
                if self.state[self.game.language.RES2[a]] == True:
                    self.handle.append(
                        plt.plot(
                            self.price_history_date,
                            self.price_history2[a],
                            color=ctts(choice(ALL_COLORS)),
                            label=str(self.game.language.RES2[a]),
                        )
                    )
                    # self.label.append(str(self.game.language.RES2[a]))
            plt.legend()

        elif which == 1:
            pass
        elif which == 2:
            pass
        plt.show()


class Nation(pg.sprite.Sprite):
    def __init__(self, game, name="Nation"):
        self.game = game
        self.name = name
        self.description = ""


class Contender(pg.sprite.Sprite):
    def __init__(
        self,
        game,
        name="Player",
        nation=0,
        player=False,
        side=0,
        exc_rt=1,
        money=0,
        global_money=0,
        reputation=0,
        stability=0,
        tax=3,
        reserve=0
    ):
        self.game = game
        self.alive = True
        self.name = name
        self.nation = self.game.nations[nation]
        self.player = player
        self.side = side
        self.id_num = 0
        self.exc_rt = exc_rt
        self.money = money
        self.global_money = global_money
        self.reputation = reputation
        self.stability = stability
        self.tax = tax
        self.reserve = reserve
        self.relations = []
        self.electricity = False
        self.cities = 0
        self.villages = 0
        self.structures = 0
        self.population = 0
        self.citizens = 0
        self.soldiers = 0

        self.image = pg.Surface((64, 64))
        self.image.fill(VIOLET)
        self.image.set_colorkey(VIOLET)
        self.image.blit(
            self.game.flags_img.copy(),
            FLAG_OFFSET,
            (0, self.side * FLAG_SIZE[1], FLAG_SIZE[0], FLAG_SIZE[1]),
        )

        self.color = pg.Surface((64, 64))
        self.color.fill(VIOLET)
        self.color.set_colorkey(VIOLET)
        self.color.blit(
            self.game.colors_img.copy(),
            (0, 0),
            (
                (self.side % 4) * TILESIZE[0],
                (self.side // 4) * TILESIZE[0],
                TILESIZE[0],
                TILESIZE[0],
            ),
        )

    def recalculate_all(self):
        self.cities = 0
        self.villages = 0
        self.structures = 0
        self.population = 0
        self.citizens = 0
        self.soldiers = 0
        for b in self.game.buildings:
            if b.owner.side == self.side:
                self.structures += 1
                if b.name == self.game.language.BUILDINGS1[2]:
                    self.cities += 1
                    self.population += b.population
                    if b.nationality == self.nation:
                        self.citizens += b.population
                elif b.name == self.game.language.BUILDINGS1[1]:
                    self.villages += 1
                    self.population += b.population
                    if b.nationality == self.nation:
                        self.citizens += b.population
        for u in self.game.units:
            if u.owner.side == self.side:
                self.soldiers += u.men
    
    def reputation_change(self, change):
        self.reputation += change
        if self.reputation > 100:
            self.reputation = 100
        elif self.reputation < -100:
            self.reputation = -100

    def buy_global_money(self, quantity, global_market):
        if self.money > quantity * self.exc_rt:
            self.money = self.money - (quantity * self.exc_rt)
            self.global_money = self.global_money + quantity

    def sell_global_money(self, quantity, global_market):
        if self.global_money > quantity:
            self.global_money = self.global_money - quantity
            self.money = self.money + (quantity * self.exc_rt)

    def make_diplo_decision(self, decision, other_player):
        if decision == "peace":
            if (
                self.game.idn
                - self.game.diplomacy.relations[self.id_num][other_player][5]
                > PEACE_TREATY
            ):
                self.game.diplomacy.relations[self.id_num][other_player][2] = True
                self.game.diplomacy.relations[other_player][self.id_num][2] = True
                self.game.diplomacy.relations[self.id_num][other_player][
                    5
                ] = self.game.idn
                self.game.diplomacy.relations[other_player][self.id_num][
                    5
                ] = self.game.idn

        if decision == "trade":
            if (
                self.game.diplomacy.relations[self.id_num][other_player][1]
                > TRADE_TREATY
            ):
                self.game.diplomacy.relations[self.id_num][other_player][3] = True
                self.game.diplomacy.relations[other_player][self.id_num][3] = True
                self.game.diplomacy.relations[self.id_num][other_player][
                    6
                ] = self.game.idn
                self.game.diplomacy.relations[other_player][self.id_num][
                    6
                ] = self.game.idn

        if decision == "alliance":
            if (
                self.game.diplomacy.relations[self.id_num][other_player][1]
                > ALLIANCE_TREATY
            ):
                self.game.diplomacy.relations[self.id_num][other_player][4] = True
                self.game.diplomacy.relations[other_player][self.id_num][4] = True
                self.game.diplomacy.relations[self.id_num][other_player][
                    7
                ] = self.game.idn
                self.game.diplomacy.relations[other_player][self.id_num][
                    7
                ] = self.game.idn

        if decision == "ask_for_money":
            if (
                self.game.diplomacy.relations[self.id_num][other_player][1]
                > GIVE_MONEY_REP
            ):
                if self.global_money > GIVE_MONEY:
                    self.global_money -= GIVE_MONEY
                    self.game.players[other_player].global_money += GIVE_MONEY
                    self.game.diplomacy.relations[self.id_num][other_player][
                        1
                    ] -= GIVE_MONEY_DEC_REP

    def daily(self):
        pass

    def hourly(self):
        self.electricity = False
        for a in self.game.buildings:
            if a.owner.name == self.name:
                if a.name == self.game.language.BUILDINGS1[11]:
                    if a.working == True:
                        self.electricity = True

    def update(self):
        pass


class Unit_Type(pg.sprite.Sprite):
    def __init__(
        self,
        game,
        name="Name",
        typ=0,
        s_normal=1,
        s_water=1,
        s_mountain=1,
        s_coast=1,
        s_river=1,
        s_no_fuel=20,
        money_usage=1,
        max_men=0,
        max_art=0,
        max_truck=5,
        max_apc=0,
        max_tank=0,
        max_heli=0,
        max_aircraft=0,
        max_rocket_truck=0,
    ):

        self.game = game
        self.name = name
        self.typ = typ
        self.s_normal = s_normal
        self.s_water = s_water
        self.s_mountain = s_mountain
        self.s_coast = s_coast
        self.s_river = s_river
        self.s_no_fuel = s_no_fuel

        self.money_usage = money_usage
        self.equipment = []
        self.max_men = max_men

        self.equipment.append("supply")
        self.equipment.append("uniforms")
        self.equipment.append("rifle")
        self.equipment.append("light_ammo")

        self.max_art = max_art
        if self.max_art > 0:
            self.equipment.append("artilleries")
            if not "heavy_ammo" in self.equipment:
                self.equipment.append("heavy_ammo")
        self.max_truck = max_truck
        if self.max_truck > 0:
            self.equipment.append("truck")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
        self.max_apc = max_apc
        if self.max_apc > 0:
            self.equipment.append("apc")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
            if not "light_ammo" in self.equipment:
                self.equipment.append("light_ammo")
        self.max_tank = max_tank
        if self.max_tank > 0:
            self.equipment.append("tank")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
            if not "heavy_ammo" in self.equipment:
                self.equipment.append("heavy_ammo")
        self.max_heli = max_heli
        if self.max_heli > 0:
            self.equipment.append("heli")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
            if not "heavy_ammo" in self.equipment:
                self.equipment.append("heavy_ammo")
        self.max_aircraft = max_aircraft
        if self.max_aircraft > 0:
            self.equipment.append("aircraft")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
            if not "heavy_ammo" in self.equipment:
                self.equipment.append("heavy_ammo")
        self.max_rocket_truck = max_rocket_truck
        if self.max_rocket_truck > 0:
            self.equipment.append("rocket_truck")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
            if not "rockets" in self.equipment:
                self.equipment.append("rockets")

        self.image = pg.Surface((TILESIZE[0], TILESIZE[0]))
        self.image.fill(VIOLET)
        self.image.set_colorkey(VIOLET)
        self.image.blit(
            self.game.units_img.copy(),
            UNIT_OFFSET,
            (0, self.typ * UNIT_SIZE[1], UNIT_SIZE[0], UNIT_SIZE[1]),
        )

    def move_cost(self, terrain):
        if terrain in {
            self.game.language.TERRAIN[0],
            self.game.language.TERRAIN[1],
            self.game.language.TERRAIN[4],
            self.game.language.TERRAIN[6],
        }:
            return self.s_normal
        elif terrain in {self.game.language.TERRAIN[2]}:
            return self.s_water
        elif terrain in {self.game.language.TERRAIN[3]}:
            return self.s_mountain
        elif terrain in {self.game.language.TERRAIN[5]}:
            return self.s_river
        else:
            return 0

    def attack(self):
        pass

    def defence(self):
        pass


class Menu(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.menus
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.list = []
        self.buttons = []

        self.m_r = pg.Surface((MENU_RIGHT[0], HEIGHT))
        self.m_r.fill(DARKGREY)
        self.c_m_r = (WIDTH - MENU_RIGHT[0], 0)
        self.list.append([self.m_r, self.c_m_r])

        self.m_t = pg.Surface((WIDTH - MENU_RIGHT[0], MENU_TOP[0]))
        self.m_t.fill(DARKGREY)
        self.c_m_t = (0, 0)
        self.list.append([self.m_t, self.c_m_t])

        self.m_b = pg.Surface((WIDTH - MENU_RIGHT[0], MENU_BOTTOM[0]))
        self.m_b.fill(DARKGREY)
        self.c_m_b = (0, HEIGHT - MENU_BOTTOM[0])
        self.list.append([self.m_b, self.c_m_b])

        self.new_building_window = New_Building_Window(
            self.game,
            text="New Building",
        )
        self.new_building_button = NB_Button(
            self.game,
            self.new_building_window,
            pos=[WIDTH - MENU_RIGHT[0] + 70, 425],
            text="New",
        )
        self.open_diplomacy_button = OT_Button(
            self.game.diplomacy.window,
            self.game,
            pos=[WIDTH - MENU_RIGHT[0] + 20, HEIGHT - 145],
            size=(135, 30),
            text="Diplomacy",
        )
        self.buttons.append(self.open_diplomacy_button)
        self.open_scenario_button = OT_Button(
            self.game.event_list.scenario,
            self.game,
            pos=[WIDTH - MENU_RIGHT[0] + 20, HEIGHT - 95],
            size=(115, 30),
            text="Scenario",
        )
        self.buttons.append(self.open_scenario_button)
        self.open_info_button = OT_Button(
            self.game.event_list.info,
            self.game,
            pos=[WIDTH - MENU_RIGHT[0] + 120, HEIGHT - 45],
            size=(65, 30),
            text="Info",
        )
        self.buttons.append(self.open_info_button)
        self.open_politics_button = OT_Button(
            self.game.politics.window,
            self.game,
            pos=[WIDTH - MENU_RIGHT[0] - 200, HEIGHT - 45],
            size=(110, 30),
            text="Politics",
        )
        self.buttons.append(self.open_politics_button)

        self.trade_window = Trade_Window(
            self.game,
            self.game.trade,
            text="Trade",
        )
        self.open_trade_window = OW_Button(
            self.game,
            self.trade_window,
            pos=[WIDTH - MENU_RIGHT[0] + 20, HEIGHT - 45],
            size=(78, 30),
            text="Trade",
        )
        self.buttons.append(self.open_trade_window)

        if 1 == 1:  # right menu
            self.position = [
                self.game.language.DISPLAY_GUI[0],
                20,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 10, 15),
            ]
            self.speed = [
                self.game.language.DISPLAY_GUI[5],
                16,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 10, 35),
            ]
            self.time = [
                self.game.language.DISPLAY_GUI[1],
                16,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 10, 55),
            ]
            self.data1 = ["Data", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 75)]
            self.data2 = ["Year", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 95)]
            self.terrain = [
                self.game.language.DISPLAY_GUI[6],
                16,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 60, 120),
            ]
            self.terrain1 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 85, 140)]
            self.terrain2 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 85, 160)]
            self.terrain3 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 85, 180)]

            self.unit = [
                self.game.language.DISPLAY_GUI[7],
                16,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 60, 210),
            ]
            self.unit1 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 30, 230)]
            self.unit2 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 30, 250)]
            self.unit3 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 270)]
            self.unit4 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 286)]
            self.unit5 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 310)]
            self.unit6 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 326)]
            self.unit7 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 350)]

            self.building = [
                self.game.language.DISPLAY_GUI[8],
                16,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 60, 400),
            ]
            self.building1 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 40, 420)]
            self.building2 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 490)]
            self.building3 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 510)]
            self.building4 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 530)]
            self.building5 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 550)]
            self.building6 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 570)]
            self.building7 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 590)]
            self.building8 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 610)]
            self.building9 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 630)]
            self.building10 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 650)]
            self.building11 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 670)]
            self.building12 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 690)]
            self.building13 = ["", 16, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 710)]

            self.game.texts.append(self.position)
            self.game.texts.append(self.speed)
            self.game.texts.append(self.time)
            self.game.texts.append(self.data1)
            self.game.texts.append(self.data2)
            self.game.texts.append(self.terrain)
            self.game.texts.append(self.terrain1)
            self.game.texts.append(self.terrain2)
            self.game.texts.append(self.terrain3)
            self.game.texts.append(self.unit)
            self.game.texts.append(self.unit1)
            self.game.texts.append(self.unit2)
            self.game.texts.append(self.unit3)
            self.game.texts.append(self.unit4)
            self.game.texts.append(self.unit5)
            self.game.texts.append(self.unit6)
            self.game.texts.append(self.unit7)
            self.game.texts.append(self.building)
            self.game.texts.append(self.building1)
            self.game.texts.append(self.building2)
            self.game.texts.append(self.building3)
            self.game.texts.append(self.building4)
            self.game.texts.append(self.building5)
            self.game.texts.append(self.building6)
            self.game.texts.append(self.building7)
            self.game.texts.append(self.building8)
            self.game.texts.append(self.building9)
            self.game.texts.append(self.building10)
            self.game.texts.append(self.building11)
            self.game.texts.append(self.building12)
            self.game.texts.append(self.building13)

        if 1 == 1:  # top bar -> tb
            self.tb_player_money = ["$ 0", 16, DARKGREEN, (340, 17)]
            self.tb_player_global_money = ["$ 0", 16, DARKGREEN, (490, 17)]

            self.game.texts.append(self.tb_player_money)
            self.game.texts.append(self.tb_player_global_money)
            
    #rendering darkgrey menu block
    def render(self, surface):
        for im in self.list:
            surface.blit(im[0], im[1])

    def make_menu(self):
        menu = pg.Surface([WIDTH, HEIGHT])
        menu.fill(VIOLET)
        menu.set_colorkey(VIOLET)
        self.render(menu)
        return menu

    def update(self):
        self.tb_player_money[0] = "$ " + str(self.game.players[1].money)
        self.tb_player_global_money[0] = "$ " + str(self.game.players[1].global_money)


class Button(pg.sprite.Sprite):  # regular button
    def __init__(
        self,
        game,
        window,
        pos=[6, 6],
        size=(20, 20),
        color=DARKGREY,
        text="X",
        textsize=24,
        textcolor=LIGHTGREY,
    ):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = pos
        # self.abs_pos = [0,0]
        # self.abs_pos[0] = self.pos[0] + self.window.pos[0]
        # self.abs_pos[1] = self.pos[1] + self.window.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor

        self.visible = self.window.visible
        # self.image = self.game.new_b_button.copy()

        self.image = self.game.button_1_img.copy()
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            (8, 4),
        )
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.visible = True
        self.game.window_display = True

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def update(self):
        # self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]


class Function_Button(Button):
    def __init__(
        self,
        game,
        window,
        pos=[6, 6],
        color=DARKGREY,
        text="X",
        textsize=20,
        textcolor=LIGHTGREY,
        function="function_name",
    ):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = pos
        self.size = (len(text) * 11 + 15, 30)
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.function = function

        self.visible = self.window.visible
        # self.image = self.game.new_b_button.copy()

        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, self.size[0], self.size[1]))
        pg.draw.rect(
            self.image,
            self.color,
            (
                0 + BUTTON_BORDER_SIZE,
                0 + BUTTON_BORDER_SIZE,
                self.size[0] - BUTTON_BORDER_SIZE * 2 - 1,
                self.size[1] - BUTTON_BORDER_SIZE * 2 - 1,
            ),
        )

        # self.image = self.game.button_1_img.copy()
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            (6, 7),
        )
        # self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.function_list(self.function)
        # self.game.window_display = True

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def update(self):
        # self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]


class CW_Button(Button):  # CW -> Close window
    def __init__(
        self,
        game,
        window,
        pos=[6, 6],
        size=(30, 30),
        color=LIGHTGREY,
        text="X",
        textsize=10,
        textcolor=BLACK,
    ):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = pos
        # self.abs_pos = [0,0]
        # self.abs_pos[0] = self.pos[0] + self.window.pos[0]
        # self.abs_pos[1] = self.pos[1] + self.window.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor

        self.visible = self.window.visible
        self.image = self.game.x_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.hide()

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def update(self):
        self.visible = self.window.visible
        # self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]


class Switch_Button(Button):
    def __init__(
        self,
        game,
        window,
        pos=[200, 60],
        size=(20, 20),
        color=LIGHTGREY,
        text="X",
        textsize=10,
        textcolor=BLACK,
        variable=None,
    ):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = pos
        # self.abs_pos = [0,0]
        # self.abs_pos[0] = self.pos[0] + self.window.pos[0]
        # self.abs_pos[1] = self.pos[1] + self.window.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.variable = variable

        self.visible = self.window.visible
        if self.window.thing.state[self.variable] == True:
            self.image = self.game.yes_img.copy()
        else:
            self.image = self.game.no_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.thing.state[self.variable] = not self.window.thing.state[
            self.variable
        ]

        if self.window.thing.state[self.variable] == True:
            self.image = self.game.yes_img.copy()
        else:
            self.image = self.game.no_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def update(self):
        self.visible = self.window.visible
        # self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]


class OW_Button(Button):  # open window
    def __init__(
        self,
        game,
        window,
        pos=[6, 6],
        size=(60, 30),
        color=DARKGREY,
        text="X",
        textsize=24,
        textcolor=LIGHTGREY,
    ):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = tuple(pos)
        self.abs_pos = [0, 0]
        self.abs_pos[0] = self.pos[0] + self.window.pos[0]
        self.abs_pos[1] = self.pos[1] + self.window.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.visible = True

        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(
            self.image,
            self.color,
            (
                0 + BUTTON_BORDER_SIZE,
                0 + BUTTON_BORDER_SIZE,
                size[0] - BUTTON_BORDER_SIZE * 2 - 1,
                size[1] - BUTTON_BORDER_SIZE * 2 - 1,
            ),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            (5, 5),
        )

        self.rect = self.image.get_rect()

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def click(self):
        self.window.show()

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class NB_Button(Button):  # new building button
    def __init__(
        self,
        game,
        window,
        pos=[6, 6],
        size=(56, 30),
        color=DARKGREY,
        text="X",
        textsize=24,
        textcolor=LIGHTGREY,
    ):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = tuple(pos)
        self.abs_pos = [0, 0]
        self.abs_pos[0] = self.pos[0] + self.window.pos[0]
        self.abs_pos[1] = self.pos[1] + self.window.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.visible = True

        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(
            self.image,
            self.color,
            (
                0 + BUTTON_BORDER_SIZE,
                0 + BUTTON_BORDER_SIZE,
                size[0] - BUTTON_BORDER_SIZE * 2 - 1,
                size[1] - BUTTON_BORDER_SIZE * 2 - 1,
            ),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            (5, 5),
        )

        self.rect = self.image.get_rect()

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def click(self):
        self.window.show()

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Window(pg.sprite.Sprite):
    def __init__(
        self,
        game,
        pos=[100, 100],
        size=(300, 400),
        color=DARKGREY,
        text="Text",
        textsize=15,
        textcolor=LIGHTGREY,
        textpos=(50, 10),
        border_size=3,
    ):
        self.groups = game.menu_windows, game.windows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.textpos = textpos
        self.border_size = border_size
        self.visible = False
        self.game.window_display = self.visible
        self.buttons = []
        self.variables = []
        self.resources = []
        self.texts = []

        # draw window
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(
            self.image,
            self.color,
            (
                0 + self.border_size,
                0 + self.border_size,
                size[0] - self.border_size * 2 - 1,
                size[1] - self.border_size * 2 - 1,
            ),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            self.textpos,
        )

        # draw buttons
        self.buttons.append(CW_Button(self.game, self, pos=[10, 10]))

        self.rect = self.image.get_rect()
        self.rectangle = pg.Surface(self.size)

    def function_list(self, function=None):
        pass

    def show(self):
        self.visible = True
        self.game.window_display = True

    def hide(self):
        self.visible = False
        self.game.window_display = False

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Info_Window(Window):
    def __init__(
        self,
        game,
        pos=[100, 100],
        size=(300, 400),
        color=DARKGREY,
        text="Text",
        textsize=15,
        textcolor=LIGHTGREY,
        textpos=(50, 10),
        border_size=3,
        display_text=["Just random text."],
        visible=False,
    ):
        self.groups = game.menu_windows, game.windows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.textpos = textpos
        self.border_size = border_size
        self.visible = visible
        self.game.window_display = self.visible
        self.buttons = []
        self.variables = []
        self.resources = []
        self.texts = display_text

        # draw window
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(
            self.image,
            self.color,
            (
                0 + self.border_size,
                0 + self.border_size,
                size[0] - self.border_size * 2 - 1,
                size[1] - self.border_size * 2 - 1,
            ),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            self.textpos,
        )

        # draw buttons
        self.buttons.append(CW_Button(self.game, self, pos=[10, 10]))

        self.rect = self.image.get_rect()
        self.rectangle = pg.Surface(self.size)

    def function_list(self, function=None):
        pass

    def new_text_to_display(self, display_text):
        self.texts = []
        for a in range(len(display_text)):
            self.texts.append([display_text[a], 16, LIGHTGREY, (10, 45 + (a * 20))])

    def show(self):
        # self.pause = True
        self.visible = True
        self.game.window_display = True

    def hide(self):
        self.visible = False
        self.game.window_display = False

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Politics_Window(Window):
    def __init__(
        self,
        game,
        pos=[100, 100],
        size=(600, 500),
        color=DARKGREY,
        text="Text",
        textsize=15,
        textcolor=LIGHTGREY,
        textpos=(50, 10),
        border_size=3,
        visible=False,
    ):
        self.groups = game.menu_windows, game.windows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.textpos = textpos
        self.border_size = border_size
        self.visible = visible
        self.game.window_display = self.visible
        self.buttons = []
        self.variables = []
        self.resources = []
        self.texts = []

        # draw window
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(
            self.image,
            self.color,
            (
                0 + self.border_size,
                0 + self.border_size,
                size[0] - self.border_size * 2 - 1,
                size[1] - self.border_size * 2 - 1,
            ),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            self.textpos,
        )

        # adding texts to display
        self.texts.append([self.game.language.POLITICS[0], 16, LIGHTGREY, (10, 45)])
        self.texts.append([str(self.game.players[self.game.player.side].tax), 16, LIGHTGREY, (190, 45)])
        self.texts.append([self.game.language.POLITICS[1], 16, LIGHTGREY, (10, 85)])
        self.texts.append([str(self.game.players[self.game.player.side].stability), 16, LIGHTGREY, (190, 85)])
        self.texts.append([self.game.language.POLITICS[2], 16, LIGHTGREY, (10, 105)])
        self.texts.append([str(self.game.players[self.game.player.side].reputation), 16, LIGHTGREY, (190, 105)])
        self.texts.append([self.game.language.POLITICS[3], 16, LIGHTGREY, (10, 125)])
        self.texts.append([str(self.game.players[self.game.player.side].cities), 16, LIGHTGREY, (190, 125)])
        self.texts.append([self.game.language.POLITICS[4], 16, LIGHTGREY, (10, 145)])
        self.texts.append([str(self.game.players[self.game.player.side].villages), 16, LIGHTGREY, (190, 145)])
        self.texts.append([self.game.language.POLITICS[5], 16, LIGHTGREY, (10, 165)])
        self.texts.append([str(self.game.players[self.game.player.side].structures), 16, LIGHTGREY, (190, 165)])
        self.texts.append([self.game.language.POLITICS[6], 16, LIGHTGREY, (10, 185)])
        self.texts.append([str(self.game.players[self.game.player.side].population), 16, LIGHTGREY, (190, 185)])
        self.texts.append([self.game.language.POLITICS[7], 16, LIGHTGREY, (10, 205)])
        self.texts.append([str(self.game.players[self.game.player.side].citizens), 16, LIGHTGREY, (190, 205)])
        self.texts.append([self.game.language.POLITICS[8], 16, LIGHTGREY, (10, 225)])
        self.texts.append([str(self.game.players[self.game.player.side].soldiers), 16, LIGHTGREY, (190, 225)])
        self.texts.append([self.game.language.POLITICS[11], 16, LIGHTGREY, (10, 245)])
        self.texts.append([str(self.game.players[self.game.player.side].reserve), 16, LIGHTGREY, (190, 245)])


        # draw buttons
        self.buttons.append(CW_Button(self.game, self, pos=[10, 10]))
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(250, 40),
                text=self.game.language.POLITICS[9],
                function="tax_decrease",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(370, 40),
                text=self.game.language.POLITICS[10],
                function="tax_increase",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(250, 235),
                text=self.game.language.POLITICS[12],
                function="conscription",
            )
        )
        
        
        self.rect = self.image.get_rect()
        self.rectangle = pg.Surface(self.size)

    def function_list(self, function=None):
        if function == "tax_decrease":
            self.tax_decrease()
        elif function == "tax_increase":
            self.tax_increase()
        elif function == "conscription":
            self.conscription()
        else:
            pass

    def tax_decrease(self):
        if self.game.players[self.game.player.side].tax >= 1:
            self.game.players[self.game.player.side].tax -= 1
        self.update_politics()

    def tax_increase(self):
        self.game.players[self.game.player.side].tax += 1
        self.game.players[self.game.player.side].stability -= 5
        self.update_politics()

    def conscription(self):
        for b in self.game.buildings:
            if b.owner.name == self.game.players[self.game.player.side].name and b.name != self.game.language.BUILDINGS1[0]:
                if b.name == self.game.language.BUILDINGS1[2]:#CITY
                    if b.nationality == self.game.players[self.game.player.side].nation:
                        if b.population > 100:
                            b.population -= CONSCRIPT_CITY_POP
                            self.game.players[self.game.player.side].reserve += CONSCRIPT_CITY_POP
                            self.game.players[self.game.player.side].stability -= CONSCRIPT_STAB_RED

                if b.name == self.game.language.BUILDINGS1[1]:#VILLAGE
                    if b.nationality == self.game.players[self.game.player.side].nation:
                        if b.population > 40:
                            b.population -= CONSCRIPT_VILL_POP
                            self.game.players[self.game.player.side].reserve += CONSCRIPT_VILL_POP
        self.update_politics()

    def update_politics(self):
        self.game.players[self.game.player.side].recalculate_all()
        self.texts[1][0] = str(self.game.players[self.game.player.side].tax)
        self.texts[3][0] = str(self.game.players[self.game.player.side].stability)
        self.texts[5][0] = str(self.game.players[self.game.player.side].reputation)
        self.texts[7][0] = str(self.game.players[self.game.player.side].cities)
        self.texts[9][0] = str(self.game.players[self.game.player.side].villages)
        self.texts[11][0] = str(self.game.players[self.game.player.side].structures)
        self.texts[13][0] = str(self.game.players[self.game.player.side].population)
        self.texts[15][0] = str(self.game.players[self.game.player.side].citizens)
        self.texts[17][0] = str(self.game.players[self.game.player.side].soldiers)
        self.texts[19][0] = str(self.game.players[self.game.player.side].reserve)

    def show(self):
        self.visible = True
        self.game.window_display = True
        self.update_politics()

    def hide(self):
        self.visible = False
        self.game.window_display = False

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Diplomacy_Window(Window):
    def __init__(
        self,
        game,
        pos=[100, 100],
        size=(300, 400),
        color=DARKGREY,
        text="Text",
        textsize=15,
        textcolor=LIGHTGREY,
        textpos=(50, 10),
        border_size=3,
        visible=False,
    ):
        self.groups = game.menu_windows, game.windows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.textpos = textpos
        self.border_size = border_size
        self.visible = visible
        self.game.window_display = self.visible
        self.buttons = []
        self.variables = []
        self.resources = []
        self.texts = []

        self.status_player = 0
        self.number_of_players = 0

        self.texts.append([self.game.language.DIPLOMACY[0], 16, LIGHTGREY, (10, 45)])
        self.texts.append(
            [self.game.players[self.status_player].name, 16, LIGHTGREY, (250, 45)]
        )

        self.texts.append([self.game.language.DIPLOMACY[1], 16, LIGHTGREY, (10, 85)])
        self.texts.append([self.game.language.DIPLOMACY[2], 16, LIGHTGREY, (10, 125)])
        self.texts.append([self.game.language.DIPLOMACY[3], 16, LIGHTGREY, (10, 165)])
        self.texts.append([self.game.language.DIPLOMACY[4], 16, LIGHTGREY, (10, 205)])
        self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (250, 85)])
        self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (250, 125)])
        self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (250, 165)])
        self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (250, 205)])
        self.texts.append([self.game.language.DIPLOMACY[5], 16, LIGHTGREY, (420, 85)])
        self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (420, 125)])
        self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (420, 165)])
        self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (420, 205)])

        for a in range(len(self.game.players)):
            self.texts.append(["side", 16, LIGHTGREY, (55, 250 + (a * 20))])
            self.texts.append(["relations", 16, LIGHTGREY, (200, 250 + (a * 20))])
            self.texts.append(["peace", 16, LIGHTGREY, (270, 250 + (a * 20))])
            self.texts.append(["trade", 16, LIGHTGREY, (350, 250 + (a * 20))])
            self.texts.append(["ally", 16, LIGHTGREY, (430, 250 + (a * 20))])

        # draw window

        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(
            self.image,
            self.color,
            (
                0 + self.border_size,
                0 + self.border_size,
                size[0] - self.border_size * 2 - 1,
                size[1] - self.border_size * 2 - 1,
            ),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            self.textpos,
        )

        # draw buttons
        self.buttons.append(CW_Button(self.game, self, pos=[10, 10]))
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(420, 20),
                text=self.game.language.BASIC[4],
                function="prev",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(520, 20),
                text=self.game.language.BASIC[5],
                function="next",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(320, 115),
                text=self.game.language.BASIC[13],
                function="peace",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(320, 155),
                text=self.game.language.BASIC[13],
                function="trade",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(320, 195),
                text=self.game.language.BASIC[13],
                function="alliance",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(700, 75),
                text=self.game.language.BASIC[14],
                function="give_money",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(700, 115),
                text=self.game.language.BASIC[15],
                function="ask_for_money",
            )
        )

        self.rect = self.image.get_rect()
        self.rectangle = pg.Surface(self.size)
        self.show_flags_and_names()

    def print_t_f(self, var):
        if var == True:
            return self.game.language.BASIC[0]
        else:
            return self.game.language.BASIC[1]

    def function_list(self, function=None):
        if function == "prev":
            self.prev()
        elif function == "next":
            self.next()
        elif function == "peace":
            self.peace()
        elif function == "trade":
            self.trade()
        elif function == "alliance":
            self.alliance()
        elif function == "ask_for_money":
            self.ask_for_money()
        elif function == "give_money":
            self.give_money()
        else:
            pass

    def update_dip_info(self):
        self.texts[6][0] = str(
            self.game.diplomacy.relations[self.status_player][self.game.player.side][1]
        )
        self.texts[7][0] = self.print_t_f(
            self.game.diplomacy.relations[self.status_player][self.game.player.side][2]
        )
        self.texts[8][0] = self.print_t_f(
            self.game.diplomacy.relations[self.status_player][self.game.player.side][3]
        )
        self.texts[9][0] = self.print_t_f(
            self.game.diplomacy.relations[self.status_player][self.game.player.side][4]
        )
        self.texts[11][0] = self.game.conv_idn_to_data(
            self.game.diplomacy.relations[self.status_player][self.game.player.side][5]
        )
        self.texts[12][0] = self.game.conv_idn_to_data(
            self.game.diplomacy.relations[self.status_player][self.game.player.side][6]
        )
        self.texts[13][0] = self.game.conv_idn_to_data(
            self.game.diplomacy.relations[self.status_player][self.game.player.side][7]
        )

    def prev(self):
        self.check_number_of_players()
        self.status_player -= 1
        if self.status_player < 0:
            self.status_player = self.number_of_players - 1
        self.texts[1][0] = self.game.players[self.status_player].name
        self.show_relations()
        self.update_dip_info()
        print(self.game.conv_idn_to_data(self.game.idn))

    def next(self):
        self.check_number_of_players()
        self.status_player += 1
        if self.status_player >= self.number_of_players:
            self.status_player = 0
        self.texts[1][0] = self.game.players[self.status_player].name
        self.show_relations()
        self.update_dip_info()
        print(self.game.conv_idn_to_data(self.game.idn))

    def peace(self):
        if self.status_player != self.game.player.side:
            if (
                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][2]
                == True
            ):
                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][2] = False
                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][1] -= 50
                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][5] = self.game.idn
                self.game.diplomacy.relations[self.game.player.side][
                    self.status_player
                ][2] = False
                self.game.diplomacy.relations[self.game.player.side][
                    self.status_player
                ][1] -= 50
                self.game.diplomacy.relations[self.game.player.side][
                    self.status_player
                ][1] -= self.game.idn
                self.trade()
                self.alliance()
            else:
                self.game.players[self.status_player].make_diplo_decision(
                    "peace", self.game.player.side
                )
            self.show_relations()
            self.update_dip_info()

    def trade(self):
        if self.status_player != self.game.player.side:
            if (
                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][2]
                == True
            ):
                if (
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][3]
                    == True
                ):
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][3] = False
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][1] -= 50
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][6] = self.game.idn
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][3] = False
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][1] -= 50
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][6] = self.game.idn
                else:
                    self.game.players[self.status_player].make_diplo_decision(
                        "trade", self.game.player.side
                    )
                self.show_relations()
                self.update_dip_info()
            else:
                if (
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][3]
                    == True
                ):
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][3] = False
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][1] -= 50
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][6] = self.game.idn
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][3] = False
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][1] -= 50
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][6] = self.game.idn

    def alliance(self):
        if self.status_player != self.game.player.side:
            if (
                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][2]
                == True
            ):
                if (
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][4]
                    == True
                ):
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][4] = False
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][1] -= 50
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][7] = self.game.idn
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][4] = False
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][1] -= 50
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][7] = self.game.idn
                else:
                    self.game.players[self.status_player].make_diplo_decision(
                        "alliance", self.game.player.side
                    )
                self.show_relations()
                self.update_dip_info()
            else:
                if (
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][4]
                    == True
                ):
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][4] = False
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][1] -= 50
                    self.game.diplomacy.relations[self.status_player][
                        self.game.player.side
                    ][7] = self.game.idn
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][4] = False
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][1] -= 50
                    self.game.diplomacy.relations[self.game.player.side][
                        self.status_player
                    ][7] = self.game.idn

    def ask_for_money(self):
        self.game.players[self.status_player].make_diplo_decision(
            "ask_for_money", self.game.player.side
        )
        self.show_relations()
        self.update_dip_info()

    def give_money(self):
        if self.game.players[self.game.player.side].global_money > GIVE_MONEY:
            self.game.players[self.game.player.side].global_money -= GIVE_MONEY
            self.game.players[self.status_player].global_money += GIVE_MONEY
            self.game.diplomacy.relations[self.status_player][self.game.player.side][
                1
            ] += 10
            self.show_relations()
            self.update_dip_info()

    def show_flags_and_names(self):
        self.check_number_of_players()
        for a in range(self.number_of_players):
            self.image.blit(self.game.players[a].image, (20, 240 + (a * 20)))
            # self.texts.append([self.game.players[a].name, 16, LIGHTGREY, (50, 68 + (a * 20))])

    def show_relations(self):
        self.check_number_of_players()
        b = 0
        for a in range(self.number_of_players):
            if self.status_player != a:
                self.texts[14 + b][0] = self.game.players[a].name
                self.texts[15 + b][0] = str(
                    self.game.diplomacy.relations[self.status_player][a][1]
                )
                self.texts[16 + b][0] = self.print_t_f(
                    self.game.diplomacy.relations[self.status_player][a][2]
                )
                self.texts[17 + b][0] = self.print_t_f(
                    self.game.diplomacy.relations[self.status_player][a][3]
                )
                self.texts[18 + b][0] = self.print_t_f(
                    self.game.diplomacy.relations[self.status_player][a][4]
                )
            else:
                self.texts[14 + b][0] = self.game.language.BASIC[11]
                self.texts[15 + b][0] = self.game.language.BASIC[12]
                self.texts[16 + b][0] = self.game.language.BASIC[12]
                self.texts[17 + b][0] = self.game.language.BASIC[12]
                self.texts[18 + b][0] = self.game.language.BASIC[12]
            b += 5

    def check_number_of_players(self):
        self.number_of_players = len(self.game.players)

    def show(self):
        self.show_relations()
        self.update_dip_info()
        self.visible = True
        self.game.window_display = True

    def hide(self):
        self.visible = False
        self.game.window_display = False

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Decision_Window(Window):
    def __init__(
        self,
        game,
        pos=[100, 100],
        size=(300, 400),
        color=DARKGREY,
        text="Text",
        textsize=15,
        textcolor=LIGHTGREY,
        textpos=(50, 10),
        border_size=3,
        available=True,
        decisions=[],
    ):
        self.groups = game.menu_windows, game.windows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.textpos = textpos
        self.border_size = border_size
        self.available = available
        self.decisions = decisions
        self.visible = False
        self.game.window_display = self.visible
        self.buttons = []
        self.variables = []
        self.resources = []
        self.texts = []
        self.scripts = []
        self.building_typ = 1

        if 1 == 1:
            # draw window
            self.image = pg.Surface(self.size)
            pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
            pg.draw.rect(
                self.image,
                self.color,
                (
                    0 + self.border_size,
                    0 + self.border_size,
                    size[0] - self.border_size * 2 - 1,
                    size[1] - self.border_size * 2 - 1,
                ),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.text, False, self.textcolor
                ),
                self.textpos,
            )
            # don't draw exit button
            # self.buttons.append(CW_Button(self.game, self, pos=[10,10]))
            self.rect = self.image.get_rect()
            self.rectangle = pg.Surface(self.size)

    def generate_wbat(self):
        self.buttons = []
        for a in range(len(self.decisions)):
            self.buttons.append(
                Function_Button(
                    self.game,
                    self,
                    pos=(20 + (a * 120), 300),
                    text=self.decisions[a],
                    function="func_" + str(a + 1),
                )
            )

    def function_list(self, function=None):
        if function == "func_1":
            self.func_1()
        elif function == "func_2":
            self.func_2()
        elif function == "func_3":
            self.func_3()
        else:
            pass

    def func_1(self):
        self.game.event_list.switch(self.scripts[0])
        self.hide()

    def func_2(self):
        self.game.event_list.switch(self.scripts[1])
        self.hide()

    def func_3(self):
        self.game.event_list.switch(self.scripts[2])
        self.hide()

    def show(self):
        self.visible = True
        self.game.window_display = True
        self.game.pause = True

    def hide(self):
        self.visible = False
        self.game.window_display = False

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class New_Building_Window(Window):
    def __init__(
        self,
        game,
        pos=[100, 100],
        size=(300, 400),
        color=DARKGREY,
        text="Text",
        textsize=15,
        textcolor=LIGHTGREY,
        textpos=(40, 10),
        border_size=3,
    ):
        self.groups = game.menu_windows, game.windows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.textpos = textpos
        self.border_size = border_size
        self.visible = False
        self.game.window_display = self.visible
        self.buttons = []
        self.variables = []
        self.resources = []
        self.texts = []
        self.building_typ = 1

        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(20, 350),
                text="Prev",
                function="func_1",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(220, 350),
                text="Next",
                function="func_2",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(120, 350),
                text="Done",
                function="func_3",
            )
        )

        self.var1 = ["", 16, LIGHTGREY, (10, 45)]
        self.var2 = ["Resouce cost:", 16, LIGHTGREY, (10, 65)]
        self.var3 = ["", 16, LIGHTGREY, (10, 85)]
        self.var4 = ["", 16, LIGHTGREY, (10, 105)]
        self.var5 = ["", 16, LIGHTGREY, (10, 125)]
        self.var6 = ["Near resources:", 16, LIGHTGREY, (140, 65)]

        self.variables.append(self.var1)
        self.variables.append(self.var2)
        self.variables.append(self.var3)
        self.variables.append(self.var4)
        self.variables.append(self.var5)
        self.variables.append(self.var6)

        if 1 == 1:
            # draw window
            self.image = pg.Surface(self.size)
            pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
            pg.draw.rect(
                self.image,
                self.color,
                (
                    0 + self.border_size,
                    0 + self.border_size,
                    size[0] - self.border_size * 2 - 1,
                    size[1] - self.border_size * 2 - 1,
                ),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.text, False, self.textcolor
                ),
                self.textpos,
            )
            # draw buttons
            self.buttons.append(CW_Button(self.game, self, pos=[10, 10]))
            self.rect = self.image.get_rect()
            self.rectangle = pg.Surface(self.size)

    def function_list(self, function=None):
        if function == "func_1":
            self.func_1()
        elif function == "func_2":
            self.func_2()
        elif function == "func_3":
            self.func_3()
        else:
            pass

    def func_1(self):
        if self.building_typ > 1:
            self.building_typ -= 1
        else:
            self.building_typ = 17

    def func_2(self):
        if self.building_typ < 17:
            self.building_typ += 1
        else:
            self.building_typ = 1

    def func_3(self):
        self.game.adding_building(self.building_typ)

    def show(self):
        self.visible = True
        self.game.window_display = True
        self.resources = []
        if len(self.game.selecting.near_resources) > 0:
            a = 0
            for r in self.game.selecting.near_resources:
                self.resources.append([r.name, 16, LIGHTGREY, (140, 85 + (a * 20))])
                self.resources.append(
                    [str(r.value), 16, LIGHTGREY, (200, 85 + (a * 20))]
                )
                a += 1

    def hide(self):
        self.visible = False
        self.game.window_display = False
        self.game.selecting.near_resources = []

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.var1[0] = self.game.language.BUILDINGS1[self.building_typ]
        self.var3[0] = (
            self.game.language.RES1[0]
            + ": "
            + str(BUILDING_COST[self.building_typ]["wood"])
        )
        self.var4[0] = (
            self.game.language.RES1[2]
            + ": "
            + str(BUILDING_COST[self.building_typ]["cement"])
        )
        self.var5[0] = (
            self.game.language.RES1[5]
            + ": "
            + str(BUILDING_COST[self.building_typ]["steel"])
        )


class Unit_Window(pg.sprite.Sprite):
    def __init__(
        self,
        unit,
        game,
        pos=[100, 100],
        size=(300, 400),
        color=DARKGREY,
        text="Text",
        textsize=15,
        textcolor=LIGHTGREY,
        textpos=(50, 10),
        border_size=3,
    ):
        self.groups = game.unit_windows, game.windows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.thing = unit
        self.game = game
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.textpos = textpos
        self.border_size = border_size
        self.visible = False
        self.game.window_display = self.visible
        self.buttons = []
        self.variables = []
        self.texts = []

        # draw window
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(
            self.image,
            self.color,
            (
                0 + self.border_size,
                0 + self.border_size,
                size[0] - self.border_size * 2 - 1,
                size[1] - self.border_size * 2 - 1,
            ),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            self.textpos,
        )

        # draw buttons
        self.buttons.append(CW_Button(self.game, self, pos=[10, 10]))
        self.buttons.append(
            Switch_Button(
                self.game,
                self,
                pos=[560, 40],
                size=(20, 20),
                color=LIGHTGREY,
                text="X",
                textsize=10,
                textcolor=BLACK,
                variable="mobilized",
            )
        )
        self.buttons.append(
            Switch_Button(
                self.game,
                self,
                pos=[560, 60],
                size=(20, 20),
                color=LIGHTGREY,
                text="X",
                textsize=10,
                textcolor=BLACK,
                variable="training",
            )
        )
        self.buttons.append(
            Switch_Button(
                self.game,
                self,
                pos=[560, 80],
                size=(20, 20),
                color=LIGHTGREY,
                text="X",
                textsize=10,
                textcolor=BLACK,
                variable="refill_equipment",
            )
        )
        self.buttons.append(
            Switch_Button(
                self.game,
                self,
                pos=[560, 100],
                size=(20, 20),
                color=LIGHTGREY,
                text="X",
                textsize=10,
                textcolor=BLACK,
                variable="refill_crew",
            )
        )
        self.buttons.append(
            Switch_Button(
                self.game,
                self,
                pos=[560, 120],
                size=(20, 20),
                color=LIGHTGREY,
                text="X",
                textsize=10,
                textcolor=BLACK,
                variable="building",
            )
        )
        self.buttons.append(
            Switch_Button(
                self.game,
                self,
                pos=[560, 140],
                size=(20, 20),
                color=LIGHTGREY,
                text="X",
                textsize=10,
                textcolor=BLACK,
                variable="patroling",
            )
        )
        self.buttons.append(
            Switch_Button(
                self.game,
                self,
                pos=[560, 160],
                size=(20, 20),
                color=LIGHTGREY,
                text="X",
                textsize=10,
                textcolor=BLACK,
                variable="engage",
            )
        )
        self.buttons.append(
            Switch_Button(
                self.game,
                self,
                pos=[560, 180],
                size=(20, 20),
                color=LIGHTGREY,
                text="X",
                textsize=10,
                textcolor=BLACK,
                variable="conquest",
            )
        )

        # draw eq names
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.DESCRIPTION[3], False, self.textcolor
            ),
            (150, 40),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[0], False, self.textcolor
            ),
            (150, 60),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[1], False, self.textcolor
            ),
            (150, 80),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[2], False, self.textcolor
            ),
            (150, 100),
        )

        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[3], False, self.textcolor
            ),
            (150, 140),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[4], False, self.textcolor
            ),
            (150, 160),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[5], False, self.textcolor
            ),
            (150, 180),
        )

        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[6], False, self.textcolor
            ),
            (150, 220),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[7], False, self.textcolor
            ),
            (150, 240),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[8], False, self.textcolor
            ),
            (150, 260),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[9], False, self.textcolor
            ),
            (150, 280),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[10], False, self.textcolor
            ),
            (150, 300),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[11], False, self.textcolor
            ),
            (150, 320),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[12], False, self.textcolor
            ),
            (150, 340),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.RES2[13], False, self.textcolor
            ),
            (150, 360),
        )

        # draw gui text
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.DESCRIPTION[1], False, self.textcolor
            ),
            (580, 42),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.DESCRIPTION[4], False, self.textcolor
            ),
            (580, 60),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.DESCRIPTION[5], False, self.textcolor
            ),
            (580, 80),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.DESCRIPTION[6], False, self.textcolor
            ),
            (580, 100),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.DESCRIPTION[8], False, self.textcolor
            ),
            (580, 120),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.DESCRIPTION[9], False, self.textcolor
            ),
            (580, 140),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.DESCRIPTION[10], False, self.textcolor
            ),
            (580, 160),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.DESCRIPTION[11], False, self.textcolor
            ),
            (580, 180),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.game.language.GUI[11], False, self.textcolor
            ),
            (400, 40),
        )

        self.rect = self.image.get_rect()
        self.rectangle = pg.Surface(self.size)
        # self.rect.x = 600
        # self.rect.y = 600

    def function_list(self, function=None):
        if function == "func_1":
            self.func_1()
        elif function == "func_2":
            self.func_2()
        else:
            pass

    def func_1(self):
        pass

    def func_2(self):
        pass

    def show(self):
        self.visible = True
        self.game.window_display = True

    def hide(self):
        self.visible = False
        self.game.window_display = False

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Building_Window(pg.sprite.Sprite):
    def __init__(
        self,
        building,
        game,
        pos=[300, 200],
        size=(700, 500),
        color=DARKGREY,
        text="",
        textsize=16,
        textcolor=LIGHTGREY,
        textpos=(35, 10),
        border_size=2,
    ):
        self.groups = game.building_windows, game.windows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.thing = building
        self.game = game
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.textpos = textpos
        self.border_size = border_size
        self.visible = False
        self.game.window_display = self.visible
        self.buttons = []
        self.variables = []
        self.texts = []

        # draw window
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(
            self.image,
            self.color,
            (
                0 + self.border_size,
                0 + self.border_size,
                size[0] - self.border_size * 2 - 1,
                size[1] - self.border_size * 2 - 1,
            ),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            self.textpos,
        )

        # draw buttons
        self.buttons.append(CW_Button(self.game, self, pos=[10, 10]))
        # self.buttons.append(Switch_Button(self.game, self, pos=[560,40], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable="mobilized"))

        # draw gui text
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.thing.name, False, self.textcolor
            ),
            (30, 10),
        )
        self.image.blit(self.thing.image, (0, 25))
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.thing.owner.name, False, self.textcolor
            ),
            (245, 10),
        )
        self.image.blit(self.thing.owner.image, (220, 0))

        self.rect = self.image.get_rect()
        self.rectangle = pg.Surface(self.size)
        # self.rect.x = 600
        # self.rect.y = 600

    def function_list(self, function=None):
        if function == "func_1":
            self.func_1()
        elif function == "func_2":
            self.func_2()
        elif function == "func_prev_unit":
            self.func_prev_unit()
        elif function == "func_new_unit":
            self.func_new_unit()
        elif function == "func_next_unit":
            self.func_next_unit()
        else:
            pass

    def func_1(self):
        pass

    def func_2(self):
        pass

    def func_prev_unit(self):
        self.thing.new_unit_typ -= 1
        if self.thing.new_unit_typ < 0:
            self.thing.new_unit_typ = 14
        self.texts[0][0] = self.game.language.UNIT_TYPE[self.thing.new_unit_typ]
        # print(self.thing.new_unit_typ)

    def func_next_unit(self):
        self.thing.new_unit_typ += 1
        if self.thing.new_unit_typ > 14:
            self.thing.new_unit_typ = 0
        self.texts[0][0] = self.game.language.UNIT_TYPE[self.thing.new_unit_typ]
        # print(self.thing.new_unit_typ)

    def func_new_unit(self):
        print("Number of graduates:")
        print(self.thing.storage["graduates"])

    def show(self):
        self.visible = True
        self.game.window_display = True

    def hide(self):
        self.visible = False
        self.game.window_display = False

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Trade_Window(Window):
    def __init__(
        self,
        game,
        trade,
        pos=[100, 100],
        size=(800, 650),
        color=DARKGREY,
        text="Trade",
        textsize=15,
        textcolor=LIGHTGREY,
        textpos=(40, 10),
        border_size=3,
    ):
        self.groups = game.menu_windows, game.windows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.thing = trade
        self.owner = self.game.players[self.game.player.side]
        self.trade_building_list = []
        for a in self.game.buildings:
            if (
                a.name == self.game.language.BUILDINGS1[3]
                or a.name == self.game.language.BUILDINGS1[4]
            ):
                if a.owner == self.owner:
                    self.trade_building_list.append(a)
        self.trade_building = None
        self.trade_building_counter = None
        self.trade_goods = 0
        self.trade_goods_name = ""
        self.trade_quantity = 0
        self.trade_transport_cost = 0
        self.trade_goods_cost = 0
        self.trade_total_cost = 0
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.textpos = textpos
        self.border_size = border_size
        self.visible = False
        self.game.window_display = self.visible
        self.buttons = []
        self.variables = []
        self.resources = []
        self.texts = []
        self.building_typ = 1

        # self.buttons.append(Function_Button(self.game, self, pos=(20, 600), size=(len(self.game.language.BASIC[4])*11+15, 30), color=DARKGREY, text=self.game.language.BASIC[4], textsize=20, textcolor=LIGHTGREY, function="func_1"))
        # self.buttons.append(Function_Button(self.game, self, pos=(170, 600), size=(len(self.game.language.BASIC[6])*11+15, 30), color=DARKGREY, text=self.game.language.BASIC[6], textsize=20, textcolor=LIGHTGREY, function="func_2"))
        # self.buttons.append(Function_Button(self.game, self, pos=(320, 600), size=(len(self.game.language.BASIC[7])*11+15, 30), color=DARKGREY, text=self.game.language.BASIC[7], textsize=20, textcolor=LIGHTGREY, function="func_3"))
        # self.buttons.append(Function_Button(self.game, self, pos=(470, 600), size=(len(self.game.language.BASIC[5])*11+15, 30), color=DARKGREY, text=self.game.language.BASIC[5], textsize=20, textcolor=LIGHTGREY, function="func_4"))
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(720, 400),
                text=self.game.language.BASIC[8],
                function="show_graph",
            )
        )

        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(660, 10),
                text=self.game.language.BASIC[6],
                function="sell_global_currency",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(740, 10),
                text=self.game.language.BASIC[7],
                function="buy_global_currency",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(200, 400),
                text=self.game.language.BASIC[4],
                function="prev_trade_building",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(300, 400),
                text=self.game.language.BASIC[5],
                function="next_trade_building",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(200, 460),
                text=self.game.language.BASIC[4],
                function="prev_trade_goods",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(300, 460),
                text=self.game.language.BASIC[5],
                function="next_trade_goods",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(175, 520),
                text=self.game.language.TRADE[4],
                function="quantity-10",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(235, 520),
                text=self.game.language.TRADE[5],
                function="quantity-1",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(290, 520),
                text=self.game.language.TRADE[6],
                function="quantity+1",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(340, 520),
                text=self.game.language.TRADE[7],
                function="quantity+10",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(255, 570),
                text=self.game.language.BASIC[7],
                function="buy_trade_goods",
            )
        )

        if 1 == 1:
            # draw window
            self.image = pg.Surface(self.size)
            pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
            pg.draw.rect(
                self.image,
                self.color,
                (
                    0 + self.border_size,
                    0 + self.border_size,
                    size[0] - self.border_size * 2 - 1,
                    size[1] - self.border_size * 2 - 1,
                ),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.text, False, self.textcolor
                ),
                self.textpos,
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.game.language.BASIC[10], False, self.textcolor
                ),
                (500, 20),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.game.language.TRADE[0], False, self.textcolor
                ),
                (30, 400),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.game.language.TRADE[2], False, self.textcolor
                ),
                (30, 460),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.game.language.TRADE[3], False, self.textcolor
                ),
                (30, 500),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.game.language.TRADE[8], False, self.textcolor
                ),
                (30, 560),
            )
            # draw buttons
            self.buttons.append(CW_Button(self.game, self, pos=[10, 10]))
            self.rect = self.image.get_rect()
            self.rectangle = pg.Surface(self.size)
            b = 0
            c = 0
            for a in self.game.language.RES1:
                self.image.blit(
                    pg.font.Font(FONT_NAME, self.textsize).render(
                        a, False, self.textcolor
                    ),
                    (110 + c, 60 + (b * 20)),
                )

                b += 1
                if b > 8:
                    c += 270
                    b = 0
            b = 0
            c = 0
            for a in self.game.language.RES2:
                self.image.blit(
                    pg.font.Font(FONT_NAME, self.textsize).render(
                        a, False, self.textcolor
                    ),
                    (110 + c, 280 + (b * 20)),
                )

                b += 1
                if b > 4:
                    c += 270
                    b = 0
            b = 0
            c = 0
            for a in range(25):
                self.buttons.append(
                    Switch_Button(
                        self.game,
                        self,
                        pos=[90 + c, 60 + (b * 20)],
                        size=(20, 20),
                        color=LIGHTGREY,
                        text="X",
                        textsize=10,
                        textcolor=BLACK,
                        variable=self.game.language.RES1[a],
                    )
                )
                b += 1
                if b > 8:
                    c += 270
                    b = 0
            b = 0
            c = 0
            for a in range(13):
                self.buttons.append(
                    Switch_Button(
                        self.game,
                        self,
                        pos=[90 + c, 280 + (b * 20)],
                        size=(20, 20),
                        color=LIGHTGREY,
                        text="X",
                        textsize=10,
                        textcolor=BLACK,
                        variable=self.game.language.RES2[a],
                    )
                )
                b += 1
                if b > 4:
                    c += 270
                    b = 0

        self.image.blit(self.game.players[self.game.player.side].image, (112, 0))
        self.image.blit(self.game.money_img, (110, 30))
        self.image.blit(self.game.global_img, (263, 8))
        self.image.blit(self.game.money_img, (260, 30))
        self.image.blit(self.game.players[self.game.player.side].image, (400, -4))
        self.image.blit(self.game.exchange_img, (400, 15))
        self.image.blit(self.game.global_img, (402, 35))

        self.texts.append(
            [
                "$ " + str(self.game.players[self.game.player.side].money),
                16,
                DARKGREEN,
                (140, 20),
            ]
        )
        self.texts.append(
            [
                "$ " + str(self.game.players[self.game.player.side].global_money),
                16,
                DARKGREEN,
                (290, 20),
            ]
        )
        self.texts.append(
            [
                str(self.game.players[self.game.player.side].exc_rt),
                16,
                LIGHTGREY,
                (430, 20),
            ]
        )
        self.texts.append([self.game.language.TRADE[1], 16, LIGHTGREY, (10, 420)])
        self.texts.append([self.game.language.TRADE[1], 16, LIGHTGREY, (10, 440)])
        self.texts.append(
            [self.game.language.RES1[self.trade_goods], 16, LIGHTGREY, (10, 480)]
        )
        self.texts.append([str(self.trade_quantity), 16, LIGHTGREY, (10, 520)])
        self.texts.append([self.game.language.TRADE[9], 16, LIGHTGREY, (10, 580)])
        self.texts.append([str(self.trade_transport_cost), 16, LIGHTGREY, (120, 580)])
        self.texts.append([self.game.language.TRADE[10], 16, LIGHTGREY, (10, 600)])
        self.texts.append([str(self.trade_goods_cost), 16, LIGHTGREY, (120, 600)])
        self.texts.append([self.game.language.TRADE[11], 16, LIGHTGREY, (10, 620)])
        self.texts.append([str(self.trade_total_cost), 16, LIGHTGREY, (120, 620)])
        self.texts.append([self.game.language.TRADE[12], 16, LIGHTGREY, (200, 620)])
        self.texts.append([self.game.language.TRADE[1], 16, LIGHTGREY, (300, 620)])

        b = 0
        c = 0
        for a in self.game.trade.resource_exchange_rate1:
            self.variables.append(
                [a, 16, self.game.trade.rating(randint(1, 3)), (20 + c, 60 + (b * 20))]
            )

            b += 1
            if b > 8:
                c += 270
                b = 0
        b = 0
        c = 0
        for a in self.game.trade.resource_exchange_rate2:
            self.variables.append(
                [a, 16, self.game.trade.rating(randint(1, 3)), (20 + c, 280 + (b * 20))]
            )
            # self.game.trade.rating(randint(1,3))
            b += 1
            if b > 4:
                c += 270
                b = 0

    def dayli(self):
        pass

    def function_list(self, function=None):
        if function == "func_1":
            self.func_1()
        elif function == "func_2":
            self.func_2()
        elif function == "func_3":
            self.func_3()
        elif function == "func_4":
            self.func_4()
        elif function == "show_graph":
            self.show_graph()
        elif function == "sell_global_currency":
            self.sell_global_currency()
        elif function == "buy_global_currency":
            self.buy_global_currency()
        elif function == "next_trade_building":
            self.next_trade_building()
        elif function == "prev_trade_building":
            self.prev_trade_building()
        elif function == "next_trade_goods":
            self.next_trade_goods()
        elif function == "prev_trade_goods":
            self.prev_trade_goods()
        elif function == "quantity-10":
            self.quantity_minus_10()
        elif function == "quantity-1":
            self.quantity_minus_1()
        elif function == "quantity+1":
            self.quantity_plus_1()
        elif function == "quantity+10":
            self.quantity_plus_10()
        elif function == "buy_trade_goods":
            self.buy_trade_goods()
        else:
            pass

    def func_1(self):
        print("prev")

    def func_2(self):
        print("sell")

    def func_3(self):
        print("buy")

    def func_4(self):
        print("next")

    def show_graph(self):
        self.game.trade.show_graph(which=0)

    def sell_global_currency(self):
        if self.owner.global_money > 100:
            self.owner.global_money -= 100
            self.owner.money += 100 * self.owner.exc_rt
            self.owner.money = round(self.owner.money, 4)
            self.owner.exc_rt = self.owner.exc_rt * 0.990
            self.owner.exc_rt = round(self.owner.exc_rt, 4)
            self.update_trade_total_cost()

    def buy_global_currency(self):
        if self.owner.money > 100 * self.owner.exc_rt:
            self.owner.money -= 100 * self.owner.exc_rt
            self.owner.money = round(self.owner.money, 2)
            self.owner.global_money += 100
            self.owner.global_money = round(self.owner.global_money, 4)
            self.owner.exc_rt = self.owner.exc_rt * 1.005
            self.owner.exc_rt = round(self.owner.exc_rt, 4)
            self.update_trade_total_cost()

    def next_trade_building(self):
        if len(self.trade_building_list) > 0:
            if self.trade_building_counter == None:
                self.trade_building_counter = 0
            if self.trade_building_counter < len(self.trade_building_list) - 1:
                self.trade_building_counter += 1
            else:
                self.trade_building_counter = 0
            self.update_trade_building()

    def prev_trade_building(self):
        if len(self.trade_building_list) > 0:
            if self.trade_building_counter == None:
                self.trade_building_counter = 0
            if self.trade_building_counter > 0:
                self.trade_building_counter -= 1
            else:
                self.trade_building_counter = len(self.trade_building_list) - 1
            self.update_trade_building()

    def next_trade_goods(self):
        self.trade_goods += 1
        if self.trade_goods >= (len(RES1_LIST) + len(RES2_LIST)):
            self.trade_goods = 0
        self.update_trade_goods()

    def prev_trade_goods(self):
        self.trade_goods -= 1
        if self.trade_goods < 0:
            self.trade_goods = int(len(RES1_LIST) + len(RES2_LIST) - 1)
        self.update_trade_goods()

    def quantity_minus_10(self):
        if self.trade_quantity >= 10:
            self.trade_quantity -= 10
            self.update_trade_quantity()

    def quantity_minus_1(self):
        if self.trade_quantity >= 1:
            self.trade_quantity -= 1
            self.update_trade_quantity()

    def quantity_plus_1(self):
        self.trade_quantity += 1
        self.update_trade_quantity()

    def quantity_plus_10(self):
        self.trade_quantity += 10
        self.update_trade_quantity()

    def update_trade_total_cost(self):
        self.trade_total_cost = self.trade_goods_cost + self.trade_transport_cost
        self.texts[12][0] = str(self.trade_total_cost)
        if (
            self.trade_total_cost > self.owner.global_money
            or self.texts[3][0] == self.game.language.TRADE[1]
        ):
            self.texts[14][0] = self.game.language.TRADE[13]
            self.texts[14][2] = DARKRED
        else:
            self.texts[14][0] = self.game.language.TRADE[14]
            self.texts[14][2] = DARKGREEN

    def update_trade_quantity(self):
        self.texts[6][0] = str(self.trade_quantity)
        self.update_trade_transport_cost()
        self.update_trade_goods_cost()

    def update_trade_goods(self):
        if self.trade_goods < len(RES1_LIST):
            self.texts[5][0] = self.game.language.RES1[self.trade_goods]
            self.trade_goods_name = RES1_LIST[self.trade_goods].lower()
            self.update_trade_goods_cost()
        else:
            self.texts[5][0] = self.game.language.RES2[
                int(self.trade_goods - len(RES1_LIST))
            ]
            self.trade_goods_name = RES2_LIST[self.trade_goods - len(RES1_LIST)].lower()
            self.update_trade_goods_cost()

    def update_trade_building(self):
        self.texts[3][0] = self.trade_building_list[self.trade_building_counter].name
        self.texts[4][0] = (
            "Pos: "
            + str(self.trade_building_list[self.trade_building_counter].col)
            + " / "
            + str(self.trade_building_list[self.trade_building_counter].row)
        )
        if (
            self.trade_building_list[self.trade_building_counter].name
            == self.game.language.BUILDINGS1[3]
        ):
            self.trade_transport_cost = HARBOR_TRANSPORT_COST * self.trade_quantity
            self.texts[8][0] = str(self.trade_transport_cost)
        if (
            self.trade_building_list[self.trade_building_counter].name
            == self.game.language.BUILDINGS1[4]
        ):
            self.trade_transport_cost = AIRPORT_TRANSPORT_COST * self.trade_quantity
            self.texts[8][0] = str(self.trade_transport_cost)
        self.trade_building = self.trade_building_list[self.trade_building_counter]
        self.update_trade_transport_cost()

    def update_trade_transport_cost(self):
        if self.texts[3][0] != self.game.language.TRADE[1]:
            if (
                self.trade_building_list[self.trade_building_counter].name
                == self.game.language.BUILDINGS1[3]
            ):
                self.trade_transport_cost = HARBOR_TRANSPORT_COST * self.trade_quantity
                self.texts[8][0] = str(self.trade_transport_cost)
            if (
                self.trade_building_list[self.trade_building_counter].name
                == self.game.language.BUILDINGS1[4]
            ):
                self.trade_transport_cost = AIRPORT_TRANSPORT_COST * self.trade_quantity
                self.texts[8][0] = str(self.trade_transport_cost)
        else:
            self.trade_transport_cost = 0
            self.texts[8][0] = str(self.trade_transport_cost)
        self.update_trade_total_cost()

    def update_trade_goods_cost(self):
        if self.trade_goods < len(RES1_LIST):
            self.trade_goods_cost = (
                self.game.trade.resource_exchange_rate1[self.trade_goods]
                * self.trade_quantity
            )
            self.trade_goods_cost = round(self.trade_goods_cost, 2)
            self.texts[10][0] = str(self.trade_goods_cost)
        else:
            self.trade_goods_cost = (
                self.game.trade.resource_exchange_rate2[
                    (self.trade_goods - len(RES1_LIST))
                ]
                * self.trade_quantity
            )
            self.trade_goods_cost = round(self.trade_goods_cost, 2)
            self.texts[10][0] = str(self.trade_goods_cost)
        self.update_trade_total_cost()

    def update_trade_building_list(self):
        self.trade_building_list = []
        for a in self.game.buildings:
            if (
                a.name == self.game.language.BUILDINGS1[3]
                or a.name == self.game.language.BUILDINGS1[4]
            ):
                if a.owner == self.owner:
                    self.trade_building_list.append(a)
        self.trade_building = None
        self.trade_building_counter = None

    def buy_trade_goods(self):
        if self.texts[14][2] == DARKGREEN:
            self.owner.global_money -= self.trade_total_cost
            d = 0
            if self.trade_building.name == self.game.language.BUILDINGS1[3]:
                d = 30
            elif self.trade_building.name == self.game.language.BUILDINGS1[4]:
                d = 10
            self.game.event_list.add_event(
                [
                    self.game.idn + d,
                    "add_to_building",
                    self.trade_building,
                    self.trade_goods_name,
                    self.trade_quantity,
                ]
            )
        else:
            pass

    def show(self):
        self.texts[3][0] = self.game.language.TRADE[1]
        self.texts[4][0] = self.game.language.TRADE[1]

        self.update_trade_building_list()
        self.visible = True
        self.game.window_display = True

    def hide(self):
        self.visible = False
        self.game.window_display = False

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.texts[0][0] = "$ " + str(self.game.players[self.game.player.side].money)
        self.texts[1][0] = "$ " + str(
            self.game.players[self.game.player.side].global_money
        )
        self.texts[2][0] = str(self.game.players[self.game.player.side].exc_rt)


class OU_Button(Button):
    def __init__(
        self,
        unit,
        game,
        pos=[6, 6],
        size=(20, 20),
        color=LIGHTGREY,
        text="X",
        textsize=10,
        textcolor=BLACK,
    ):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.unit = unit
        self.window = self.unit.window
        self.pos = tuple(pos)
        self.abs_pos = [0, 0]
        self.abs_pos[0] = self.pos[0] + self.unit.pos[0]
        self.abs_pos[1] = self.pos[1] + self.unit.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.visible = True
        self.image = self.game.o_window_img.copy()
        self.image.set_colorkey(VIOLET)

        self.rect = self.image.get_rect()
        # self.rect.x =

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def click(self):
        self.unit.window.show()

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class OB_Button(Button):
    def __init__(
        self,
        building,
        game,
        pos=[6, 6],
        size=(20, 20),
        color=LIGHTGREY,
        text="X",
        textsize=10,
        textcolor=BLACK,
    ):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.building = building
        self.window = self.building.window
        self.pos = tuple(pos)
        # self.abs_pos = [0,0]
        # self.abs_pos[0] = self.pos[0] + self.building.pos[0]
        # self.abs_pos[1] = self.pos[1] + self.building.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.visible = True
        self.image = self.game.o_window_img.copy()
        self.image.set_colorkey(VIOLET)

        self.rect = self.image.get_rect()
        # self.rect.x =

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def click(self):
        self.building.window.show()

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class OT_Button(Button):
    def __init__(
        self,
        window,
        game,
        pos=[6, 6],
        size=(20, 20),
        color=DARKGREY,
        text="X",
        textsize=24,
        textcolor=LIGHTGREY,
    ):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = tuple(pos)
        # self.abs_pos = [0,0]
        # self.abs_pos[0] = self.pos[0] + self.building.pos[0]
        # self.abs_pos[1] = self.pos[1] + self.building.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.visible = True
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(
            self.image,
            self.color,
            (
                0 + BUTTON_BORDER_SIZE,
                0 + BUTTON_BORDER_SIZE,
                size[0] - BUTTON_BORDER_SIZE * 2 - 1,
                size[1] - BUTTON_BORDER_SIZE * 2 - 1,
            ),
        )
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            (5, 5),
        )
        self.rect = self.image.get_rect()

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def click(self):
        self.window.show()

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
