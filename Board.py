import imp
from Chance import Chance
from CommunityChest import CommunityChest
from Chance import Chance
from Group import Group
from Property import Property
from Railroad import Railroad
from Utility import Utility
from SpecialSpace import SpecialSpace

class Board:
    def __init__(self):
        self.get_out_of_jail_free_cards = 4
        self.houses = 36
        self.hotels = 12
        self.cc_cards = CommunityChest()
        self.cc_cards.shuffle()
        self.chance_cards = Chance()
        self.chance_cards.shuffle()

        self.brown = Group("Brown", 50)
        self.brown1 = Property("Mediterranean Avenue", 60, 2, [30, 90, 160, 250])
        self.brown2 = Property("Baltic Avenue", 60, 4, [60, 180, 320, 450])
        self.brown.add_properties([self.brown1, self.brown2])

        self.light_blue = Group('Light Blue', 50)
        self.lb1 = Property('Oriental Avenue', 100, 6, [90, 270, 400, 550])
        self.lb2 = Property("Vermont Avenue", 100, 6, [90, 270, 400, 550])
        self.lb3 = Property("Connecticut Avenue", 120, 8, [100, 300, 450, 600])
        self.light_blue.add_properties([self.lb1, self.lb2, self.lb3])

        self.pink = Group('Pink', 100)
        self.pink1 = Property("St. Charles Place", 140, 10, [150, 450, 625, 750])
        self.pink2 = Property("States Avenue", 140, 10, [150, 450, 625, 750])
        self.pink3 = Property("Viginia Avenue", 160, 12, [180, 500, 700, 900])
        self.pink.add_properties([self.pink1, self.pink2, self.pink3])

        self.orange = Group('Orange', 100)
        self.orange1 = Property("St. James Place", 180, 14, [200, 550, 750, 950])
        self.orange2 = Property("Tennessee Avenue", 180, 14, [200, 550, 750, 950])
        self.orange3 = Property("New York Avenue", 200, 16, [220, 600, 800, 1000])
        self.orange.add_properties([self.orange1, self.orange2, self.orange3])

        self.red = Group('Red', 150)
        self.red1 = Property("Kentucky Avenue", 220, 18, [250, 700, 875, 1050])
        self.red2 = Property("Indiana Avenue", 220, 18, [250, 700, 875, 1050])
        self.red3 = Property("Illinois Avenue", 240, 20, [300, 750, 925, 1100])
        self.red.add_properties([self.red1, self.red2, self.red3])
        
        self.yellow = Group('Yellow', 150)
        self.yellow1 = Property("Atlantic Avenue", 260, 22, [330, 800, 975, 1150])
        self.yellow2 = Property("Ventnor Avenue", 260, 22, [330, 800, 975, 1150])
        self.yellow3 = Property("Marvin Garden", 280, 24, [360, 850, 1025, 1200])
        self.yellow.add_properties([self.yellow1, self.yellow2, self.yellow3])

        self.green = Group('Green', 200)
        self.green1 = Property("Pacific Avenue", 300, 26, [390, 900, 1100, 1275])
        self.green2 = Property("North Carolina Avenue", 300, 26, [390, 900, 1100, 1275])
        self.green3 = Property("Pennsylvania Avenue", 320, 28, [450, 1000, 1200, 1400])
        self.green.add_properties([self.green1, self.green2, self.green3])
        

        self.blue = Group('Blue', 200)
        self.blue1 = Property("Park Place", 350, 35, [500, 1100, 1300, 1500])
        self.blue2 = Property("Boardwalk", 400, 50, [600, 1400, 1700, 2000])
        self.blue.add_properties([self.blue1, self.blue2])

        self.rr = Group('Railroad', None)
        self.rr1 = Railroad('Reading Railroad')
        self.rr2 = Railroad('Pennsylvania Railroad')
        self.rr3 = Railroad('B. & O. Railroad')
        self.rr4 = Railroad('Short Line')
        self.rr.add_properties([self.rr1, self.rr2, self.rr3, self.rr4])

        self.utilities = Group('Utility', 10)
        self.ec = Utility('Electric Company')
        self.ww = Utility('Water Works')
        self.utilities.add_properties([self.ec, self.ww])

        self.go = SpecialSpace('GO', 'You landed on Go!')
        self.jail = SpecialSpace('Jail', 'Just visting!')
        self.fp = SpecialSpace('Free Parking', 'Enjoy free parking!')
        self.gtj = SpecialSpace('Go to Jail', '', 'go to jail', {'player': 'current player'})

        self.income = SpecialSpace('Income Tax', 'Tax is $200', 'make payment', {'from': 'current player', 'to': 'BANK', 'amount': 200})
        self.luxury = SpecialSpace('Luxury Tax', 'Tax is $100', 'make payment', {'from': 'current player', 'to': 'BANK', 'amount': 100})

        self.cc = SpecialSpace('Community Chest', 'Draw a card!', 'draw a card', {'card type': 'cc', 'player': 'current player'})
        self.chance = SpecialSpace('Chance', 'Draw a card!', 'draw a card', {'card type': 'chance', 'player': 'current player'})

        self.property_array = []
        self.property_array.append(self.go)
        self.property_array.append(self.brown1)
        self.property_array.append(self.cc)
        self.property_array.append(self.brown2)
        self.property_array.append(self.income)
        self.property_array.append(self.rr1)
        self.property_array.append(self.lb1)
        self.property_array.append(self.chance)
        self.property_array.append(self.lb2)
        self.property_array.append(self.lb3)
        self.property_array.append(self.jail)
        self.property_array.append(self.pink1)
        self.property_array.append(self.ec)
        self.property_array.append(self.pink2)
        self.property_array.append(self.pink3)
        self.property_array.append(self.rr2)
        self.property_array.append(self.orange1)
        self.property_array.append(self.cc)
        self.property_array.append(self.orange2)
        self.property_array.append(self.orange3)
        self.property_array.append(self.fp)
        self.property_array.append(self.red1)
        self.property_array.append(self.chance)
        self.property_array.append(self.red2)
        self.property_array.append(self.red3)
        self.property_array.append(self.rr3)
        self.property_array.append(self.yellow1)
        self.property_array.append(self.yellow2)
        self.property_array.append(self.ww)
        self.property_array.append(self.yellow3)
        self.property_array.append(self.gtj)
        self.property_array.append(self.green1)
        self.property_array.append(self.green2)
        self.property_array.append(self.cc)
        self.property_array.append(self.green3)
        self.property_array.append(self.rr4)
        self.property_array.append(self.chance)
        self.property_array.append(self.blue1)
        self.property_array.append(self.luxury)
        self.property_array.append(self.blue2)