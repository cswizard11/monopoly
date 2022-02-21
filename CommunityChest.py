from Action import Action
from Player import Player
from random import randint

class CommunityChest:
    def __init__(self):
        self.full_deck = []
        self.empty_deck = []

        self.consultancy_fee = ('Recieve $25 consultancy fee', Action('make payment', {'from': 'BANK', 'to': 'current player', 'amount': 25}))
        self.drs_fee = ('Doctor\'s fees. Pay $50', Action('make payment', {'from': 'current player', 'to': 'BANK', 'amount': 50}))
        self.holiday_fund = ('Holiday fund matures. Recieve $100', Action('make payment', {'from': 'BANK', 'to': 'current player', 'amount': 100}))
        self.life_insurance = ('Life insurance matures. Collect $100', Action('make payment', {'from': 'BANK', 'to': 'current player', 'amount': 100}))
        self.stock_sale = ('From sale of stock you get $50', Action('make payment', {'from': 'BANK', 'to': 'current player', 'amount': 50}))
        self.income_tax_refund = ('Income tax refund. Collect $20', Action('make payment', {'from': 'BANK', 'to': 'current player', 'amount': 20}))
        self.school_fee = ('School fees. Pay $50', Action('make payment', {'from': 'current player', 'to': 'BANK', 'amount': 50}))
        self.bank_error = ('Bank error in your favor. Collect $200', Action('make payment', {'from': 'BANK', 'to': 'current player', 'amount': 200}))
        self.hospital_fee = ('Hospital fees. Pay $100', Action('make payment', {'from': 'current player', 'to': 'BANK', 'amount': 100}))
        self.beauty_contest = ('You have won second prize in a beauty contest. Collect $10',
                                Action('make payment', {'from': 'BANK', 'to': 'current player', 'amount': 10}))
        self.inheritance = ('You inherit $100', Action('make payment', {'from': 'BANK', 'to': 'current player', 'amount': 100}))
        self.birthday = ('It is your birthday. Collect $10 from every player', Action('make payment', {'from': 'ALL', 'to': 'current player', 'amount': 10}))
        self.gtj = ('Go to Jail', Action('go to jail', {'player': 'current player'}))
        self.advance_to_go = ('Advance to Go. (Collect $200)', Action('move to square', {'player': 'current player', 'name': 'GO'}))
        self.repairs = ('You are assessed for street repairs: pay $40 per house and $115 per hotel you own', 
                         Action('repairs', {'player': 'current player', 'house cost': 40, 'hotel cost': 115}))
        self.get_out_of_jail_free = ('Get out of jail free. This card may be kept until needed or traded',
                                      Action('goojfc', {'player': 'current player', 'from': 'cc'}))

        self.empty_deck.append(self.consultancy_fee)
        self.empty_deck.append(self.drs_fee)
        self.empty_deck.append(self.holiday_fund)
        self.empty_deck.append(self.life_insurance)
        self.empty_deck.append(self.stock_sale)
        self.empty_deck.append(self.income_tax_refund)
        self.empty_deck.append(self.school_fee)
        self.empty_deck.append(self.bank_error)
        self.empty_deck.append(self.hospital_fee)
        self.empty_deck.append(self.beauty_contest)
        self.empty_deck.append(self.inheritance)
        self.empty_deck.append(self.birthday)
        self.empty_deck.append(self.gtj)
        self.empty_deck.append(self.advance_to_go)
        self.empty_deck.append(self.repairs)
        self.empty_deck.append(self.get_out_of_jail_free)

    def shuffle(self):
        #print('Shuffling Community Chest cards...')
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