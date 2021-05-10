import pygame as pg
from settings import LANGUAGE

class Language:
    def __init__(self):
        if LANGUAGE == "EN":
            self.BASIC = ["True", "False", "Yes", "No", "Previous", "Next", "Sell", "Buy"]
            self.SEASONS = ["Spring", "Summer", "Autumn", "Winter"]
            self.DAY = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            self.DISPLAY_GUI = ["Position: ", "Time: ", "Week: ", " , Day: ", "Pause", "Game Speed: ", "Terrain", "Unit", "Building"]
            self.TERRAIN = ["Grass", "Desert", "See", "Mountain", "Coast", "River", "Ford"]
            self.RESOURCES = ["Resource","Tree","Grain","Oil","Iron","Coal","Calcium","Silicon","Cotton","Rubber","Bauxite","Uranium","Water"]
            self.RES1 = ["Wood", "Food", "Cement", "Iron Ore", "Coal", "Steel", "Water", "Tools", "Parts", "Aluminum", "Oil", "Fuel", "Plastic", "Chemical Compounds", "Fertilizer",
            "Silicon", "Calcium", "Electronics", "Cotton", "Textiles", "Rubber", "Bauxite", "Furniture", "Civilian Machines"]
            self.RES2 = ["Supply", "Uniforms", "Fuel", "Light Ammo", "Heavy Ammo", "Rockets", "Rifle", "Artilleries", "Truck", "APC", "Tank", "Helicopters", "Aircrafts"] 

            self.UNIT_TYPE = ["Infantry","Armored","Artillery","Mechanized","Reconnaissance","Motorized","Other","Logistic","Headquarters","Helicopters","Aircraft","Anti-Aircraft","Anti-Tank","Missile","Engineering"]
            self.UNIT_STRU = ["Brigade", "Regiment", "Battalion", "Company"]
            self.UNIT_STRU_SHORT = [", Brig.: ", ", Reg.: ", ", Batt.: ", ", Comp.: "]
            self.BUILDINGS1 = ["Construction","Village","City","Harbor","Airport","Warehouse","Barracks","Mine","Smelter","Oil Well","Power Plant","Production Plant","Chemical Plant","High-Tech Plant","Mechanical Plant","Armament Plant","Aviation Plant","Shipyard"]
            self.RANKS1 = ["Lieutenant","Captain","Major","Colonel","General"]
            self.RANKS2 = ["Fugleman","Leader","Commander","Chieftain","Warlord"]

            self.COMMANDS = ["Waiting", "Going to: ", "Training", "Constructing", "Civilian Tasks"]
            self.DESCRIPTION = ["Experience", "Mobilized", "Combat Ability", "Men", "Training", "Refill eq.", "Refill crew", "Tiredness", "Building", "Patroling", "Engage"]
            self.GUI = ["Nearby resources: ", "Extraction", "Working", "Waiting"]

        elif LANGUAGE == "PL":
            self.BASIC = ["Prawda", "Fałsz", "Tak", "Nie", "Wstecz", "Następny", "Sprzedaj", "Kup"]
            self.SEASONS = ["Wiosna", "Lato", "Jesien", "Zima"]
            self.DAY = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
            self.DISPLAY_GUI = ["Pozycja: ", "Czas", "Tydzień", "Dzień: ", "Pauza", "Prędkość Gry: ", "Teren", "Jednostka", "Budynek"]
            self.TERRAIN = ["Zielen", "Pustynia", "Morze", "Gory", "Wybrzeże", "Rzeka", "Brod"]
            self.RESOURCES = ["Zasob","Drewno","Zboze","Ropa","Zelazo","Wegiel","Wapn","Krzem","Bawelna","Guma","Boksyt","Uran","Woda"]
            self.RES1 = ["Drewno", "Jedzenie", "Cement", "Ruda żelaza", "Koks", "Stal", "Woda", "Narzędzie", "Części", "Aluminium", "Ropa", "Paliwo", "Plastik", "Produkty Chemiczne", "Nawozy",
            "Krzem", "Wapń", "Elektronika", "Bawełna", "Tkaniny", "Guma", "Boksyt", "Meble", "Urządzenia Cywilne"]
            self.RES2 = ["Zaopatrzenie", "Mudury", "Paliwo", "Lekka Amunicja", "Ciężka Amunicja", "Rakiety", "Karabiny", "Artyleria", "Ciężarówki", "BWPy", "Czołgi", "Helikoptery", "Samoloty"] 
            
            self.UNIT_TYPE = ["Piechota","Pancerna","Artyleria","Zmechanizowana","Zwiad","Zmotoryzowana","Inne","Logistyka","Sztab","Helikoptery","Samoloty","PLOT","Przeciwpancerna","Rakietowa","Inżynieryjna"]
            self.UNIT_STRU = ["Brygada", "Pułk", "Batalion", "Kompania"]
            self.UNIT_STRU_SHORT = [", Bryg.: ", ", Pułk.: ", ", Bat.: ", ", Komp.: "]


            self.BUILDINGS1 = ["Budowa","Wioska","Miasto","Port","Lotnisko","Magazyn","Baraki","Kopalnia","Huta","Szyb Naftowy","Elektrownia","Zaklad Produkcyjny","Zaklad Chemiczny","Zaklad High-Tech","Zaklad Mechaniczny","Zaklad Zbrojeniowy","Zaklad Lotniczy","Stocznia"]
            self.RANKS1 = ["Porucznik","Kapitan","Major","Pulkownik","General"]
            self.RANKS2 = ["Przywodca","Lider","Dowodca","Wodz","Watazka"]

            self.COMMANDS = ["Czeka", "Idzie do: ", "Trenuje", "Buduje", "Zadania Cywilne"]
            self.DESCRIPTION = ["Doswiadczenie", "Zmobilizowana", "Zdolosc bojowa", "Ludzie", "Trening", "Uzup. ekw.", "Uzup. załoge", "Zmęczenie", "Budowanie", "Patroluj", "Bojowy"]
            self.GUI = ["Pobliskie zasoby: ", "Wydobycie", "Pracuje", "Czeka"]

        self.PERSON_NAME1 = ["Alexi Jastremsky","Stoycho Jellinek","Krastan Lhotzky","Ognyan Wolenska","Kalin Levitsky","Techoslav Sacharov","Blagovest Soloukhin","Razvigor Novak","Vojta Gindin","Borik Malenkov"]
        self.PERSON_NAME2 = ["Darko Brodsky","Tomislav Kruskal","Ljupco Jelinek","Vojkan Winogradsky","Drago Tomasek","Mecek Kudelin","Milo Mirkovic","Savo Sedlacek","Mutimir Volinin","Milutin Wolansky"]
        self.CITY_NAME1 = ["Serpurom","Minepetsk","Lenikovsk","Birovsk","Khabayev","Pavloransk","Buzuratov","Vladiransk","Lesogiyev","Velisinsk"]
        self.CITY_NAME2 = ["Ryazny","Budyomkhovo","Gronovsk","Ulyalchik","Lirtovsk","Kameznetsk","Belgoyarsk","Tuymanskoy","Iskidzhan","Fryalozhsk"]
        self.CITY_NAME3 = ["Novouborsk","Godedovo","Sorzhinsk","Kalinskovo","Kasinsk","Chernoratov","Batagarsk","Kovroznetsk","Kaliylovsk","Vybotamak"]
