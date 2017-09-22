import random
import time
import os

def clear():
    os.system( 'clear' )

class Deck(object):
    
    def __init__(self):
        
        self.cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.d_horizontal = ''
        self.d_vertical = ''
        self.d_center = ''
        self.p_horizontal = ''
        self.p_vertical = ''
        self.p_center = ''
        self.s_horizontal = ''
        self.s_vertical = ''
        self.s_center = ''
        
    def generate_random_card(self):
        return random.choice(self.cards)
    
    def calculate_sum(self, hand_cards):
        cards_sum = 0
        
        number_of_aces = hand_cards.count('A')
        
        for card in hand_cards:
            if card not in 'A J Q K'.split():
                cards_sum += int(card)
            elif card in 'J Q K'.split():
                cards_sum += 10
            else:
                pass #aces will be added outside this loop!
                
        for i in range(0,number_of_aces):
            cards_sum += 11
            if cards_sum > 21:
                cards_sum -= 10
        
        #print('Your sum is: ' + cards_sum)
        return cards_sum
    
    
    def show_deck(self,dealer_hand,player_hand,second_hand = []):
        clear()
        
        self.d_horizontal = ''
        self.d_vertical = ''
        self.d_center = ''
        self.p_horizontal = ''
        self.p_vertical = ''
        self.p_center = ''
        self.s_horizontal = ''
        self.s_vertical = ''
        self.s_center = ''
        
        print('DEALER:')
        for dealer_card in dealer_hand:
            if dealer_card == '10':
                self.d_horizontal += ' ------    '
                self.d_vertical += '|      |   '
                self.d_center += '|  ' + dealer_card + '  |   '
            else:
                self.d_horizontal += ' -----    '
                self.d_vertical += '|     |   '
                self.d_center += '|  ' + dealer_card + '  |   '
        print(self.d_horizontal)
        print(self.d_vertical)
        print(self.d_center)
        print(self.d_vertical)
        print(self.d_horizontal)
        
        print('\n \nPLAYER:')
        for player_card in player_hand:
            if player_card == '10':
                self.p_horizontal += ' ------    '
                self.p_vertical += '|      |   '
                self.p_center += '|  ' + player_card + '  |   '
            else:
                self.p_horizontal += ' -----    '
                self.p_vertical += '|     |   '
                self.p_center += '|  ' + player_card + '  |   '
        print(self.p_horizontal)
        print(self.p_vertical)
        print(self.p_center)
        print(self.p_vertical)
        print(self.p_horizontal)
        print('\n')
        
        if len(second_hand) != 0:
            for second_card in second_hand:
                if second_card == '10':
                    self.s_horizontal += ' ------    '
                    self.s_vertical += '|      |   '
                    self.s_center += '|  ' + second_card + '  |   '
                else:
                    self.s_horizontal += ' -----    '
                    self.s_vertical += '|     |   '
                    self.s_center += '|  ' + second_card + '  |   '
            print(self.s_horizontal)
            print(self.s_vertical)
            print(self.s_center)
            print(self.s_vertical)
            print(self.s_horizontal)
            print('\n')
            

    def check_result(self,hand):
        """
        Returns: total count if no blackjack or bust
                 1           if blackjack
                 2           if bust
        """
        cards_sum = self.calculate_sum(hand)
        if 0 <= cards_sum < 21:
            return cards_sum
        elif cards_sum == 21:
            return 1
        else:
            return 2
        
    def pick_cards(self,p,d):
        """
        Result: total count if no blackjack or bust
                 1           if blackjack
                 2           if bust
        """
        while True:
            
            self.show_deck(d.hand, p.hand, p.second_hand)
            
            if len(p.second_hand) != 0:
                print('Playing for hand %d' %(p.pointer))
            
            p.select_option()
            
            if p.option == 1:
                if p.pointer == 1:
                    p.hand += [self.generate_random_card()]
                    self.show_deck(d.hand, p.hand, p.second_hand)
                    result = self.check_result(p.hand)
                else:
                    p.second_hand += [self.generate_random_card()]
                    self.show_deck(d.hand, p.hand, p.second_hand)
                    result = self.check_result(p.second_hand)
                
                if result == 1:
                    p.result[p.pointer - 1] = 1 
                    p.pointer = 2
                    break
                elif result == 2:
                    p.result[p.pointer - 1] = 2
                    p.pointer = 2
                    break
                else:
                    continue
            elif p.option == 2:
                if p.pointer ==1:
                    result = self.check_result(p.hand)
                else:
                    result = self.check_result(p.second_hand)
                p.result[p.pointer - 1] = result
                p.pointer = 2
                break
            
    def dealer_pick_cards(self,p,d):
        """
        Returns: total count if no blackjack or bust
                 1           if blackjack
                 2           if bust
        """
        while True:
            d.hand += [self.generate_random_card()]
            self.show_deck(d.hand, p.hand, p.second_hand)
            d.result = self.check_result(d.hand)
                
            time.sleep(1) 
            d.has_not_picked = False
            
            if d.result == 1 or d.result == 2:
                break   
            elif d.result < 16:
                continue
            else:
                break
      
            
    def decide_winner(self,p,d,index):
        if p.result[index - 1] == 1:
            p.win_bj()
        elif p.result[index - 1] == 2:
            p.lose()
        else:
            if d.has_not_picked:
                self.dealer_pick_cards(p,d)
                
            if d.result == 1 or d.result > p.result[index - 1]:
                p.lose()
            elif d.result == 2 or d.result < p.result[index - 1]:
                p.win()
            else:
                p.tie()

