import pygame as pg
from settings import *
from languages import *
from sprites import *
from random import randint

class Diplomacy(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game

class Trade(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.resource_exchange_rate1 = [4,3,3,2,2, #"Wood", "Food", "Cement", "Iron Ore", "Coal",
        5,1,10,10,5,#    "Steel":5, "Water":1, "Tools":10, "Parts":10, "Aluminum":5, 
        2,3,2,3,1,#      "Oil":2, "Fuel":3, "Plastic":2, "Chemical Compounds":3, "Fertilizer":1, 
        1,1,20,1,2,#     "Silicon":1, "Calcium":1, "Electronics":20, "Cotton":1, "Textiles":2, 
        1,1,5,30]#       "Rubber":1, "Bauxite":1, "Furniture":5, "Civilian Machines":30,
        self.resource_exchange_rate2 = [4,#    "Supply":4, 
        3,3,2,4,30,#    "Uniforms":3, "Fuel":3, "Light Ammo":2, "Heavy Ammo":4, "Rockets":30, 
        8,40,100,200,300,#    "Rifle":8, "Artilleries":40, "Truck":100, "APC":200, "Tank":300, 
        500,1000]#    "Helicopters":500, "Aircrafts":1000
        self.resource_rating = [4,3,3,2,2, #"Wood", "Food", "Cement", "Iron Ore", "Coal",
        5,1,10,10,5,#    "Steel":5, "Water":1, "Tools":10, "Parts":10, "Aluminum":5, 
        2,3,2,3,1,#      "Oil":2, "Fuel":3, "Plastic":2, "Chemical Compounds":3, "Fertilizer":1, 
        1,1,20,1,2,#     "Silicon":1, "Calcium":1, "Electronics":20, "Cotton":1, "Textiles":2, 
        1,1,5,30]
    
    def rating(self, value):#convert int rating to color 1=fall/red 2=stable/grey 3=rising/green
        if value == 1:
            return DARKRED
        elif value == 2:
            return LIGHTGREY
        elif value == 3:
            return DARKGREEN

class Nation(pg.sprite.Sprite):
    def __init__(self, game, name="Nation"):
        self.game = game
        self.name = name
        self.description = ""

class Contender(pg.sprite.Sprite):
    def __init__(self, game, name="Player", nation=0, player=False, side=0, exc_rt=1, money=0, global_money=0, reputation=0, stability=0):
        self.game = game
        self.name = name
        self.nation = self.game.nations[nation]
        self.player = player
        self.side = side
        self.exc_rt = exc_rt
        self.money = money
        self.global_money = global_money
        self.reputation = reputation
        self.stability = stability

        self.image = pg.Surface((64, 64))
        self.image.fill(VIOLET)
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.game.flags_img.copy(), FLAG_OFFSET, (0, self.side*FLAG_SIZE[1], FLAG_SIZE[0], FLAG_SIZE[1]))

    def buy_global_money(self, quantity, global_market):
        if self.money > quantity * self.exc_rt:
            self.money = self.money - (quantity * self.exc_rt)
            self.global_money = self.global_money + quantity

    def sell_global_money(self, quantity, global_market):
        if self.global_money > quantity:
            self.global_money = self.global_money - quantity
            self.money = self.money + (quantity * self.exc_rt)

    def do(self):
        pass

    def update(self):
        pass


class Unit_Type(pg.sprite.Sprite):
    def __init__(self, game, name="Name", typ=0, s_normal=1, s_water=1, s_mountain=1, s_coast=1, s_river=1, s_no_fuel=20, fuel_usage=0, food_usage=1, money_usage=1):
        self.game = game
        self.name = name
        self.typ = typ
        self.s_normal = s_normal
        self.s_water = s_water
        self.s_mountain = s_mountain
        self.s_coast = s_coast
        self.s_river = s_river
        self.s_no_fuel = s_no_fuel

        self.fuel_usage = fuel_usage
        self.food_usage = food_usage
        self.money_usage = money_usage

        self.image = pg.Surface((TILESIZE[0], TILESIZE[0]))
        self.image.fill(VIOLET)
        self.image.set_colorkey(VIOLET)
        self.image.blit(self.game.units_img.copy(), UNIT_OFFSET, (0, self.typ*UNIT_SIZE[1], UNIT_SIZE[0], UNIT_SIZE[1]))

    def move_cost(self, terrain):
        if terrain in {self.game.language.TERRAIN[0], self.game.language.TERRAIN[1], self.game.language.TERRAIN[4], self.game.language.TERRAIN[6]}:
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

        self.new_building_window = New_Building_Window(self.game, pos=[100,100], size=(300, 400), color=DARKGREY, text="New Building", textsize=18, textcolor=LIGHTGREY, textpos=(40,10), border_size=3)
        
        self.new_building_button = OW_Button(self.game, self.new_building_window, pos=[WIDTH - MENU_RIGHT[0]+70, 425], size=(56, 30), color=DARKGREY, text="New", textsize=24, textcolor=LIGHTGREY)
        self.buttons.append(self.new_building_button)

        
        self.trade_window = Trade_Window(self.game, pos=[100,100], size=(700, 650), color=DARKGREY, text="Trade", textsize=15, textcolor=LIGHTGREY, textpos=(50,10), border_size=3)
        self.open_trade_window = OW_Button(self.game, self.trade_window, pos=[WIDTH - MENU_RIGHT[0]+15, HEIGHT-45], size=(78, 30), color=DARKGREY, text="Trade", textsize=24, textcolor=LIGHTGREY)
        #self.open_trade_window.image = 
        self.buttons.append(self.open_trade_window)

        if 1 == 1: # right menu
            self.position = [self.game.language.DISPLAY_GUI[0], 20, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 15)]
            self.speed = [self.game.language.DISPLAY_GUI[5], 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 35)]
            self.time = [self.game.language.DISPLAY_GUI[1], 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 55)]
            self.data1 = ['Data', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 75)]
            self.data2 = ['Year', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 95)]
            self.terrain = [self.game.language.DISPLAY_GUI[6], 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+60, 120)]
            self.terrain1 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+85, 140)]
            self.terrain2 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+85, 160)]
            self.terrain3 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+85, 180)]

            self.unit = [self.game.language.DISPLAY_GUI[7], 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+60, 210)]
            self.unit1 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+30, 230)]
            self.unit2 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+30, 250)]
            self.unit3 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 270)]
            self.unit4 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 286)]
            self.unit5 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 310)]
            self.unit6 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 326)]
            self.unit7 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 350)]

            self.building = [self.game.language.DISPLAY_GUI[8], 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+60, 400)]
            self.building1 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+40, 420)]
            self.building2 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+70, 445)]
            self.building3 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+70, 465)]
            self.building4 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+20, 490)]
            self.building5 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+20, 510)]
            self.building6 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+20, 530)]
            self.building7 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+20, 550)]

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

        if 1 == 1:  #top bar -> tb
            self.tb_player_money  = ['$ 4000000', 16, DARKGREEN, (340, 17)]
            self.tb_player_global_money  = ['$ 400', 16, DARKGREEN, (490, 17)]
        
            self.game.texts.append(self.tb_player_money)
            self.game.texts.append(self.tb_player_global_money)

            #for a in range(len(self.game.players)-1):
                #self.tb_ex_rate  = ['1', 16, GREY, (340, 20)]
                #self.game.texts.append(self.tb_player_ex_rate)

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

