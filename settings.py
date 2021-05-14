def ctts(tuple): #changing color in tuple to color in # + 6 digits
    global a
    a = "#"
    for b in range(len(tuple)):
        c = str(hex(tuple[b]))[2:]
        if (len(c)) < 2:
            c = "0" + c
        a = a + c
    return a

def mergeDict(dict1, dict2):    # adding two dictionary 
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = value + dict1[key]
   return dict3




# define some colors in tuples(R, G, B) and as hexadecimal string
WHITE = (255, 255, 255)
LIGHTGREY = (160, 160, 160)
GREY = (100, 100, 100)
DARKGREY = (40, 40, 40)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
DARKRED = (160, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 127, 0)
BLUE = (0, 0, 250)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
VIOLET = (255, 0, 255)

MAROON = (127, 0, 0)



# game settings
WIDTH = 1600    #1600     #1280   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 900   #900      #768    # 16 * 48 or 32 * 24 or 64 * 12
OFFSET = -1
FPS = 60
TITLE = "Testing"
BGCOLOR = BLACK
FONT_NAME = "MyUnderwood.ttf"
FONT_SIZE = 15
TILESIZE = (64, 48) #48
GRIDWIDTH = WIDTH / TILESIZE[0]
GRIDHEIGHT = HEIGHT / TILESIZE[1]
MENU_RIGHT = (200, 100)
MENU_TOP = (50, 100)
MENU_BOTTOM = (50, 100)
FLAG_SIZE = (17, 11)
FLAG_OFFSET = (1, 9)
UNIT_SIZE = (18, 10)
UNIT_OFFSET = (11, 4)
TOP_BAR_DISTANS = 600
TOP_BAR_STEP = 100
STABILITY_SIZE = (21, 21)
STABILITY_OFFSET = (0, 0)

BUTTON_BORDER_SIZE = 2

SCROLL_SPEED = 10
GAME_SPEED = 1.0
LANGUAGE = "EN" # "EN" / "PL"

PLAYER_IMG = "player.bmp"
FLAGS_IMG = "flags.bmp"
UNITS_IMG = "units.bmp"

RES1_LIST = ["Wood", "Food", "Cement", "Iron Ore", "Coal", "Steel", "Water", "Tools", "Parts", "Aluminum", "Oil", "Fuel", "Plastic", "Chemical Compounds", "Fertilizer",
            "Silicon", "Calcium", "Electronics", "Cotton", "Textiles", "Rubber", "Bauxite", "Furniture", "Civilian Machines"]
RES2_LIST = ["Supply", "Uniforms", "Fuel", "Light Ammo", "Heavy Ammo", "Rockets", "Rifle", "Artilleries", "Truck", "APC", "Tank", "Helicopters", "Aircrafts"] 


RESOURCE_IMG = "resource.bmp"
TREE_IMG = "tree.bmp"
GRAIN_IMG = "grain.bmp"
OIL_IMG = "oil.bmp"
IRON_IMG = "iron.bmp"
COAL_IMG = "coal.bmp"
CALCIUM_IMG = "calcium.bmp"
SILICON_IMG = "silicon.bmp"
COTTON_IMG = "cotton.bmp"
RUBBER_IMG = "rubber.bmp"
BAUXITE_IMG = "bauxite.bmp"
URANIUM_IMG = "uranium.bmp"
WATER_IMG = "water.bmp"

MONEY_IMG = "money.bmp"
GLOBAL_IMG = "global.bmp"
EXCHANGE_IMG = "exchange.bmp"
REPUTATION_IMG = "reputation.bmp"
STABILITY_IMG = "stability.bmp"

#list of buildings
CONSTRUCTION_IMG = "construction.bmp"#0

VILLAGE_IMG = "village.bmp"
CITY_IMG = "city.bmp"

HARBOR_IMG = "harbor.bmp"
AIRPORT_IMG = "airport.bmp"
WAREHOUSE_IMG = "warehouse.bmp"
BARRACKS_IMG = "barracks.bmp"

MINE_IMG = "mine.bmp"
SMELTER_IMG = "smelter.bmp"
OIL_WELL_IMG = "oil_well.bmp"
RAFINERY_IMG = "rafinery.bmp"
POWER_PLANT_IMG = "power_plant.bmp"#11
PRODUCTION_PLANT_IMG = "production_plant.bmp"
CHEMICAL_PLANT_IMG = "chemical_plant.bmp"
HIGH_TECH_PLANT_IMG = "high_tech_plant.bmp"
MECHANICAL_PLANT_IMG = "mechanical_plant.bmp"
ARMAMENT_PLANT_IMG = "armament_plant.bmp"
AVIATION_PLANT_IMG = "aviation_plant.bmp"
SHIPYARD_IMG = "shipyard.bmp"#18
            

X_IMG = "x.bmp"
WINDOW_IMG = "window.bmp"
O_WINDOW_IMG = "o_window.bmp"
YES_IMG = "yes.bmp"
NO_IMG = "no.bmp"

TRUCK_FUEL_USAGE = 1
APC_FUEL_USAGE = 2
TANK_FUEL_USAGE = 3
HELI_FUEL_USAGE = 2
AIRCRAFT_FUEL_USAGE = 5

TRUCK_FUEL_CAP = 50
APC_FUEL_CAP = 150
TANK_FUEL_CAP = 200
HELI_FUEL_CAP = 100
AIRCRAFT_FUEL_CAP = 300

