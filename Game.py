from Board import Board
from Player import Player
from Action import Action
from Property import Property
from Railroad import Railroad
from SpecialSpace import SpecialSpace
from Utility import Utility
import asyncio
import json

class Game(object):
    def __init__(self, web_info):
        self.web_info = web_info
        self.player_choice = None
        self.num_players = 0
        self.setup_complete = False
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

    async def setup(self):
        self.get_input('How many players are playing? (2-6)\n', [str(x) for x in range(2,7)], cancel=False)
        self.num_players = await self.get_web_input()
        self.get_input('Please enter your names\n', ['Player ' + str(x) for x in range(1, self.num_players + 1)])
        player_names = await self.get_web_input()
        for i in player_names:
            self.player_array.append(Player(i))

        self.web_info.information += 'Turn order will be determined by dice roll, highest roll goes first\n'
        for i in self.player_array:
            self.get_input(i.name + ', please roll\n', ['Click to roll!'], cancel=False)
            await self.get_web_input()
            self.web_info.information += i.roll()

        same_rolls = self.player_array.copy()
        same_rolls.sort(key=(lambda x: x.dice_roll), reverse=True)
        same_rolls = [x for x in same_rolls if x.dice_roll == same_rolls[0].dice_roll]
        while len(same_rolls) > 1:
            self.web_info.information += 'There is a tie for the highest roll\n'
            for i in same_rolls:
                self.get_input(i.name + ', please roll\n', ['Click to roll!'], cancel=False)
                await self.get_web_input()
                self.web_info.information += i.roll()
            same_rolls.sort(key=(lambda x: x.dice_roll), reverse=True)
            same_rolls = [x for x in same_rolls if x.dice_roll == same_rolls[0].dice_roll]

        highest_roller = same_rolls[0]
        self.web_info.information += highest_roller.name + ' will go first\n'
        while not(self.player_array[0] == highest_roller):
            self.player_array.append(self.player_array.pop(0))

        self.setup_complete = True
        self.get_input('You\'re ready to play!\n', ['Click to start the game!'], cancel=False)
        await self.get_web_input()
        
    async def handleAction(self, action):
        if action.type == 'make payment':
            return await self.handle_payment(action)
        elif action.type == 'for sale':
            return await self.handle_for_sale(action)
        elif action.type == 'auction':
            return await self.handle_auction(action)
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
            return await self.handle_trade(action)
        elif action.type == 'board state':
            return self.handle_board_state(action)
        elif action.type == 'player info':
            return await self.handle_player_info(action)
        elif action.type == 'draw a card':
            return await self.handle_draw_card(action)
        elif action.type == 'move to square':
            return self.handle_move_to_square(action)
        elif action.type == 'repairs':
            return self.handle_repairs(action)
        elif action.type == 'goojfc':
            return self.handle_goojfc(action)
        elif action.type == 'go to jail':
            return self.handle_go_to_jail(action)
        elif action.type == 'attempt to leave jail':
            return await self.handle_attempt_to_leave_jail(action)
        elif action.type == 'bankrupt':
            return await self.handle_bankrupt(action)
        elif action.type == 'error':
            self.web_info.information += action.information + '\n'
            return None

    async def handle_payment(self, action):
        money_from = action.information['from']
        money_to = action.information['to']
        amount = action.information['amount']
        bankrupcy = False
        next_action = None
        self.get_input('Click the button to continue\n', ['Continue'], cancel=False)
        await self.get_web_input()
        if money_from == 'ALL':
            other_players = [x for x in self.player_array if not(x.bankrupt)]
            other_players.remove(money_to)
            for i in other_players:
                await self.handleAction(Action('make payment', {'from': i, 'to': money_to, 'amount': amount}))
        elif money_to == 'ALL':
            other_players = [x for x in self.player_array if not(x.bankrupt)]
            other_players.remove(money_from)
            bankrupcy_check_bool = await self.bankrupcy_check(money_from, amount*len(other_players))
            if bankrupcy_check_bool:
                bankrupcy = True
                money_to = 'BANK'
            else:
                for i in other_players:
                    money_from.money -= amount
                    i.money += amount
                    self.web_info.information += money_from.name + ' paid ' + i.name + ' $' + str(amount) + '\n'
                    self.web_info.information += i.print_money()
                self.web_info.information += money_from.print_money()
        elif money_from == 'BANK':
            money_to.money += amount
            self.web_info.information += 'The bank paid ' + money_to.name + ' $' + str(amount) + '\n'
            self.web_info.information += money_to.print_money()
        elif money_to == 'BANK':
            bankrupcy_check_bool = await self.bankrupcy_check(money_from, amount)
            if bankrupcy_check_bool:
                bankrupcy = True
            else:
                money_from.money -= amount
                self.web_info.information += money_from.name + ' paid the bank $' + str(amount) + '\n'
                self.web_info.information += money_from.print_money()
        else:
            bankrupcy_check_bool = await self.bankrupcy_check(money_from, amount)
            if bankrupcy_check_bool:
                bankrupcy = True
            else:
                money_from.money -= amount
                money_to.money += amount
                self.web_info.information += money_from.name + ' paid ' + money_to.name + ' $' + str(amount) + '\n'
                self.web_info.information += money_from.print_money()
                self.web_info.information += money_to.print_money()
        if bankrupcy:
            await self.handleAction(Action('bankrupt', {'bankrupt player': money_from, 'bankrupt to': money_to}))
        return next_action

    async def handle_for_sale(self, action):
        player = action.information['player']
        property = action.information['property']
        cost = property.cost
        if cost > player.money:
            self.web_info.information += player.name + ', you can\'t afford this property.\n'
            await self.raise_money(player)
        if cost > player.money:
            next_action = Action('auction', {'player': player, 'property': property, 'cost': 10, 'players bidding': self.player_array.copy()})
        else:
            options = ['buy property', 'auction']
            self.web_info.information += player.print_money()
            self.get_input(player.name + ', would you like to buy this property for $' + str(cost) + '?\n', options, cancel=False)
            response = await self.get_web_input()
            next_action = Action(response, {'player': player, 'property': property, 'cost': property.cost})
        return next_action

    async def handle_auction(self, action):
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
            self.web_info.information += player.name + ', you can\'t afford to auction.\n'
            await self.raise_money(player)
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
            self.web_info.information += 'Current bid is $' + str(cost) + '\n'
            self.get_input(player.name + ', how much would you like to bid?\n', options_str, cancel='No bid')
            response = await self.get_web_input()
            if response == 'No bid':
                remove_player = True
            else:
                options_index = options_str.index(response)
                cost += options[options_index]
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
            self.web_info.information += property.name + ' will remain unowned\n'
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
        self.web_info.information += player.name + ' bought ' + property.name + ' for $' + str(cost) + '\n'
        self.web_info.information += player.print_money()
        player.sort_properties(self.board.property_array)
        return None

    def handle_mortgage(self, action):
        player = action.information['player']
        property = action.information['property']
        property.mortgaged = True
        player.money += property.cost // 2
        self.web_info.information += property.name + ' is now mortgaged\n'
        self.web_info.information += player.print_money()
        return None

    def handle_unmortgage(self, action):
        player = action.information['player']
        property = action.information['property']
        property.mortgaged = False
        player.money -= ((property.cost // 2) // 10) + (property.cost // 2)
        self.web_info.information += property.name + ' is now unmortgaged\n'
        self.web_info.information += player.print_money()
        return None

    def handle_sell_house(self, action):
        player = action.information['player']
        property = action.information['property']
        player.money += property.group.house_cost // 2
        property.houses -= 1
        self.board.houses += 1
        self.web_info.information += property.name + ' now has ' + str(property.houses) + ' houses\n'
        self.web_info.information += player.print_money()
        return None

    def handle_sell_hotel(self, action):
        player = action.information['player']
        property = action.information['property']
        player.money += property.group.house_cost // 2
        property.hotels -= 1
        self.board.hotels += 1
        self.web_info.information += property.name + ' now has ' + str(property.hotels) + ' hotels\n'
        self.web_info.information += player.print_money()
        return None

    def handle_buy_house(self, action):
        player = action.information['player']
        property = action.information['property']
        player.money -= property.group.house_cost
        property.houses += 1
        self.board.houses -= 1
        self.web_info.information += property.name + ' now has ' + str(property.houses) + ' houses\n'
        self.web_info.information += player.print_money()
        return None

    def handle_buy_hotel(self, action):
        player = action.information['player']
        property = action.information['property']
        player.money -= property.group.house_cost
        property.hotels += 1
        self.board.hotels -= 1
        self.web_info.information += property.name + ' now has ' + str(property.hotels) + ' hotel\n'
        self.web_info.information += player.print_money()
        return None

    async def handle_trade(self, action):
        player_offering = action.information['player offering']
        next_action = None
        try:
            player_recieving = action.information['player recieving']
        except:
            options = [x for x in self.player_array if not(x.bankrupt)]
            options.remove(player_offering)
            options_str = [x.name for x in options]
            self.get_input('Who would you like to trade with?\n', options_str)
            response = await self.get_web_input()
            if response == 'Cancel':
                next_action = Action('error', 'Trade canceled')
            else:
                index = options_str.index(response)
                player_recieving = options[index]
        if next_action == None:
            ask_for_list, ask_for_list_str = await self.get_trade_items(player_recieving,
                                                                  player_offering.name + ', what would you like from '
                                                                  + player_recieving.name + '?\n',
                                                                  player_offering.name + ', how much more money would you like from '
                                                                  + player_recieving.name + '?\n')
            give_list, give_list_str = await self.get_trade_items(player_offering,
                                                            player_offering.name + ', what would you like to give '
                                                            + player_recieving.name + '?\n',
                                                            player_offering.name + ', how much more money would you like to give '
                                                            + player_recieving.name + '?\n')
            self.web_info.information += player_offering.name + ' is asking for:\n'
            self.web_info.information += self.list_items(ask_for_list_str, cancel=False)[0]
            self.web_info.information += player_offering.name + ' is willing to give:\n'
            self.web_info.information += self.list_items(give_list_str, cancel=False)[0]
            confirm_options = ['Accept Trade', 'Decline Trade', 'Counter Offer']
            self.get_input(player_recieving.name + ', is this trade acceptable?\n', confirm_options, cancel=False)
            trade_choice = await self.get_web_input()
            if trade_choice == 'Accept Trade':
                self.web_info.information += 'Trade accepted\n'
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
                    await self.recieved_mortgaged_properties(player_offering, player_offering_mortgage_list)
                if len(player_recieving_mortgage_list) > 0:
                    await self.recieved_mortgaged_properties(player_recieving, player_recieving_mortgage_list)
            elif trade_choice == 'Decline Trade':
                self.web_info.information += 'Trade declined\n'
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
                self.web_info.information += (i.name + ' is on ' + self.board.property_array[i.square].name + ' - '
                + self.board.property_array[i.square].group.name + ' - space number ' + str(i.square + 1) + '\n')
            else:
                self.web_info.information += (i.name + ' is on ' + self.board.property_array[i.square].name + ' - space number ' + str(i.square + 1) + '\n')
        unowned_properties = [x for x in self.board.property_array if not(type(x) == SpecialSpace)]
        unowned_properties = list(filter(lambda x: x.ownership == 'Unowned', unowned_properties))
        unowned_properties = [x.name + ' - ' + x.group.name for x in unowned_properties]
        self.web_info.information += 'Current unowned properties:\n'
        self.web_info.information += self.list_items(unowned_properties, False)[0]
        self.web_info.information += 'There are ' + str(self.board.houses) + ' houses left to buy\n'
        self.web_info.information += 'There are ' + str(self.board.hotels) + ' hotels left to buy\n'
        return None

    async def handle_player_info(self, action):
        current_players = [x for x in self.player_array if not(x.bankrupt)]
        current_players_str = [x.name for x in current_players]
        self.get_input('Who would you like information about?\n', current_players_str)
        about = await self.get_web_input()
        if not(about == 'Cancel'):
            index = current_players_str.index(about)
            player = current_players[index]
            player_stuff = [x.name + ' - ' + x.group.name + ' - ' + str(x.houses) + ' houses - ' + str(x.hotels)
            + ' hotels' for x in player.properties_owned if type(x) == Property]
            for i in player.properties_owned:
                if not(type(i) == Property):
                    player_stuff.append(i.name + ' - ' + i.group.name)
            for i in player.get_out_of_jail_free_cards:
                player_stuff.append('Get Out of Jail Free card')
            player_stuff.append('$' + str(player.money))
            self.web_info.information += player.name + ' currently has:\n'
            self.web_info.information += self.list_items(player_stuff, False)[0]
        return None

    async def handle_draw_card(self, action):
        card_type = action.information['card type']
        player = action.information['player']
        self.get_input('Click the button to draw a card\n', ['Draw a card!'], cancel=False)
        await self.get_web_input()
        if card_type == 'cc':
            card = self.board.cc_cards.draw(player)
        elif card_type == 'chance':
            card = self.board.chance_cards.draw(player)
        self.web_info.information += card[0] + '\n'
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
                self.web_info.information += player.name + ', you have passed Go! You have collected $200\n'
                player.money += 200
                self.web_info.information += player.print_money()
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
        self.web_info.information += player.name + ', you owe $' + str(money_owed) + ' for house and hotel repairs\n'
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
        self.web_info.information += player.name + ', go directly to jail. Do not pass Go. Do not collect $200\n'
        return None

    async def handle_attempt_to_leave_jail(self, action):
        player = action.information['player']
        options = ['Roll']
        if player.money >= 50:
            options.append('Pay $50')
        if len(player.get_out_of_jail_free_cards) > 0:
            options.append('Use a Get Out of Jail Free card')
        self.get_input('How would you like to leave jail?\n', options)
        choice = await self.get_web_input()
        if choice == 'Cancel':
            self.web_info.information += 'Choice canceled\n'
            next_action = None
        elif choice == 'Pay $50':
            player.money -= 50
            player.jail = 0
            self.web_info.information += player.name + ' paid $50 to leave jail\n'
            self.web_info.information += player.print_money()
            next_action = None
        elif choice == 'Roll':
            self.web_info.information += player.roll()
            if player.doubles == 1:
                self.web_info.information += player.name + ' sucessfully rolled doubles and has left jail\n'
                player.jail = 0
                next_action = self.advance_player(player)
            else:
                player.jail += 1
                self.web_info.information += player.name + ' did not roll doubles\n'
                next_action = None
                if player.jail > 3:
                    self.web_info.information += player.name + ', you have been in jail for 3 turns and must now pay $50\n'
                    bankrupcy_check_bool = await self.bankrupcy_check(player, 50)
                    if bankrupcy_check_bool:
                        next_action = Action('bankrupt', {'bankrupt player': player, 'bankrupt to': 'BANK'})
                    else:
                        player.money -= 50
                        self.web_info.information += player.print_money()
                        player.jail = 0
                        next_action = self.advance_player(player)
        elif choice == 'Use a Get Out of Jail Free card':
            self.return_card(player.get_out_of_jail_free_cards.pop(0))
            player.jail = 0
            self.web_info.information += player.name + ' used a Get Out of Jail Free card to leave jail\n'
            next_action = None
        return next_action

    async def handle_bankrupt(self, action):
        bankrupt_player = action.information['bankrupt player']
        bankrupt_to = action.information['bankrupt to']
        bankrupt_player.bankrupt = True
        bankrupt_player.pass_turn = True
        next_action = None
        self.web_info.information += bankrupt_player.name + ' has gone bankrupt!\n'
        bankrupt_players = 0
        for i in self.player_array:
            if i.bankrupt:
                bankrupt_players += 1
        if not(len(self.player_array) - 1 == bankrupt_players):
            if bankrupt_to == 'BANK':
                self.web_info.information += bankrupt_player.name + '\'s properties will now be auctioned\n'
                for i in bankrupt_player.get_out_of_jail_free_cards:
                    self.return_card(i)
                players_left = [x for x in self.player_array if not(x.bankrupt)]
                next_player = players_left[0]
                for i in bankrupt_player.properties_owned:
                    self.web_info.information += i.name + '\n'
                    i.mortgaged = False
                    if type(i) == Property:
                        self.board.houses += i.houses
                        self.board.hotels += i.hotels
                        i.houses = 0
                        i.hotels = 0
                    auction_action = Action('auction', {'player': next_player, 'property': i})
                    while not(auction_action == None):
                        auction_action = await self.handleAction(auction_action)
            else:
                self.web_info.information += bankrupt_to.name + ', you have recieved:\n'
                self.web_info.information += '$' + str(bankrupt_player.money) + '\n'
                bankrupt_to.money += bankrupt_player.money
                mortgaged_list = [x for x in bankrupt_player.properties_owned if x.mortgaged]
                for i in bankrupt_player.properties_owned:
                    bankrupt_to.properties_owned.append(i)
                    i.ownership = bankrupt_to
                    self.web_info.information += i.name + ' - ' + i.group.name + '\n'
                if len(bankrupt_player.get_out_of_jail_free_cards) > 0:
                    self.web_info.information += str(len(bankrupt_player.get_out_of_jail_free_cards)) + ' Get Out of Jail Free card(s)\n'
                    for i in bankrupt_player.get_out_of_jail_free_cards:
                        bankrupt_to.get_out_of_jail_free_cards.append(i)
                bankrupt_to.sort_properties(self.board.property_array)
                if len(mortgaged_list) > 0:
                    await self.recieved_mortgaged_properties(bankrupt_to, mortgaged_list)
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
            self.web_info.information += player.name + ', you have passed Go! You have collected $200\n'
            player.money += 200
            self.web_info.information += player.print_money()
        player.square = new_space
        next_action = self.board.property_array[player.square].get_action(player)
        if next_action[1].type == 'make payment':
            if square_type == Utility:
                player.roll()
                next_action[1].information['amount'] = player.dice_roll * multiplier
                message = (self.board.property_array[player.square].name + ' - Utility - Owned by: '
                + self.board.property_array[player.square].ownership.name
                + ' - Current Rent: 10 times amount shown on dice - $' + str(next_action[1].information['amount']))
                self.web_info.information += message + '\n'
            elif square_type == Railroad:
                next_action[1].information['amount'] *= multiplier
                message = (self.board.property_array[player.square].name + ' - Railroad - Owned by: '
                + self.board.property_array[player.square].ownership.name + ' - Current Rent: $' + str(next_action[1].information['amount']))
                self.web_info.information += message + '\n'
        else:
            self.web_info.information += next_action[0] + '\n'
        player.dice_roll = old_roll
        player.doubles = old_doubles
        return next_action[1]

    async def recieved_mortgaged_properties(self, player, mortgaged_list):
        for i in mortgaged_list:
            now_cost = ((i.cost // 2) // 10) + (i.cost // 2)
            later_cost = ((i.cost // 2) // 10)
            self.web_info.information += i.name + ' - ' + i.group.name + ' is currently mortgaged\n'
            options = ['Leave it mortgaged for $' + str(later_cost)]
            if player.money < now_cost:
                self.web_info.information += player.name + ', you can\'t afford to unmortgage this property for $' + str(now_cost) + '\n'
                await self.raise_money(player)
            if player.money >= now_cost:
                options.append('Unmortgage it now for $' + str(now_cost))
            self.get_input(player.name + ', what would you like to do?\n', options, cancel=False)
            choice = await self.get_web_input()
            if choice == 'Leave it mortgaged for $' + str(later_cost):
                bankrupcy_check_bool = await self.bankrupcy_check(player, later_cost)
                if bankrupcy_check_bool:
                    await self.handleAction(Action('bankrupt', {'bankrupt player': player, 'bankrupt to': 'BANK'}))
                    break
                else:
                    await self.handleAction(Action('make payment', {'from': player, 'to': 'BANK', 'amount': later_cost}))
            elif choice == 'Unmortgage it now for $' + str(now_cost):
                await self.handleAction(Action('unmortgage', {'player': player, 'property': i}))

    async def get_trade_items(self, player, question1, question2):
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
        while not(choice == 'Continue'):
            self.get_input(question1, choices_str, cancel='Continue')
            choice = await self.get_web_input()
            if not(choice == 'Continue'):
                if choice == 'Money':
                    get_money = None
                    money_options = []
                    while not(get_money == 'Continue'):
                        if (money_amount + 100) <= player.money:
                            money_options = [1, 10, 100]
                        elif (money_amount + 10) <= player.money:
                            money_options = [1, 10]
                        elif (money_amount + 1) <= player.money:
                            money_options = [1]
                        else:
                            money_options = []
                        self.web_info.information += player.print_money()
                        self.web_info.information += 'You have currently entered $' + str(money_amount) + '\n'
                        self.get_input(question2, [str(x) for x in money_options], cancel='Continue')
                        get_money = await self.get_web_input()
                        if not(get_money == 'Continue'):
                            money_amount += int(get_money)
                elif choice == 'Get Out of Jail Free card':
                    return_list_str.append('Get Out of Jail Free card')
                    return_list.append('Get Out of Jail Free card')
                    choices_str.remove('Get Out of Jail Free card')
                else:
                    index = choices_str.index(choice)
                    return_list_str.append(choices_str.pop(index))
                    return_list.append(choices.pop(index))
        if money_amount > 0:
            return_list.append(money_amount)
            return_list_str.append('$' + str(money_amount))
        return return_list, return_list_str

    def list_items(self, item_list, cancel):
        dialog = ''
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
        self.web_info.information += prompt
        options = item_array.copy()
        if not(cancel == False):
            options.append(cancel)
        self.web_info.type = options
        self.player_choice = None

    async def get_web_input(self):
        while self.player_choice == None:
            await asyncio.sleep(0)
        return self.player_choice

    async def raise_money(self, player):
        self.get_input('Would you like to raise money?\n', ['Yes', 'No'], cancel=False)
        get_money = await self.get_web_input()
        if get_money == 'Yes':
            choice = None
            while not(choice == 'Cancel'):
                choices = player.need_money()
                for i in self.always_option:
                    choices.append(i)
                self.get_input(player.name + ', what woud you like to do?\n', choices)
                choice_2 = await self.get_web_input()
                if choice_2 == 'Cancel':
                    choice = 'Cancel'
                else:
                    choice = choice_2
                    await self.take_turn(player, choice)

    async def bankrupcy_check(self, player, cost):
        if player.money < cost:
            self.web_info.information += player.name + ', you are about to go bankrupt\n'
            self.web_info.information += 'You have $' + str(player.money) + '\n'
            self.web_info.information += 'You need $' + str(cost) + '\n'
            await self.raise_money(player)
        if player.money < cost:
            bankrupt = True
        else:
            bankrupt = False
        return bankrupt

    def advance_player(self, player, go_check=True):
        next_square = (player.square + player.dice_roll) % len(self.board.property_array)
        if (next_square < player.square) and go_check:
            self.web_info.information += player.name + ', you have passed Go! You have collected $200\n'
            player.money += 200
            self.web_info.information += player.print_money()
        player.square = next_square
        next_action = self.board.property_array[player.square].get_action(player)
        self.web_info.information += next_action[0] + '\n'
        return next_action[1]

    def return_card(self, card_type):
        if card_type == 'cc':
            self.board.cc_cards.return_goojf()
        elif card_type == 'chance':
            None

    async def take_turn(self, player, choice):
        if choice == 'roll':
            self.web_info.information += player.roll()
            if player.doubles == 3:
                self.web_info.information += player.name + ', you rolled 3 doubles in a row\n'
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
            self.web_info.information += 'Passing the turn...\n'
            action = None
        else:
            legal_properties = player.get_legal_properties(choice)
            self.get_input(self.question_map[choice] + '\n', legal_properties[0])
            response = await self.get_web_input()
            if response == 'Cancel':
                action = Action('error', 'Choice canceled')
            else:
                index = legal_properties[0].index(response)
                action = Action(choice, {'player': player, 'property': legal_properties[1][index]})

        while not(action == None):
            action = await self.handleAction(action)

    async def play(self):
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
   
                self.get_input(current_player.name + ', what would you like to do?\n', filterd_list, cancel=False)
                choice = await self.get_web_input()
                await self.take_turn(current_player, choice)

            move_player = self.player_array.pop(0)
            self.player_array.append(move_player)

            self.player_array = [x for x in self.player_array if not(x.bankrupt)]
        
        self.web_info.information += self.player_array[0].name + ', you WIN THE GAME!'