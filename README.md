# Josha Cirbo's 5 Card Draw Poker

## Description
This is a Poker Simulator made by Josha Cirbo for the final project of CSC2017 Advanced Python. In order to run it, you must have the TKinter, pythonGraph, and Pygame packages installed. Pygame is included because it is a dependency of pythonGraph.

To install the necessary packages, copy the following command (terminal) prompts.
- pip3 install tk
- pip3 install pygame
- pip3 install pythongraph

## Play
When the game starts, it asks your name, an initial cash infusion if you have no bank file or have a balance of 0, and the number of decks you want to use. Deck number is a crucial variable for game play. So, it is mandatory.

In order to place bets, you need to have chips in your *bank*. You can add chips if you have the *cash* to do it. Each chip costs $5. You need to bet at least one chip to play. You may raise your bet by one chip, a custom chip amount, or you may bet your entire bank (so-called *all in*). You may bet up to 50 chips with single bets or custom bets, but you can bet your entire bank with the all in button if you are feeling lucky. If you choose to raise your bet by 1 chip and you do not have a balance in your bank, you will be asked to increase your cash or fund your bank.

When you are ready to play, press the **deal** button. Five cards will be dealt. You may choose to keep or discard any or all of the five. When you have chosen your discard group, press the **discard** button. Your cards will be taken. After the cards have been removed, press the **deal** button again, and your discarded cards will be replaced. At this time, your game is scored, and your payout is given.

You can optionally play straight poker by unchecking the **deuces wild** checkbox in the top left, which treats 2's of any suit as wilds. Your score with wilds will be the highest possible out of all combinations of regular cards and wilds. With wilds on, five of a kind is possible. It is not possible with wilds off.

## Scoring
1. Five of a Kind: 5000 chips
2. Royal Flush: 2000 chips
3. Straight Flush: 250 chips
4. Four of a Kind: 125
5. Full House: 40
6. Flush: 25
7. Straight: 20
8. Three of a Kind: 15
9. Two Pair: 10
10. High Pair (Jacks or better): 1
11. Anything else: 0 (loss)

If you bet is larger than 1 chip, the bet will be multiplied by the score. High Pairs pay one to one. So, even though it is not a loss, it also not a win. You break even.

## Features
This project includes the basic rules of the project plus deuces wild and audio through pythonGraphics. No unittests were conducted, but every aspect of each class was thoroughly tested. Please let me know if you find any bugs.