'''
Josha Cirbo
08/03/2025
CSC2017 Advanced Python
score
This file contains definitions for Score class
'''

if __name__ == '__main__' or __name__ == 'score':
    from setup import *
else:
    from Poker.setup import *
    

class Score():
    def __init__(self, hand: list, wilds: bool):
        self.__suits = [0 for _ in range(NUM_SUITS)]
        self.__values = [0 for _ in range(NUM_VALUES + 1)]
        self.__deuces = 0
        self.__wilds = wilds
        
        
        self.__load_values(hand)
    
    def __str__(self):
        # Every word in a score should be capitalized except for 'of' or 'a'
        text = ''.join(i.capitalize() + ' ' if i != 'of' and i != 'a' else i + ' ' for i in self.__score_hand().split(' '))
        text[-1].strip()
        return text

    def __int__(self):
        return Score.__SCORES[self.__score_hand()]
        
    def __load_values(self, hand):
        for card in hand:
            # Neither suit or value matter with deuces. They are wild
            if self.__wilds and int(card) % NUM_VALUES == 1:
                self.__deuces += 1
            else:
                self.__suits[int(card) // NUM_VALUES] += 1
                self.__values[int(card) % NUM_VALUES] += 1
                
                # Aces are both 0 and 13 (low ace/high ace)
                if not int(card) % NUM_VALUES:
                    self.__values[NUM_VALUES] += 1
    
    def __score_hand(self):
        # Flush flag
        flush = self.__is_flush()
        
        # Straight flags
        straight, high_straight = self.__is_straight()
        
        # Card multiples flags
        pairs, pair_index, three, four, five = self.__is_multiple()
        
        # Check five of a kind
        if five:
            return 'five of a kind'
        
        # Check royal flush
        if high_straight and flush:
            return 'royal flush'
        
        # Check straight flush
        if straight and flush:
            return 'straight flush'
        
        # Four of a kind
        if four:
            return 'four of a kind'
        
        # Check full house
        if three and pairs:
            return 'full house'
        
        # Output flush
        if flush:
            return 'flush'
        
        # Output straight
        if straight:
            return 'straight'
        
        # Check three of a kind
        if three:
            return 'three of a kind'
        
        # Check two pair
        if pairs > 1:
            return 'two pair'
        
        # Check high pair
        if pairs and pair_index > 9:
            return 'high pair'
        
        # Lose
        return 'lose'
    
    def __is_flush(self):
        for suit in self.__suits:
            if suit + self.__deuces == 5:
                return True
        
        return False
    
    def __is_straight(self):
        max_index = -1
        
        # Iterate up to index 9
        for index in range(10):
            counter = 0
            # From current index, iterate up 5 positions
            for runner in range(5):
                # Add one to counter if and only if value is 1. 2 breaks the straight
                counter += 1 if self.__values[index + runner] == 1 else 0
        
            # Set tracker to the highest index with a potential straight
            if counter + self.__deuces == 5:
                max_index = index
        
        if max_index > -1:
            # If max_index is 9, the straight is royal
            return (True, True) if max_index > 8 else (True, False)
        
        return (False, False)
    
    def __is_multiple(self):
        twos = 0
        pairs = 0
        pair_index = 0
        three = False
        
        for index in range(NUM_VALUES):
            # Five of a kind
            # Explicitly check for 4 wilds; it can cause incorrect return of 4 of a kind
            if self.__wilds and ((self.__values[index] + self.__deuces > 4) or (self.__deuces > 3)):
                return (0, 0, 0, False, True)

            # Four of a kind
            if self.__values[index] + self.__deuces > 3:
                return (0, 0, 0, True, False)
            
            # No wilds: natural threes and pairs
            if not self.__deuces:
                if self.__values[index] == 2:
                    pairs += 1
                    
                    #Aces are lowest and highest values
                    if not index:
                        pair_index = 13
                        
                    pair_index = index if index > pair_index else pair_index
                elif self.__values[index] == 3:
                    three = True
            else:
                # If there is one value with two, that is a 
                if self.__values[index] == 2:
                    twos += 1
                # With at lease 1 wild, any value less than two becomes a potential high pair
                elif self.__values[index] == 1:
                    # Aces are lowest and highest value
                    if not index:
                        pair_index = 13
                        
                    pair_index = index if index > pair_index else pair_index
        
        # Wilds breakdown: If no four of a kind, only one or two wilds are possible
        # Two wilds and no natural pairs can only yield a three of a kind
        if self.__deuces == 2:
            three = True
            
        # One wild can yield a high pair, thee of a kind, or full house
        elif self.__deuces == 1:
            # Two pair with one wild is a full house
            if twos > 1:
                pairs = 1
                three = True
            # One pair with one wild is a three of a kind
            elif twos == 1:
                pairs = 0
                three = True
            # One wild and no natural pair is a possible high pair
            else:
                pairs = 1
        
        return (pairs, pair_index, three, False, False)
        
    __SCORES = {'five of a kind'  : 5000,
                'royal flush'     : 2000,
                'straight flush'  : 250,
                'four of a kind'  : 125,
                'full house'      : 40,
                'flush'           : 25,
                'straight'        : 20,
                'three of a kind' : 15,
                'two pair'        : 10,
                'high pair'       : 1,
                'lose'            : 0}

if __name__ == '__main__':
    from card import Card
    from random import randint
    
    a = Score([Card(randint(0, 51)) for _ in range(5)], True)
    
    print(a)
    print(int(a))