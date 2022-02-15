from Action import Action
from Player import Player

class SpecialSpace:
    def __init__(self, name, message, action_type=None, action_information={}):
        self.name = name
        self.message = message
        self.action_type = action_type
        self.action_information = action_information

    def get_action(self, current_player):
        for i in self.action_information:
            if (self.action_information[i] == 'current player') or (type(self.action_information[i]) == Player):
                self.action_information[i] = current_player
        message = self.name + '\n' + self.message
        action = Action(self.action_type, self.action_information)
        return message, action