class Button(pg.sprite.Sprite): #regular button
    def __init__(self, game, window, pos=[6,6], size=(20, 20), color=LIGHTGREY, text="X", textsize=24, textcolor=BLACK):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = pos
        #self.abs_pos = [0,0]
        #self.abs_pos[0] = self.pos[0] + self.window.pos[0]
        #self.abs_pos[1] = self.pos[1] + self.window.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor

        self.visible = self.window.visible
        #self.image = self.game.new_b_button.copy()

        self.image = self.game.button_1_img.copy()
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.text, False, self.textcolor), (8,4))
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.visible = True
        self.game.window_display = True

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def update(self):
        #self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]

class Function_Button(Button):
    def __init__(self, game, window, pos=[6,6], size=(20, 20), color=LIGHTGREY, text="X", textsize=24, textcolor=BLACK, function="function_name"):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.function = function

        self.visible = self.window.visible
        #self.image = self.game.new_b_button.copy()

        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(self.image, self.color, (0+BUTTON_BORDER_SIZE, 0+BUTTON_BORDER_SIZE, size[0]-BUTTON_BORDER_SIZE*2-1, size[1]-BUTTON_BORDER_SIZE*2-1))
       

        #self.image = self.game.button_1_img.copy()
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.text, False, self.textcolor), (6,7))
        #self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.function_list(self.function)
        #self.game.window_display = True

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def update(self):
        #self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]

