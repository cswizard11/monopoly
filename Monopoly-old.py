from random import *

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 100
        self.properties_owned = []
        self.properties_morgaged = []
        self.square = 0

    def Roll(self):
        last_square = self.square
        dice1 = randint(1,6)
        dice2 = randint(1,6)
        print ("You rolled " + str(dice1 + dice2))
        print("")
        self.square = (self.square + (dice1 + dice2)) % 40
        
        if last_square > self.square:
            self.money += 200
            
        property_array[self.square].Print()
        print("")
        
        
    def Buy(self):
        self.position = property_array[self.square]
        if self.position.property == True:
            if self.position.bought == False:
                print("")
                print("You bought " + self.position.name + " for $" + str(self.position.cost))
                print("")
                self.position.bought = True
                self.money -= self.position.cost
            else:
                print("")
                print("This property has already been bought")
                print("")
        else:
            print("")
            print("You cannot buy this square")
            print("")

class Property:
    def __init__(self, name, group, group_num, cost):
        self.name = name
        self.group = group
        self.group_num = group_num
        self.property = True
        self.bought = False
        self.cost = cost
        self.houses = 0
        self.hotel = False

    def Print(self):
        print (self.name)
        print (self.group)
        print ("There are %s properties in this group" % self.group_num)
        print ("$" + str(self.cost))
        if self.bought == False:
            print ("Unowned")
        else:
            print ("Owned")

class Square:
    def __init__(self, name):
        self.name = name
        self.property = False

    def Print(self):
        print (self.name)
        if self.name == "Go":
            print ("Collect $200")

class Railroad:
    def __init__(self, name):
        self.name = name
        self.property = True
        self.bought = False
        self.cost = 200

    def Print(self):
        print (self.name)
        print ("Railroad")
        print ("$" + str(self.cost))
        if self.bought == False:
            print ("Unowned")
        else:
            print("Owned")

class Utility:
    def __init__(self, name):
        self.name = name
        self.property = True
        self.bought = False
        self.cost = 150

    def Print(self):
        print(self.name)
        print("Utility")
        print("$" + str(self.cost))
        if self.bought == False:
            print ("Unowned")
        else:
            print("Owned")

class CardSquare:
    def __init__(self, name):
        self.name = name
        self.property = False

    def Print(self):
        print(self.name)

class Tax:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay
        self.property = False

    def Print(self):
        print(self.name)
        print("You payed $" + str(self.pay))
        

brown1 = Property("Mediterranean Avenue", "Brown", 2, 60)
brown2 = Property("Baltic Avenue", "Brown", 2, 60)

lightBlue1 = Property("Oriental Avenue", "Light blue", 3, 100)
lightBlue2 = Property("Vermont Avenue", "Light blue", 3, 100)
lightBlue3 = Property("Connecticut Avenue", "Light blue", 3, 120)

pink1 = Property("St. Charles Place", "Pink", 3, 140)
pink2 = Property("States Avenue", "Pink", 3, 140)
pink3 = Property("Viginia Avenue", "Pink", 3, 160)

orange1 = Property("St. James Place", "Orange", 3, 180)
orange2 = Property("Tennessee Avenue", "Orange", 3, 180)
orange3 = Property("New York Avenue", "Orange", 3, 180)

red1 = Property("Kentucky Avenue", "Red", 3, 220)
red2 = Property("Indiana Avenue", "Red", 3, 220)
red3 = Property("Illinois Avenue", "Red", 3, 240)

yellow1 = Property("Atlantic Avenue", "Yellow", 3, 260)
yellow2 = Property("Ventnor Avenue", "Yellow", 3, 260)
yellow3 = Property("Marvin Garden", "Yellow", 3, 280)

green1 = Property("Pacific Avenue", "Green", 3, 300)
green2 = Property("North Carolina Avenue", "Green", 3, 300)
green3 = Property("Pennsylvania Avenue", "Green", 3, 320)

blue1 = Property("Park Place", "Blue", 2, 350)
blue2 = Property("Boardwalk", "Blue", 2, 400)

go = Square("Go")
just_visiting = Square("Just Visiting")
free_parking = Square("Free Parking")
go_to_jail = Square("Go to jail")

reading = Railroad("Reading Railroad")
pennsylvania = Railroad("Pennsylvania Railroad")
bno = Railroad("B. & O. Railroad")
short_line = Railroad("Short Line")

electric_co = Utility("Electric Company")
water_works = Utility("Water Works")

community_chest = CardSquare("Community Chest")
chance = CardSquare("Chance")

income_tax = Tax("Income Tax", 200)
luxury_tax = Tax("Luxury Tax", 100)

property_array = []

property_array.append(go)
property_array.append(brown1)
property_array.append(community_chest)
property_array.append(brown2)
property_array.append(income_tax)
property_array.append(reading)
property_array.append(lightBlue1)
property_array.append(chance)
property_array.append(lightBlue2)
property_array.append(lightBlue3)
property_array.append(just_visiting)
property_array.append(pink1)
property_array.append(electric_co)
property_array.append(pink2)
property_array.append(pink3)
property_array.append(pennsylvania)
property_array.append(orange1)
property_array.append(community_chest)
property_array.append(orange2)
property_array.append(orange3)
property_array.append(free_parking)
property_array.append(red1)
property_array.append(chance)
property_array.append(red2)
property_array.append(red3)
property_array.append(bno)
property_array.append(yellow1)
property_array.append(yellow2)
property_array.append(water_works)
property_array.append(yellow3)
property_array.append(go_to_jail)
property_array.append(green1)
property_array.append(green2)
property_array.append(community_chest)
property_array.append(green3)
property_array.append(short_line)
property_array.append(chance)
property_array.append(blue1)
property_array.append(luxury_tax)
property_array.append(blue2)

def turn(player):
    playing = True
    rolled = False
    while(playing):
        choice = input(player.name + ", what would you like to do? ")
        if choice.lower() == "roll" or choice.lower() == "r":
            if not(rolled):
                player.Roll()
                rolled = True
            else:
                print("You have already rolled for this turn")

        if choice.lower() == "buy" or choice.lower() == "b":
            player.Buy()

        if choice.lower() == "money" or choice.lower() == "m":
            print("You have $" + str(player.money))

        if choice.lower() == "square" or choice.lower() == "s":
            print("You are on " + property_array[player.square].name)
            
        if choice.lower() == "kill":
            player_array = [player_array[0]]

        if choice.lower() == "end" or choice.lower() == "e":
            if not(rolled):
                print("You need to roll before you end your turn")
            else:
                playing = False

Nathan = Player("Nathan")
Benjamin = Player("Benjamin")
Joshua = Player("Joshua")
Elizabeth = Player("Elizabeth")

player_array = [Nathan, Benjamin, Joshua, Elizabeth]

player_index = 0
while len(player_array) > 1:
    turn(player_array[player_index])

    if player_array[player_index].money <= 0:
        player_array.remove(player_array[player_index])
        player_index -= 1

    player_index = (player_index + 1) % len(player_array)
    
print(player_array[0].name + ", You Win!")
