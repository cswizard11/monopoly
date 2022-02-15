from Action import Action

class Utility:
    cost = 150
    def __init__(self, name):
        self.name = name
        self.ownership = 'Unowned'
        self.mortgaged = False

    def add_to_group(self, group):
        self.group = group

    def get_action(self, current_player):
        if self.ownership == 'Unowned':
            message = self.name + ' - Utility - Cost: $' + str(self.cost) + ' - Base Rent: 4 times amount shown on dice'
            action = Action('for sale', {'player': current_player, 'property': self, 'cost': self.cost})
        elif self.ownership == current_player:
            message = self.name + ' - Utility'
            action = Action('error', current_player.name + ', you own this utility!')
        elif self.mortgaged:
            message = self.name + ' - Railroad - Owned by: ' + self.ownership.name
            action = Action('error', self.name + ' is currently mortgaged')
        else:
            if self.ownership.complete_property_group(self):
                pay_rent = current_player.dice_roll * 10
                message = self.name + ' - Utility - Owned by: ' + self.ownership.name + ' - Current Rent: 10 times amount shown on dice - $' + str(pay_rent)
            else:
                pay_rent = current_player.dice_roll * 4
                message = self.name + ' - Utility - Owned by: ' + self.ownership.name + ' - Current Rent: 4 times amount shown on dice - $' + str(pay_rent)
            action = Action('make payment', {'from': current_player, 'to': self.ownership, 'amount': pay_rent})
        return message, action