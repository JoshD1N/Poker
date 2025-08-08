'''
Josha Cirbo
08/03/2025
CSC2017 Advanced Python
game
This file contains the logic and window handling of the main game
'''

if __name__ == '__main__' or __name__ == 'game':
    from setup import *
    from player import Player
    from card import Card
    from score import Score
    from deck import Deck
else:
    from Poker.setup import *
    from Poker.player import Player
    from Poker.card import Card
    from Poker.score import Score
    from Poker.deck import Deck

from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
import pythonGraph as pg
from os.path import join

class Game(Tk):
    def __init__(self):
        #Set up main window
        super().__init__()
        self.title("Josha Cirbo's 5 Card Draw Poker")
        self.geometry('800x600')
        
        # Hide main window
        self.withdraw()
        
        # Initialize attributes
        self.__dealt = False
        self.__bet = IntVar(self, 0)
        self.__wilds = BooleanVar(self, True)
        self.__auto_bet = BooleanVar(self, False)
        self.__auto_bet_amount = 0
        self.__running = False
        self.__finished = False
        self.__cards_to_discard = []
        self.__selections = []
        self.__score = None
        self.__style = Style(self)
        
        
        # Open and store all card files in memory for quick access
        self.__IMAGES = {'back': PhotoImage(file=join('Poker', 'imgs', 'back.gif')),
                         'table' : PhotoImage(file=join('Poker', 'imgs', 'table.png'))}

        for valkey in VALUES:
            for suitkey in SUITS:
                name = VALUES[valkey] + ' of ' + SUITS[suitkey]
                self.__IMAGES[name] = PhotoImage(file=join('Poker', 'imgs', name + '.gif'))
        
        # Get player info
        self.__get_info()
        
        # Create main canvas
        self.__table = Canvas(self, width=WIDTH, height=HEIGHT)
        self.__table.pack()
        
        # Generate and place components
        self.__generate_components()
        
        # Setup event handlers
        self.__set_binds()
        
        # Setup styles for Ttk components
        self.__set_style()
    
    def __set_style(self):
        self.__style.map('TCheckbutton', 
                         foreground=[('!active', 'black'), ('active', 'magenta')],
                         background=[('!active', 'green'), ('active', 'green')],
                         font=[('!active', BLD_FONT), ('active', BLD_FONT), ('pressed', BLD_FONT)])

        self.__style.map('TButton', 
                         foreground=[('!active', 'black'), ('pressed', 'red'), ('active', 'magenta')],
                         bordercolor=[('!active', 'red'), ('pressed', 'red'), ('active', 'red')],
                         font=[('!active', BLD_FONT), ('active', BLD_FONT), ('pressed', BLD_FONT)])
        self.__style.configure('TButton', width=10, relief='sunken')
        
        self.__style.configure('Win.TLabel', font=('Courier New', 26, 'bold'), foreground='blue')
        self.__style.configure('Lose.TLabel', font=('Courier New', 26, 'bold'), foreground='red')
    
    def __get_info(self):
        # Get user name
        name = simpledialog.askstring('Name', 'Enter your name')
        
        # Create player
        self.__player = Player(name)
        self.__player_info = StringVar(self)
        
        money =  self.__player.money
         
        # Check that player bank has money in it
        if not money:
            self.__add_funds()
        
        # Initialize player with all of the money in bank file converted to chips
        self.__player.chips = self.__player.money // CHIP_VALUE
        self.__player.money -= self.__player.chips * CHIP_VALUE
        
        # Update player info
        self.__update_info()
        
        while True:
            try:
                # Get number of decks
                num_decks = simpledialog.askinteger('Decks', 'Please enter number of decks', minvalue=1, maxvalue=10)
                self.deck = Deck(num_decks)
                
                break
            except TypeError as err:
                showwarning('Warning', 'Please enter a valid integer for number of decks')
    
    def __generate_components(self):
        self.__table.create_image(0, 0, image=self.__IMAGES['table'], anchor=NW)
        
        self.__table.create_image(*DECK_POSITION, image=self.__IMAGES['back'], anchor=NW)
        
        self.__table.create_image(*DISCARD_POSITION, image=self.__IMAGES['back'], anchor=NW)
        
        self.__deal_button = Button(self, text='DEAL', command=self.__play, style='TButton')
        self.__table.create_window(340, 100, window=self.__deal_button, anchor=NW)
        
        self.__exit_button = Button(self, text='EXIT', command=self.destroy, style='TButton')
        self.__table.create_window(340, 20, window=self.__exit_button, anchor=NW)
        
        self.__fund_button = Button(self, text='ADD CASH', command=self.__add_funds, style='TButton')
        self.__table.create_window(650, 100, window=self.__fund_button, anchor=NW)
        
        self.__chips_button = Button(self, text='ADD CHIPS', command=self.__add_chips, style='TButton')
        self.__table.create_window(650, 150, window=self.__chips_button, anchor=NW)
        
        self.__bet1_button = Button(self, text='BET 1 COIN', command=self.__bet1_click)
        self.__table.create_window(25, 225, window=self.__bet1_button, anchor=NW)
        
        self.__betmore_button = Button(self, text='CUSTOM BET', command=self.__betmore_click)
        self.__table.create_window(25, 175, window=self.__betmore_button, anchor=NW)
        
        self.__betall_button = Button(self, text='ALL IN', command=self.__betall_click)
        self.__table.create_window(25, 125, window=self.__betall_button, anchor=NW)
        
        self.__wilds_checkbox = Checkbutton(self, text='DEUCES WILD', variable=self.__wilds, command=self.__check_wilds, style='TCheckbutton')
        self.__table.create_window(25, 25, window=self.__wilds_checkbox, anchor=NW)
        
        self.__auto_bet_checkbox = Checkbutton(self, text='AUTO BET', variable=self.__auto_bet, command=self.__set_auto_bet, style='TCheckbutton')
        self.__table.create_window(25, 50, window=self.__auto_bet_checkbox, anchor=NW)
        
        self.__player_info_text = self.__table.create_text(700, 50, text=self.__player_info.get(), font=BLD_FONT)
        
        for i in range(5):
            self.__selections.append(self.__table.create_text(CARD_POSITIONS[i][0] + 10, CARD_POSITIONS[i][1] - 20, text='KEEP', anchor=NW, font=STD_FONT, fill='green'))
    
    def __set_binds(self):
        # When either player money, chips, or bet changes, automatically update display info
        self.__player_info.trace_add('write', self.__info_trace)
        self.__bet.trace_add('write', self.__info_trace)
        
        # Each of the card boxes should have mouse events (mouse_over, mouse_out, and on_click)
        for index in range(5):
            self.__table.tag_bind(self.__selections[index], '<Enter>', lambda event, i = index: self.__text_mouse_event(event, i))
            self.__table.tag_bind(self.__selections[index], '<Leave>', lambda event, i = index: self.__text_mouse_event(event, i))
            self.__table.tag_bind(self.__selections[index], '<Button-1>', lambda event, i = index: self.__text_mouse_event(event, i))
    
    # Generate card graphics and move card to final position
    def __deal_card(self, card: Card, index):
        card.set_image(self.__table, self.__IMAGES)
        card.move(CARD_POSITIONS[index], True)
    
    # Mouse event for discard text
    def __text_mouse_event(self, event: Event, index):
        # if the game is running, don't do anything
        if self.__running:
            if event.type == EventType.Enter:
                self.__table.itemconfigure(self.__selections[index], fill='#FFFFFF', font=BLD_FONT)
                self.__table.move(self.__selections[index], -3, 0)
                
            elif event.type == EventType.Leave:
                self.__table.itemconfigure(self.__selections[index], fill='#000000', font=STD_FONT)
                self.__table.move(self.__selections[index], 3, 0)
            
            # Only handle events if left mouse button is pressed 
            elif event.type == EventType.ButtonPress and event.num == 1:
                if self.__table.itemcget(self.__selections[index], 'text') == 'KEEP':
                    self.__table.itemconfigure(self.__selections[index], text='DISCARD')
                    self.__table.move(self.__selections[index], -10, 0)
                    
                    self.__cards_to_discard.append(index)
                else:
                    self.__table.itemconfigure(self.__selections[index], text='KEEP')
                    self.__table.move(self.__selections[index], 10, 0)
                    
                    self.__cards_to_discard.remove(index)
                
                # Sort the discard list to avoid index errors (highest to lowest)
                self.__cards_to_discard.sort(reverse=True)
                
                # Flip each card that has been selected
                self.__player.hand[index].flip()
    
    def __discard(self, card: Card, index):
        # Remove card from player hand at index and start animation
        card.move(DISCARD_POSITION)
        self.__player -= index  
    
    def __bet1_click(self):
        # If the game running, there should be no betting
        if not self.__running:
            try:
                # If bank is out, add to bank and subtract a chip
                if self.__player.chips < 1:
                    if self.__player.money < 5:
                        self.__add_funds()
                        self.__player.money -= 5
                        self.__player.chips += 1
                    else:
                        self.__add_chips()

                # Only if there are available chips should there be a change in bet or bank
                if self.__bet.get() < 50 and self.__player.chips > 0:
                    self.__bet.set(self.__bet.get() + 1)
                    self.__player.chips -= 1
                    
                    self.__update_info()
            except TypeError:
                pass
            
            except ValueError as err:
                pass
    
    def __betmore_click(self):
        if not self.__running:
            limit = 50 - self.__bet.get()
            
            try:
                value = simpledialog.askinteger('Custom Bet', 'Please enter amound to bet', minvalue=1, maxvalue=limit if limit < self.__player.chips else self.__player.chips)
                
                self.__bet.set(self.__bet.get() + value)
                self.__player.chips -= value
                
                self.__update_info()
            except TypeError:
                pass
            
            except ValueError as err:
                showerror(err.args[0])
        
    def __betall_click(self):
        if not self.__running:
            choice = askyesno('All In', 'Would you like to bet all of your bank?')
            
            if choice == True:
                self.__bet.set(self.__bet.get() + self.__player.chips)
                self.__player.chips = 0
                
                self.__update_info()
            
    def __play(self):
        # If the score is being displayed, no dealing events should be happening
        if not self.__finished:
            # No bet. No play
            if self.__bet.get(): 
                # Dealing phase     
                if not self.__dealt:
                    # First Deal phase
                    if not self.__running:
                        # Shuffle deck if it is lower than 40%
                        if self.deck.cards_left < self.deck.limit:
                            self.deck.shuffle()
                            showinfo('Shuffle', 'RESHUFFLING...')
                        
                        # Load player hand and perform dealing animation
                        for i in range(NUM_CARDS):
                            self.__player += Card(next(self.deck))
                            self.after(ANIMATION_RATE * ANIMATION_RATE * i, self.__deal_card, self.__player.hand[i], i)
                        
                        # Show discard selection text
                        self.__unhide_selections()
                        
                        # Initial dealing has bee achieve, and game is running
                        self.__dealt = True
                        self.__running = True
                        
                        # Entering discard phase
                        self.__deal_button.configure(text="DISCARD")
                    # Second Deal phase, after discard
                    else:
                        # Replace cards in player hand and start animation
                        for i in self.__cards_to_discard:
                            self.__player += Card(next(self.deck))
                        
                        # Cards not added to hand in order they are in discard pile
                        # Animate discarded cards in separate for loop to avoid calling flip() in None
                        for i in self.__cards_to_discard:
                            self.after(ANIMATION_RATE * ANIMATION_RATE * i, self.__deal_card, self.__player.hand[i], i)
                        
                        # Scoring phase; game has FINISHED
                        self.__score_hand()
                        self.__finished = True
                # Discard phase
                else:
                    # Take selected card indicies from pllayer hand and initiate animation
                    for i in self.__cards_to_discard:
                        self.__discard(self.__player.hand[i], i)
                    
                    # Entering Second Dealing phase
                    self.__dealt = False
                    self.__deal_button.configure(text='DEAL')
            else:
                showinfo('Bet Required', 'Please make a bet of at least one coin')
    
    def __add_funds(self):
        try:
            self.__player.money += simpledialog.askinteger('Funding', 'Enter amount to fund', minvalue=0)
            self.__player.save_bankroll()
            
            self.__update_info()
        except TypeError:
            pass
        except ValueError as err:
            showerror('ERROR', err.args[0])
    
    def __add_chips(self):
        try:
            value = simpledialog.askinteger('Chips', 'Add Chips', minvalue=1, maxvalue=self.__player.money // CHIP_VALUE)
            
            self.__player.money -= value * CHIP_VALUE
            self.__player.chips += value
            
            self.__update_info()
        except TypeError:
            pass
        except ValueError as err:
            showerror('ERROR', err.args[0])
    
    def __reset(self):
        self.__player.clear()
        self.__dealt = False
        self.__finished = False
        self.__score = None
        self.__running = False
        
        self.__cards_to_discard.clear()
        
        self.__reset_selections()
        
        # Save bank to file after every turn incase of unexpected program termination
        self.__player.save_bankroll()
        
        # If auto bet is set, check to make sure there are chips in player's bank
        if self.__auto_bet.get() and self.__player.chips > 0:
            if self.__auto_bet_amount > self.__player.chips:
                self.__bet.set(self.__player.chips)
            else:
                self.__bet.set(self.__auto_bet_amount)
        else:
            self.__bet.set(0)
        
        self.__update_info()
    
    def __update_info(self):
        self.__player_info.set(str(self.__player) + f'\n{'BET':>4} {self.__bet.get()}')
    
    def __info_trace(self, *args):
        self.__table.itemconfigure(self.__player_info_text, text=self.__player_info.get())
    
    def __check_wilds(self):
        if self.__running:
            if self.__wilds.get() == True:
                self.__wilds.set(False)
            else:
                self.__wilds.set(True)
    
    def __set_auto_bet(self):
        if self.__running:
            if self.__auto_bet.get() == True:
                self.__auto_bet.set(False)
            else:
                self.__auto_bet.set(True)
        else:
            if self.__auto_bet.get():
                self.__auto_bet_amount = simpledialog.askinteger('Auto Bet', 'How much would you like to auto bet', minvalue=0, maxvalue=50)
                self.__bet.set(self.__auto_bet_amount if not self.__bet.get() else self.__bet.get())
                self.__update_info()
    
    def __reset_selections(self):
        # Turn 'discard' into 'keep' and make text same color as background
        for selection in self.__selections:
            if self.__table.itemcget(selection, 'text') == 'DISCARD':
                self.__table.itemconfigure(selection, text='KEEP')
                self.__table.move(selection, 10, 0)
            
            self.__table.itemconfigure(selection, fill='green')
    
    def __unhide_selections(self):
        for selection in self.__selections:
            self.__table.itemconfigure(selection, text='KEEP', fill='#000000')
    
    def __scoring_window(self):
        window = Toplevel(self)
        
        # Remove frame to avoid closing window with 'x' button: causes aberrant behavior
        window.overrideredirect(True)
        window.geometry(f'+300+300')
        
        message = f'{str(self.__score)}\nPayout: {self.__bet.get() * int(self.__score)} chips'
        
        
        label = Label(window, text=message, style='Win.TLabel' if int(self.__score) > 0 else 'Lose.TLabel')
        label.pack()
        
        def done():
            window.destroy()
            self.__reset()
        
        button = Button(window, text='OK', command=done, style='TButton')
        button.pack()
    
    def __score_hand(self):
        self.__score = Score(self.__player.hand, self.__wilds.get())
        self.__player.chips += int(self.__score) * self.__bet.get()
        
        # Win/Loss sounds
        if int(self.__score) > 0:
            pg.play_sound_effect(join('Poker', 'sounds', 'win.wav'))
        else:
            pg.play_sound_effect(join('Poker', 'sounds', 'lose.mp3'))
        
        self.__scoring_window()
        
                
    def run(self):
        self.deiconify()
        
        # Start the main loop        
        mainloop()

if __name__ == '__main__':
    a = Game()
    a.run()