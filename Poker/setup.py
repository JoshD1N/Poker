'''
Josha Cirbo
08/03/2025
CSC2017 Advanced Python
setup
This file contains constants and functions used throughout the game
'''

# Initialize for pythonGraph
import pygame
pygame.mixer.init()

# Global Constants
CARDS_PER_DECK = 52
CHIP_VALUE     = 5
MIN_BET        = 1
MAX_BET        = 50
NUM_CARDS      = 5
NUM_SUITS      = 4
NUM_VALUES     = 13
WIDTH          = 800
HEIGHT         = 600
FLIP_SCALE     = 3
FLIP_COMP      = 8
ANIMATION_RATE = 10
TRANSPARENCY   = '#FADEC0'

STD_FONT = ('Courier New', 12)
BLD_FONT = ('Courier New', 14, 'bold')

# Component positions
CARD_POSITIONS   = [[175, 350], [275, 400], [375, 415], [475, 400], [575, 350]]
DECK_POSITION    = [250, 115]
DISCARD_POSITION = [500, 115]

def validate(name, *args):
    def decorator(func):
        def wrapper(*func_args): 
            # Func is either method or function. Methods have self as first parameter
            integer = int(func_args[0] if len(func_args) == 1 else func_args[1])
            
            # If args is empty, decorator is checking index of Player hand
            if len(args) == 0:
                lower = 0
                upper = len(func_args[0].hand) - 1
            else:
                lower = args[0]
                upper = args[1] if len(args) > 1 else -1
                
            if integer < lower:
                raise ValueError(f'{name} must be greater than {lower}')
            
            # If there is a second arguement passed to factory, it is upper limit
            if upper > -1 and integer > upper:
                    raise ValueError(f'{name} must be no greater than {upper}')
            
            # Set parameters for function
            if len(func_args) == 1:
                parameters = [integer]
            # Two arguements to a function indicates a method. First arguement is self; second is value
            elif len(func_args) == 2:
                parameters = [func_args[0], integer]
            # Anything other than two arguements should be passed into function as is
            else:
                parameters = func_args
            return func(*parameters)
        return wrapper
    return decorator

# Card reference dictionaries

VALUES = {0:  'Ace',
          1:  '2',
          2:  '3',
          3:  '4',
          4:  '5',
          5:  '6',
          6:  '7',
          7:  '8',
          8:  '9',
          9:  '10',
          10: 'Jack',
          11: 'Queen',
          12: 'King'
}

SUITS = {0: 'Spades',
         1: 'Diamonds',
         2: 'Clubs',
         3: 'Hearts'
}