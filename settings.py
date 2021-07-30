def ctts(tuple):
    """
    Changing color in tuple to color in # + 6 digits
    """
    global a
    a = "#"
    for b in range(len(tuple)):
        c = str(hex(tuple[b]))[2:]
        if (len(c)) < 2:
            c = "0" + c
        a = a + c
    return a


def mergeDict(dict1, dict2):
    """
    Adding two dictionary
    """
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = value + dict1[key]
    return dict3

def return_bool(var):
    if var == True:
        return "True"
    elif var == False:
        return "False"

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

ALL_COLORS = [
    WHITE,
    LIGHTGREY,
    GREY,
    DARKGREY,
    RED,
    DARKRED,
    GREEN,
    DARKGREEN,
    BLUE,
    YELLOW,
    CYAN,
    VIOLET,
    MAROON,
]

# game settings
WIDTH = 1600#1920       #1280   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 900#1080      #768    # 16 * 48 or 32 * 24 or 64 * 12
OFFSET = -1
FPS = 60
TITLE = "Testing"
BGCOLOR = BLACK
#FONT_NAME = "MyUnderwood.ttf"
FONT_NAME = "ZaiConsulPolishTypewriter.ttf"
FONT_SIZE = 18 #15
FONT_MENU_SIZE = 18
FONT_BUTTON_SIZE = 24
FONT_MINI_BUTTON_SIZE = 16
FONT_OW_BUTTON_SIZE = 24
FONT_MENU_TEXT_SIZE = 26
FONT_SWITCH_BUTTONS_SIZE = 16
FONT_WINDOW_SIZE = 18
TILESIZE = (64, 48)  # 48
GRIDWIDTH = WIDTH / TILESIZE[0]
GRIDHEIGHT = HEIGHT / TILESIZE[1]
MENU_RIGHT = (200, 100)
MENU_TOP = (50, 100)
MENU_BOTTOM = (60, 100)
FLAG_SIZE = (17, 11)
FLAG_OFFSET = (1, 9)
UNIT_SIZE = (18, 10)
UNIT_OFFSET = (11, 4)
TOP_BAR_DISTANS = 600
TOP_BAR_STEP = 100
STABILITY_SIZE = (21, 21)
STABILITY_OFFSET = (0, 0)

BUTTON_BORDER_SIZE = 2
MINI_BUTTON_BORDER_SIZE = 1

SCROLL_SPEED = 10
GAME_SPEED = 1.0
LANGUAGE = "EN"  # "EN" / "PL"

PLAYER_IMG = "player.bmp"
FLAGS_IMG = "flags.bmp"
UNITS_IMG = "units.bmp"
COLOR_GRIDS = "colors.bmp"

RES1_LIST = [
    "Wood",
    "Food",
    "Cement",
    "Iron_Ore",
    "Coal",

    "Steel",
    "Water",
    "Tools",
    "Parts",
    "Aluminum",

    "Oil",
    "Fuel",
    "Plastic",
    "Chem_Comp",
    "Fertilizer",

    "Silicon",
    "Calcium",
    "Electronics",
    "Cotton",
    "Textiles",

    "Rubber",
    "Bauxite",
    "Furniture",
    "civ_mach",
    "elec_comp",
]
RES2_LIST = [
    "Supply",
    "Uniforms",
    "Fuel",
    "Light_Ammo",
    "Heavy_Ammo",

    "Rockets",
    "Rifle",
    "Artilleries",
    "Truck",
    "APC",
    
    "Tank",
    "Heli",
    "Aircrafts",
]


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

# list of buildings
CONSTRUCTION_IMG = "construction.bmp"  # 0

VILLAGE_IMG = "village.bmp"
CITY_IMG = "city.bmp"

HARBOR_IMG = "harbor.bmp"
AIRPORT_IMG = "airport.bmp"
WAREHOUSE_IMG = "warehouse.bmp"
BARRACK_IMG = "barrack.bmp"

