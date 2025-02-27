import random
import time
import os
from typing import List, Tuple
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
        
    def get_numeric_value(self) -> int:
        values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11}
        return values.get(self.value) or int(self.value)
        
    def get_symbol(self) -> str:
        symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        return symbols[self.suit]
    
    def get_color(self) -> str:
        return Fore.RED if self.suit in ['Hearts', 'Diamonds'] else Fore.WHITE
        
    def display(self) -> str:
        color = self.get_color()
        symbol = self.get_symbol()
        val = self.value.ljust(2)
        return color + CARD_TEMPLATE.format(val, symbol, val) + Style.RESET_ALL

class PaiGowHand:
    def __init__(self, cards: List[Card]):
        self.cards = sorted(cards, key=lambda x: x.get_numeric_value(), reverse=True)
        
    def get_hand_rank(self) -> Tuple[int, List[int]]:
        values = [card.get_numeric_value() for card in self.cards]
        suits = [card.suit for card in self.cards]
        
        # Check for straight flush
        if (len(set(suits)) == 1 and 
            max(values) - min(values) == len(values) - 1):
            return (8, values)
            
        # Check for four of a kind
        for val in set(values):
            if values.count(val) == 4:
                kickers = [v for v in values if v != val]
                return (7, [val] * 4 + kickers)
                
        # Check for full house
        if len(set(values)) == 2:
            val1 = max(set(values), key=values.count)
            val2 = min(set(values), key=values.count)
            if values.count(val1) == 3:
                return (6, [val1] * 3 + [val2] * 2)
                
        # Check for flush
        if len(set(suits)) == 1:
            return (5, values)
            
        # Check for straight
        if max(values) - min(values) == len(values) - 1:
            return (4, values)
            
        # Check for three of a kind
        for val in set(values):
            if values.count(val) == 3:
                kickers = sorted([v for v in values if v != val], reverse=True)
                return (3, [val] * 3 + kickers)
                
        # Check for two pair
        pairs = [val for val in set(values) if values.count(val) == 2]
        if len(pairs) == 2:
            kicker = [val for val in values if val not in pairs][0]
            return (2, sorted(pairs, reverse=True) * 2 + [kicker])
            
        # Check for one pair
        for val in set(values):
            if values.count(val) == 2:
                kickers = sorted([v for v in values if v != val], reverse=True)
                return (1, [val] * 2 + kickers)
                
        # High card
        return (0, values)
        
    def display(self) -> str:
        cards_display = [card.display().split('\n') for card in self.cards]
        result = []
        for i in range(len(cards_display[0])):
            line = ''
            for card_lines in cards_display:
                if i < len(card_lines):
                    line += card_lines[i] + ' '
            result.append(line)
        return '\n'.join(result)

class PaiGow:
    def __init__(self):
        self.deck = self.create_deck()
        self.stats = {'games': 0, 'wins': 0, 'pushes': 0}
        
    def create_deck(self) -> List[Card]:
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(deck)
        return deck
        
    def deal_hands(self) -> Tuple[List[Card], List[Card]]:
        player_cards = [self.deck.pop() for _ in range(7)]
        dealer_cards = [self.deck.pop() for _ in range(7)]
        return player_cards, dealer_cards
        
    def set_hands(self, cards: List[Card], is_dealer: bool = False) -> Tuple[PaiGowHand, PaiGowHand]:
        if is_dealer:
            # Simple dealer strategy: put highest cards in back hand
            sorted_cards = sorted(cards, key=lambda x: x.get_numeric_value(), reverse=True)
            back_hand = PaiGowHand(sorted_cards[:5])
            front_hand = PaiGowHand(sorted_cards[5:])
            return back_hand, front_hand
            
        while True:
            print("\nYour seven cards:")
            for i, card in enumerate(cards):
                print(f"{i+1}: {card.value} of {card.suit}")
                
            try:
                indices = input("\nEnter five numbers for back hand (e.g., 1 2 3 4 5): ").split()
                if len(indices) != 5:
                    print("Please select exactly 5 cards for the back hand!")
                    continue
                    
                indices = [int(i) - 1 for i in indices]
                if not all(0 <= i < 7 for i in indices):
                    print("Invalid card numbers!")
                    continue
                    
                back_cards = [cards[i] for i in indices]
                front_cards = [card for i, card in enumerate(cards) if i not in indices]
                
                back_hand = PaiGowHand(back_cards)
                front_hand = PaiGowHand(front_cards)
                
                # Check if back hand is stronger than front hand
                if back_hand.get_hand_rank() <= front_hand.get_hand_rank():
                    print("Back hand must be stronger than front hand!")
                    continue
                    
                return back_hand, front_hand
                
            except ValueError:
                print("Invalid input! Please enter numbers separated by spaces.")
                
    def compare_hands(self, player_back: PaiGowHand, player_front: PaiGowHand,
                     dealer_back: PaiGowHand, dealer_front: PaiGowHand) -> str:
        back_result = player_back.get_hand_rank() > dealer_back.get_hand_rank()
        front_result = player_front.get_hand_rank() > dealer_front.get_hand_rank()
        
        if back_result and front_result:
            return 'win'
        elif not back_result and not front_result:
            return 'lose'
        else:
            return 'push'

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + """
    ╔════════════════════════════════╗
    ║         PAI GOW POKER          ║
    ╚════════════════════════════════╝
    """ + Style.RESET_ALL)
    
    game = PaiGow()
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
            
            # Deal and display cards
            player_cards, dealer_cards = game.deal_hands()
            
            # Player sets hands
            print(f"\n{Fore.GREEN}Setting your hands...{Style.RESET_ALL}")
            player_back, player_front = game.set_hands(player_cards)
            
            # Dealer sets hands
            print(f"\n{Fore.CYAN}Dealer setting hands...{Style.RESET_ALL}")
            dealer_back, dealer_front = game.set_hands(dealer_cards, is_dealer=True)
            
            # Display both hands
            print(f"\n{Fore.GREEN}Your back hand:{Style.RESET_ALL}")
            print(player_back.display())
            print(f"\n{Fore.GREEN}Your front hand:{Style.RESET_ALL}")
            print(player_front.display())
            
            print(f"\n{Fore.CYAN}Dealer's back hand:{Style.RESET_ALL}")
            print(dealer_back.display())
            print(f"\n{Fore.CYAN}Dealer's front hand:{Style.RESET_ALL}")
            print(dealer_front.display())
            
            # Determine winner
            result = game.compare_hands(player_back, player_front, dealer_back, dealer_front)
            
            if result == 'win':
                game.stats['wins'] += 1
                balance += bet * 2
                print(f"\n{Fore.GREEN}You win ${bet}!{Style.RESET_ALL}")
            elif result == 'push':
                game.stats['pushes'] += 1
                balance += bet
                print(f"\n{Fore.YELLOW}Push! Bet returned.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}You lose ${bet}!{Style.RESET_ALL}")
            
            # Create new deck if running low
            if len(game.deck) < 14:
                game.deck = game.create_deck()
                print(f"\n{Fore.YELLOW}Shuffling new deck...{Style.RESET_ALL}")
                
    except KeyboardInterrupt:
        print("\nCashing out...")
    finally:
        print(f"\n{Fore.YELLOW}Game Over!")
        print(f"Final Balance: ${balance}")
        print(f"Games Played: {game.stats['games']}")
        print(f"Wins: {game.stats['wins']}")
        print(f"Pushes: {game.stats['pushes']}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