class CW_Button(Button): #CW -> Close window
    def __init__(self, game, window, pos=[6,6], size=(30, 30), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = pos
        #self.abs_pos = [0,0]
        #self.abs_pos[0] = self.pos[0] + self.window.pos[0]
        #self.abs_pos[1] = self.pos[1] + self.window.pos[1]
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
        #self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]

class Switch_Button(Button):
    def __init__(self, game, window, pos=[200,60], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable=None):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = pos
        #self.abs_pos = [0,0]
        #self.abs_pos[0] = self.pos[0] + self.window.pos[0]
        #self.abs_pos[1] = self.pos[1] + self.window.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.variable = variable

        self.visible = self.window.visible
        if self.window.unit.state[self.variable] == True:
            self.image = self.game.yes_img.copy()
        else:
            self.image = self.game.no_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.unit.state[self.variable] = not self.window.unit.state[self.variable]
        #print(self.window.unit.state[self.variable])

        if self.window.unit.state[self.variable] == True:
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
        #self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]

class Mobilized_Button(Button): #old button
    def __init__(self, game, window, pos=[300,40], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.unit = self.window.unit
        self.pos = pos
        self.abs_pos = [0,0]
        self.abs_pos[0] = self.pos[0] + self.window.pos[0]
        self.abs_pos[1] = self.pos[1] + self.window.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor

        self.visible = self.window.visible
        if self.window.unit.mobilized == True:
            self.image = self.game.yes_img.copy()
        else:
            self.image = self.game.no_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.unit.mobilized = not self.window.unit.mobilized
        if self.window.unit.mobilized == True:
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
        self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]

class Training_Button(Button): #old button
    def __init__(self, game, window, pos=[300,60], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = pos
        self.abs_pos = [0,0]
        self.abs_pos[0] = self.pos[0] + self.window.pos[0]
        self.abs_pos[1] = self.pos[1] + self.window.pos[1]
        self.size = size
        self.color = color
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor

        self.visible = self.window.visible
        if self.window.unit.training == True:
            self.image = self.game.yes_img.copy()
        else:
            self.image = self.game.no_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.unit.training = not self.window.unit.training
        if self.window.unit.training == True:
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
        self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]

class OW_Button(Button): #open window
    def __init__(self, game, window, pos=[6,6], size=(60, 30), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.window = window
        self.pos = tuple(pos)
        self.abs_pos = [0,0]
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
        pg.draw.rect(self.image, self.color, (0+BUTTON_BORDER_SIZE, 0+BUTTON_BORDER_SIZE, size[0]-BUTTON_BORDER_SIZE*2-1, size[1]-BUTTON_BORDER_SIZE*2-1))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.text, False, self.textcolor), (5,5))



        #self.image = self.game.o_window_img.copy()
        #self.image.set_colorkey(VIOLET)

        self.rect = self.image.get_rect()
        #self.rect.x = 

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def click(self):
        self.window.show()

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

class Window(pg.sprite.Sprite):
    def __init__(self, game, pos=[100,100], size=(300, 400), color=DARKGREY, text="Text", textsize=15, textcolor=LIGHTGREY, textpos=(50,10), border_size=3):
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

        #draw window
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(self.image, self.color, (0+self.border_size, 0+self.border_size, size[0]-self.border_size*2-1, size[1]-self.border_size*2-1))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.text, False, self.textcolor), self.textpos)

        #draw buttons
        self.buttons.append(CW_Button(self.game, self, pos=[10,10]))

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

