from Board import Board
from Player import Player
from Action import Action
from Property import Property
from Railroad import Railroad
from SpecialSpace import SpecialSpace
from Utility import Utility

class Game:
    def __init__(self):
        self.board = Board()
        self.player_array = []
        self.choice_list = ['mortgage', 'unmortgage', 'sell house', 'sell hotel']
        self.always_option = ['trade', 'board state', 'player info']
        self.question_map = {'mortgage': 'Which property would you like to mortgage? ', 
                             'unmortgage': 'Which property would you like to unmortgage? ',  
                             'sell house': 'Which property would you like to sell a house from? ',
                             'sell hotel': 'Which property would you like to sell a hotel from? ',
                             'buy house': 'Which property would you like to buy a house for? ',
                             'buy hotel': 'Which property would you like to buy a hotel for? '}

    def setup(self):
        self.num_players = 0
        while not(1 < self.num_players < 7):
            self.num_players = input('How many players are playing? (2-6) ')
            try:
                self.num_players = int(self.num_players)
            except:
                self.num_players = 0

        for i in range(1, self.num_players + 1):
            name = input('Name for Player ' + str(i) + ' ')
            player = Player(name)
            self.player_array.append(player)

        print('Turn order will be determined by dice roll, highest roll goes first')
        for i in self.player_array:
            input(i.name + ', press enter to roll')
            i.roll()

        same_rolls = self.player_array.copy()
        same_rolls.sort(key=(lambda x: x.dice_roll), reverse=True)
        same_rolls = [x for x in same_rolls if x.dice_roll == same_rolls[0].dice_roll]
        while len(same_rolls) > 1:
            print('There is a tie for the highest roll')
            for i in same_rolls:
                input(i.name + ', press enter to roll')
                i.roll()
            same_rolls.sort(key=(lambda x: x.dice_roll), reverse=True)
            same_rolls = [x for x in same_rolls if x.dice_roll == same_rolls[0].dice_roll]

        highest_roller = same_rolls[0]
        print(highest_roller.name + ' will go first')
        while not(self.player_array[0] == highest_roller):
            self.player_array.append(self.player_array.pop(0))
        
    def handleAction(self, action):
        if action.type == 'make payment':
            return self.handle_payment(action)
        elif action.type == 'for sale':
            return self.handle_for_sale(action)
        elif action.type == 'auction':
            return self.handle_auction(action)
        elif action.type == 'buy property':
            return self.handle_buy_property(action)
        elif action.type == 'mortgage':
            return self.handle_mortgage(action)
        elif action.type == 'unmortgage':
            return self.handle_unmortgage(action)
        elif action.type == 'sell house':
            return self.handle_sell_house(action)
        elif action.type == 'sell hotel':
            return self.handle_sell_hotel(action)
        elif action.type == 'buy house':
            return self.handle_buy_house(action)
        elif action.type == 'buy hotel':
            return self.handle_buy_hotel(action)
        elif action.type == 'trade':
            return self.handle_trade(action)
        elif action.type == 'board state':
            return self.handle_board_state(action)
        elif action.type == 'player info':
            return self.handle_player_info(action)
        elif action.type == 'draw a card':
            return self.handle_draw_card(action)
        elif action.type == 'move to square':
            return self.handle_move_to_square(action)
        elif action.type == 'repairs':
            return self.handle_repairs(action)
        elif action.type == 'goojfc':
            return self.handle_goojfc(action)
        elif action.type == 'go to jail':
            return self.handle_go_to_jail(action)
        elif action.type == 'attempt to leave jail':
            return self.handle_attempt_to_leave_jail(action)
        elif action.type == 'bankrupt':
            return self.handle_bankrupt(action)
        elif action.type == 'error':
            print(action.information)
            return None

    def handle_payment(self, action):
        money_from = action.information['from']
        money_to = action.information['to']
        amount = action.information['amount']
        bankrupcy = False
        next_action = None
        input('Press enter to continue')
        if money_from == 'ALL':
            other_players = [x for x in self.player_array if not(x.bankrupt)]
            other_players.remove(money_to)
            for i in other_players:
                self.handleAction(Action('make payment', {'from': i, 'to': money_to, 'amount': amount}))
        elif money_to == 'ALL':
            other_players = [x for x in self.player_array if not(x.bankrupt)]
            other_players.remove(money_from)
            if self.bankrupcy_check(money_from, amount*len(other_players)):
                bankrupcy = True
                money_to = 'BANK'
            else:
                for i in other_players:
                    money_from.money -= amount
                    i.money += amount
                    print(money_from.name + ' paid ' + i.name + ' $' + str(amount))
                    i.print_money()
                money_from.print_money()
        elif money_from == 'BANK':
            money_to.money += amount
            print('The bank paid ' + money_to.name + ' $' + str(amount))
            money_to.print_money()
        elif money_to == 'BANK':
            if self.bankrupcy_check(money_from, amount):
                bankrupcy = True
            else:
                money_from.money -= amount
                print(money_from.name + ' paid the bank $' + str(amount))
                money_from.print_money()
        else:
            if self.bankrupcy_check(money_from, amount):
                bankrupcy = True
            else:
                money_from.money -= amount
                money_to.money += amount
                print(money_from.name + ' paid ' + money_to.name + ' $' + str(amount))
                money_from.print_money()
                money_to.print_money()
        if bankrupcy:
            self.handleAction(Action('bankrupt', {'bankrupt player': money_from, 'bankrupt to': money_to}))
        return next_action

    def handle_for_sale(self, action):
        player = action.information['player']
        property = action.information['property']
        cost = property.cost
        if cost > player.money:
            print(player.name + ', you can\'t afford this property.')
            self.raise_money(player)
        if cost > player.money:
            next_action = Action('auction', {'player': player, 'property': property, 'cost': 10, 'players bidding': self.player_array.copy()})
        else:
            options = ['buy property', 'auction']
            player.print_money()
            response = self.get_input(player.name + ', would you like to buy this property for $' + str(cost) + '? ', options, cancel=False)
            next_action = Action(options[response], {'player': player, 'property': property, 'cost': property.cost})
        return next_action

    def handle_auction(self, action):
        player = action.information['player']
        property = action.information['property']
        remove_player = False
        try:
            players_bidding = action.information['players bidding']
            cost = action.information['cost']
        except:
            players_bidding = [x for x in self.player_array if not(x.bankrupt)]
            cost = 10
        if cost >= player.money:
            print(player.name + ', you can\'t afford to auction.')
            self.raise_money(player)
        if (cost + 100) <= player.money:
            options = [1, 10, 100]
        elif (cost + 10) <= player.money:
            options = [1, 10]
        elif (cost + 1) <= player.money:
            options = [1]
        else:
            remove_player = True
        if not(remove_player):
            options_str = ['$' + str(x) for x in options]
            print('Current bid is $' + str(cost))
            response = self.get_input(player.name + ', how much would you like to bid? ', options_str, cancel='No bid')
            if response == len(options):
                remove_player = True
            else:
                cost += options[response]
        index = players_bidding.index(player)
        next_player = players_bidding[(index + 1) % len(players_bidding)]
        if remove_player:
            players_bidding.remove(player)
        if len(players_bidding) == 1:
            if cost == 10:
                next_action = Action('auction', {'player': next_player, 'property': property, 'cost': cost, 'players bidding': players_bidding})
            else:
                next_action = Action('buy property', {'player': next_player, 'property': property, 'cost': cost})
        elif len(players_bidding) == 0:
            print(property.name + ' will remain unowned')
            property.ownership = 'Unowned'
            next_action = None
        else:
            next_action = Action('auction', {'player': next_player, 'property': property, 'cost': cost, 'players bidding': players_bidding})
        return next_action

    def handle_buy_property(self, action):
        player = action.information['player']
        property = action.information['property']
        cost = action.information['cost']
        player.money -= cost
        player.properties_owned.append(property)
        property.ownership = player
        print(player.name + ' bought ' + property.name + ' for $' + str(cost))
        player.print_money()
        player.sort_properties(self.board.property_array)
        return None

    def handle_mortgage(self, action):
        player = action.information['player']
        property = action.information['property']
        property.mortgaged = True
        player.money += property.cost // 2
        print(property.name + ' is now mortgaged')
        player.print_money()
        return None

    def handle_unmortgage(self, action):
        player = action.information['player']
        property = action.information['property']
        property.mortgaged = False
        player.money -= ((property.cost // 2) // 10) + (property.cost // 2)
        print(property.name + ' is now unmortgaged')
        player.print_money()
        return None

    def handle_sell_house(self, action):
        player = action.information['player']
        property = action.information['property']
        player.money += property.group.house_cost // 2
        property.houses -= 1
        self.board.houses += 1
        print(property.name + ' now has ' + str(property.houses) + ' houses')
        player.print_money()
        return None

    def handle_sell_hotel(self, action):
        player = action.information['player']
        property = action.information['property']
        player.money += property.group.house_cost // 2
        property.hotels -= 1
        self.board.hotels += 1
        print(property.name + ' now has ' + str(property.hotels) + ' hotels')
        player.print_money()
        return None

    def handle_buy_house(self, action):
        player = action.information['player']
        property = action.information['property']
        player.money -= property.group.house_cost
        property.houses += 1
        self.board.houses -= 1
        print(property.name + ' now has ' + str(property.houses) + ' houses')
        player.print_money()
        return None

    def handle_buy_hotel(self, action):
        player = action.information['player']
        property = action.information['property']
        player.money -= property.group.house_cost
        property.hotels += 1
        self.board.hotels -= 1
        print(property.name + ' now has ' + str(property.hotels) + ' hotel')
        player.print_money()
        return None

    def handle_trade(self, action):
        player_offering = action.information['player offering']
        next_action = None
        try:
            player_recieving = action.information['player recieving']
        except:
            options = [x for x in self.player_array if not(x.bankrupt)]
            options.remove(player_offering)
            options_str = [x.name for x in options]
            response = self.get_input('Who would you like to trade with? ', options_str)
            if response == len(options):
                next_action = Action('error', 'Trade canceled')
            else:
                player_recieving = options[response]
        if next_action == None:
            ask_for_list, ask_for_list_str = self.get_trade_items(player_recieving,
                                                                  player_offering.name + ', what would you like from '
                                                                  + player_recieving.name + '? ',
                                                                  player_offering.name + ', how much more money would you like from '
                                                                  + player_recieving.name + '? ')
            give_list, give_list_str = self.get_trade_items(player_offering,
                                                            player_offering.name + ', what would you like to give '
                                                            + player_recieving.name + '? ',
                                                            player_offering.name + ', how much more money would you like to give '
                                                            + player_recieving.name + '? ')
            print(player_offering.name + ' is asking for:')
            print(self.list_items(ask_for_list_str, cancel=False)[0])
            print(player_offering.name + ' is willing to give:')
            print(self.list_items(give_list_str, cancel=False)[0])
            confirm_options = ['Accept Trade', 'Decline Trade', 'Counter Offer']
            trade_choice = confirm_options[self.get_input(player_recieving.name + ', is this trade acceptable? ', confirm_options, cancel=False)]
            if trade_choice == 'Accept Trade':
                print('Trade accepted')
                for i in ask_for_list:
                    if type(i) == int:
                        player_offering.money += i
                        player_recieving.money -= i
                    elif i == 'Get Out of Jail Free card':
                        giving = player_recieving.get_out_of_jail_free_cards.pop(0)
                        player_offering.get_out_of_jail_free_cards.append(giving)
                    else:
                        player_offering.properties_owned.append(i)
                        player_recieving.properties_owned.remove(i)
                        i.ownership = player_offering
                for i in give_list:
                    if type(i) == int:
                        player_recieving.money += i
                        player_offering.money -= i
                    elif i == 'Get Out of Jail Free card':
                        giving = player_offering.get_out_of_jail_free_cards.pop(0)
                        player_recieving.get_out_of_jail_free_cards.append(giving)
                    else:
                        player_recieving.properties_owned.append(i)
                        player_offering.properties_owned.remove(i)
                        i.ownership = player_recieving
                player_offering_mortgage_list = [x for x in ask_for_list if not(type(x) == int)]
                player_offering_mortgage_list = [x for x in player_offering_mortgage_list if not(type(x) == str)]
                player_offering_mortgage_list = [x for x in player_offering_mortgage_list if x.mortgaged]
                player_recieving_mortgage_list = [x for x in give_list if not(type(x) == int)]
                player_recieving_mortgage_list = [x for x in player_recieving_mortgage_list if not(type(x) == str)]
                player_recieving_mortgage_list = [x for x in player_recieving_mortgage_list if x.mortgaged]
                if len(player_offering_mortgage_list) > 0:
                    self.recieved_morgaged_properties(player_offering, player_offering_mortgage_list)
                if len(player_recieving_mortgage_list) > 0:
                    self.recieved_morgaged_properties(player_recieving, player_recieving_mortgage_list)
            elif trade_choice == 'Decline Trade':
                print('Trade declined')
                next_action = None
            elif trade_choice == 'Counter Offer':
                next_action = Action('trade', {'player offering': player_recieving, 'player recieving': player_offering})
            player_offering.sort_properties(self.board.property_array)
            player_recieving.sort_properties(self.board.property_array)
        return next_action

    def handle_board_state(self, action):
        current_players = [x for x in self.player_array if not(x.bankrupt)]
        for i in current_players:
            if not(type(self.board.property_array[i.square]) == SpecialSpace):
                print(i.name + ' is on ' + self.board.property_array[i.square].name + ' - '
                + self.board.property_array[i.square].group.name + ' - space number ' + str(i.square + 1))
            else:
                print(i.name + ' is on ' + self.board.property_array[i.square].name + ' - space number ' + str(i.square + 1))
        unowned_properties = [x for x in self.board.property_array if not(type(x) == SpecialSpace)]
        unowned_properties = list(filter(lambda x: x.ownership == 'Unowned', unowned_properties))
        unowned_properties = [x.name + ' - ' + x.group.name for x in unowned_properties]
        print('Current unowned properties:')
        print(self.list_items(unowned_properties, False)[0])
        print('There are ' + str(self.board.houses) + ' houses left to buy')
        print('There are ' + str(self.board.hotels) + ' hotels left to buy')
        return None

    def handle_player_info(self, action):
        current_players = [x for x in self.player_array if not(x.bankrupt)]
        current_players_str = [x.name for x in current_players]
        about = self.get_input('Who would you like information about? ', current_players_str)
        if not(about == len(current_players_str)):
            player = current_players[about]
            player_stuff = [x.name + ' - ' + x.group.name + ' - ' + str(x.houses) + ' houses - ' + str(x.hotels)
            + ' hotels' for x in player.properties_owned if type(x) == Property]
            for i in player.properties_owned:
                if not(type(i) == Property):
                    player_stuff.append(i.name + ' - ' + i.group.name)
            for i in player.get_out_of_jail_free_cards:
                player_stuff.append('Get Out of Jail Free card')
            player_stuff.append('$' + str(player.money))
            print(player.name + ' currently has:')
            print(self.list_items(player_stuff, False)[0])
        return None

    def handle_draw_card(self, action):
        card_type = action.information['card type']
        player = action.information['player']
        input('Press enter to draw a card')
        if card_type == 'cc':
            card = self.board.cc_cards.draw(player)
        elif card_type == 'chance':
            card = self.board.chance_cards.draw(player)
        print(card[0])
        return card[1]

    def handle_move_to_square(self, action):
        player = action.information['player']
        next_square = action.information['name']
        if next_square == 'BACK':
            spaces = action.information['spaces']
            player.square = (player.square - (spaces + player.dice_roll)) % len(self.board.property_array)
            next_action = self.advance_player(player, go_check=False)
        elif next_square == 'NEXT UTILITY':
            next_action = self.move_to_type(player, action, Utility)
        elif next_square == 'NEXT RAILROAD':
            next_action = self.move_to_type(player, action, Railroad)
        else:
            for i in self.board.property_array:
                if i.name == next_square:
                    new_space = self.board.property_array.index(i)
                    break
            if new_space < player.square:
                print(player.name + ', you have passed Go! You have collected $200')
                player.money += 200
                player.print_money()
            player.square = (new_space - player.dice_roll) % len(self.board.property_array)
            next_action = self.advance_player(player, go_check=False)
        return next_action

    def handle_repairs(self, action):
        player = action.information['player']
        house_cost = action.information['house cost']
        hotel_cost = action.information['hotel cost']
        money_owed = 0
        properties_to_assess = [x for x in player.properties_owned if type(x) == Property]
        for i in properties_to_assess:
            if i.hotels > 0:
                money_owed += hotel_cost * i.hotels
            else:
                money_owed += house_cost * i.houses
        print(player.name + ', you owe $' + str(money_owed) + ' for house and hotel repairs')
        if money_owed > 0:
            next_action = Action('make payment', {'from': player, 'to': 'BANK', 'amount': money_owed})
        else:
            next_action = None
        return next_action

    def handle_goojfc(self, action):
        player = action.information['player']
        card_type = action.information['from']
        player.get_out_of_jail_free_cards.append(card_type)
        return None

    def handle_go_to_jail(self, action):
        player = action.information['player']
        player.doubles = 0
        player.square = self.board.property_array.index(self.board.jail)
        player.jail = 1
        print(player.name + ', go directly to jail. Do not pass Go. Do not collect $200')
        return None

    def handle_attempt_to_leave_jail(self, action):
        player = action.information['player']
        options = ['Roll']
        if player.money >= 50:
            options.append('Pay $50')
        if len(player.get_out_of_jail_free_cards) > 0:
            options.append('Use a Get Out of Jail Free card')
        choice = self.get_input('How would you like to leave jail? ', options)
        if choice == len(options):
            print('Choice canceled')
            next_action = None
        elif options[choice] == 'Pay $50':
            player.money -= 50
            player.jail = 0
            print(player.name + ' paid $50 to leave jail')
            player.print_money()
            next_action = None
        elif options[choice] == 'Roll':
            player.roll()
            if player.doubles == 1:
                print(player.name + ' sucessfully rolled doubles and has left jail')
                player.jail = 0
                next_action = self.advance_player(player)
            else:
                player.jail += 1
                print(player.name + ' did not roll doubles')
                next_action = None
                if player.jail > 3:
                    print(player.name + ', you have been in jail for 3 turns and must now pay $50')
                    if self.bankrupcy_check(player, 50):
                        next_action = Action('bankrupt', {'bankrupt player': player, 'bankrupt to': 'BANK'})
                    else:
                        player.money -= 50
                        player.print_money()
                        player.jail = 0
                        next_action = self.advance_player(player)
        elif options[choice] == 'Use a Get Out of Jail Free card':
            self.return_card(player.get_out_of_jail_free_cards.pop(0))
            player.jail = 0
            print(player.name + ' used a Get Out of Jail Free card to leave jail')
            next_action = None
        return next_action

    def handle_bankrupt(self, action):
        bankrupt_player = action.information['bankrupt player']
        bankrupt_to = action.information['bankrupt to']
        bankrupt_player.bankrupt = True
        bankrupt_player.pass_turn = True
        next_action = None
        print(bankrupt_player.name + ' has gone bankrupt!')
        bankrupt_players = 0
        for i in self.player_array:
            if i.bankrupt:
                bankrupt_players += 1
        if not(len(self.player_array) - 1 == bankrupt_players):
            if bankrupt_to == 'BANK':
                print(bankrupt_player.name + '\'s properties will now be auctioned')
                for i in bankrupt_player.get_out_of_jail_free_cards:
                    self.return_card(i)
                players_left = [x for x in self.player_array if not(x.bankrupt)]
                next_player = players_left[0]
                for i in bankrupt_player.properties_owned:
                    print(i.name)
                    i.mortgaged = False
                    if type(i) == Property:
                        self.board.houses += i.houses
                        self.board.hotels += i.hotels
                        i.houses = 0
                        i.hotels = 0
                    auction_action = Action('auction', {'player': next_player, 'property': i})
                    while not(auction_action == None):
                        auction_action = self.handleAction(auction_action)
            else:
                print(bankrupt_to.name + ', you have recieved:')
                print('$' + str(bankrupt_player.money))
                bankrupt_to.money += bankrupt_player.money
                mortgaged_list = [x for x in bankrupt_player.properties_owned if x.mortgaged]
                for i in bankrupt_player.properties_owned:
                    bankrupt_to.properties_owned.append(i)
                    i.ownership = bankrupt_to
                    print(i.name + ' - ' + i.group.name)
                if len(bankrupt_player.get_out_of_jail_free_cards) > 0:
                    print(str(len(bankrupt_player.get_out_of_jail_free_cards)) + ' Get Out of Jail Free card(s)')
                    for i in bankrupt_player.get_out_of_jail_free_cards:
                        bankrupt_to.get_out_of_jail_free_cards.append(i)
                bankrupt_to.sort_properties(self.board.property_array)
                if len(mortgaged_list) > 0:
                    self.recieved_morgaged_properties(bankrupt_to, mortgaged_list)
        else:
            for i in self.player_array:
                i.pass_turn = True
        return next_action

    def move_to_type(self, player, action, square_type):
        multiplier = action.information['payment multiplier']
        old_roll = player.dice_roll
        old_doubles = player.doubles
        step = player.square + 1
        new_space = None
        while new_space == None:
            if type(self.board.property_array[step]) == square_type:
                new_space = step
                break
            step = (step + 1) % len(self.board.property_array)
        if new_space < player.square:
            print(player.name + ', you have passed Go! You have collected $200')
            player.money += 200
            player.print_money()
        player.square = new_space
        next_action = self.board.property_array[player.square].get_action(player)
        if next_action[1].type == 'make payment':
            if square_type == Utility:
                player.roll()
                next_action[1].information['amount'] = player.dice_roll * multiplier
                message = (self.board.property_array[player.square].name + ' - Utility - Owned by: '
                + self.board.property_array[player.square].ownership.name
                + ' - Current Rent: 10 times amount shown on dice - $' + str(next_action[1].information['amount']))
                print(message)
            elif square_type == Railroad:
                next_action[1].information['amount'] *= multiplier
                message = (self.board.property_array[player.square].name + ' - Railroad - Owned by: '
                + self.board.property_array[player.square].ownership.name + ' - Current Rent: $' + str(next_action[1].information['amount']))
                print(message)
        else:
            print(next_action[0])
        player.dice_roll = old_roll
        player.doubles = old_doubles
        return next_action[1]

    def recieved_morgaged_properties(self, player, mortgaged_list):
        for i in mortgaged_list:
            now_cost = ((i.cost // 2) // 10) + (i.cost // 2)
            later_cost = ((i.cost // 2) // 10)
            print(i.name + ' - ' + i.group.name + ' is currently mortgaged')
            options = ['Leave it mortgaged for $' + str(later_cost)]
            if player.money < now_cost:
                print(player.name + ', you can\'t afford to unmortgage this property for $' + str(now_cost))
                self.raise_money(player)
            if player.money >= now_cost:
                options.append('Unmortgage it now for $' + str(now_cost))
            choice = options[self.get_input(player.name + ', what would you like to do? ', options, cancel=False)]
            if choice == 'Leave it mortgaged for $' + str(later_cost):
                if self.bankrupcy_check(player, later_cost):
                    self.handleAction(Action('bankrupt', {'bankrupt player': player, 'bankrupt to': 'BANK'}))
                    break
                else:
                    self.handleAction(Action('make payment', {'from': player, 'to': 'BANK', 'amount': later_cost}))
            elif choice == 'Unmortgage it now for $' + str(now_cost):
                self.handleAction(Action('unmortgage', {'player': player, 'property': i}))

    def get_trade_items(self, player, question1, question2):
        choices = []
        for i in player.properties_owned:
            if not(type(i) == Property):
                choices.append(i)
            elif player.complete_property_group(i):
                legal = True
                for j in i.group.properties:
                    if j.houses > 0:
                        legal = False
                        break
                if legal:
                    choices.append(i)
            else:
                choices.append(i)
        choices_str = [x.name + ' - ' + x.group.name for x in choices]
        choices_str.append('Money')
        for i in player.get_out_of_jail_free_cards:
            choices_str.append('Get Out of Jail Free card')
        return_list = []
        return_list_str = []
        choice = None
        money_amount = 0
        while not(choice == len(choices_str)):
            old_money_amount = money_amount
            choice = self.get_input(question1, choices_str, cancel='Continue')
            if not(choice == len(choices_str)):
                if choices_str[choice] == 'Money':
                    get_money = None
                    money_options = []
                    while not(get_money == len(money_options)):
                        if (money_amount + 100) <= player.money:
                            money_options = [1, 10, 100]
                        elif (money_amount + 10) <= player.money:
                            money_options = [1, 10]
                        elif (money_amount + 1) <= player.money:
                            money_options = [1]
                        else:
                            money_options = []
                        player.print_money()
                        print('You have currently entered $' + str(money_amount))
                        get_money = self.get_input(question2, [str(x) for x in money_options], cancel='Continue')
                        if not(get_money == len(money_options)):
                            money_amount += money_options[get_money]
                    if money_amount > old_money_amount:
                        return_list.append(money_amount)
                        return_list_str.append('$' + str(money_amount))
                elif choices_str[choice] == 'Get Out of Jail Free card':
                    return_list_str.append('Get Out of Jail Free card')
                    return_list.append('Get Out of Jail Free card')
                    choices_str.remove('Get Out of Jail Free card')
                    choice -= 1
                else:
                    return_list_str.append(choices_str.pop(choice))
                    return_list.append(choices.pop(choice))
                    choice -= 1
        return return_list, return_list_str

    def list_items(self, item_list, cancel):
        dialog = '\n'
        num = 0
        for i in item_list:
            num += 1
            dialog += str(num) + '. '
            dialog += i
            dialog += '\n'
        if not(cancel == False):
            num += 1
            dialog += str(num) + '. ' + cancel + '\n'
        return dialog, num

    def get_input(self, prompt, item_array, cancel='Cancel'):
        items = self.list_items(item_array, cancel)
        print(items[0])
        answer = 0
        num = items[1]
        while not(0 < answer <= num):
            answer = input(prompt)
            try:
                answer = int(answer)
            except:
                answer = -1
        return answer - 1

    def raise_money(self, player):
        get_money = self.get_input('Would you like to raise money? ', ['no', 'yes'], cancel=False)
        if get_money:
            choice = None
            while not(choice == 'Cancel'):
                choices = player.need_money()
                for i in self.always_option:
                    choices.append(i)
                choice_num = self.get_input(player.name + ', what woud you like to do? ', choices)
                if len(choices) == choice_num:
                    choice = 'Cancel'
                else:
                    choice = choices[choice_num]
                    self.take_turn(player, choice)

    def bankrupcy_check(self, player, cost):
        if player.money < cost:
            print(player.name + ', you are about to go bankrupt')
            print('You have $' + str(player.money))
            print('You need $' + str(cost))
            self.raise_money(player)
        if player.money < cost:
            bankrupt = True
        else:
            bankrupt = False
        return bankrupt

    def advance_player(self, player, go_check=True):
        next_square = (player.square + player.dice_roll) % len(self.board.property_array)
        if (next_square < player.square) and go_check:
            print(player.name + ', you have passed Go! You have collected $200')
            player.money += 200
            player.print_money()
        player.square = next_square
        next_action = self.board.property_array[player.square].get_action(player)
        print(next_action[0])
        return next_action[1]

    def return_card(self, card_type):
        if card_type == 'cc':
            self.board.cc_cards.return_goojf()
        elif card_type == 'chance':
            None

    def take_turn(self, player, choice):
        if choice == 'roll':
            player.roll()
            if player.doubles == 3:
                print(player.name + ', you rolled 3 doubles in a row')
                action = Action('go to jail', {'player': player})
            else:
                action = self.advance_player(player)

        elif choice == 'trade':
            action = Action(choice, {'player offering': player})

        elif choice == 'board state' or choice == 'player info':
            action = Action(choice, None)

        elif choice == 'attempt to leave jail':
            action = Action(choice, {'player': player})
        
        elif choice == 'pass':
            player.pass_turn = True
            print('Passing the turn...')
            action = None
        else:
            legal_properties = player.get_legal_properties(choice)
            response = self.get_input(self.question_map[choice], legal_properties[0])
            if response == len(legal_properties[0]):
                action = Action('error', 'Choice canceled')
            else:
                action = Action(choice, {'player': player, 'property': legal_properties[1][response]})

        while not(action == None):
            action = self.handleAction(action)

    def play(self):
        input('Press enter to start the game')
        
        while len(self.player_array) > 1:
            current_player = self.player_array[0]
            current_player.dice_roll = None
            current_player.pass_turn = False
            current_player.doubles = 0
            while not(current_player.pass_turn):
                filterd_list = self.choice_list.copy()
                if self.board.houses > 0:
                    filterd_list.append('buy house')
                if self.board.hotels > 0:
                    filterd_list.append('buy hotel')
                filterd_list = [x for x in filterd_list if type(current_player.get_legal_properties(x)) == tuple]
                for i in self.always_option:
                    filterd_list.append(i)
                if current_player.dice_roll == None or current_player.doubles > 0:
                    if current_player.jail > 0:
                        filterd_list.append('attempt to leave jail')
                    else:
                        filterd_list.append('roll')
                else:
                    filterd_list.append('pass')
                
                choice_num = self.get_input(current_player.name + ', what would you like to do? ', filterd_list, cancel=False)
                choice = filterd_list[choice_num]
                self.take_turn(current_player, choice)

            move_player = self.player_array.pop(0)
            self.player_array.append(move_player)

            self.player_array = [x for x in self.player_array if not(x.bankrupt)]
        
        print(self.player_array[0].name + ', you WIN THE GAME!')