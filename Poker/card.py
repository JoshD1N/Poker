'''
Josha Cirbo
08/03/2025
CSC2017 Advanced Python
card
This file contains definitions for Card class
'''

if __name__ == '__main__' or __name__ == 'card':
    from setup import *
else:
    from Poker.setup import *

class Card:
    @validate('card value', 0, 51)
    def __init__(self, value):
        self.__value = value
        self.__name = VALUES[value % NUM_VALUES] + ' of ' + SUITS[value // NUM_VALUES]
        
        # Graphics variables to be set after intialization of window
        self.__master = None
        self.__image = None
        self.__first = None
        self.__second = None
        self.__current = None
        self.__switch = False
    
    def __str__(self):
        return self.__name
    
    def __int__(self):
        return self.__value
    
    @property
    def position(self):
        return self.__master.coords(self.__image)
    
    def set_image(self, canvas, images: dict):
        # Load canvas object into memory
        self.__master = canvas
        
        # First face for every card is the back
        self.__first = images['back']
        
        # Face card is second
        self.__second = images[str(self)]
        
        # Dummy attribute for stretching during flipping
        self.__current = self.__first
        
        # Image element starts at the deck before being dealt
        self.__image = canvas.create_image(DECK_POSITION[0], DECK_POSITION[1], image=self.__current, anchor='nw')

    def flip(self, side = None, scale = 1):
        # Default value for calling
        if side == None:
            side = self.__first
        
        # If the side is the first, flipping will move to the right and shrink
        if side == self.__first:
            scale += FLIP_SCALE
            self.__master.move(self.__image, FLIP_COMP, 0)
        
        # When the second side is up, flipping moves to the left and stretches
        else:
            scale -= FLIP_SCALE
            self.__master.move(self.__image, -FLIP_COMP, 0)
        
        # Load stretched face into dummy variable
        self.__current = side.subsample(scale, 1)
        self.__master.itemconfigure(self.__image, image=self.__current)
        
        # There are 4 'frames' of the animation. After the fourth, switch sides
        if scale > 12:
            self.__switch = True
        
        # Flipping phase is determined by which image is loaded
        if not self.__switch:
            animation_id = self.__master.after(ANIMATION_RATE, self.flip, self.__first, scale)
        else:
            animation_id = self.__master.after(ANIMATION_RATE, self.flip, self.__second, scale)
        
        # If the scale has gone below 1, animation is over
        if scale < 1:
            self.__master.after_cancel(animation_id)
            self.__switch = False
            
            # Assign dummy variable current, unstretched face
            self.__current = side.subsample(1, 1)
            self.__master.itemconfigure(self.__image, image=self.__current)
            
            # Move the image back to its original location
            self.__master.move(self.__image, FLIP_COMP, 0)
            
            # Swap faces
            self.__first, self.__second = self.__second, self.__first
        
    def move(self, pos, flip: bool = False):
        # Determine direction of motion relative to the destination (pos)
        x, y = self.position
        
        dx = 1 if x < pos[0] else -1
        dy = 1 if y < pos[1] else -1
        
        # For each axis, move forward (positive) or backward (negative) depending on relation to destination
        self.__master.move(self.__image, dx if x != pos[0] else 0, dy if y != pos[1] else 0)
        
        # Recursive loop
        animation_id = self.__master.after(1, self.move, pos, flip)
        
        # If image has reached coordinates, stop animation, and flip if called for
        if x == pos[0] and y == pos[1]:
            self.__master.after_cancel(animation_id)
            if flip:
                self.flip()
    