class New_Building_Window(Window):
    def __init__(self, game, pos=[100,100], size=(300, 400), color=DARKGREY, text="Text", textsize=15, textcolor=LIGHTGREY, textpos=(50,10), border_size=3):
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
        self.building_typ = 1

        self.buttons.append(Function_Button(self.game, self, pos=(20, 350), size=(60, 30), color=DARKGREY, text="Prev", textsize=20, textcolor=LIGHTGREY, function="func_1"))
        self.buttons.append(Function_Button(self.game, self, pos=(220, 350), size=(60, 30), color=DARKGREY, text="Next", textsize=20, textcolor=LIGHTGREY, function="func_2"))
        self.buttons.append(Function_Button(self.game, self, pos=(120, 350), size=(60, 30), color=DARKGREY, text="Done", textsize=20, textcolor=LIGHTGREY, function="func_3"))


        self.var1 = ['', 16, LIGHTGREY, (10, 45)]
        self.var2 = ['Resouce cost:', 16, LIGHTGREY, (10, 65)]
        self.var3 = ['', 16, LIGHTGREY, (10, 85)]
        self.var4 = ['', 16, LIGHTGREY, (10, 105)]
        self.var5 = ['', 16, LIGHTGREY, (10, 125)]
        self.var6 = ['Near resources:', 16, LIGHTGREY, (140, 65)]



        self.variables.append(self.var1)
        self.variables.append(self.var2)
        self.variables.append(self.var3)
        self.variables.append(self.var4)
        self.variables.append(self.var5)
        self.variables.append(self.var6)

        if 1 == 1:
            #draw window
            self.image = pg.Surface(self.size)
            pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
            pg.draw.rect(self.image, self.color, (0+self.border_size, 0+self.border_size, size[0]-self.border_size*2-1, size[1]-self.border_size*2-1))
            self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.text, False, self.textcolor), self.textpos)
            #draw buttons
            self.buttons.append(CW_Button(self.game, self, pos=[10,10]))
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
        print(self.building_typ)

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
                self.resources.append([str(r.value), 16, LIGHTGREY, (200, 85 + (a * 20))])
                a += 1

    def hide(self):
        self.visible = False
        self.game.window_display = False
        self.game.selecting.near_resources = []

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.var1[0] = self.game.language.BUILDINGS1[self.building_typ]
        self.var3[0] = self.game.language.RES1[0] + ": " + str(BUILDING_COST[self.building_typ]['wood'])
        self.var4[0] = self.game.language.RES1[2] + ": " + str(BUILDING_COST[self.building_typ]['cement'])
        self.var5[0] = self.game.language.RES1[5] + ": " + str(BUILDING_COST[self.building_typ]['steel'])

