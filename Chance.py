from Action import Action
from Player import Player
from random import randint

class Chance:
    def __init__(self):
        self.full_deck = []
        self.empty_deck = []

        self.building_loan = ('Your building loan matures. Collect $150', Action('make payment', {'from': 'BANK', 'to': 'current player', 'amount': 150}))
        self.board_chairman = ('You have been elected chairman of the board. Pay each player $50',
                                Action('make payment', {'from': 'current player', 'to': 'ALL', 'amount': 50}))
        self.dividend = ('Bank pays you dividend of $50', Action('make payment', {'from': 'BANK', 'to': 'current player', 'amount': 50}))
        self.speeding_fine = ('Speeding fine $15', Action('make payment', {'from': 'current player', 'to': 'BANK', 'amount': 15}))
        self.gtj = ('Go to Jail', Action('go to jail', {'player': 'current player'}))
        self.advance_to_go = ('Advance to Go. (Collect $200)', Action('move to square', {'player': 'current player', 'name': 'GO'}))
        self.repairs = ('Make general repairs on all your properties: for each house pay $25, for each hotel pay $100', 
                         Action('repairs', {'player': 'current player', 'house cost': 25, 'hotel cost': 100}))
        self.get_out_of_jail_free = ('Get out of jail free. This card may be kept until needed or traded',
                                      Action('goojfc', {'player': 'current player', 'from': 'chance'}))
        self.advance_to_st_charles = ('Advance to St. Charles Place. If you pass go, collect $200',
                                       Action('move to square', {'player': 'current player', 'name': 'St. Charles Place'}))
        self.advance_to_illinois = ('Advance to Illinois Avenue. If you pass go, collect $200',
                                     Action('move to square', {'player': 'current player', 'name': 'Illinois Avenue'}))
        self.advance_to_boardwalk = ('Advance to Boardwalk', Action('move to square', {'player': 'current player', 'name': 'Boardwalk'}))
        self.advance_to_reading_rr = ('Take a trip to Reading Railroad. If you pass go, collect $200',
                                       Action('move to square', {'player': 'current player', 'name': 'Reading Railroad'}))
        self.back_three = ('Go back 3 spaces', Action('move to square', {'player': 'current player', 'name': 'BACK', 'spaces': 3}))
        self.nearest_utility = ('Advance to the nearest utility\nIf UNOWNED, you may buy it from the bank\n' + 
                                'If OWNED, throw dice and pay the owner 10 times the amount thrown',
                                 Action('move to square', {'player': 'current player', 'name': 'NEXT UTILITY', 'payment multiplier': 10}))
        self.nearest_rr = ('Advance to the nearest railroad\nIf UNOWNED, you may buy it from the bank\n' + 
                                'If OWNED, pay the owner twice the rental to which they are otherwise entitled',
                                 Action('move to square', {'player': 'current player', 'name': 'NEXT RAILROAD', 'payment multiplier': 2}))
        
        self.empty_deck.append(self.building_loan)
        self.empty_deck.append(self.board_chairman)
        self.empty_deck.append(self.dividend)
        self.empty_deck.append(self.speeding_fine)
        self.empty_deck.append(self.gtj)
        self.empty_deck.append(self.advance_to_go)
        self.empty_deck.append(self.repairs)
        self.empty_deck.append(self.get_out_of_jail_free)
        self.empty_deck.append(self.advance_to_st_charles)
        self.empty_deck.append(self.advance_to_illinois)
        self.empty_deck.append(self.advance_to_boardwalk)
        self.empty_deck.append(self.advance_to_reading_rr)
        self.empty_deck.append(self.back_three)
        self.empty_deck.append(self.nearest_utility)
        self.empty_deck.append(self.nearest_rr)
        self.empty_deck.append(self.nearest_rr)

    def shuffle(self):
        #print('Shuffling Chance cards...')
        while len(self.empty_deck) > 0:
            card_num = randint(0, len(self.empty_deck) - 1)
            card = self.empty_deck.pop(card_num)
            self.full_deck.append(card)

    def draw(self, current_player):
        card = self.full_deck.pop(0)
        if not(card == self.get_out_of_jail_free):
            self.empty_deck.append(card)
        if len(self.full_deck) == 0:
            self.shuffle()
        for i in card[1].information:
            if (card[1].information[i] == 'current player') or (type(card[1].information[i]) == Player):
                card[1].information[i] = current_player
        return card

    def return_goojf(self):
        self.empty_deck.append(self.get_out_of_jail_free)