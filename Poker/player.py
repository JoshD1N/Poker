'''
Josha Cirbo
08/03/2025
CSC2017 Advanced Python
player
This file contains definitions for Player class
'''

if __name__ == '__main__' or __name__ == 'player':
    from setup import *
    from card import Card
else:
    from Poker.setup import *
    from Poker.card import Card

from os.path import join

class Player:
    def __init__(self, name):
        self.__name = name
        self.__money = self.__open_bank()
        self.__chips = 0
        self.__hand = []
    
    # Overload += operator for smoother card addition
    def __iadd__(self, card: Card):
        # Add value to end of hand if hand is not full
        if len(self.__hand) < NUM_CARDS:
            self.__hand.append(card)
        else:
            # If hand is full, put value is first card that is None
            for index in range(NUM_CARDS):
                if self.__hand[index] == None:
                    self.__hand[index] = card
                    break
                    
        # Return same object with updated hand
        return self
    
    @validate('player hand index')
    def __isub__(self, index: int):
        # Set card at decremented index to None
        self.__hand[index] = None
        
        return self
    
    def __str__(self):
        return f'{'NAME':>4} {self.name}\n{'CASH':>4} {self.money}\n{'BANK':>4} {self.chips}'
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def hand(self) -> list:
        return self.__hand
    
    @property
    def hand_names(self):
        return [str(i) for i in self.__hand]
    
    @property
    def money(self) -> int:
        return self.__money
    
    @money.setter
    @validate('money', 0)
    def money(self, value: int) -> None:
        self.__money = value
    
    @property
    def chips(self):
        return self.__chips
    
    @chips.setter
    @validate('chip amount', 0)
    def chips(self, value):
        self.__chips = value
    
    def clear(self):
        self.__hand.clear()
    
    def save_bankroll(self):
        # Use context manager to save money to file to avoid issue incase of crash
        with open(join('Poker', 'banks', f'{self.__name}.bank'), 'w') as file:
            value = self.__money + (self.__chips * CHIP_VALUE)
            file.write(str(value))
    
    def __open_bank(self):
        try:
            # Attempt to open bankroll file; if file exists, read amount, and return integer value
            with open(join('Poker', 'banks', f'{self.__name}.bank'), 'r') as file:
                data = file.read().strip()
            
            return int(data)
        
        # If the file does not exist or has invalid data, open file and initialze value to zero
        except (FileNotFoundError, ValueError):
            with open(join('Poker', 'banks', f'{self.__name}.bank'), 'w') as file:
                file.write('0')
            
            return 0

if __name__ == '__main__':
    a = Player('josh')
    print(a)