class Player(object):
    
    def __init__(self):
        self.hand = []
        self.second_hand = []
        self.can_split = True
        self.pointer = 1 #points to either first or second hand in case of a split
        self.result = [0, 0]
        while True:
            try:
                self.bankroll = int(input("Pick your bankroll "))
            except:
                print('Not valid entry')
                continue
            else:
                if self.bankroll <= 0:
                    print('Not valid entry')
                    continue
                else:
                    break
                
                
    def pick_your_bet(self):
        while True:
            try:
                self.user_bet = int(input("Pick your bet "))
            except:
                print('Not valid entry')
                continue
            else:
                if (self.bankroll - self.user_bet) >= 0:
                    self.bankroll -= self.user_bet
                    break
                else:
                    print('You do not have that amount of money')
                    continue
                    
    def select_option(self):
        while True:
            try:
                self.option = int(input('Type: \n1 for Hit \n2 for Stand \n'))
            except:
                print('Not valid entry')
                continue
            else:
                if self.option not in range(1,3):
                    print('Not valid entry')
                    continue
                else:
                    break            
            
            
    def win_bj(self):
        print("Congratulations!!! You WON!!!")
        self.bankroll += self.user_bet * 2.5
        print('Your new bankroll is : %s' %(self.bankroll))
        
    def win(self):
        print("Congratulations!!! You WON!!!")
        self.bankroll += self.user_bet * 2
        print('Your new bankroll is : %s' %(self.bankroll))
        
    def lose(self):
        print('Dealer won! Your bankroll is : %s' %(self.bankroll))
        
    def tie(self):
        print("Tie")
        self.bankroll += self.user_bet
        print('Your new bankroll is : %s' %(self.bankroll))        
        
    def split(self):
        if self.hand[0] == self.hand[1]:
            reply = input('Do you want to split? (y/n)').lower()
            if reply == 'y':
                if (self.bankroll - self.user_bet) < 0:
                    print("You do not have sufficient bankroll account")
                    return False
                else:
                    self.bankroll -= self.user_bet
                    self.second_hand += [self.hand.pop(1)]
                    self.can_split = False
                    return True
            else:
                return False
            
    def reset(self):
        self.hand = []
        self.second_hand = []
        self.can_split = True
        self.pointer = 1 #points to either first or second hand in case of a split
        self.result = [0, 0]


class Dealer(object):
    
    def __init__(self,name = 'Dealer'):
        self.hand = []
        self.name = name
        self.result = 0
        self.has_not_picked = True
        
    def reset(self):
        self.hand = []
        self.result = 0
        self.has_not_picked = True

def play():
    
    p = Player()
    deck = Deck()
    d = Dealer()
    game_on = True
    
    while game_on:
        
        p.pick_your_bet()
        
        p.hand += [deck.generate_random_card()]
        p.hand += [deck.generate_random_card()] 
        d.hand += [deck.generate_random_card()]
        
        deck.show_deck(d.hand, p.hand)
        
        #Check if there is blackjack
        if deck.check_result(p.hand) == 1:
            p.win_bj()
            break
            
        #Check if there is a split opportunity
        if p.split():
            p.hand += [deck.generate_random_card()]
            p.second_hand += [deck.generate_random_card()]
            
            deck.pick_cards(p,d)
            if p.result[0] == 1 or p.result[0] == 2:
                deck.decide_winner(p,d,1)
                input("Ready for the second hand?")
            
                deck.pick_cards(p,d)
                deck.decide_winner(p,d,2)
            else:
                deck.pick_cards(p,d)
                deck.decide_winner(p,d,1)
                deck.decide_winner(p,d,2)
        else:
            deck.pick_cards(p,d)
            deck.decide_winner(p,d,1)
            
        reply = input('Do you want continue playing? (y/n)').lower()
        if reply == 'y':
            p.reset()
            d.reset()
        else:
            game_on = False
                
play()