TERRAIN_GRASS =    (1, 2, 3, 4, 5, 6, 7, 8)
TERRAIN_DESSERT =  (9, 10, 11, 12, 13, 14, 15, 16)
TERRAIN_SEE =      (17, 18, 19, 20, 21, 22, 23, 24)
TERRAIN_MOUNTAIN = (25, 26, 27, 28, 29, 30, 31, 32)
TERRAIN_RIVER =    (33, 34, 35, 36,
                    37, 38, 39, 40,
                    41, 42, 43, 44,
                    45, 46, 47, 48,
                    49, 50, 51, 52,
                    53, 54, 55, 56,
                    57, 58, 59, 60,
                    61, 62, 63, 64,
                    65, 66, 67, 68,
                    69, 70, 71, 72,
                    73, 74, 75, 76,
                    77, 78, 79, 80,
                    81, 82, 83, 84,
                    85, 86, 87, 88,
                    89, 90, 91, 92,
                    96, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 148, 152, 156, 160, 164)
TERRAIN_FORD =     (36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92)
TERRAIN_COAST =    (93, 94, 95, 96, 97, 98, 99, 100,
                    101, 102, 103, 104, 105, 106, 107, 108,
                    109, 110, 111, 112, 113, 114, 115, 116,
                    117, 118, 119, 120, 121, 122, 123, 124,
                    125, 126, 127, 128, 129, 130, 131, 132,
                    133, 134, 135, 136, 137, 138, 139, 140,
                    141, 142, 143, 144, 145, 146, 147, 148,
                    149, 150, 151, 152, 153, 154, 155, 156,
                    157, 158, 159, 160, 161, 162, 163, 164)

#Buildings

BUILDING_LIST = ['CONSTRUCTION', 'VILLAGE', 'CITY', 'HARBOR', 'AIRPORT', 'WAREHOUSE', 'BARRACKS', 'MINE', 'SMELTER', 'OIL_WELL', 'POWER_PLANT', 'PRODUCTION_PLANT', 'CHEMICAL_PLANT', 'HIGH_TECH_PLANT', 'MECHANICAL_PLANT', 'ARMAMENT_PLANT', 'AVIATION_PLANT', 'SHIPYARD']

CONSTRUCTION_COST = {'wood': 0, 'cement': 0, 'steel': 0}
VILLAGE_COST = {'wood': 0, 'cement': 0, 'steel': 100}
CITY_COST = {'wood': 2000, 'cement': 5000, 'steel': 2000}
HARBOR_COST = {'wood': 500, 'cement': 500, 'steel': 200}
AIRPORT_COST = {'wood': 100, 'cement': 5000, 'steel': 500}
WAREHOUSE_COST = {'wood': 500, 'cement': 500, 'steel': 100}
BARRACKS_COST = {'wood': 200, 'cement': 100, 'steel': 50}

MINE_COST = {'wood': 500, 'cement': 500, 'steel': 100}
SMELTER_COST = {'wood': 100, 'cement': 500, 'steel': 500}
OIL_WELL_COST = {'wood': 100, 'cement': 200, 'steel': 1000}
POWER_PLANT_COST = {'wood': 100, 'cement': 5000, 'steel': 2000}
PRODUCTION_PLANT_COST = {'wood': 400, 'cement': 1000, 'steel': 500}
CHEMICAL_PLANT_COST = {'wood': 100, 'cement': 1000, 'steel': 1000}
HIGH_TECH_PLANT_COST = {'wood': 100, 'cement': 1000, 'steel': 1000}
MECHANICAL_PLANT_COST = {'wood': 400, 'cement': 1000, 'steel': 1000}
ARMAMENT_PLANT_COST = {'wood': 500, 'cement': 1000, 'steel': 1000}
AVIATION_PLANT_COST = {'wood': 500, 'cement': 1000, 'steel': 1000}
SHIPYARD_COST = {'wood': 500, 'cement': 1000, 'steel': 1000}

BUILDING_COST = [CONSTRUCTION_COST, VILLAGE_COST, CITY_COST, HARBOR_COST, AIRPORT_COST, WAREHOUSE_COST, BARRACKS_COST, MINE_COST, SMELTER_COST, OIL_WELL_COST, POWER_PLANT_COST, PRODUCTION_PLANT_COST, CHEMICAL_PLANT_COST,
HIGH_TECH_PLANT_COST, MECHANICAL_PLANT_COST, ARMAMENT_PLANT_COST, AVIATION_PLANT_COST, SHIPYARD_COST]

#Production Cost
CEMENT_COST = {}
STEEL_COST = {}
TOOL_COST = {}
PARTS_COST = {}
ALUMINUM_COST = {}
FUEL_COST = {}
PLASTIC_COST = {}
CHEMICAL_COMPOUNDS_COST = {}
FERTILIZER_COST = {}
ELECTRONICS_COST = {}
TEXTILSE_COST = {}
SYNTHETIC_RUBBER_COST = {}
FURNITURE_COST = {}
CIVILIAN_MACHINES_COST = {}

BULLETS_COST = {}
AMONITION_COST = {}
ROCKET_COST = {}
SUPPLY_COST = {}
RILFE_COST = {}
TRUCK_COST = {}
APC_COST = {}
TANK_COST = {}
ARTILLERIE_COST = {}
HELICOPTER_COST = {}
AIRCRAFT_COST = {} 

#Technologies Cost
#empty for now