MINE_IMG = "mine.bmp"
SMELTER_IMG = "smelter.bmp"
OIL_WELL_IMG = "oil_well.bmp"
RAFINERY_IMG = "rafinery.bmp"
POWER_PLANT_IMG = "power_plant.bmp"  # 11
LIGHT_INDUSTRY_PLANT_IMG = "light_industry.bmp"
HEAVY_INDUSTRY_PLANT_IMG = "heavy_industry.bmp"
CHEMICAL_PLANT_IMG = "chemical_plant.bmp"
HIGH_TECH_PLANT_IMG = "high_tech_plant.bmp"
MECHANICAL_PLANT_IMG = "mechanical_plant.bmp"
ARMAMENT_PLANT_IMG = "armament_plant.bmp"
AVIATION_PLANT_IMG = "aviation_plant.bmp"
SHIPYARD_IMG = "shipyard.bmp"  # 18


X_IMG = "x.bmp"
WINDOW_IMG = "window.bmp"
O_WINDOW_IMG = "o_window.bmp"
YES_IMG = "yes.bmp"
NO_IMG = "no.bmp"
ELECT_YES = "elect_yes.bmp"
ELECT_NO = "elect_no.bmp"

TRUCK_FUEL_USAGE = 1
ROCKET_TRUCK_FUEL_USAGE = 1
APC_FUEL_USAGE = 2
TANK_FUEL_USAGE = 3
HELI_FUEL_USAGE = 2
AIRCRAFT_FUEL_USAGE = 5

TRUCK_FUEL_CAP = 100
ROCKET_TRUCK_FUEL_CAP = 100
APC_FUEL_CAP = 250
TANK_FUEL_CAP = 300
HELI_FUEL_CAP = 200
AIRCRAFT_FUEL_CAP = 300

MEN_TRANSPORT_CAP = 4
TRUCK_TRANSPORT_CAP = 400
ROCKET_TRANSPORT_CAP = 100
APC_TRANSPORT_CAP = 100
TANK_TRANSPORT_CAP = 100
HELI_TRANSPORT_CAP = 50
AIRCRAFT_TRANSPORT_CAP = 400

MEN_MAX_SUPPLY = 4
MAX_UNIFORMS = 2

MAX_CARRY_LIGHT_AMMO_MEN = 10
MAX_CARRY_LIGHT_AMMO_APC = 400
MAX_CARRY_LIGHT_AMMO_TANK = 200
MAX_CARRY_LIGHT_AMMO_HELI = 200
MAX_CARRY_LIGHT_AMMO_AIRCRAFT = 0

MAX_CARRY_HEAVY_AMMO_MEN = 0
MAX_CARRY_HEAVY_AMMO_APC = 0
MAX_CARRY_HEAVY_AMMO_TANK = 60
MAX_CARRY_HEAVY_AMMO_HELI = 6
MAX_CARRY_HEAVY_AMMO_AIRCRAFT = 12

MAX_CARRY_ROCKETS_MEN = 1
MAX_CARRY_ROCKETS_APC = 3
MAX_CARRY_ROCKETS_TANK = 0
MAX_CARRY_ROCKETS_HELI = 6
MAX_CARRY_ROCKETS_AIRCRAFT = 12
MAX_CARRY_ROCKETS_ROCKET_TRUCK = 40

SUPPLY_WEIGHT = 1
UNIFORMS_WEIGHT = 1
FUEL_WEIGHT = 1
LIGHT_AMMO_WEIGHT = 1
HEAVY_AMMO_WEIGHT = 3
ROCKETS_WEIGHT = 5
RIFLE_WEIGHT = 1
ARTILLERIES_WEIGHT = 100
TRUCK_WEIGHT = 200
APC_WEIGHT = 200
TANK_WEIGHT = 400
HELI_WEIGHT = 400
AIRCRAFT_WEIGHT = 800
ROCKET_TRUCK_WEIGHT = 200



TERRAIN_GRASS = (1, 2, 3, 4, 5, 6, 7, 8)
TERRAIN_DESSERT = (9, 10, 11, 12, 13, 14, 15, 16)
TERRAIN_SEE = (17, 18, 19, 20, 21, 22, 23, 24)
TERRAIN_MOUNTAIN = (25, 26, 27, 28, 29, 30, 31, 32)
TERRAIN_RIVER = (
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
    96,
    100,
    104,
    108,
    112,
    116,
    120,
    124,
    128,
    132,
    136,
    140,
    144,
    148,
    152,
    156,
    160,
    164,
)
TERRAIN_FORD = (36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92)
TERRAIN_COAST = (
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
    119,
    120,
    121,
    122,
    123,
    124,
    125,
    126,
    127,
    128,
    129,
    130,
    131,
    132,
    133,
    134,
    135,
    136,
    137,
    138,
    139,
    140,
    141,
    142,
    143,
    144,
    145,
    146,
    147,
    148,
    149,
    150,
    151,
    152,
    153,
    154,
    155,
    156,
    157,
    158,
    159,
    160,
    161,
    162,
    163,
    164,
)

