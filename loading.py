import pygame as pg
from settings import *
from languages import *
from sprites import *
from hexo import *
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
            textpos=(120, 10),
            border_size=3,
            display_text=[],
            visible=False,
        )
        self.info = Info_Window(
            self.game,
            size=(500, 500),
            text="Info Window",
            textpos=(120, 10),
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
        self.game.players[player].stability += gain
        if self.game.players[player].stability > 100:
            self.game.players[player].stability = 100
        elif self.game.players[player].stability < -100:
            self.game.players[player].stability = -100

    def strengthen_the_currency(self, player, value):
        self.game.players[player].exc_rt = self.game.players[player].exc_rt * value
        self.game.players[player].exc_rt = round(self.game.players[player].exc_rt, 4)

    def get_control_over_grids(self, player, grid_list, units):
        for grid in self.game.map.grids:    #[self.hexid].owner
            if grid.id in grid_list:
                #grid.owner = self.game.players[player]
                grid.owner = player
                self.game.map.new_owner(
                    player, roffset_from_cube(-1, grid.hex))
                if grid.building != None:
                    if grid.building == self.game.building:
                        self.game.deselect()
                    grid.building.change_owner(player) #self.game.players[player]
                    

        for unit in self.game.units:
            if units == "True" and unit.hexid in grid_list:
                if unit == self.game.uniting:
                    self.game.deselect()
                unit.change_owner(player)

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
        elif var[0] == "get_control_over_grids":
            self.get_control_over_grids(var[1], var[2], var[3])

    def open_decision_window(self):
        self.window.show()

    def dayli(self):
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
                elif c[1] == "get_control_over_grids":
                    print("Get control over grid")
                    self.get_control_over_grids(c[2], c[3], c[4])

                self.check = None
                self.dayli()
            else:
                print("none event")
                self.queue.put((self.check[0], self.check[1]))
        self.check = None


class Int_Politics(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.window = Int_Politics_Window(
            self.game,
            pos=[100, 100],
            text="Internal policy",
        )
    
    def update_window_value(self):
        self.window.update_politics()

    def dayli(self):
        #calculate of country global reputation
        for d in range(len(self.game.diplomacy.relations)):
            gr_change = 0
            not_in_war = True
            for r in self.game.diplomacy.relations[d]:
                #if r[2] == False that mean at war
                if r[2] == False:
                    gr_change -= 2
                    not_in_war = False
            #if not at single war
            if not_in_war == True:
                gr_change += 1

            self.game.players[d].reputation_change(gr_change)

        for p in self.game.players:
            pass

        for b in self.game.buildings:
            pass
        #tax_from_pop=0,
        #export=0,
        #import=0,
        #upkeep_of_buildings=0,
        #salary=0,
        #weekly_change=0


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
            for r in p:  # r is each players relation
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
            4,3,3,2,2,          #"Wood", "Food", "Cement", "Iron Ore", "Coal",
            5,1,10,10,5,        #"Steel", "Water", "Tools", "Parts", "Aluminum",
            2,3,2,3,1,          #"Oil":2, "Fuel":3, "Plastic":2, "Chemical Compounds", "Fertilizer",
            1,1,20,1,2,         #"Silicon":1, "Calcium":1, "Electronics":20, "Cotton":1, "Textiles",
            1,1,5,30,5,         #"Rubber":1, "Bauxite":1, "Furniture":5, "Civilian Machines":30, "Electronic Comp.":3
        ] 
        self.resource_exchange_rate2 = [
            4,3,3,2,4,          #"Supply","Uniforms","Fuel","Light_Ammo","Heavy_Ammo",
            30,8,40,100,200,    #"Rockets","Rifle","Artilleries","Truck","APC",
            300,500,1000,       #"Tank","Heli","Aircrafts",
        ]
        self.resource_base_rate1 = [
            4,3,3,2,2,          #"Wood", "Food", "Cement", "Iron Ore", "Coal",
            5,1,10,10,5,        #"Steel", "Water", "Tools", "Parts", "Aluminum",
            2,3,2,3,1,          #"Oil":2, "Fuel":3, "Plastic":2, "Chemical Compounds", "Fertilizer",
            1,1,20,1,2,         #"Silicon":1, "Calcium":1, "Electronics":20, "Cotton":1, "Textiles",
            1,1,5,30,5,         #"Rubber":1, "Bauxite":1, "Furniture":5, "Civilian Machines":30, "Electronic Comp.":3
        ]
        self.resource_base_rate2 = [
            4,3,3,2,4,          #"Supply","Uniforms","Fuel","Light_Ammo","Heavy_Ammo",
            30,8,40,100,200,    #"Rockets","Rifle","Artilleries","Truck","APC",
            300,500,1000,       #"Tank","Heli","Aircrafts",
        ]
        self.available_orders = []
        self.active_orders = []

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
        self.window = Trade_Window(
            self.game,
            self,
            text="Trade",
        )

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
        #delete order from list if they are outdated
        for o in self.available_orders:
            if o[4] <= self.game.idn:
                self.available_orders.remove(o)
        
        for a in self.active_orders:
            #if goods are in building
            if a[3].storage[a[0]] >= a[2]:
                a[3].storage[a[0]] -= a[2]
                self.game.players[self.game.player.side].global_money += a[1]
                self.game.players[self.game.player.side].reputation_change(TRADE_DONE_REP)
                t = []
                t.append(self.game.language.TRADE_ORDER[7] + str(a[2]) + " " + a[0])
                t.append("+$ " + str(a[1]))
                self.game.event_list.show_new_info(t)
                self.active_orders.remove(a)

            #if its too late
            if a[4] <= self.game.idn:
                self.game.players[self.game.player.side].reputation_change(TRADE_LOSE_REP)
                self.active_orders.remove(a)

        #changing goods price
        if 1 == 1:
            for a in range(len(self.resource_exchange_rate1)):
                c = self.window.variables
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
                c = self.window.variables
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
        #adding values to history records
        if 1 == 1:
            for c in range(len(self.resource_exchange_rate1)):
                self.price_history1[c].append(self.resource_exchange_rate1[c])
            for d in range(len(self.resource_exchange_rate2)):
                self.price_history2[d].append(self.resource_exchange_rate2[d])
            self.price_history_date.append(
                self.game.day
                + ((self.game.week - 1) * 7)
                + (self.game.season * 13)
                + ((self.game.year - 1980) * 364)
            )
        #updating trade window if open
        if self.window.visible == True:
            self.window.update_trade_quantity()
        #adding new production task to available orders
            #self.game.conv_idn_to_data(idn) converting day to date
        if 1 == 1:
            a = randint(1,8)
            #probability new task 4 / 8
            #if 1, 2 or 3 then civ resource
            #if 3 then military resource
            if a > 4:
                #which goods from resources 1
                b = randint(1,len(self.resource_base_rate1))
                #value of order
                c = 100 * randint(4,20)
                #quantity of goods
                d = (c * 0.9)  // self.resource_exchange_rate1[b-1]
                d -= 1
                d = int(d)
                #players building where need to be transported
                self.window.update_trade_building_list()
                e = choice(self.window.trade_building_list)
                #order fulfillment time
                f = self.game.idn + randint(7,14)
                self.available_orders.append([RES1_LIST[b-1].lower(), c, d, e, f])

            if a == 4:
                #which goods from resources 2
                b = randint(1,len(self.resource_base_rate2))
                #value of goods
                c = 1000 * randint(1,5)
                #quantity of goods
                d = (c * 0.9) // self.resource_exchange_rate2[b-1]
                d -= 1
                d = int(d)
                #players building where need to be transported
                self.window.update_trade_building_list()
                e = choice(self.window.trade_building_list)
                #order fulfillment time
                f = self.game.idn + randint(5,15)
                #adding task if quantity of order goods is more then 0
                if d > 0:
                    self.available_orders.append([RES2_LIST[b-1].lower(), c, d, e, f])

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
        self.id_num = 0
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
        pop_tax=4,
        build_tax=10,
        reserve=0,
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
        self.pop_tax = pop_tax
        self.build_tax = build_tax
        self.reserve = reserve
        self.relations = []
        self.electricity = False
        self.cities = 0
        self.villages = 0
        self.structures = 0
        self.population = 0
        self.citizens = 0
        self.soldiers = 0
        self.tax_from_pop = 0
        self.tax_from_buildings = 0
        self.export_goods = 0
        self.import_goods = 0
        self.upkeep_of_buildings = 0
        self.salary = 0
        self.weekly_change = 0

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
        self.tax_from_pop = 0
        self.tax_from_buildings = 0
        self.upkeep_of_buildings = 0
        self.salary = 0
        self.weekly_change = 0

        #taxation predictions
        for b in self.game.buildings:
            if b.owner.side == self.side:
                #civilain villages/cities taxations
                self.structures += 1
                if b.name == self.game.language.BUILDINGS1[2]:
                    self.cities += 1
                    self.population += b.population
                    if b.nationality == self.nation:
                        self.citizens += b.population
                    self.tax_from_pop += round(b.population * b.owner.pop_tax / 10, 2)
                elif b.name == self.game.language.BUILDINGS1[1]:
                    self.villages += 1
                    self.population += b.population
                    if b.nationality == self.nation:
                        self.citizens += b.population
                    self.tax_from_pop += round(b.population * b.owner.pop_tax / 10, 2)
                self.upkeep_of_buildings += b.upkeep
            else:
                if b.grid.owner == self.id_num:
                    self.tax_from_buildings += self.build_tax


        for u in self.game.units:
            u.calculate_cost()
            if u.owner.side == self.side:
                self.soldiers += u.men
                self.salary += u.weekly_cost

        self.weekly_change += self.tax_from_pop
        self.weekly_change += self.tax_from_buildings
        self.weekly_change += self.export_goods
        self.weekly_change -= self.import_goods
        self.weekly_change -= self.upkeep_of_buildings
        self.weekly_change -= self.salary
        self.weekly_change = round(self.weekly_change, 2)
    
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

                t = []
                t.append(self.name + " " + self.game.language.INFO_TEXTS[6])
                self.game.event_list.show_new_info(t)

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

                t = []
                t.append(self.name + " " + self.game.language.INFO_TEXTS[7])
                self.game.event_list.show_new_info(t)

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

                t = []
                t.append(self.name + " " + self.game.language.INFO_TEXTS[8])
                self.game.event_list.show_new_info(t)

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
                    t = []
                    t.append(self.name + " " + self.game.language.INFO_TEXTS[8])
                    self.game.event_list.show_new_info(t)

    def daily(self):
        if self.stability < 100:
            self.stability += 1
        self.recalculate_all()

    def hourly(self):
        self.electricity = False
        for a in self.game.buildings:
            if a.owner.name == self.name:
                if a.name == self.game.language.BUILDINGS1[11]:
                    if a.working == True:
                        self.electricity = True

    def weekly(self):
        self.export_goods=0
        self.import_goods=0
        self.recalculate_all()

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
        max_truck=0,
        max_apc=0,
        max_tank=0,
        max_heli=0,
        max_aircraft=0,
        max_rocket_truck=0,
        min_men=0,
        min_art=0,
        min_truck=0,
        min_apc=0,
        min_tank=0,
        min_heli=0,
        min_aircraft=0,
        min_rocket_truck=0,
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
        self.min_men = min_men

        self.equipment.append("supply")
        self.equipment.append("uniforms")
        self.equipment.append("rifle")
        self.equipment.append("light_ammo")

        self.max_art = max_art
        self.min_art = min_art
        if self.max_art > 0:
            self.equipment.append("artilleries")
            if not "heavy_ammo" in self.equipment:
                self.equipment.append("heavy_ammo")
        self.max_truck = max_truck
        self.min_truck = min_truck
        if self.max_truck > 0:
            self.equipment.append("truck")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
        self.max_apc = max_apc
        self.min_apc = min_apc
        if self.max_apc > 0:
            self.equipment.append("apc")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
            if not "light_ammo" in self.equipment:
                self.equipment.append("light_ammo")
        self.max_tank = max_tank
        self.min_tank = min_tank
        if self.max_tank > 0:
            self.equipment.append("tank")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
            if not "heavy_ammo" in self.equipment:
                self.equipment.append("heavy_ammo")
        self.max_heli = max_heli
        self.min_heli = min_heli
        if self.max_heli > 0:
            self.equipment.append("heli")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
            if not "heavy_ammo" in self.equipment:
                self.equipment.append("heavy_ammo")
        self.max_aircraft = max_aircraft
        self.min_aircraft = min_aircraft
        if self.max_aircraft > 0:
            self.equipment.append("aircraft")
            if not "fuel" in self.equipment:
                self.equipment.append("fuel")
            if not "heavy_ammo" in self.equipment:
                self.equipment.append("heavy_ammo")
        self.max_rocket_truck = max_rocket_truck
        self.min_rocket_truck = min_rocket_truck
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
            self.game.int_politics.window,
            self.game,
            pos=[WIDTH - MENU_RIGHT[0] - 200, HEIGHT - 45],
            size=(110, 30),
            text="Internal",
        )
        self.buttons.append(self.open_politics_button)

        
        self.open_trade_window = OT_Button(
            self.game.trade.window,
            self.game,
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
                FONT_MENU_SIZE,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 10, 35),
            ]
            self.time = [
                self.game.language.DISPLAY_GUI[1],
                FONT_MENU_SIZE,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 10, 55),
            ]
            self.data1 = ["Data", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 75)]
            self.data2 = ["Year", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 95)]
            self.terrain = [
                self.game.language.DISPLAY_GUI[6],
                FONT_MENU_SIZE,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 60, 120),
            ]
            self.terrain1 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 85, 140)]
            self.terrain2 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 85, 160)]
            self.terrain3 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 85, 180)]

            self.unit = [
                self.game.language.DISPLAY_GUI[7],
                FONT_MENU_SIZE,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 60, 210),
            ]
            self.unit1 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 30, 230)]
            self.unit2 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 30, 250)]
            self.unit3 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 270)]
            self.unit4 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 286)]
            self.unit5 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 310)]
            self.unit6 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 326)]
            self.unit7 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 350)]

            self.building = [
                self.game.language.DISPLAY_GUI[8],
                FONT_MENU_SIZE,
                LIGHTGREY,
                (WIDTH - MENU_RIGHT[0] + 60, 400),
            ]
            self.building1 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 40, 420)]
            self.building2 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 490)]
            self.building3 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 510)]
            self.building4 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 530)]
            self.building5 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 550)]
            self.building6 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 570)]
            self.building7 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 590)]
            self.building8 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 610)]
            self.building9 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 630)]
            self.building10 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 650)]
            self.building11 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 670)]
            self.building12 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 690)]
            self.building13 = ["", FONT_MENU_SIZE, LIGHTGREY, (WIDTH - MENU_RIGHT[0] + 10, 710)]

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
            self.tb_player_money = ["$ 0", FONT_MENU_SIZE, DARKGREEN, (340, 17)]
            self.tb_player_global_money = ["$ 0", FONT_MENU_SIZE, DARKGREEN, (490, 17)]

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
        self.tb_player_money[0] = "$ " + str(self.game.players[self.game.player.side].money)
        self.tb_player_global_money[0] = "$ " + str(self.game.players[self.game.player.side].global_money)


