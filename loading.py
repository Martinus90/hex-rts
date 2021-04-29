import pygame as pg
from settings import *

class Diplomacy(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game

class Contender(pg.sprite.Sprite):
    def __init__(self, game, name="Player", player=False, side=0, exc_rt=1, money=0, global_money=0, stability=0, reputation=0):
        self.game = game
        self.name = name
        self.player = player
        self.side = side
        self.exc_rt = exc_rt
        self.money = money
        self.global_money = global_money
        self.stability = stability
        self.reputation = reputation

        self.image = pg.Surface((TILESIZE[0], TILESIZE[0]))
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

class Unit_Type(pg.sprite.Sprite):
    def __init__(self, game, name="Name", typ=0, s_normal=1, s_water=1, s_mountain=1, s_river=1, fuel_usage=0, food_usage=1, money_usage=1):
        self.game = game
        self.name = name
        self.typ = typ
        self.s_normal = s_normal
        self.s_water = s_water
        self.s_mountain = s_mountain
        self.s_river = s_river

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

        self.position = ['Pozycja', 20, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 15)]
        self.speed = ['Predkosc', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 35)]
        self.time = ['Czas', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 55)]
        self.data1 = ['Data', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 75)]
        self.data2 = ['Year', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+10, 95)]
        self.terrain = ['Terrain:', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+60, 120)]
        self.terrain1 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+85, 140)]
        self.terrain2 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+85, 160)]
        self.terrain3 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+85, 180)]

        self.unit = ['Unit:', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+60, 210)]
        self.unit1 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+30, 230)]
        self.unit2 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+30, 250)]
        self.unit3 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+30, 270)]
        self.unit4 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+30, 290)]
        self.unit5 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+30, 310)]
        self.unit6 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+30, 330)]
        self.unit7 = ['', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+30, 350)]

        self.building = ['Building:', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+60, 400)]
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


    def render(self, surface):
        for im in self.list:
            surface.blit(im[0], im[1])

    def make_menu(self):
        menu = pg.Surface([WIDTH, HEIGHT])
        menu.fill(VIOLET)
        menu.set_colorkey(VIOLET)
        self.render(menu)
        return menu

class Button(pg.sprite.Sprite): #regular button
    def __init__(self, game, window, pos=[6,6], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK):
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
        self.image = self.game.x_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.visible = False
        self.game.window_display = False

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def update(self):
        self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]

class CW_Button(Button): #CW -> Close window
    def __init__(self, game, window, pos=[6,6], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK):
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
        self.image = self.game.x_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        print("Kliknięto w przycisk")
        self.window.hide()

    def check_col(self, mouse):
        if self.rect.collidepoint(mouse):
            self.click()

    def update(self):
        self.visible = self.window.visible
        self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]

class Switch_Button(Button):
    def __init__(self, game, window, pos=[200,60], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable=None):
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
        self.variable = variable
        print("Here")
        print(self.variable)
        print(self.window.unit.state[self.variable])

        self.visible = self.window.visible
        if self.window.unit.state[self.variable] == True:
            self.image = self.game.yes_img.copy()
        else:
            self.image = self.game.no_img.copy()
        self.image.set_colorkey(VIOLET)
        self.rect = self.image.get_rect()

    def click(self):
        self.window.unit.state[self.variable] = not self.window.unit.state[self.variable]
        print(self.window.unit.state[self.variable])

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
        self.abs_pos = self.pos + self.window.pos
        self.rect.x = self.pos[0] + self.window.pos[0]
        self.rect.y = self.pos[1] + self.window.pos[1]

class Mobilized_Button(Button):
    def __init__(self, game, window, pos=[200,40], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK):
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

class Training_Button(Button):
    def __init__(self, game, window, pos=[200,60], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK):
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



class Window(pg.sprite.Sprite):
    def __init__(self, unit, game, pos=[100,100], size=(300, 300), color=DARKGREY, text="Text", textsize=15, textcolor=LIGHTGREY, textpos=(50,10), border_size=3):
        self.groups = game.windows
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

        self.buttons.append(CW_Button(self.game, self))
        self.buttons.append(Switch_Button(self.game, self, pos=[200,60], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable="training"))
        self.buttons.append(Switch_Button(self.game, self, pos=[200,40], size=(20,20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK, variable="mobilized"))
        #self.buttons.append(Mobilized_Button(self.game, self))
        #self.buttons.append(Training_Button(self.game, self))

        #self.image = self.game.window_img.copy()

        self.image = pg.Surface(self.size)
        
        pg.draw.rect(self.image, self.textcolor, (0, 0, size[0], size[1]))
        pg.draw.rect(self.image, self.color, (0+self.border_size, 0+self.border_size, size[0]-self.border_size*2-1, size[1]-self.border_size*2-1))
        #pg.draw.rect
        self.image.blit(pg.font.Font(FONT_NAME, self.textsize).render(self.text, False, self.textcolor), self.textpos)
        #['Building:', 16, LIGHTGREY, (WIDTH-MENU_RIGHT[0]+60, 400)]
        #self.image.fill(self.color, (pos[0]+self.border_size, pos[1]+self.border_size, size[0]-self.border_size, size[1]-self.border_size))
        #self.image.fill(self.color, (100, 100, 20, 20))
        
        
        #self.image.fill(textcolor)

        self.rect = self.image.get_rect()
        print("TU")
        print(self.image)
        self.rectangle = pg.Surface(self.size)
        print("A tu następne")
        print(self.rectangle)
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

class OU_Button(Button):
    def __init__(self, game, unit, pos=[6,6], size=(20, 20), color=LIGHTGREY, text="X", textsize=10, textcolor=BLACK):
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

    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
