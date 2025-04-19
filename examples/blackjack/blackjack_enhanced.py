#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Enhanced Blackjack Game
=======================

This script implements a command-line Blackjack game with complete user experience features:
  - Exit option: Players can quit the game at any time
  - Pause function: Game can be paused during play
  - Restart option: Players can restart the game without exiting
  - Help menu: Comprehensive instructions available
  - Score tracking: Wins, losses, and draws are tracked across sessions

This demonstrates how proper default features enhance user experience in game applications.
"""

import random
import os
import time

# Game variables
player_cards = []
dealer_cards = []
game_over = False
player_score = 0
dealer_score = 0
paused = False
wins = 0
losses = 0
draws = 0

def clear_screen():
    """Clear the terminal screen for better user experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def deal_card():
    """Return a random card from the deck.
    
    Returns:
        int: Card value (Ace=11, face cards=10)
    """
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
    """Calculate the score of a hand, handling Aces appropriately.
    
    Args:
        cards (list): List of card values
        
    Returns:
        int: Score value (0 = Blackjack)
    """
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Blackjack (Ace + 10)
    
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    
    return sum(cards)

def display_cards():
    """Display the current game state including scores and cards."""
    clear_screen()
    print("=" * 50)
    print("BLACKJACK".center(50))
    print("=" * 50)
    print(f"Score: {wins} Wins, {losses} Losses, {draws} Draws")
    print("-" * 50)
    
    print("Your cards:", player_cards)
    print("Your score:", player_score)
    print()
    
    if game_over:
        print("Dealer's cards:", dealer_cards)
        print("Dealer's score:", dealer_score)
    else:
        print(f"Dealer's cards: [{dealer_cards[0]}, ?]")
        print(f"Dealer's visible score: {dealer_cards[0]}")
    
    print("-" * 50)

def compare(user_score, computer_score):
    """Compare player and dealer scores to determine the winner.
    
    Args:
        user_score (int): Player's score
        computer_score (int): Dealer's score
        
    Returns:
        str: Result message
    """
    global wins, losses, draws
    
    if user_score == computer_score:
        draws += 1
        return "Draw!"
    elif computer_score == 0:
        losses += 1
        return "You lose! Dealer has Blackjack."
    elif user_score == 0:
        wins += 1
        return "You win! You have Blackjack!"
    elif user_score > 21:
        losses += 1
        return "You lose! You went over 21."
    elif computer_score > 21:
        wins += 1
        return "You win! Dealer went over 21."
    elif user_score > computer_score:
        wins += 1
        return "You win!"
    else:
        losses += 1
        return "You lose!"

def pause_game():
    """Pause the game until user input is received."""
    global paused
    paused = True
    print("Game paused. Press Enter to continue...")
    input()
    paused = False
    display_cards()

def play_game():
    """Main game loop handling player actions and game logic.
    
    Returns:
        bool: True to play again, False to exit
    """
    global player_cards, dealer_cards, game_over, player_score, dealer_score
    
    # Reset game state
    player_cards = []
    dealer_cards = []
    game_over = False
    
    # Deal initial cards
    for _ in range(2):
        player_cards.append(deal_card())
        dealer_cards.append(deal_card())
    
    player_score = calculate_score(player_cards)
    dealer_score = calculate_score(dealer_cards)
    
    display_cards()
    
    # Player's turn
    while not game_over:
        if paused:
            time.sleep(0.1)
            continue
            
        player_score = calculate_score(player_cards)
        dealer_score = calculate_score(dealer_cards)
        
        if player_score == 0 or dealer_score == 0 or player_score > 21:
            game_over = True
        else:
            print("Actions: [H]it, [S]tand, [P]ause, [Q]uit, [R]estart")
            choice = input("> ").lower()
            
            if choice == 'h':
                player_cards.append(deal_card())
                player_score = calculate_score(player_cards)
                display_cards()
            elif choice == 's':
                game_over = True
                display_cards()
            elif choice == 'p':
                pause_game()
            elif choice == 'q':
                print("Thanks for playing!")
                return False  # Exit game
            elif choice == 'r':
                return True  # Restart game
            else:
                print("Invalid action. Please try again.")
                time.sleep(1)
                display_cards()
    
    # Dealer's turn
    while dealer_score != 0 and dealer_score < 17 and player_score <= 21:
        dealer_cards.append(deal_card())
        dealer_score = calculate_score(dealer_cards)
    
    display_cards()
    result = compare(player_score, dealer_score)
    print(result)
    
    # Ask to play again
    print("Actions: [Y]es play again, [N]o quit game")
    while True:
        choice = input("> ").lower()
        if choice == 'y':
            return True  # Continue playing
        elif choice == 'n':
            print("Thanks for playing!")
            return False  # Exit game
        else:
            print("Invalid action. Please enter Y or N")

def display_help():
    """Display game rules and controls."""
    clear_screen()
    print("=" * 50)
    print("BLACKJACK HELP".center(50))
    print("=" * 50)
    print("Game Rules:")
    print("1. You and the dealer each receive two cards")
    print("2. Cards 2-10 are worth their face value")
    print("3. Face cards (J/Q/K) are worth 10 points")
    print("4. Aces are worth 11 or 1 points (automatically adjusted)")
    print("5. The goal is to get as close to 21 as possible without exceeding it")
    print("6. The dealer must hit until they have at least 17 points")
    print("7. If you exceed 21 points, you lose immediately")
    print("\nControls:")
    print("  H - Hit (take another card)")
    print("  S - Stand (end your turn)")
    print("  P - Pause game")
    print("  Q - Quit game")
    print("  R - Restart game")
    print("\nPress Enter to return to the game...")
    input()

def show_welcome():
    """Display welcome screen and main menu.
    
    Returns:
        bool: True to start game, False to exit
    """
    clear_screen()
    print("=" * 50)
    print("WELCOME TO BLACKJACK".center(50))
    print("=" * 50)
    print("\n[1] Start Game")
    print("[2] Help")
    print("[3] Exit")
    
    choice = input("\nSelect an option: ")
    if choice == '1':
        return True
    elif choice == '2':
        display_help()
        return show_welcome()
    elif choice == '3':
        print("Thanks for your interest. Goodbye!")
        return False
    else:
        print("Invalid selection. Please try again.")
        time.sleep(1)
        return show_welcome()

def main():
    """Main program entry point."""
    if not show_welcome():
        return
    
    playing = True
    while playing:
        playing = play_game()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")