class Unit_Window(pg.sprite.Sprite):
    def __init__(self, unit, game, pos=[100,100], size=(300, 400), color=DARKGREY, text="Text", textsize=15, textcolor=LIGHTGREY, textpos=(50,10), border_size=3):
        self.groups = game.unit_windows, game.windows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.unit = unit
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

        #draw window
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(self.image, self.color, (0+self.border_size, 0+self.border_size, size[0]-self.border_size*2-1, size[1]-self.border_size*2-1))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.text, False, self.textcolor), self.textpos)

        #draw buttons
        self.buttons.append(CW_Button(self.game, self, pos=[10,10]))
        self.buttons.append(Switch_Button(self.game, self, pos=[360,40], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable="mobilized"))
        self.buttons.append(Switch_Button(self.game, self, pos=[360,60], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable="training"))
        self.buttons.append(Switch_Button(self.game, self, pos=[360,80], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable="refill_equipment"))
        self.buttons.append(Switch_Button(self.game, self, pos=[360,100], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable="refill_crew"))
        self.buttons.append(Switch_Button(self.game, self, pos=[360,120], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable="building"))
        self.buttons.append(Switch_Button(self.game, self, pos=[360,140], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable="patroling"))
        self.buttons.append(Switch_Button(self.game, self, pos=[360,160], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable="engage"))

        #draw eq names
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.DESCRIPTION[3], False, self.textcolor), (50, 40))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[0], False, self.textcolor), (50, 60))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[1], False, self.textcolor), (50, 80))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[2], False, self.textcolor), (50, 100))

        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[3], False, self.textcolor), (50, 140))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[4], False, self.textcolor), (50, 160))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[5], False, self.textcolor), (50, 180))

        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[6], False, self.textcolor), (50, 220))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[7], False, self.textcolor), (50, 240))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[8], False, self.textcolor), (50, 260))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[9], False, self.textcolor), (50, 280))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[10], False, self.textcolor), (50, 300))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[11], False, self.textcolor), (50, 320))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.RES2[12], False, self.textcolor), (50, 340))

        #draw gui text
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.DESCRIPTION[1], False, self.textcolor), (380,42))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.DESCRIPTION[4], False, self.textcolor), (380,60))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.DESCRIPTION[5], False, self.textcolor), (380,80))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.DESCRIPTION[6], False, self.textcolor), (380,100))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.DESCRIPTION[8], False, self.textcolor), (380,120))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.DESCRIPTION[9], False, self.textcolor), (380,140))
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.game.language.DESCRIPTION[10], False, self.textcolor), (380,160))


        self.rect = self.image.get_rect()
        self.rectangle = pg.Surface(self.size)
        #self.rect.x = 600
        #self.rect.y = 600
    
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
    def __init__(self, game, pos=[100,100], size=(500, 500), color=DARKGREY, text="Trade", textsize=15, textcolor=LIGHTGREY, textpos=(50,10), border_size=3):
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
        self.building_typ = 1

        self.buttons.append(Function_Button(self.game, self, pos=(20, 550), size=(len(self.game.language.BASIC[4])*11+15, 30), color=DARKGREY, text=self.game.language.BASIC[4], textsize=20, textcolor=LIGHTGREY, function="func_1"))
        self.buttons.append(Function_Button(self.game, self, pos=(170, 550), size=(len(self.game.language.BASIC[6])*11+15, 30), color=DARKGREY, text=self.game.language.BASIC[6], textsize=20, textcolor=LIGHTGREY, function="func_2"))
        self.buttons.append(Function_Button(self.game, self, pos=(320, 550), size=(len(self.game.language.BASIC[7])*11+15, 30), color=DARKGREY, text=self.game.language.BASIC[7], textsize=20, textcolor=LIGHTGREY, function="func_3"))
        self.buttons.append(Function_Button(self.game, self, pos=(470, 550), size=(len(self.game.language.BASIC[5])*11+15, 30), color=DARKGREY, text=self.game.language.BASIC[5], textsize=20, textcolor=LIGHTGREY, function="func_3"))


        if 1 == 1:
            #draw window
            self.image = pg.Surface(self.size)
            pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
            pg.draw.rect(self.image, self.color, (0+self.border_size, 0+self.border_size, size[0]-self.border_size*2-1, size[1]-self.border_size*2-1))
            self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.text, False, self.textcolor), self.textpos)
            #draw buttons
            self.buttons.append(CW_Button(self.game, self, pos=[10,10]))
            self.rect = self.image.get_rect()
            self.rectangle = pg.Surface(self.size)
            b = 0
            c = 0
            for a in RES1_LIST:
                self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(a, False, self.textcolor), (70 + c, 60 + (b*20)))
                b += 1
                if b > 7:
                    c += 240
                    b = 0
            b = 0
            c = 0 
            for a in RES2_LIST:
                self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(a, False, self.textcolor), (70 + c, 260 + (b*20)))
                b += 1
                if b > 4:
                    c += 240
                    b = 0

        b = 0
        c = 0
        for a in self.game.trade.resource_exchange_rate1:
            self.variables.append([a, 16, self.game.trade.rating(randint(1,3)), (10 + c, 60 + (b*20))])

            b += 1
            if b > 7:
                c += 240
                b = 0
        b = 0
        c = 0
        for a in self.game.trade.resource_exchange_rate2:
            self.variables.append([a, 16, self.game.trade.rating(randint(1,3)), (10 + c, 260 + (b*20))])
            #self.game.trade.rating(randint(1,3))
            b += 1
            if b > 4:
                c += 240
                b = 0





        #print(self.game.trade.resource_exchange_rate1)
        #print(self.game.trade.resource_exchange_rate2)




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
        print(self.building_typ)

    def func_3(self):
        self.game.adding_building(self.building_typ)

    def show(self):
        self.visible = True
        self.game.window_display = True

    def hide(self):
        self.visible = False
        self.game.window_display = False

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

class OU_Button(Button):
    def __init__(self, unit, game, pos=[6,6], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.unit = unit
        self.window = self.unit.window
        self.pos = tuple(pos)
        self.abs_pos = [0,0]
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
        #self.rect.x = 

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def click(self):
        self.unit.window.show()
        print("Unit window")

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