# Buildings

BUILDING_LIST = [
    "CONSTRUCTION",
    "VILLAGE",
    "CITY",
    "HARBOR",
    "AIRPORT",
    "WAREHOUSE",
    "BARRACKS",
    "MINE",
    "SMELTER",
    "OIL_WELL",
    "POWER_PLANT",
    "PRODUCTION_PLANT",
    "CHEMICAL_PLANT",
    "HIGH_TECH_PLANT",
    "MECHANICAL_PLANT",
    "ARMAMENT_PLANT",
    "AVIATION_PLANT",
    "SHIPYARD",
]

CONSTRUCTION_COST = {"wood": 0, "cement": 0, "steel": 0}
VILLAGE_COST = {"wood": 0, "cement": 0, "steel": 10}
CITY_COST = {"wood": 2000, "cement": 5000, "steel": 2000}
HARBOR_COST = {"wood": 500, "cement": 500, "steel": 200}
AIRPORT_COST = {"wood": 100, "cement": 5000, "steel": 500}
WAREHOUSE_COST = {"wood": 500, "cement": 500, "steel": 100}
BARRACKS_COST = {"wood": 200, "cement": 100, "steel": 50}

MINE_COST = {"wood": 500, "cement": 500, "steel": 100}
SMELTER_COST = {"wood": 100, "cement": 500, "steel": 500}
OIL_WELL_COST = {"wood": 100, "cement": 200, "steel": 1000}
POWER_PLANT_COST = {"wood": 100, "cement": 5000, "steel": 2000}
PRODUCTION_PLANT_COST = {"wood": 400, "cement": 1000, "steel": 500}
CHEMICAL_PLANT_COST = {"wood": 100, "cement": 1000, "steel": 1000}
HIGH_TECH_PLANT_COST = {"wood": 100, "cement": 1000, "steel": 1000}
MECHANICAL_PLANT_COST = {"wood": 400, "cement": 1000, "steel": 1000}
ARMAMENT_PLANT_COST = {"wood": 500, "cement": 1000, "steel": 1000}
AVIATION_PLANT_COST = {"wood": 500, "cement": 1000, "steel": 1000}
SHIPYARD_COST = {"wood": 500, "cement": 1000, "steel": 1000}

BUILDING_COST = [
    CONSTRUCTION_COST,
    VILLAGE_COST,
    CITY_COST,
    HARBOR_COST,
    AIRPORT_COST,
    WAREHOUSE_COST,
    BARRACKS_COST,
    MINE_COST,
    SMELTER_COST,
    OIL_WELL_COST,
    POWER_PLANT_COST,
    PRODUCTION_PLANT_COST,
    CHEMICAL_PLANT_COST,
    HIGH_TECH_PLANT_COST,
    MECHANICAL_PLANT_COST,
    ARMAMENT_PLANT_COST,
    AVIATION_PLANT_COST,
    SHIPYARD_COST,
]

UPKEEP_BUILDING = {"construction": 10, "village": 10, "city": 20, "harbor": 25, "airport": 100, "warehouse": 20, 
"barrack": 50, "mine": 200, "smelter": 100, "oil_well": 100, "rafinery": 100, "power_plant": 200, 
"light_industry_plant": 200, "heavy_industry_plant":300, "chemical_plant":200, "high_tech_plant":500, 
"mechanical_plant":300, "armament_plant":500, "aviation_plant":500, "shipyard":300}