class Button(pg.sprite.Sprite):  # regular button
    def __init__(
        self,
        game,
        window,
        pos=[6, 6],
        size=(100, 30),
        color=DARKGREY,
        text="X",
        textsize=FONT_BUTTON_SIZE,
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


        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, self.size[0], self.size[1]))
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
            (5, 1),
        )
        self.rect = self.image.get_rect()



        '''
        self.image = self.game.button_1_img.copy()
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            (16, 4),
        )
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()
        '''

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
        textsize=FONT_BUTTON_SIZE,
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
            (4, 2),
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

class Mini_Function_Button(Button):
    def __init__(
        self,
        game,
        window,
        pos=[6, 6],
        color=DARKGREY,
        text="X",
        textsize=FONT_MINI_BUTTON_SIZE,
        textcolor=LIGHTGREY,
        function="function_name",
    ):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = pos
        self.size = (len(text) * 8 + 10, 15)
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
                0 + MINI_BUTTON_BORDER_SIZE,
                0 + MINI_BUTTON_BORDER_SIZE,
                self.size[0] - MINI_BUTTON_BORDER_SIZE * 2 - 1,
                self.size[1] - MINI_BUTTON_BORDER_SIZE * 2 - 1,
            ),
        )

        # self.image = self.game.button_1_img.copy()
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            (4, 0),
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
        textsize=FONT_OW_BUTTON_SIZE,
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
        self.text = text
        self.size = (len(self.text) * 6 + 35, 28)
        self.color = color
        self.textsize = textsize
        self.textcolor = textcolor
        self.visible = True

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
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            (4, 3),
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
        pos=[WIDTH - MENU_RIGHT[0] + 70, 425],
        size=(60, 30),
        color=DARKGREY,
        text="New",
        textsize=28,
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
        self.image.blit(
            pg.font.Font(FONT_NAME, self.textsize).render(
                self.text, False, self.textcolor
            ),
            (7, 1),
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
        textsize=FONT_MENU_TEXT_SIZE,
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
        textsize=FONT_MENU_TEXT_SIZE,
        textcolor=LIGHTGREY,
        textpos=(40, 10),
        border_size=3,
        display_text=[],
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
        self.all_texts = []
        self.which_text_display = 0

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
                pos=(350, 10),
                text=self.game.language.BASIC[4],
                function="prev_texts",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(430, 10),
                text=self.game.language.BASIC[5],
                function="next_texts",
            )
        )

        self.rect = self.image.get_rect()
        self.rectangle = pg.Surface(self.size)

    def function_list(self, function=None):
        if function == "next_texts":
            self.next_texts()
        elif function == "prev_texts":
            self.prev_texts()

    def next_texts(self):
        self.which_text_display += 1
        if self.which_text_display > len(self.all_texts) - 1:
            self.which_text_display = 0
        
        if len(self.all_texts) > 0:
            self.texts = self.all_texts[self.which_text_display]

    def prev_texts(self):
        self.which_text_display -= 1
        if self.which_text_display < 0:
            self.which_text_display = len(self.all_texts) - 1
            
        if len(self.all_texts) > 0:
            self.texts = self.all_texts[self.which_text_display]

    def new_text_to_display(self, display_text):
        #self.old_texts.pop()
        self.texts = []
        for a in range(len(display_text)):
            self.texts.append([display_text[a], 16, LIGHTGREY, (10, 45 + (a * 20))])
        self.all_texts.insert(0,self.texts)
        self.which_text_display = 0

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


