import random
import time
import os
from colorama import init, Fore, Style

init(autoreset=True)

CARD_TEMPLATE = """
┌─────────┐
│ {}      │
│         │
│    {}   │
│         │
│      {} │
└─────────┘"""

class Card:
    def __init__(self, suit: str, value: str):
        self.suit = suit
        self.value = value
        
    def get_numeric_value(self) -> list:
        if self.value in ['J', 'Q', 'K']:
            return [10]
        elif self.value == 'A':
            return [1, 11]
        return [int(self.value)]
        
    def get_symbol(self) -> str:
        symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        return symbols[self.suit]
    
    def get_color(self) -> str:
        return Fore.RED if self.suit in ['Hearts', 'Diamonds'] else Fore.WHITE
    
    def display(self, hidden: bool = False) -> str:
        if hidden:
            return Fore.BLUE + """
┌─────────┐
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
└─────────┘""" + Style.RESET_ALL
        
        color = self.get_color()
        symbol = self.get_symbol()
        val = self.value.ljust(2)
        return color + CARD_TEMPLATE.format(val, symbol, val) + Style.RESET_ALL

class Deck:
    def __init__(self, num_decks: int = 6):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [Card(suit, value) for _ in range(num_decks) 
                     for suit in suits for value in values]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self) -> Card:
        if len(self.cards) < 20:  # Reshuffle when low on cards
            print(f"{Fore.YELLOW}Shuffling new deck...{Style.RESET_ALL}")
            self.__init__()
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card: Card):
        self.cards.append(card)
    
    def get_value(self) -> int:
        values = [0]
        for card in self.cards:
            new_values = []
            for card_value in card.get_numeric_value():
                for value in values:
                    new_values.append(value + card_value)
            values = new_values
        
        valid_values = [v for v in values if v <= 21]
        return max(valid_values) if valid_values else min(values)
    
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_bust(self) -> bool:
        return self.get_value() > 21
    
    def display(self, hide_first: bool = False):
        cards_display = [card.display(hidden=(hide_first and i == 0)) 
                        for i, card in enumerate(self.cards)]
        
        # Split each card's display into lines
        card_lines = [card.split('\n') for card in cards_display]
        
        # Filter out empty lines and ensure all lines are present
        card_lines = [[line for line in card if line.strip()] for card in card_lines]
        
        # Combine lines from all cards
        result = []
        if card_lines:
            for i in range(len(card_lines[0])):
                line = ''
                for card in card_lines:
                    if i < len(card):
                        line += card[i] + ' '
                result.append(line)
        
        return '\n'.join(result)

class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.stats = {'games': 0, 'wins': 0, 'pushes': 0, 'blackjacks': 0}
    
    def deal_initial_cards(self) -> tuple:
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.add_card(self.deck.draw())
        dealer_hand.add_card(self.deck.draw())
        player_hand.add_card(self.deck.draw())
        dealer_hand.add_card(self.deck.draw())
        
        return player_hand, dealer_hand
    
    def play_round(self, player_hand: Hand, dealer_hand: Hand, bet: int) -> tuple:
        # Check for initial blackjacks
        if player_hand.is_blackjack() and dealer_hand.is_blackjack():
            return 'push', bet
        elif player_hand.is_blackjack():
            self.stats['blackjacks'] += 1
            return 'blackjack', bet * 2.5
        elif dealer_hand.is_blackjack():
            return 'dealer', 0
        
        # Player's turn
        while True:
            print(f"\n{Fore.GREEN}Your hand ({player_hand.get_value()}):{Style.RESET_ALL}")
            print(player_hand.display())
            print(f"\n{Fore.CYAN}Dealer's hand:{Style.RESET_ALL}")
            print(dealer_hand.display(hide_first=True))
            
            action = input("\nWhat would you like to do? (hit/stand): ").lower()
            if action == 'hit':
                player_hand.add_card(self.deck.draw())
                if player_hand.is_bust():
                    return 'dealer', 0
            elif action == 'stand':
                break
        
        # Dealer's turn
        print(f"\n{Fore.CYAN}Dealer reveals cards:{Style.RESET_ALL}")
        print(dealer_hand.display())
        time.sleep(1)
        
        while dealer_hand.get_value() < 17:
            print(f"\n{Fore.CYAN}Dealer hits...{Style.RESET_ALL}")
            dealer_hand.add_card(self.deck.draw())
            print(dealer_hand.display())
            time.sleep(1)
        
        player_value = player_hand.get_value()
        dealer_value = dealer_hand.get_value()
        
        if dealer_hand.is_bust():
            return 'player', bet * 2
        elif player_value > dealer_value:
            return 'player', bet * 2
        elif dealer_value > player_value:
            return 'dealer', 0
        else:
            return 'push', bet

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + """
    ╔════════════════════════════════╗
    ║          BLACKJACK             ║
    ╚════════════════════════════════╝
    """ + Style.RESET_ALL)
    
    game = Blackjack()
    balance = 100
    initial_balance = balance
    
    try:
        while balance > 0:
            print(f"\n{Fore.YELLOW}Balance: ${balance}")
            print(f"Session: {'▲' if balance > initial_balance else '▼'} ${abs(balance - initial_balance)}")
            
            bet = 0
            while True:
                try:
                    bet = int(input(f"Enter bet amount (1-{balance}, 0 to quit): "))
                    if bet == 0:
                        raise KeyboardInterrupt
                    if 0 < bet <= balance:
                        break
                    print(f"Please enter a bet between 1 and {balance}")
                except ValueError:
                    print("Invalid bet amount!")
            
            balance -= bet
            game.stats['games'] += 1
            
            player_hand, dealer_hand = game.deal_initial_cards()
            result, winnings = game.play_round(player_hand, dealer_hand, bet)
            
            if result == 'player':
                game.stats['wins'] += 1
                print(f"\n{Fore.GREEN}You win ${winnings - bet}!{Style.RESET_ALL}")
            elif result == 'blackjack':
                game.stats['wins'] += 1
                print(f"\n{Fore.GREEN}BLACKJACK! You win ${winnings - bet}!{Style.RESET_ALL}")
            elif result == 'push':
                game.stats['pushes'] += 1
                print(f"\n{Fore.YELLOW}Push! Bet returned.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Dealer wins! You lose ${bet}!{Style.RESET_ALL}")
            
            balance += winnings
            
    except KeyboardInterrupt:
        print("\nCashing out...")
    finally:
        print(f"\n{Fore.YELLOW}Game Over!")
        print(f"Final Balance: ${balance}")
        print(f"Games Played: {game.stats['games']}")
        print(f"Wins: {game.stats['wins']}")
        print(f"Pushes: {game.stats['pushes']}")
        print(f"Blackjacks: {game.stats['blackjacks']}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
