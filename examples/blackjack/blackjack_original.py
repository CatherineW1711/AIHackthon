#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic Blackjack Game
====================

This script implements a simple command-line Blackjack game without default features.
This represents what a typical AI-generated code might look like - functional but
missing important user experience features.
"""

import random

def deal_card():
    """Return a random card from the deck."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
    """Calculate the score of a hand, handling Aces appropriately."""
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Blackjack (Ace + 10)
    
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    
    return sum(cards)

def compare(user_score, computer_score):
    """Compare player and dealer scores to determine the winner."""
    if user_score == computer_score:
        return "Draw!"
    elif computer_score == 0:
        return "You lose! Dealer has Blackjack."
    elif user_score == 0:
        return "You win! You have Blackjack!"
    elif user_score > 21:
        return "You lose! You went over 21."
    elif computer_score > 21:
        return "You win! Dealer went over 21."
    elif user_score > computer_score:
        return "You win!"
    else:
        return "You lose!"

def play_game():
    """Play a single game of Blackjack."""
    user_cards = []
    computer_cards = []
    
    # Deal initial cards
    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())
    
    # Player's turn
    game_over = False
    while not game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)
        
        print(f"Your cards: {user_cards}, current score: {user_score}")
        print(f"Computer's first card: {computer_cards[0]}")
        
        if user_score == 0 or computer_score == 0 or user_score > 21:
            game_over = True
        else:
            should_continue = input("Type 'y' to get another card, type 'n' to pass: ")
            if should_continue == 'y':
                user_cards.append(deal_card())
            else:
                game_over = True
    
    # Computer's turn
    while computer_score != 0 and computer_score < 17 and user_score <= 21:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)
    
    print(f"Your final hand: {user_cards}, final score: {user_score}")
    print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
    print(compare(user_score, computer_score))

# Start the game
play_game()
