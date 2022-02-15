from Action import Action

class Property:
    def __init__(self, name, cost, rent, house_prices):
        self.name = name
        self.cost = cost
        self.rent = rent
        self.house_prices = house_prices
        self.ownership = 'Unowned'
        self.houses = 0
        self.hotels = 0
        self.mortgaged = False

    def add_to_group(self, group):
        self.group = group

    def get_action(self, current_player):
        if self.ownership == 'Unowned':
            message = self.name + ' - ' + self.group.name + ' - Cost: $' + str(self.cost) + ' - Base Rent: $' + str(self.rent) + '\n' + self.ownership
            action = Action('for sale', {'player': current_player, 'property': self, 'cost': self.cost})
        elif self.ownership == current_player:
            message = self.name + ' - ' + self.group.name
            action = Action('error', current_player.name + ', you own this property!')
        elif self.mortgaged:
            message = self.name + ' - ' + self.group.name + ' - Owned by: ' + self.ownership.name
            action = Action('error', self.name + ' is currently mortgaged')
        else:
            pay_rent = self.rent
            if self.ownership.complete_property_group(self):
                if self.houses == 5:
                    pay_rent = self.house_prices[3]
                elif self.houses == 4:
                    pay_rent = self.house_prices[2]
                elif self.houses == 3:
                    pay_rent = self.house_prices[1]
                elif self.houses == 2:
                    pay_rent = self.house_prices[0]
                elif self.houses == 1:
                    pay_rent *= 5
                else:
                    pay_rent *= 2
            message = self.name + ' - ' + self.group.name + ' - Owned by: ' + self.ownership.name + ' - Current Rent: $' + str(pay_rent)
            action = Action('make payment', {'from': current_player, 'to': self.ownership, 'amount': pay_rent})
        return message, action