# Production Cost
# Time 1=15(?) min, 4=1h, 96=1day, 480=5 work days
CEMENT_COST = {"calcium": 1, "coal": 1, "output": 1}#coal min max = 1
STEEL_COST = {"iron": 1, "coal": 1, "output": 2}
TOOL_COST = {"steel": 3, "plastic": 1, "output": 1}
PARTS_COST = {"steel": 4, "aluminum": 4, "output": 1}
ALUMINUM_COST = {"bauxite": 2, "output": 1}
FUEL_COST = {"oil": 4, "output": 2}
PLASTIC_COST = {"oil": 4, "output": 2}
CHEM_COMP_COST = {"oil": 4, "output": 2}
FERTILIZER_COST = {"calcium": 3, "chem_comp": 1, "output": 2}
ELEC_COMP_COST = {"aluminum": 3, "chem_comp": 3, "silicon": 3, "output": 2}
ELECTRONICS_COST = {"steel": 3, "plastic": 3, "elec_comp": 2, "output": 1}
PET_TEXTILES_COST = {"plastic": 4, "output": 1}
TEXTILES_COST = {"cotton": 4, "output": 1}
SYNTHETIC_RUBBER_COST = {"oil": 4, "output": 1}
FURNITURE_COST = {"wood": 3, "output": 1}
CIV_MACH_COST = {"steel": 100, "aluminum": 30, "plastic": 20, "parts": 10, "time": 100}

SUPPLY_COST = {"food": 4, "steel": 1, "output": 3}  # ns
UNIFORMS_COST = {"textiles": 4, "output": 1}
LIGHT_AMMO_COST = {"steel": 1, "textiles": 1, "chem_comp": 1, "output": 2, "time": 1}
HEAVY_AMMO_COST = {"steel": 5, "plastic": 5, "chem_comp": 5, "output": 1, "time": 4}
ROCKETS_COST = {"aluminum": 5, "chem_comp": 10, "plastic": 5, "parts": 1, "output": 1, "time": 12}
RIFLE_COST = {"steel": 4, "plastic": 1, "time": 4}
ARTILLERIES_COST = {"steel": 100,"rubber": 50,"parts": 10,"electronics": 5,"time": 100}
TRUCK_COST = {"steel": 200,"rubber": 100,"parts": 20,"tools": 5,"textiles": 200,"electronics": 10,"time": 200,}
APC_COST = {"steel": 1000,"rubber": 100,"parts": 20,"tools": 5,"textiles": 100,"electronics": 20,"time": 500}
TANK_COST = {"steel": 3000, "rubber": 400, "parts": 30, "tools": 10, "electronics": 30, "time": 1200}
HELICOPTERS_COST = {"aluminum": 1000, "rubber": 200, "parts": 50, "tools": 10, "elec_comp": 200, "time": 1000}
AIRCRAFT_COST = {"aluminum": 1800, "rubber": 400, "parts": 100, "tools": 25, "elec_comp": 500, "time": 2000}


HARBOR_TRANSPORT_COST = 200
AIRPORT_TRANSPORT_COST = 500
HARBOR_SHIPING_TIME = 10
AIRPORT_SHIPING_TIME = 2
HARBOR_TRANSPORT_MAX = 1000
AIRPORT_TRANSPORT_MAX = 100

PEACE_TREATY = 20
TRADE_TREATY = 50
ALLIANCE_TREATY = 100
GIVE_MONEY_REP = 50
GIVE_MONEY = 1000
GIVE_MONEY_DEC_REP = 30

CONSCRIPT_CITY_POP = 10
CONSCRIPT_CITY_LOY = 10
CONSCRIPT_VILL_POP = 5
CONSCRIPT_VILL_LOY = 5

CONSCRIPT_STAB_RED = 1

LOSE_REP_WAR = 30
LOSE_REP_TRADE = 5
LOSE_REP_ALLY = 10

LOSE_RELATIONS_WAR = 50
LOSE_RELATIONS_TRADE = 2
LOSE_RELATIONS_ALLY = 3

UPKEEP_TRUCK = 10
UPKEEP_APC = 20
UPKEEP_TANK = 50
UPKEEP_HELI = 200
UPKEEP_AIRCRAFT = 500
UPKEEP_ROCKET_TRUCK = 10

LOYALTY_DAYLI_GAIN = 1

#reputation gain/lose after diffrent scenarios
TRADE_DONE_REP = 5
TRADE_LOSE_REP = -10


# Technologies Cost
# empty for now
