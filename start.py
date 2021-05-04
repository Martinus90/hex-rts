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
    def __init__(self):
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

            self.construction_img = pg.image.load(path.join(img_folder, CONSTRUCTION_IMG))
            self.village_img = pg.image.load(path.join(img_folder, VILLAGE_IMG))
            self.city_img = pg.image.load(path.join(img_folder, CITY_IMG))
            self.harbor_img = pg.image.load(path.join(img_folder, HARBOR_IMG))
            self.airport_img = pg.image.load(path.join(img_folder, AIRPORT_IMG))
            self.warehouse_img = pg.image.load(path.join(img_folder, WAREHOUSE_IMG))
            self.barracks_img = pg.image.load(path.join(img_folder, BARRACKS_IMG))
            self.mine_img = pg.image.load(path.join(img_folder, MINE_IMG))
            self.smelter_img = pg.image.load(path.join(img_folder, SMELTER_IMG))
            self.oil_well_img = pg.image.load(path.join(img_folder, OIL_WELL_IMG))
            self.power_plant_img = pg.image.load(path.join(img_folder, POWER_PLANT_IMG))
            self.production_plant_img = pg.image.load(path.join(img_folder, PRODUCTION_PLANT_IMG))
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
        self.buttons = pg.sprite.Group()
        self.settlements = pg.sprite.Group()
        self.buildings = pg.sprite.Group()
        self.units = pg.sprite.Group()
        self.texts = []

        #first on the list is always neutral, second is player, 3+ are others / to change color just change side
        self.players.append(Contender(self, name="Neutral", player=False, side=0, exc_rt=1, money=0, global_money=0, stability=0, reputation=0))
        self.players.append(Contender(self, name="Sovenya", player=True, side=1, exc_rt=1, money=1000, global_money=100, stability=0, reputation=0))
        self.players.append(Contender(self, name="Nebohray", player=False, side=2, exc_rt=1, money=1000, global_money=100, stability=0, reputation=0))

        #self.UNIT_TYPE = ["Artillery","Mechanized","Reconnaissance","Motorized","Other","Logistic","Headquarters","Helicopters","Aircraft","Anti-Aircraft","Anti-Tank","Missile","Engineering"]

        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[0], typ=0, s_normal=4, s_water=100, s_mountain=6, s_coast=4, s_river=12, s_no_fuel=20, fuel_usage=0, food_usage=1, money_usage=2))
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[1], typ=1, s_normal=2, s_water=100, s_mountain=12, s_coast=4, s_river=12, s_no_fuel=20, fuel_usage=1, food_usage=1, money_usage=2))
        self.types.append(Unit_Type(self, name=self.language.UNIT_TYPE[2], typ=2, s_normal=2, s_water=100, s_mountain=12, s_coast=4, s_river=12, s_no_fuel=20, fuel_usage=1, food_usage=1, money_usage=2))


        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        for grid in self.map.grids:
            grid.get_neighbors(self.map)
            #print(roffset_from_cube(-1, grid.hex)[1])

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
            if b[2] == "Construction":
                Construction(self, b[0], b[1], b[3], b[4])
            #elif b[2] == "Village":
            #    Village(self, b[0], b[1], b[3], b[4])

        for u in self.map.units:
            Unit(self, u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8], u[9], u[10], u[11], u[12], u[13], u[14], u[15], u[16], u[17], u[18], u[19], u[20], u[21], u[22])



        #print(self.map.trees)
        #print(self.map.units)

        #print([x.hex for x in self.walls])
        #for h in self.walls:
        #    print(h.col)
        #    print(h.row)
        #    print(h.hex)
        #    print(h.hex.q)
        #    self.od.append(h.hex)

        #print(hex_distance(self.od[0], self.od[1]))

        #result = [x for x in self.walls if x.hex.r > 4]
        #print(result)

        self.player = Player(self, 0, 0)
        self.camera = Camera(self.map.width, self.map.height)

        #self.windek = Window(self)

    def time(self):
        if self.timer > 1: #def 1
            self.timer -= 1
            self.quarter += 1
            for unit in self.units:
                unit.do()
            for res in self.resources:
                res.do()

        if self.quarter > 3: #def 3
            self.quarter -= 4
            self.hour += 1
        if self.hour > 23: #def 23
            self.hour -= 24
            self.day += 1
            for res in self.resources:
                res.daily()

        if self.day > 7: #def 7
            self.day -= 7
            self.week += 1
        if self.week > 3: #13
            self.week -= 3
            self.season += 1
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
            if (b.col == self.mouse_pos.col) and (b.row == self.mouse_pos.row):
                self.building = b
                self.menu.building1[0] = self.building.description[0]
                self.menu.building2[0] = self.building.description[1]
                self.menu.building3[0] = self.building.description[2]
                self.menu.building4[0] = self.building.description[3]
                self.menu.building5[0] = self.building.description[4]
                self.menu.building6[0] = self.building.description[5]
                self.menu.building7[0] = self.building.description[6]
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
        for sprite in self.all_sprites:
            #if (self.player.x - 8 < sprite.x < self.player.x + 8) and (self.player.y - 8 < sprite.y < self.player.y + 8):
                #print(sprite.x, sprite.y, sprite.z)
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            #self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.screen.blit(self.menu2, (0, 0))
        self.screen.blit(self.players[1].image, (12, 0))
        self.screen.blit(self.money_img, (10, 30))
        self.screen.blit(self.global_img, (163, 8))
        self.screen.blit(self.money_img, (160, 30))
        self.screen.blit(self.exchange_img, (312, 6))
        self.screen.blit(self.money_img, (310, 30))
        

        

        for text in self.texts:
            self.screen.blit(pg.font.Font(FONT_NAME, text[1]).render(text[0], False, text[2]), text[3])

        
        if self.selecting != None:
            self.screen.blit(self.map.tmxdata.images[self.selecting.gid], (WIDTH - MENU_RIGHT[0]+10, 140))
        if self.resourcing != None:
            self.screen.blit(self.resourcing.image, (WIDTH - MENU_RIGHT[0]+10, 140))
        if self.building != None:
            self.screen.blit(self.building.image, (WIDTH - MENU_RIGHT[0]+0, 435))
            self.screen.blit(self.building.owner.image, (WIDTH - MENU_RIGHT[0]+10, 412))
        if self.uniting != None:
            self.screen.blit(self.uniting.owner.image, (WIDTH - MENU_RIGHT[0]+5, 222))
            self.screen.blit(self.uniting.unit_typ.image, (WIDTH - MENU_RIGHT[0]-5, 248))
            self.screen.blit(self.uniting.button.image, self.uniting.button.pos)
            if self.uniting.window.visible == True:
                self.screen.blit(self.uniting.window.image, self.uniting.window.pos)
                #for var in self.uniting.window.variables:
            
        for window in self.windows:
            if window.visible == True:
                self.screen.blit(window.image, window.pos)
                for button in window.buttons:
                    window.image.blit(button.image, button.pos)
                if 1 == 1: #rolling display unit variables
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.men), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 38))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.supply), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 58))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.uniforms), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 78))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.fuel), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 98))
                    
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.light_ammo), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 138))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.heavy_ammo), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 158))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.rockets), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 178))
                    
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.rifle), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 218))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.art), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 238))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.truck), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 258))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.apc), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 278))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.tank), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 298))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.heli), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 318))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(str(window.unit.aircraft), False, LIGHTGREY), (window.pos[0] + 10, window.pos[1] + 338))

                    self.screen.blit(self.uniting.owner.image, (window.pos[0] + 170, window.pos[1] + 30))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.unit.owner.name, False, LIGHTGREY), (window.pos[0] + 200, window.pos[1] + 38))
                    self.screen.blit(self.uniting.unit_typ.image, (window.pos[0] + 160, window.pos[1] + 56))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.unit.unit_typ.name, False, LIGHTGREY), (window.pos[0] + 200, window.pos[1] + 58))

                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.unit.print_mobilized(), False, LIGHTGREY), (window.pos[0] + 170, window.pos[1] + 80))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.DESCRIPTION[2] + ": " + str(window.unit.combat_ability) + "/" + str(window.unit.combat_ability_max), False, LIGHTGREY), (window.pos[0] + 170, window.pos[1] + 96))
                    
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.DESCRIPTION[0] + ": " + str(window.unit.experience), False, LIGHTGREY), (window.pos[0] + 170, window.pos[1] + 117))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(self.language.DESCRIPTION[7] + ": " + str(window.unit.tiredness) + "/" + str(window.unit.tiredness_max), False, LIGHTGREY), (window.pos[0] + 170, window.pos[1] + 133))
                    self.screen.blit(pg.font.Font(FONT_NAME, FONT_SIZE).render(window.unit.task, False, LIGHTGREY), (window.pos[0] + 170, window.pos[1] + 153))

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
                if event.key == pg.K_m:
                    self.territory_visible = not self.territory_visible
                if (event.key == 61) or (event.key == 270): #plus key
                    if self.speed < 50:
                        self.speed = self.speed + 1
                    #print(self.speed)
                if (event.key == 45) or (event.key == 269): #minus key
                    if self.speed >= 2:
                        self.speed = self.speed - 1
                    #print(self.speed)
                if event.key == pg.K_PAUSE:
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
                        if self.uniting: 
                            self.uniting.button.check_col(pg.mouse.get_pos())


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