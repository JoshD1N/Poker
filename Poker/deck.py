'''
Josha Cirbo
08/03/2025
CSC2017 Advanced Python
deck
This file contains definitions for Deck class
'''

from random import shuffle
if __name__ == '__main__' or __name__ == 'deck':
    from setup import *
else:
    from Poker.setup import *

class Deck:
    @validate('number of decks', 1, 10)
    def __init__(self, num_decks: int):
        # Initialize deck with num_decks cards randomly shuffled in
        self.__num_decks = num_decks
        
        # Card limit is 40% of the number of cards in the deck
        self.__limit = (4 * num_decks * CARDS_PER_DECK) // 10
        
        # Generate deck with num_decks repetitions of a 52 card deck
        self.__deck = [i for i in range(CARDS_PER_DECK)] * self.__num_decks
        
        # Set deck and tracker
        self.shuffle()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.__count == len(self.__deck):
            raise StopIteration('no more cards in deck')
        
        # Pull card
        card = self.__deck[self.__count]
        
        # Increment counter
        self.__count += 1
        
        # Yield
        return card
        
    @property
    def cards_left(self):
        return len(self.__deck) - self.__count
    
    @property
    def limit(self) -> int:
        return self.__limit
    
    def shuffle(self) -> None:
        # Reset iteration tracker
        self.__count = 0
        
        # Use shuffle instead of sample to randomize the card list in place and avoid doubling memory usage
        shuffle(self.__deck)