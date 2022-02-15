from Action import Action

class Railroad:
    cost = 200
    rent = 25

    def __init__(self, name):
        self.name = name
        self.ownership = 'Unowned'
        self.mortgaged = False

    def add_to_group(self, group):
        self.group = group

    def get_action(self, current_player):
        if self.ownership == 'Unowned':
            message = self.name + ' - Railroad - Cost: $' + str(self.cost) + ' - Base Rent: $' + str(self.rent) + '\n' + self.ownership
            action = Action('for sale', {'player': current_player, 'property': self, 'cost': self.cost})
        elif self.ownership == current_player:
            message = self.name + ' - Railroad'
            action = Action('error', current_player.name + ', you own this railroad!')
        elif self.mortgaged:
            message = self.name + ' - Railroad - Owned by: ' + self.ownership.name
            action = Action('error', self.name + ' is currently mortgaged')
        else:
            railroads_owned = self.ownership.num_railroads_owned(self)
            pay_rent = (self.rent * (2**(railroads_owned - 1)))
            message = self.name + ' - Railroad - Owned by: ' + self.ownership.name + ' - Current Rent: $' + str(pay_rent)
            action = Action('make payment', {'from': current_player, 'to': self.ownership, 'amount': pay_rent})
        return message, action