class Int_Politics_Window(Window):
    def __init__(
        self,
        game,
        pos=[100, 100],
        size=(600, 500),
        color=DARKGREY,
        text="Text",
        textsize=FONT_MENU_TEXT_SIZE,
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
        self.texts.append([str(self.game.players[self.game.player.side].pop_tax), 16, LIGHTGREY, (190, 45)])
        self.texts.append([self.game.language.POLITICS[20], 16, LIGHTGREY, (10, 65)])
        self.texts.append([str(self.game.players[self.game.player.side].build_tax), 16, LIGHTGREY, (190, 65)])
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

        self.texts.append([self.game.language.POLITICS[13], 16, LIGHTGREY, (10, 285)])
        self.texts.append([str(self.game.players[self.game.player.side].tax_from_pop), 16, LIGHTGREY, (190, 285)])
        self.texts.append([self.game.language.POLITICS[21], 16, LIGHTGREY, (10, 305)])
        self.texts.append([str(self.game.players[self.game.player.side].tax_from_buildings), 16, LIGHTGREY, (190, 305)])
        self.texts.append([self.game.language.POLITICS[14], 16, LIGHTGREY, (10, 325)])
        self.texts.append([str(self.game.players[self.game.player.side].export_goods), 16, LIGHTGREY, (190, 325)])
        self.texts.append([self.game.language.POLITICS[15], 16, LIGHTGREY, (10, 345)])
        self.texts.append([str(self.game.players[self.game.player.side].import_goods), 16, LIGHTGREY, (190, 345)])
        self.texts.append([self.game.language.POLITICS[16], 16, LIGHTGREY, (10, 365)])
        self.texts.append([str(self.game.players[self.game.player.side].upkeep_of_buildings), 16, LIGHTGREY, (190, 365)])
        self.texts.append([self.game.language.POLITICS[17], 16, LIGHTGREY, (10, 385)])
        self.texts.append([str(self.game.players[self.game.player.side].salary), 16, LIGHTGREY, (190, 385)])
        self.texts.append([self.game.language.POLITICS[18], 16, LIGHTGREY, (10, 405)])
        self.texts.append([str(self.game.players[self.game.player.side].weekly_change), 16, LIGHTGREY, (190, 405)])


        # draw buttons
        self.buttons.append(CW_Button(self.game, self, pos=[10, 10]))
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(250, 45),
                text=self.game.language.POLITICS[9],
                function="tax_pop_dec",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(350, 45),
                text=self.game.language.POLITICS[10],
                function="tax_pop_inc",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(250, 65),
                text=self.game.language.POLITICS[9],
                function="tax_build_dec",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(350, 65),
                text=self.game.language.POLITICS[10],
                function="tax_build_inc",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(250, 245),
                text=self.game.language.POLITICS[12],
                function="conscription",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(500, 20),
                text=self.game.language.POLITICS[19],
                function="print_money",
            )
        )
        
        
        
        self.rect = self.image.get_rect()
        self.rectangle = pg.Surface(self.size)

    def function_list(self, function=None):
        if function == "tax_pop_dec":
            self.tax_pop_dec()
        elif function == "tax_pop_inc":
            self.tax_pop_inc()
        elif function == "tax_build_dec":
            self.tax_build_dec()
        elif function == "tax_build_inc":
            self.tax_build_inc()
        elif function == "conscription":
            self.conscription()
        elif function == "print_money":
            self.print_money()
        else:
            pass

    def tax_pop_dec(self):
        if self.game.players[self.game.player.side].pop_tax >= 1:
            self.game.players[self.game.player.side].pop_tax -= 1
        self.update_politics()

    def tax_pop_inc(self):
        self.game.players[self.game.player.side].pop_tax += 1
        self.game.players[self.game.player.side].stability -= 5
        self.update_politics()
    
    def tax_build_dec(self):
        if self.game.players[self.game.player.side].build_tax >= 1:
            self.game.players[self.game.player.side].build_tax -= 1
        self.update_politics()

    def tax_build_inc(self):
        self.game.players[self.game.player.side].build_tax += 1
        self.game.players[self.game.player.side].stability -= 1
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
                            b.loyalty -= CONSCRIPT_CITY_LOY

                if b.name == self.game.language.BUILDINGS1[1]:#VILLAGE
                    if b.nationality == self.game.players[self.game.player.side].nation:
                        if b.population > 40:
                            b.population -= CONSCRIPT_VILL_POP
                            self.game.players[self.game.player.side].reserve += CONSCRIPT_VILL_POP
                            b.loyalty -= CONSCRIPT_VILL_LOY
        self.update_politics()

    def print_money(self):
        self.game.players[self.game.player.side].money += 1000
        self.game.players[self.game.player.side].exc_rt += 1
        self.game.players[self.game.player.side].stability -= 5
        self.update_politics()

    def update_politics(self):
        self.game.players[self.game.player.side].recalculate_all()
        self.texts[1][0] = str(self.game.players[self.game.player.side].pop_tax)
        self.texts[3][0] = str(self.game.players[self.game.player.side].build_tax)
        self.texts[5][0] = str(self.game.players[self.game.player.side].stability)
        self.texts[7][0] = str(self.game.players[self.game.player.side].reputation)
        self.texts[9][0] = str(self.game.players[self.game.player.side].cities)
        self.texts[11][0] = str(self.game.players[self.game.player.side].villages)
        self.texts[13][0] = str(self.game.players[self.game.player.side].structures)
        self.texts[15][0] = str(self.game.players[self.game.player.side].population)
        self.texts[17][0] = str(self.game.players[self.game.player.side].citizens)
        self.texts[19][0] = str(self.game.players[self.game.player.side].soldiers)
        self.texts[21][0] = str(self.game.players[self.game.player.side].reserve)

        self.texts[23][0] = str(self.game.players[self.game.player.side].tax_from_pop)
        self.texts[25][0] = str(self.game.players[self.game.player.side].tax_from_buildings)
        self.texts[27][0] = str(self.game.players[self.game.player.side].export_goods)
        self.texts[29][0] = str(self.game.players[self.game.player.side].import_goods)
        self.texts[31][0] = str(self.game.players[self.game.player.side].upkeep_of_buildings)
        self.texts[33][0] = str(self.game.players[self.game.player.side].salary)
        self.texts[35][0] = str(self.game.players[self.game.player.side].weekly_change)
        if self.game.players[self.game.player.side].weekly_change >= 0:
            self.texts[35][2] = DARKGREEN
        else:
            self.texts[35][2] = DARKRED

        
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
        textsize=FONT_MENU_TEXT_SIZE,
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
            self.texts.append(["side", 16, LIGHTGREY, (55, 270 + (a * 20))])
            self.texts.append(["relations", 16, LIGHTGREY, (200, 270 + (a * 20))])
            self.texts.append(["peace", 16, LIGHTGREY, (270, 270 + (a * 20))])
            self.texts.append(["trade", 16, LIGHTGREY, (370, 270 + (a * 20))])
            self.texts.append(["ally", 16, LIGHTGREY, (450, 270 + (a * 20))])

        self.texts.append([self.game.language.DIPLOMACY[6], 16, LIGHTGREY, (200, 250)])
        self.texts.append([self.game.language.DIPLOMACY[7], 16, LIGHTGREY, (270, 250)])
        self.texts.append([self.game.language.DIPLOMACY[8], 16, LIGHTGREY, (370, 250)])
        self.texts.append([self.game.language.DIPLOMACY[9], 16, LIGHTGREY, (450, 250)])

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

    def next(self):
        self.check_number_of_players()
        self.status_player += 1
        if self.status_player >= self.number_of_players:
            self.status_player = 0
        self.texts[1][0] = self.game.players[self.status_player].name
        self.show_relations()
        self.update_dip_info()

    def peace(self):
        if self.status_player != self.game.player.side:
            if (
                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][2]
                == True
            ):
                t = []
                t.append(self.game.conv_idn_to_data(self.game.idn))
                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][2] = False
                t.append(self.game.language.INFO_TEXTS[4] + self.game.players[self.status_player].name)

                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][1] -= LOSE_RELATIONS_WAR
                t.append(self.game.language.INFO_TEXTS[5] + str(LOSE_RELATIONS_WAR))

                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][5] = self.game.idn

                self.game.diplomacy.relations[self.game.player.side][
                    self.status_player
                ][2] = False

                self.game.diplomacy.relations[self.game.player.side][
                    self.status_player
                ][1] -= LOSE_RELATIONS_WAR

                self.game.diplomacy.relations[self.game.player.side][
                    self.status_player
                ][1] -= self.game.idn

                self.game.players[self.game.player.side].reputation -= LOSE_REP_WAR
                self.game.int_politics.window.update_politics()
                self.trade()
                self.alliance()

                self.game.event_list.show_new_info(t)
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
                    self.game.players[self.game.player.side].reputation -= LOSE_REP_TRADE
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
                    self.game.players[self.game.player.side].reputation -= LOSE_REP_TRADE

    def alliance(self):
        if self.status_player != self.game.player.side:
            if (
                self.game.diplomacy.relations[self.status_player][
                    self.game.player.side
                ][2]
                == True #if countries are in peace
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
                    self.game.players[self.game.player.side].reputation -= LOSE_REP_ALLY
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
                    self.game.players[self.game.player.side].reputation -= LOSE_REP_ALLY

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
            self.image.blit(self.game.players[a].image, (20, 260 + (a * 20)))
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
        textsize=FONT_MENU_TEXT_SIZE,
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
        textsize=FONT_MENU_TEXT_SIZE,
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
        textsize=FONT_MENU_TEXT_SIZE,
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

        self.new_task_properties = [0, 0, [0, 0], ""]
        self.selected_goods = 0
        self.selected_order = 0

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
        if 1==1:
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
                    variable="repeat",
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
                    variable="building",
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
                    variable="engage",
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
                    variable="conquest",
                )
            )
            self.buttons.append(
                Function_Button(
                    self.game,
                    self,
                    pos=(20, 450),
                    text=self.game.language.DECISIONS[3],
                    function="give_bonus",
                )
            )
            self.buttons.append(
                Function_Button(
                    self.game,
                    self,
                    pos=(440, 300),
                    text=self.game.language.BASIC[4],
                    function="prev_order",
                )
            )
            self.buttons.append(
                Function_Button(
                    self.game,
                    self,
                    pos=(600, 300),
                    text=self.game.language.BASIC[5],
                    function="next_order",
                )
            )
            self.buttons.append(
                Function_Button(
                    self.game,
                    self,
                    pos=(520, 300),
                    text=self.game.language.BASIC[9],
                    function="adding_task",
                )
            )
            self.buttons.append(
                Function_Button(
                    self.game,
                    self,
                    pos=(600, 350),
                    text=self.game.language.BASIC[16],
                    function="delete_task",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(420, 360),
                    text=self.game.language.BASIC[4],
                    function="prev_task",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(470, 360),
                    text=self.game.language.BASIC[5],
                    function="next_task",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(420, 380),
                    text=self.game.language.BASIC[4],
                    function="task_line_1_prev",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(470, 380),
                    text=self.game.language.BASIC[5],
                    function="task_line_1_next",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(420, 400),
                    text=self.game.language.BASIC[4],
                    function="task_line_2_prev",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(470, 400),
                    text=self.game.language.BASIC[5],
                    function="task_line_2_next",
                )
            )
        
        # change company composition
        if 1==1:
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 40),
                    text=self.game.language.BASIC[17],
                    function="-max_men",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 40),
                    text=self.game.language.BASIC[18],
                    function="+max_men",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 60),
                    text=self.game.language.BASIC[17],
                    function="-max_supply",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 60),
                    text=self.game.language.BASIC[18],
                    function="+max_supply",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 80),
                    text=self.game.language.BASIC[17],
                    function="-max_uniforms",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 80),
                    text=self.game.language.BASIC[18],
                    function="+max_uniforms",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 100),
                    text=self.game.language.BASIC[17],
                    function="-max_fuel",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 100),
                    text=self.game.language.BASIC[18],
                    function="+max_fuel",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 140),
                    text=self.game.language.BASIC[17],
                    function="-max_light_ammo",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 140),
                    text=self.game.language.BASIC[18],
                    function="+max_light_ammo",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 160),
                    text=self.game.language.BASIC[17],
                    function="-max_heavy_ammo",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 160),
                    text=self.game.language.BASIC[18],
                    function="+max_heavy_ammo",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 180),
                    text=self.game.language.BASIC[17],
                    function="-max_rockets",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 180),
                    text=self.game.language.BASIC[18],
                    function="+max_rockets",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 220),
                    text=self.game.language.BASIC[17],
                    function="-max_rifle",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 220),
                    text=self.game.language.BASIC[18],
                    function="+max_rifle",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 240),
                    text=self.game.language.BASIC[17],
                    function="-max_artilleries",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 240),
                    text=self.game.language.BASIC[18],
                    function="+max_artilleries",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 260),
                    text=self.game.language.BASIC[17],
                    function="-max_truck",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 260),
                    text=self.game.language.BASIC[18],
                    function="+max_truck",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 280),
                    text=self.game.language.BASIC[17],
                    function="-max_apc",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 280),
                    text=self.game.language.BASIC[18],
                    function="+max_apc",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 300),
                    text=self.game.language.BASIC[17],
                    function="-max_tank",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 300),
                    text=self.game.language.BASIC[18],
                    function="+max_tank",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 320),
                    text=self.game.language.BASIC[17],
                    function="-max_heli",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 320),
                    text=self.game.language.BASIC[18],
                    function="+max_heli",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 340),
                    text=self.game.language.BASIC[17],
                    function="-max_aircraft",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 340),
                    text=self.game.language.BASIC[18],
                    function="+max_aircraft",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(110, 360),
                    text=self.game.language.BASIC[17],
                    function="-max_rocket_truck",
                )
            )
            self.buttons.append(
                Mini_Function_Button(
                    self.game,
                    self,
                    pos=(130, 360),
                    text=self.game.language.BASIC[18],
                    function="+max_rocket_truck",
                )
            )
        
        # draw eq names
        if 1==1:
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
        if 1==1:
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
                    self.game.language.DESCRIPTION[9], False, self.textcolor
                ),
                (580, 80),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.game.language.DESCRIPTION[8], False, self.textcolor
                ),
                (580, 100),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.game.language.DESCRIPTION[10], False, self.textcolor
                ),
                (580, 120),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.game.language.DESCRIPTION[11], False, self.textcolor
                ),
                (580, 140),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.game.language.GUI[11], False, self.textcolor
                ),
                (400, 60),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, self.textsize).render(
                    self.game.language.GUI[15], False, RED#self.textcolor
                ),
                (300, 220),
            )


        self.rect = self.image.get_rect()
        self.rectangle = pg.Surface(self.size)
        # self.rect.x = 600
        # self.rect.y = 600

    def function_list(self, function=None):
        # tasks
        # 0 go_to
        # 1 wait_time
        # 2 pick_up
        # 3 leave
        # 4 refill_eq
        # 5 refill_cr


        if function == "give_bonus":
            self.give_bonus()
        elif function == "prev_order":
            if len(self.thing.order_list) > 0:
                self.prev_order()
        elif function == "next_order":
            if len(self.thing.order_list) > 0:
                self.next_order()
        elif function == "adding_task":
            self.adding_task()
        elif function == "delete_task":
            if len(self.thing.order_list) > 0:
                self.delete_task()
        elif function == "prev_task":
            self.prev_task()
        elif function == "next_task":
            self.next_task()
        #task var line 1 button prev
        elif function == "task_line_1_prev":
            if self.new_task_properties[0] == 0:
                if self.game.multi_task == True:
                    self.new_pos(0, -10)
                else:
                    self.new_pos(0, -1)
            elif self.new_task_properties[0] == 1 or self.new_task_properties[0] == 4 or self.new_task_properties[0] == 5:
                if self.game.multi_task == True:
                    self.add_int(-4)
                else:
                    self.add_int(-1)
            elif self.new_task_properties[0] == 2 or self.new_task_properties[0] == 3:
                if self.game.multi_task == True:
                    self.prev_goods()
                    self.prev_goods()
                    self.prev_goods()
                else:
                    self.prev_goods()

        #task var line 1 button next
        elif function == "task_line_1_next":
            if self.new_task_properties[0] == 0:
                if self.game.multi_task == True:
                    self.new_pos(0, 10)
                else:
                    self.new_pos(0, 1)
            elif self.new_task_properties[0] == 1 or self.new_task_properties[0] == 4 or self.new_task_properties[0] == 5:
                if self.game.multi_task == True:
                    self.add_int(4)
                else:
                    self.add_int(1)
            elif self.new_task_properties[0] == 2 or self.new_task_properties[0] == 3:
                if self.game.multi_task == True:
                    self.next_goods()
                    self.next_goods()
                    self.next_goods()
                else:
                    self.next_goods()
        #task var line 2 button prev
        elif function == "task_line_2_prev":
            if self.new_task_properties[0] == 0:
                if self.game.multi_task == True:
                    self.new_pos(1, -10)
                else:
                    self.new_pos(1, -1)
            elif self.new_task_properties[0] == 1 or self.new_task_properties[0] == 4 or self.new_task_properties[0] == 5:
                if self.game.multi_task == True:
                    self.add_int(-48)
                else:
                    self.add_int(-12)
            elif self.new_task_properties[0] == 2 or self.new_task_properties[0] == 3:
                if self.game.multi_task == True:
                    self.new_task_properties[3] -= 25
                else:    
                    self.new_task_properties[3] -= 5
                if self.new_task_properties[3] < 0:
                    self.new_task_properties[3] = 0
        #task var line 2 button next
        elif function == "task_line_2_next":
            if self.new_task_properties[0] == 0:
                if self.game.multi_task == True:
                    self.new_pos(1, 5)
                else:
                    self.new_pos(1, 1)
            elif self.new_task_properties[0] == 1 or self.new_task_properties[0] == 4 or self.new_task_properties[0] == 5:
                if self.game.multi_task == True:
                    self.add_int(48)
                else:
                    self.add_int(12)
            elif self.new_task_properties[0] == 2 or self.new_task_properties[0] == 3:
                if self.game.multi_task == True:
                    self.new_task_properties[3] += 25
                else:    
                    self.new_task_properties[3] += 5
        #funciont with +
        elif function[0] == "+":
            if function[1:] == "max_men":
                print(self.thing.unit_typ.name)
                if self.game.multi_task == True:
                    self.thing.max_men += 5
                else:
                    self.thing.max_men += 1

                if self.thing.max_men > self.thing.unit_typ.max_men:
                    self.thing.max_men = self.thing.unit_typ.max_men
            if function[1:] == "max_supply":
                if self.game.multi_task == True:
                    self.thing.max_supply += 5
                else:
                    self.thing.max_supply += 1

                if self.thing.max_supply > self.thing.max_men * MEN_MAX_SUPPLY:
                    self.thing.max_supply = self.thing.max_men * MEN_MAX_SUPPLY
            if function[1:] == "max_uniforms":
                if self.game.multi_task == True:
                    self.thing.max_uniforms += 5
                else:
                    self.thing.max_uniforms += 1

                if self.thing.max_uniforms > self.thing.max_men * MAX_UNIFORMS:
                    self.thing.max_uniforms = self.thing.max_men * MAX_UNIFORMS
            if function[1:] == "max_fuel":
                if self.game.multi_task == True:
                    self.thing.max_fuel += 5
                else:
                    self.thing.max_fuel += 1

                if self.thing.max_fuel > (
                    (self.thing.truck * TRUCK_FUEL_CAP)
                    + (self.thing.apc * APC_FUEL_CAP)
                    + (self.thing.tank * TANK_FUEL_CAP)
                    + (self.thing.heli * HELI_FUEL_CAP)
                    + (self.thing.aircraft * AIRCRAFT_FUEL_CAP)
                    + (self.thing.rocket_truck * ROCKET_TRUCK_FUEL_CAP)
                ):
                    self.thing.max_fuel = (
                    (self.thing.truck * TRUCK_FUEL_CAP)
                    + (self.thing.apc * APC_FUEL_CAP)
                    + (self.thing.tank * TANK_FUEL_CAP)
                    + (self.thing.heli * HELI_FUEL_CAP)
                    + (self.thing.aircraft * AIRCRAFT_FUEL_CAP)
                    + (self.thing.rocket_truck * ROCKET_TRUCK_FUEL_CAP)
                )
            if function[1:] == "max_light_ammo":
                if self.game.multi_task == True:
                    self.thing.max_light_ammo += 5
                else:
                    self.thing.max_light_ammo += 1

                if self.thing.max_light_ammo > (
                    (self.thing.men * MAX_CARRY_LIGHT_AMMO_MEN)
                    + (self.thing.apc * MAX_CARRY_LIGHT_AMMO_APC)
                    + (self.thing.tank * MAX_CARRY_LIGHT_AMMO_TANK)
                    + (self.thing.heli * MAX_CARRY_LIGHT_AMMO_HELI)
                    + (self.thing.aircraft * MAX_CARRY_LIGHT_AMMO_AIRCRAFT)
                ):
                    self.thing.max_light_ammo = (
                    (self.thing.men * MAX_CARRY_LIGHT_AMMO_MEN)
                    + (self.thing.apc * MAX_CARRY_LIGHT_AMMO_APC)
                    + (self.thing.tank * MAX_CARRY_LIGHT_AMMO_TANK)
                    + (self.thing.heli * MAX_CARRY_LIGHT_AMMO_HELI)
                    + (self.thing.aircraft * MAX_CARRY_LIGHT_AMMO_AIRCRAFT)
                )
            if function[1:] == "max_heavy_ammo":
                if self.game.multi_task == True:
                    self.thing.max_heavy_ammo += 5
                else:
                    self.thing.max_heavy_ammo += 1

                if self.thing.max_heavy_ammo > (
                    (self.thing.men * MAX_CARRY_HEAVY_AMMO_MEN)
                    + (self.thing.apc * MAX_CARRY_HEAVY_AMMO_APC)
                    + (self.thing.tank * MAX_CARRY_HEAVY_AMMO_TANK)
                    + (self.thing.heli * MAX_CARRY_HEAVY_AMMO_HELI)
                    + (self.thing.aircraft * MAX_CARRY_HEAVY_AMMO_AIRCRAFT)
                ):
                    self.thing.max_heavy_ammo = (
                    (self.thing.men * MAX_CARRY_HEAVY_AMMO_MEN)
                    + (self.thing.apc * MAX_CARRY_HEAVY_AMMO_APC)
                    + (self.thing.tank * MAX_CARRY_HEAVY_AMMO_TANK)
                    + (self.thing.heli * MAX_CARRY_HEAVY_AMMO_HELI)
                    + (self.thing.aircraft * MAX_CARRY_HEAVY_AMMO_AIRCRAFT)
                )
            if function[1:] == "max_rockets":
                if self.game.multi_task == True:
                    self.thing.max_rockets += 5
                else:
                    self.thing.max_rockets += 1

                if self.thing.max_rockets > (
                    (self.thing.men * MAX_CARRY_ROCKETS_MEN)
                    + (self.thing.apc * MAX_CARRY_ROCKETS_APC)
                    + (self.thing.tank * MAX_CARRY_ROCKETS_TANK)
                    + (self.thing.heli * MAX_CARRY_ROCKETS_HELI)
                    + (self.thing.aircraft * MAX_CARRY_ROCKETS_AIRCRAFT)
                    + (self.thing.rocket_truck * MAX_CARRY_ROCKETS_ROCKET_TRUCK)
                ):
                    self.thing.max_rockets = (
                    (self.thing.men * MAX_CARRY_ROCKETS_MEN)
                    + (self.thing.apc * MAX_CARRY_ROCKETS_APC)
                    + (self.thing.tank * MAX_CARRY_ROCKETS_TANK)
                    + (self.thing.heli * MAX_CARRY_ROCKETS_HELI)
                    + (self.thing.aircraft * MAX_CARRY_ROCKETS_AIRCRAFT)
                    + (self.thing.rocket_truck * MAX_CARRY_ROCKETS_ROCKET_TRUCK)
                )
            if function[1:] == "max_rifle":
                if self.game.multi_task == True:
                    self.thing.max_rifle += 5
                else:
                    self.thing.max_rifle += 1

                if self.thing.max_rifle > self.thing.men:
                    self.thing.max_rifle = self.thing.men
            if function[1:] == "max_artilleries":
                if self.game.multi_task == True:
                    self.thing.max_artilleries += 5
                else:
                    self.thing.max_artilleries += 1

                if self.thing.max_artilleries > self.thing.unit_typ.max_art:
                    self.thing.max_artilleries = self.thing.unit_typ.max_art
            if function[1:] == "max_truck":
                if self.game.multi_task == True:
                    self.thing.max_truck += 5
                else:
                    self.thing.max_truck += 1

                if self.thing.max_truck > self.thing.unit_typ.max_truck:
                    self.thing.max_truck = self.thing.unit_typ.max_truck
            if function[1:] == "max_apc":
                if self.game.multi_task == True:
                    self.thing.max_apc += 5
                else:
                    self.thing.max_apc += 1

                if self.thing.max_apc > self.thing.unit_typ.max_apc:
                    self.thing.max_apc = self.thing.unit_typ.max_apc
            if function[1:] == "max_tank":
                if self.game.multi_task == True:
                    self.thing.max_tank += 5
                else:
                    self.thing.max_tank += 1

                if self.thing.max_tank > self.thing.unit_typ.max_tank:
                    self.thing.max_tank = self.thing.unit_typ.max_tank
            if function[1:] == "max_heli":
                if self.game.multi_task == True:
                    self.thing.max_heli += 5
                else:
                    self.thing.max_heli += 1

                if self.thing.max_heli > self.thing.unit_typ.max_heli:
                    self.thing.max_heli = self.thing.unit_typ.max_heli
            if function[1:] == "max_aircraft":
                if self.game.multi_task == True:
                    self.thing.max_aircraft += 5
                else:
                    self.thing.max_aircraft += 1

                if self.thing.max_aircraft > self.thing.unit_typ.max_aircraft:
                    self.thing.max_aircraft = self.thing.unit_typ.max_aircraft
            if function[1:] == "max_rocket_truck":
                if self.game.multi_task == True:
                    self.thing.max_rocket_truck += 5
                else:
                    self.thing.max_rocket_truck += 1

                if self.thing.max_rocket_truck > self.thing.unit_typ.max_rocket_truck:
                    self.thing.max_rocket_truck = self.thing.unit_typ.max_rocket_truck
     
        #function with -
        elif function[0] == "-":
            if function[1:] == "max_men":
                if self.game.multi_task == True:
                    self.thing.max_men -= 5
                else:
                    self.thing.max_men -= 1
                    
                if self.thing.max_men < self.thing.unit_typ.min_men:
                    self.thing.max_men = self.thing.unit_typ.min_men   
            if function[1:] == "max_supply":
                if self.game.multi_task == True:
                    self.thing.max_supply -= 5
                else:
                    self.thing.max_supply -= 1
                    
                if self.thing.max_supply < self.thing.max_men:
                    self.thing.max_supply = self.thing.max_men
            if function[1:] == "max_uniforms":
                if self.game.multi_task == True:
                    self.thing.max_uniforms -= 5
                else:
                    self.thing.max_uniforms -= 1
                    
                if self.thing.max_uniforms < self.thing.men:
                    self.thing.max_uniforms = self.thing.men
            if function[1:] == "max_fuel":
                if self.game.multi_task == True:
                    self.thing.max_fuel -= 5
                else:
                    self.thing.max_fuel -= 1
                    
                if self.thing.max_fuel < 0:
                    self.thing.max_fuel = 0
            if function[1:] == "max_light_ammo":
                if self.game.multi_task == True:
                    self.thing.max_light_ammo -= 5
                else:
                    self.thing.max_light_ammo -= 1
                    
                if self.thing.max_light_ammo < 0:
                    self.thing.max_light_ammo = 0
            if function[1:] == "max_heavy_ammo":
                if self.game.multi_task == True:
                    self.thing.max_heavy_ammo -= 5
                else:
                    self.thing.max_heavy_ammo -= 1
                    
                if self.thing.max_heavy_ammo < 0:
                    self.thing.max_heavy_ammo = 0
            if function[1:] == "max_rockets":
                if self.game.multi_task == True:
                    self.thing.max_rockets -= 5
                else:
                    self.thing.max_rockets -= 1
                    
                if self.thing.max_rockets < 0:
                    self.thing.max_rockets = 0
            if function[1:] == "max_rifle":
                if self.game.multi_task == True:
                    self.thing.max_rifle -= 5
                else:
                    self.thing.max_rifle -= 1
                    
                if self.thing.max_rifle < 0:
                    self.thing.max_rifle = 0
            if function[1:] == "max_artilleries":
                if self.game.multi_task == True:
                    self.thing.max_artilleries -= 5
                else:
                    self.thing.max_artilleries -= 1
                    
                if self.thing.max_artilleries < self.thing.unit_typ.min_art:
                    self.thing.max_artilleries = self.thing.unit_typ.min_art
            if function[1:] == "max_truck":
                if self.game.multi_task == True:
                    self.thing.max_truck -= 5
                else:
                    self.thing.max_truck -= 1
                    
                if self.thing.max_truck < self.thing.unit_typ.min_truck:
                    self.thing.max_truck = self.thing.unit_typ.min_truck
            if function[1:] == "max_apc":
                if self.game.multi_task == True:
                    self.thing.max_apc -= 5
                else:
                    self.thing.max_apc -= 1
                    
                if self.thing.max_apc < self.thing.unit_typ.min_apc:
                    self.thing.max_apc = self.thing.unit_typ.min_apc
            if function[1:] == "max_tank":
                if self.game.multi_task == True:
                    self.thing.max_tank -= 5
                else:
                    self.thing.max_tank -= 1
                    
                if self.thing.max_tank < self.thing.unit_typ.min_tank:
                    self.thing.max_tank = self.thing.unit_typ.min_tank
            if function[1:] == "max_heli":
                if self.game.multi_task == True:
                    self.thing.max_heli -= 5
                else:
                    self.thing.max_heli -= 1
                    
                if self.thing.max_heli < self.thing.unit_typ.min_heli:
                    self.thing.max_heli = self.thing.unit_typ.min_heli
            if function[1:] == "max_aircraft":
                if self.game.multi_task == True:
                    self.thing.max_aircraft -= 5
                else:
                    self.thing.max_aircraft -= 1
                    
                if self.thing.max_aircraft < self.thing.unit_typ.min_aircraft:
                    self.thing.max_aircraft = self.thing.unit_typ.min_aircraft
            if function[1:] == "max_rocket_truck":
                if self.game.multi_task == True:
                    self.thing.max_rocket_truck -= 5
                else:
                    self.thing.max_rocket_truck -= 1
                    
                if self.thing.max_rocket_truck < self.thing.unit_typ.min_rocket_truck:
                    self.thing.max_rocket_truck = self.thing.unit_typ.min_rocket_truck
        else:
            pass


    def give_bonus(self):
        if self.thing.owner.money > self.thing.men:
            self.thing.owner.money -= self.thing.men
            self.thing.loyalty += 5


    def prev_order(self):
        self.selected_order -= 1
        if self.selected_order < 0:
            self.selected_order = len(self.thing.order_list)
        task = self.thing.order_list[self.selected_order - 1]
        if self.selected_order == 0:
            #new task
            self.new_task_properties = [0, 0, [0, 0], ""]
        else:
            if task[0] == "go_to":
                self.new_task_properties = [0, 0, [task[1][0], task[1][1]], ""]
            elif task[0] == "wait_time":
                self.new_task_properties = [1, 0, task[1][0], ""]
            elif task[0] == "pick_up":
                self.selected_goods = self.int_of_goods(task[1][0])
                self.new_task_properties = [2, 0, self.name_of_goods(), task[1][1]]
            elif task[0] == "leave":
                self.selected_goods = self.int_of_goods(task[1][0])
                self.new_task_properties = [3, 0, self.name_of_goods(), task[1][1]]
            elif task[0] == "refill_eq":
                self.new_task_properties = [4, 0, task[1][0], ""]
            elif task[0] == "refill_cr":
                self.new_task_properties = [5, 0, task[1][0], ""]
            elif task[0] == "reorganize":
                self.new_task_properties = [6, 0, task[1][0], ""]


    def next_order(self):
        self.selected_order += 1
        if self.selected_order > len(self.thing.order_list):
            self.selected_order = 0
        task = self.thing.order_list[self.selected_order - 1]
        if self.selected_order == 0:
            pass
        if self.selected_order == 0:
            #new task
            self.new_task_properties = [0, 0, [0, 0], ""]
        else:
            if task[0] == "go_to":
                self.new_task_properties = [0, 0, [task[1][0], task[1][1]], ""]
            elif task[0] == "wait_time":
                self.new_task_properties = [1, 0, task[1][0], ""]
            elif task[0] == "pick_up":
                self.selected_goods = self.int_of_goods(task[1][0])
                self.new_task_properties = [2, 0, self.name_of_goods(), task[1][1]]
            elif task[0] == "leave":
                self.selected_goods = self.int_of_goods(task[1][0])
                self.new_task_properties = [3, 0, self.name_of_goods(), task[1][1]]
            elif task[0] == "refill_eq":
                self.new_task_properties = [4, 0, task[1][0], ""]
            elif task[0] == "refill_cr":
                self.new_task_properties = [5, 0, task[1][0], ""]
            elif task[0] == "reorganize":
                self.new_task_properties = [6, 0, task[1][0], ""]


    def adding_task(self):
        if self.selected_order > len(self.thing.order_list):
            print("Problem, order larger then lenght of order list.")
            self.reset_task()
        else:
            if self.selected_order == 0:
                if self.new_task_properties[0] == 0:   #0 == go_to
                    self.thing.order_list.append(["go_to", OffsetCoord(self.new_task_properties[2][0], self.new_task_properties[2][1])])
                elif self.new_task_properties[0] == 1: #1 == wait
                    self.thing.order_list.append(["wait_time", [self.new_task_properties[2], ""]])
                elif self.new_task_properties[0] == 2: #2 == pick up goods
                    self.thing.order_list.append(["pick_up", [self.new_task_properties[2], self.new_task_properties[3]]])
                elif self.new_task_properties[0] == 3: #3 == leave goods
                    self.thing.order_list.append(["leave", [self.new_task_properties[2], self.new_task_properties[3]]])
                elif self.new_task_properties[0] == 4: #4 == refill equpment
                    self.thing.order_list.append(["refill_eq", [self.new_task_properties[2], ""]])
                elif self.new_task_properties[0] == 5: #5 == refill crew
                    self.thing.order_list.append(["refill_cr", [self.new_task_properties[2], ""]])
                elif self.new_task_properties[0] == 6: #6 == reorganize
                    self.thing.order_list.append(["reorganize", ["", ""]])
                else:
                    pass
            else:
                if self.selected_order == 1:
                    self.thing.stop()
                if self.new_task_properties[0] == 0:   #0 == go_to
                    self.thing.order_list[self.selected_order - 1] = ["go_to", OffsetCoord(self.new_task_properties[2][0], self.new_task_properties[2][1])]
                elif self.new_task_properties[0] == 1: #1 == wait
                    self.thing.order_list[self.selected_order - 1] = ["wait_time", [self.new_task_properties[2], ""]]
                elif self.new_task_properties[0] == 2: #2 == pick up goods
                    self.thing.order_list[self.selected_order - 1] = ["pick_up", [self.new_task_properties[2], self.new_task_properties[3]]]
                elif self.new_task_properties[0] == 3: #3 == leave goods
                    self.thing.order_list[self.selected_order - 1] = ["leave", [self.new_task_properties[2], self.new_task_properties[3]]]
                elif self.new_task_properties[0] == 4: #4 == refill equipment
                    self.thing.order_list[self.selected_order - 1] = ["refill_eq", [self.new_task_properties[2], ""]]
                elif self.new_task_properties[0] == 5: #5 == refill crew
                    self.thing.order_list[self.selected_order - 1] = ["refill_cr", [self.new_task_properties[2], ""]]
                elif self.new_task_properties[0] == 6: #6 == reorganize crew
                    self.thing.order_list[self.selected_order - 1] = ["reorganize", ["", ""]]
                
                else:
                    pass


    def delete_task(self):
        if self.selected_order == 1:
            self.thing.stop()
        if self.selected_order > len(self.thing.order_list) or self.selected_order == 0:
            print("Problem, order larger then lenght of order list")
            print("or selected is new order.")
            self.reset_task()
        else:
            self.thing.order_list.pop(self.selected_order - 1)
            self.reset_task()


    def new_pos(self, axis, val):
        self.new_task_properties[2][axis] += val


    def add_int(self, time):
        self.new_task_properties[2] += time
        if self.new_task_properties[2] < 0:
            self.new_task_properties[2] = 0
    

    def prev_goods(self):
        self.selected_goods -= 1
        if self.selected_goods < 0:
            self.selected_goods = int(len(RES1_LIST) + len(RES2_LIST) - 1)
        self.new_task_properties[2] = self.name_of_goods()


    def next_goods(self):
        self.selected_goods += 1
        if self.selected_goods >= (len(RES1_LIST) + len(RES2_LIST)):
            self.selected_goods = 0
        self.new_task_properties[2] = self.name_of_goods()


    def name_of_goods(self):
        if self.selected_goods < len(RES1_LIST):
            return RES1_LIST[self.selected_goods].lower()
        else:
            return RES2_LIST[self.selected_goods - len(RES1_LIST)].lower()


    def int_of_goods(self, name):
        i = 0
        rrr = None
        for r in RES1_LIST:
            rr = r.lower()
            if name == rr:
                rrr = i
                return rrr
            i += 1
        for r in RES2_LIST:
            rr = r.lower()
            if name == rr:
                rrr = i
                return rrr
            i += 1
        

    def prev_task(self):
        self.new_task_properties[0] -= 1
        if self.new_task_properties[0] < 0:
            self.new_task_properties[0] = len(self.game.language.NEW_TASKS) - 1

        if self.new_task_properties[0] == 0:
            self.new_task_properties = [0, 0, [self.thing.col, self.thing.row], ""]
        elif self.new_task_properties[0] == 1:
            self.new_task_properties = [1, 0, 0, ""]
        elif self.new_task_properties[0] == 2:
            self.new_task_properties = [2, 0, self.name_of_goods(), 0]
        elif self.new_task_properties[0] == 3:
            self.new_task_properties = [3, 0, self.name_of_goods(), 0]
        elif self.new_task_properties[0] == 4:
            self.new_task_properties = [4, 0, 0, ""]
        elif self.new_task_properties[0] == 5:
            self.new_task_properties = [5, 0, 0, ""]
        elif self.new_task_properties[0] == 6:
            self.new_task_properties = [6, 0, "", ""]
        

    def next_task(self):
        self.new_task_properties[0] += 1
        if self.new_task_properties[0] >= len(self.game.language.NEW_TASKS):
            self.new_task_properties[0] = 0

        if self.new_task_properties[0] == 0:
            self.new_task_properties = [0, 0, [self.thing.col, self.thing.row], ""]
        elif self.new_task_properties[0] == 1:
            self.new_task_properties = [1, 0, 0, ""]
        elif self.new_task_properties[0] == 2:
            self.new_task_properties = [2, 0, self.name_of_goods(), 0]
        elif self.new_task_properties[0] == 3:
            self.new_task_properties = [3, 0, self.name_of_goods(), 0]
        elif self.new_task_properties[0] == 4:
            self.new_task_properties = [4, 0, 0, ""]
        elif self.new_task_properties[0] == 5:
            self.new_task_properties = [5, 0, 0, ""]
        elif self.new_task_properties[0] == 6:
            self.new_task_properties = [6, 0, "", ""]

    def recalc_new_task(self):
        pass

    def reset_task(self):
        self.new_task_properties = [0, 0, [0, 0], ""]
        self.selected_goods = 0
        self.selected_order = 0

    def show(self):
        self.thing.calculate_cost()
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
        textsize=FONT_WINDOW_SIZE,
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
        elif function == "grant_money":
            self.grant_money()
        elif function == "calling_up":
            self.calling_up()
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

    def grant_money(self):
        if self.thing.owner.money > self.thing.population:
            self.thing.owner.money -= self.thing.population
            self.thing.loyalty += 5

    def calling_up(self):
        if self.thing.nationality == self.thing.owner.nation:
            if self.thing.population >= 25 and self.thing.loyalty >= 30:
                self.thing.population -= 25
                self.thing.loyalty -= 10

                self.game.adding_unit(self.thing.x, self.thing.y, 
                    self.thing.loyalty, 
                    self.thing.nationality.id_num,
                    self.thing.owner.id_num, 15, "Volunteers", 25)
                    


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
        textsize=FONT_MENU_TEXT_SIZE,
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
        self.trade_goods_name = "wood"
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
        self.selected_trade_contract = None
        self.selected_trade_building = None
        self.num_ava_ord = len(self.thing.available_orders)
        self.active_trade_contract = None
        self.num_active_ord = len(self.thing.active_orders)


        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(710, 210),
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
            Mini_Function_Button(
                self.game,
                self,
                pos=(170, 400),
                text=self.game.language.BASIC[4],
                function="prev_trade_building",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(220, 400),
                text=self.game.language.BASIC[5],
                function="next_trade_building",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(170, 460),
                text=self.game.language.BASIC[4],
                function="prev_trade_goods",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(220, 460),
                text=self.game.language.BASIC[5],
                function="next_trade_goods",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(170, 500),
                text=self.game.language.TRADE[4],
                function="quantity-10",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(220, 500),
                text=self.game.language.TRADE[5],
                function="quantity-1",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(260, 500),
                text=self.game.language.TRADE[6],
                function="quantity+1",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(300, 500),
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
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(540, 400),
                text=self.game.language.BASIC[4],
                function="prev_ava_order",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(590, 400),
                text=self.game.language.BASIC[5],
                function="next_ava_order",
            )
        )
        self.buttons.append(
            Function_Button(
                self.game,
                self,
                pos=(640, 400),
                text=self.game.language.BASIC[9],
                function="accept_trade_offer",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(540, 520),
                text=self.game.language.BASIC[4],
                function="prev_active_order",
            )
        )
        self.buttons.append(
            Mini_Function_Button(
                self.game,
                self,
                pos=(590, 520),
                text=self.game.language.BASIC[5],
                function="next_active_order",
            )
        )
        


        #draw window
        if 1 == 1:
            
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
                pg.font.Font(FONT_NAME, FONT_WINDOW_SIZE).render(
                    self.text, False, self.textcolor
                ),
                self.textpos,
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, FONT_WINDOW_SIZE).render(
                    self.game.language.BASIC[10], False, self.textcolor
                ),
                (500, 20),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, FONT_WINDOW_SIZE).render(
                    self.game.language.TRADE[0], False, self.textcolor
                ),
                (30, 400),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, FONT_WINDOW_SIZE).render(
                    self.game.language.TRADE[2], False, self.textcolor
                ),
                (30, 460),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, FONT_WINDOW_SIZE).render(
                    self.game.language.TRADE[3], False, self.textcolor
                ),
                (30, 500),
            )
            self.image.blit(
                pg.font.Font(FONT_NAME, FONT_WINDOW_SIZE).render(
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
                    pg.font.Font(FONT_NAME, FONT_WINDOW_SIZE).render(
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
                    pg.font.Font(FONT_NAME, FONT_WINDOW_SIZE).render(
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

        #draw texts in window
        if 1 == 1:
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
            self.texts.append([self.game.language.TRADE[12], 16, LIGHTGREY, (200, 600)])
            self.texts.append([self.game.language.TRADE[1], 16, LIGHTGREY, (200, 620)])

            #draw available trade offers
            self.texts.append([self.game.language.TRADE_ORDER[0], 16, LIGHTGREY, (350, 400)])
            self.texts.append([str(self.num_ava_ord), 16, LIGHTGREY, (520, 400)])
            self.texts.append([self.game.language.TRADE_ORDER[1], 16, LIGHTGREY, (350, 420)])
            self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (500, 420)])
            self.texts.append([self.game.language.TRADE_ORDER[2], 16, LIGHTGREY, (350, 440)])
            self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (500, 440)])
            self.texts.append([self.game.language.TRADE_ORDER[3], 16, LIGHTGREY, (350, 460)])
            self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (500, 460)])
            self.texts.append([self.game.language.TRADE_ORDER[4], 16, LIGHTGREY, (350, 480)])
            self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (500, 480)])
            self.texts.append([self.game.language.TRADE_ORDER[5], 16, LIGHTGREY, (350, 500)])
            self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (500, 500)])

            #draw active trade offers
            self.texts.append([self.game.language.TRADE_ORDER[6], 16, LIGHTGREY, (350, 520)])
            self.texts.append([str(self.num_ava_ord), 16, LIGHTGREY, (520, 520)])
            self.texts.append([self.game.language.TRADE_ORDER[1], 16, LIGHTGREY, (350, 540)])
            self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (500, 540)])
            self.texts.append([self.game.language.TRADE_ORDER[2], 16, LIGHTGREY, (350, 560)])
            self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (500, 560)])
            self.texts.append([self.game.language.TRADE_ORDER[3], 16, LIGHTGREY, (350, 580)])
            self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (500, 580)])
            self.texts.append([self.game.language.TRADE_ORDER[4], 16, LIGHTGREY, (350, 600)])
            self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (500, 600)])
            self.texts.append([self.game.language.TRADE_ORDER[5], 16, LIGHTGREY, (350, 620)])
            self.texts.append([self.game.language.BASIC[12], 16, LIGHTGREY, (500, 620)])



        b = 0
        c = 0
        for a in self.thing.resource_exchange_rate1:
            self.variables.append(
                [a, 16, self.thing.rating(randint(1, 3)), (20 + c, 60 + (b * 20))]
            )

            b += 1
            if b > 8:
                c += 270
                b = 0
        b = 0
        c = 0
        for a in self.thing.resource_exchange_rate2:
            self.variables.append(
                [a, 16, self.thing.rating(randint(1, 3)), (20 + c, 280 + (b * 20))]
            )
            # self.thing.rating(randint(1,3))
            b += 1
            if b > 4:
                c += 270
                b = 0

    def dayli(self):
        self.update_trade_offers()

    def function_list(self, function=None):
        if function == "show_graph":
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
        elif function == "next_ava_order":
            self.next_ava_order()
        elif function == "prev_ava_order":
            self.prev_ava_order()
        elif function == "accept_trade_offer":
            self.accept_trade_offer()
        elif function == "prev_active_order":
            self.prev_active_order()
        elif function == "next_active_order":
            self.next_active_order()
        else:
            pass

    def show_graph(self):
        self.thing.show_graph(which=0)

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
            self.trade_transport_cost = HARBOR_TRANSPORT_COST
            self.texts[8][0] = str(self.trade_transport_cost)
        if (
            self.trade_building_list[self.trade_building_counter].name
            == self.game.language.BUILDINGS1[4]
        ):
            self.trade_transport_cost = AIRPORT_TRANSPORT_COST
            self.texts[8][0] = str(self.trade_transport_cost)
        self.trade_building = self.trade_building_list[self.trade_building_counter]
        self.update_trade_transport_cost()

    def update_trade_transport_cost(self):
        if self.texts[3][0] != self.game.language.TRADE[1]:
            if (
                self.trade_building_list[self.trade_building_counter].name
                == self.game.language.BUILDINGS1[3]
            ):
                self.trade_transport_cost = HARBOR_TRANSPORT_COST
                self.texts[8][0] = str(self.trade_transport_cost)
            if (
                self.trade_building_list[self.trade_building_counter].name
                == self.game.language.BUILDINGS1[4]
            ):
                self.trade_transport_cost = AIRPORT_TRANSPORT_COST
                self.texts[8][0] = str(self.trade_transport_cost)
        else:
            self.trade_transport_cost = 0
            self.texts[8][0] = str(self.trade_transport_cost)
        self.update_trade_total_cost()

    def update_trade_goods_cost(self):
        if self.trade_goods < len(RES1_LIST):
            self.trade_goods_cost = (
                self.thing.resource_exchange_rate1[self.trade_goods]
                * self.trade_quantity
            )
            self.trade_goods_cost = round(self.trade_goods_cost, 2)
            self.texts[10][0] = str(self.trade_goods_cost)
        else:
            self.trade_goods_cost = (
                self.thing.resource_exchange_rate2[
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
        

    def buy_trade_goods(self):
        #if check text color is darkgreen / you have more money
        if self.texts[14][2] == DARKGREEN:
            self.owner.global_money -= self.trade_total_cost
            d = 0
            #checking shipping time
            if self.trade_building.name == self.game.language.BUILDINGS1[3]:
                d = HARBOR_SHIPING_TIME
            elif self.trade_building.name == self.game.language.BUILDINGS1[4]:
                d = AIRPORT_SHIPING_TIME
            #adding 
            self.game.event_list.add_event(
                [
                    self.game.idn + d,
                    "add_to_building",
                    self.trade_building,
                    self.trade_goods_name,
                    self.trade_quantity,
                ]
            )
            self.owner.import_goods += self.trade_total_cost
            self.game.int_politics.window.update_politics()
            t = []
            t.append(self.game.language.INFO_TEXTS[0] + self.trade_goods_name)
            t.append(self.game.language.INFO_TEXTS[1] + str(self.trade_quantity))
            t.append(self.game.language.INFO_TEXTS[2] + self.trade_building.name + 
            ": " + str(self.trade_building.x) + "/" + str(self.trade_building.y))
            t.append(self.game.language.INFO_TEXTS[3] + str(d))

            self.game.event_list.show_new_info(t)
        else:
            pass

    def update_trade_offers(self):
        self.num_ava_ord = len(self.thing.available_orders)
        self.texts[16][0] = str(self.num_ava_ord)
        self.num_active_ord = len(self.thing.active_orders)
        self.texts[28][0] = str(self.num_active_ord)

    def prev_ava_order(self):
        self.update_trade_offers()
        if self.num_ava_ord > 0:
            if self.selected_trade_contract == None:
                self.selected_trade_contract = 0
            self.selected_trade_contract -= 1
            if self.selected_trade_contract < 0:
                self.selected_trade_contract = self.num_ava_ord - 1
            b = self.thing.available_orders[self.selected_trade_contract]
            self.selected_trade_building = b[3]
            self.texts[18][0] = str(b[0])
            self.texts[20][0] = str(b[1])
            self.texts[22][0] = str(b[2])
            self.texts[24][0] = str(self.selected_trade_building.name) + ": " + str(self.selected_trade_building.x) + "/" + str(self.selected_trade_building.y)
            self.texts[26][0] = self.game.conv_idn_to_data(b[4])
        else:
            self.selected_trade_contract = None
            self.selected_trade_building = None
            self.texts[18][0] = self.game.language.BASIC[12]
            self.texts[20][0] = self.game.language.BASIC[12]
            self.texts[22][0] = self.game.language.BASIC[12]
            self.texts[24][0] = self.game.language.BASIC[12]
            self.texts[26][0] = self.game.language.BASIC[12]

    def next_ava_order(self):
        self.update_trade_offers()
        if self.num_ava_ord > 0:
            if self.selected_trade_contract == None:
                self.selected_trade_contract = 0
            self.selected_trade_contract += 1
            if self.selected_trade_contract > self.num_ava_ord - 1:
                self.selected_trade_contract = 0
            b = self.thing.available_orders[self.selected_trade_contract]
            self.selected_trade_building = b[3]
            self.texts[18][0] = str(b[0])
            self.texts[20][0] = str(b[1])
            self.texts[22][0] = str(b[2])
            self.texts[24][0] = str(self.selected_trade_building.name) + ": " + str(self.selected_trade_building.x) + "/" + str(self.selected_trade_building.y)
            self.texts[26][0] = self.game.conv_idn_to_data(b[4])
        else:
            self.selected_trade_contract = None
            self.selected_trade_building = None
            self.texts[18][0] = self.game.language.BASIC[12]
            self.texts[20][0] = self.game.language.BASIC[12]
            self.texts[22][0] = self.game.language.BASIC[12]
            self.texts[24][0] = self.game.language.BASIC[12]
            self.texts[26][0] = self.game.language.BASIC[12]

    def prev_active_order(self):
        self.update_trade_offers()
        if self.num_active_ord > 0:
            if self.active_trade_contract == None:
                self.active_trade_contract = 0
            self.active_trade_contract -= 1
            if self.active_trade_contract < 0:
                self.active_trade_contract = self.num_active_ord - 1
            b = self.thing.active_orders[self.active_trade_contract]
            self.texts[30][0] = str(b[0])
            self.texts[32][0] = str(b[1])
            self.texts[34][0] = str(b[2])
            self.texts[36][0] = str(b[3].name) + ": " + str(b[3].x) + "/" + str(b[3].y)
            self.texts[38][0] = self.game.conv_idn_to_data(b[4])
        else:
            self.active_trade_contract = None
            self.texts[30][0] = self.game.language.BASIC[12]
            self.texts[32][0] = self.game.language.BASIC[12]
            self.texts[34][0] = self.game.language.BASIC[12]
            self.texts[36][0] = self.game.language.BASIC[12]
            self.texts[38][0] = self.game.language.BASIC[12]

    def next_active_order(self):
        self.update_trade_offers()
        if self.num_active_ord > 0:
            if self.active_trade_contract == None:
                self.active_trade_contract = 0
            self.active_trade_contract += 1
            if self.active_trade_contract > self.num_active_ord - 1:
                self.active_trade_contract = 0
            b = self.thing.active_orders[self.active_trade_contract]
            self.texts[30][0] = str(b[0])
            self.texts[32][0] = str(b[1])
            self.texts[34][0] = str(b[2])
            self.texts[36][0] = str(b[3].name) + ": " + str(b[3].x) + "/" + str(b[3].y)
            self.texts[38][0] = self.game.conv_idn_to_data(b[4])
        else:
            self.active_trade_contract = None
            self.texts[30][0] = self.game.language.BASIC[12]
            self.texts[32][0] = self.game.language.BASIC[12]
            self.texts[34][0] = self.game.language.BASIC[12]
            self.texts[36][0] = self.game.language.BASIC[12]
            self.texts[38][0] = self.game.language.BASIC[12]

    def accept_trade_offer(self):
        if self.selected_trade_contract != None:
            self.thing.active_orders.append(self.thing.available_orders[self.selected_trade_contract])
            self.thing.available_orders.remove(self.thing.available_orders[self.selected_trade_contract])
            self.update_trade_offers()
            self.selected_trade_contract = None
            self.selected_trade_building = None
            self.texts[18][0] = self.game.language.BASIC[12]
            self.texts[20][0] = self.game.language.BASIC[12]
            self.texts[22][0] = self.game.language.BASIC[12]
            self.texts[24][0] = self.game.language.BASIC[12]
            self.texts[26][0] = self.game.language.BASIC[12]

    def show(self):
        self.texts[3][0] = self.game.language.TRADE[1]
        self.texts[4][0] = self.game.language.TRADE[1]

        self.update_trade_building_list()
        self.trade_building = None
        self.trade_building_counter = None
        self.visible = True
        self.game.window_display = True

    def hide(self):
        self.visible = False
        self.game.window_display = False
        self.selected_trade_contract = None
        self.selected_trade_building = None
        self.texts[18][0] = self.game.language.BASIC[12]
        self.texts[20][0] = self.game.language.BASIC[12]
        self.texts[22][0] = self.game.language.BASIC[12]
        self.texts[24][0] = self.game.language.BASIC[12]
        self.texts[26][0] = self.game.language.BASIC[12]
        self.active_trade_contract = None
        self.texts[30][0] = self.game.language.BASIC[12]
        self.texts[32][0] = self.game.language.BASIC[12]
        self.texts[34][0] = self.game.language.BASIC[12]
        self.texts[36][0] = self.game.language.BASIC[12]
        self.texts[38][0] = self.game.language.BASIC[12]


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
        pos=[WIDTH - MENU_RIGHT[0] + 130, 230],
        size=(68, 30),
        color=DARKGREY,
        text="Open",
        textsize=FONT_MENU_TEXT_SIZE,
        textcolor=LIGHTGREY,
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

        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, self.size[0], self.size[1]))
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
            (7, 1),
        )
        self.rect = self.image.get_rect()

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
        pos=[WIDTH - MENU_RIGHT[0] + 130, 430],
        size=(68, 30),
        color=DARKGREY,
        text="Open",
        textsize=FONT_MENU_TEXT_SIZE,
        textcolor=LIGHTGREY,
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

        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, self.size[0], self.size[1]))
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
            (7, 1),
        )
        self.rect = self.image.get_rect()
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
        textsize=FONT_MENU_TEXT_SIZE,
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
        pg.draw.rect(self.image, self.textcolor, (0, 0, self.size[0], self.size[1]))
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
            (5, 1),
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
