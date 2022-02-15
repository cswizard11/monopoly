from Property import Property
from random import randint

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.properties_owned = []
        self.square = 0
        self.dice_roll = None
        self.doubles = 0
        self.jail = 0
        self.get_out_of_jail_free_cards = []
        self.pass_turn = False
        self.bankrupt = False

    def roll(self):
        dice1 = randint(1,6)
        dice2 = randint(1,6)
        total = dice1 + dice2
        print(str(dice1) + ' + ' + str(dice2) + ' = ' + str(total))
        if dice1 == dice2:
            self.doubles += 1
            print('Doubles!')
        else:
            self.doubles = 0
        self.dice_roll = total

    def print_money(self):
        print(self.name + ' has $' + str(self.money))

    def sort_properties(self, board_property_list):
        self.properties_owned.sort(key=(lambda x: board_property_list.index(x)))
        just_properties = [x for x in self.properties_owned if type(x) == Property]
        not_properties = [x for x in self.properties_owned if not(type(x) == Property)]
        not_properties.sort(key=(lambda x: x.group.name))
        for i in not_properties:
            just_properties.append(i)
        self.properties_owned = just_properties

    def complete_property_group(self, property):
        complete = True
        for i in property.group.properties:
            if not(i in self.properties_owned):
                complete = False
        return complete

    def num_railroads_owned(self, railroad):
        railroads_owned = 0
        for i in railroad.group.properties:
            if i.ownership == self:
                railroads_owned += 1
        return railroads_owned

    def get_legal_properties(self, choice):
        if choice == 'mortgage':
            filtered_list = []
            for i in self.properties_owned:
                if not(type(i) == Property) or not(self.complete_property_group(i)):
                    filtered_list.append(i)
                else:
                    legal = True
                    for j in i.group.properties:
                        if j.houses > 0:
                            legal = False
                            break
                    if legal:
                        filtered_list.append(i)
            filtered_list = list(filter(lambda x: not(x.mortgaged), filtered_list))
            filtered_list_names = [x.name + ' - $' + str(x.cost//2) for x in filtered_list]
            if len(filtered_list_names) > 0:
                return (filtered_list_names, filtered_list)
            else:
                return 'Nothing availibe to mortgage'

        elif choice == 'unmortgage':
            filtered_list = list(filter(lambda x: x.mortgaged, self.properties_owned))
            filtered_list = list(filter(lambda x: self.money > ((x.cost // 2) // 10) + (x.cost // 2), filtered_list))
            filtered_list_names = [x.name + ' - $' + str(((x.cost // 2) // 10) + (x.cost // 2)) for x in filtered_list]
            if len(filtered_list_names) > 0:
                return (filtered_list_names, filtered_list)
            else:
                return 'Nothing availibe to unmortgage'

        elif choice == 'sell house':
            filtered_list = list(filter(lambda x: type(x) == Property, self.properties_owned))
            filtered_list = list(filter(lambda x: self.complete_property_group(x), filtered_list))
            filtered_list = list(filter(lambda x: x.hotels == 0, filtered_list))
            filtered_list = list(filter(lambda x: x.houses > 0, filtered_list))
            filtered_list_legal = []
            for i in filtered_list:
                legal = True
                for j in i.group.properties:
                    if (j.houses > i.houses) or (j.hotels > 0):
                        legal = False
                if legal:
                    filtered_list_legal.append(i)
            filtered_list_names = [x.name + ' - ' + str(x.houses) + ' houses - $' + str(x.group.house_cost // 2) for x in filtered_list_legal]
            if len(filtered_list_names) > 0:
                return (filtered_list_names, filtered_list_legal)
            else:
                return 'No availible properties'

        elif choice == 'sell hotel':
            filtered_list = list(filter(lambda x: type(x) == Property, self.properties_owned))
            filtered_list = list(filter(lambda x: self.complete_property_group(x), filtered_list))
            filtered_list = list(filter(lambda x: x.hotels == 1, filtered_list))
            filtered_list_names = [x.name + ' - ' + str(x.hotels) + ' hotel - $' + str(x.group.house_cost // 2) for x in filtered_list]
            if len(filtered_list_names) > 0:
                return (filtered_list_names, filtered_list)
            else:
                return 'No availible properties'
   
        elif choice == 'buy house':
            filtered_list = list(filter(lambda x: type(x) == Property, self.properties_owned))
            filtered_list = list(filter(lambda x: self.complete_property_group(x), filtered_list))
            filtered_list = list(filter(lambda x: x.houses < 4, filtered_list))
            filtered_list = list(filter(lambda x: self.money > x.group.house_cost, filtered_list))
            new_filtered_list = []
            for i in filtered_list:
                no_mortgaged_properties = True
                for j in i.group.properties:
                    if j.mortgaged:
                        no_mortgaged_properties = False
                if no_mortgaged_properties:
                    new_filtered_list.append(i)
            filtered_list_legal = []
            for i in new_filtered_list:
                legal = True
                for j in i.group.properties:
                    if j.houses < i.houses:
                        legal = False
                        break
                if legal:
                    filtered_list_legal.append(i)
            filtered_list_names = [x.name + ' - ' + str(x.houses) + ' houses - $' + str(x.group.house_cost) for x in filtered_list_legal]
            if len(filtered_list_names) > 0:
                return (filtered_list_names, filtered_list_legal)
            else:
                return 'No availible properties'

        elif choice == 'buy hotel':
            filtered_list = list(filter(lambda x: type(x) == Property, self.properties_owned))
            filtered_list = list(filter(lambda x: self.complete_property_group(x), filtered_list))
            filtered_list = list(filter(lambda x: x.hotels == 0, filtered_list))
            filtered_list = list(filter(lambda x: x.houses < 5, filtered_list))
            filtered_list = list(filter(lambda x: self.money > x.group.house_cost, filtered_list))
            filtered_list_legal = []
            for i in filtered_list:
                legal = True
                for j in i.group.properties:
                    if j.houses < 4:
                        legal = False
                        break
                if legal:
                    filtered_list_legal.append(i)
            filtered_list_names = [x.name + ' - ' + str(x.hotels) + ' hotels - $' + str(x.group.house_cost) for x in filtered_list_legal]
            if len(filtered_list_names) > 0:
                return (filtered_list_names, filtered_list_legal)
            else:
                return 'No availible properties'

    def need_money(self):
        choices = []
        if type(self.get_legal_properties('mortgage')) == tuple:
            choices.append('mortgage')
        if type(self.get_legal_properties('sell house')) == tuple:
            choices.append('sell house')
        if type(self.get_legal_properties('sell hotel')) == tuple:
            choices.append('sell hotel')
        return choices