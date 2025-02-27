import random
import time
import os
from typing import List, Tuple
from colorama import init, Fore, Back, Style

init(autoreset=True)

CARD_TEMPLATE = """
┌─────────┐
│ {}      │
│         │
│    {}   │
│         │
│       {}│
└─────────┘"""

CARD_BACK = """
┌─────────┐
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
└─────────┘"""

class Card:
    def __init__(self, suit: str, value: str):
        self.suit = suit
        self.value = value
        
    def get_numeric_value(self) -> int:
        if self.value in ['J', 'Q', 'K', '10']:
            return 0
        elif self.value == 'A':
            return 1
        return int(self.value)
        
    def __str__(self):
        return f"{self.value} of {self.suit}"
    
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

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.cards)
    
    def draw(self) -> Card:
        return self.cards.pop()

class Baccarat:
    def __init__(self):
        self.deck = Deck()
        self.history = []
        self.stats = {'player_wins': 0, 'banker_wins': 0, 'ties': 0}
        
    def calculate_hand(self, cards: List[Card]) -> int:
        return sum(card.get_numeric_value() for card in cards) % 10
        
    def should_draw_third_card(self, hand: List[Card], is_player: bool, banker_score: int = None) -> bool:
        score = self.calculate_hand(hand)
        
        if is_player:
            return score < 6
        else:
            if score < 3:
                return True
            if score >= 7:
                return False
            
            player_third = banker_score
            if score == 3 and player_third != 8:
                return True
            if score == 4 and player_third in [2, 3, 4, 5, 6, 7]:
                return True
            if score == 5 and player_third in [4, 5, 6, 7]:
                return True
            if score == 6 and player_third in [6, 7]:
                return True
            return False

    def deal_initial_cards(self) -> Tuple[List[Card], List[Card]]:
        player_hand = [self.deck.draw(), self.deck.draw()]
        banker_hand = [self.deck.draw(), self.deck.draw()]
        return player_hand, banker_hand

    def display_hands(self, player_hand: List[Card], banker_hand: List[Card], hide_player_second: bool = False):
        print("\n" + Fore.CYAN + "Banker's Hand:" + Style.RESET_ALL)
        banker_cards = [card.display().split('\n') for card in banker_hand]
        for i in range(len(banker_cards[0])):
            print(''.join(card[i] for card in banker_cards))
            
        print("\n" + Fore.GREEN + "Player's Hand:" + Style.RESET_ALL)
        if hide_player_second:
            player_cards = [player_hand[0].display().split('\n')]
            player_cards.append(CARD_BACK.split('\n'))
        else:
            player_cards = [card.display().split('\n') for card in player_hand]
        
        for i in range(len(player_cards[0])):
            print(''.join(card[i] for card in player_cards))

    def play_game(self, bet_on: str, player_hand: List[Card], banker_hand: List[Card]) -> Tuple[str, int]:
        player_score = self.calculate_hand(player_hand)
        banker_score = self.calculate_hand(banker_hand)
        
        print("\n" + Fore.YELLOW + "Revealing all cards..." + Style.RESET_ALL)
        time.sleep(1)
        self.display_hands(player_hand, banker_hand, hide_player_second=False)
        
        if player_score >= 8 or banker_score >= 8:
            print(Fore.YELLOW + "\nNatural win!" + Style.RESET_ALL)
            final_player = player_score
            final_banker = banker_score
        else:
            player_third_card = None
            if self.should_draw_third_card(player_hand, True):
                print(Fore.GREEN + "\nPlayer draws third card..." + Style.RESET_ALL)
                time.sleep(1)
                player_hand.append(self.deck.draw())
                player_third_card = player_hand[-1].get_numeric_value()
                player_score = self.calculate_hand(player_hand)
                self.display_hands(player_hand, banker_hand)
            
            if self.should_draw_third_card(banker_hand, False, player_third_card):
                print(Fore.CYAN + "\nBanker draws third card..." + Style.RESET_ALL)
                time.sleep(1)
                banker_hand.append(self.deck.draw())
                banker_score = self.calculate_hand(banker_hand)
                self.display_hands(player_hand, banker_hand)
                
        final_player = player_score
        final_banker = banker_score
        
        print(f"\n{Fore.GREEN}Player Score: {final_player}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Banker Score: {final_banker}{Style.RESET_ALL}")
        
        if final_player > final_banker:
            winner = 'player'
            self.stats['player_wins'] += 1
        elif final_banker > final_player:
            winner = 'banker'
            self.stats['banker_wins'] += 1
        else:
            winner = 'tie'
            self.stats['ties'] += 1
            
        winnings = -1
        if winner == bet_on:
            if bet_on == 'banker':
                winnings = 0.95  # 5% commission on banker wins
            elif bet_on == 'tie':
                winnings = 8
            else:
                winnings = 1
                
        self.history.append({'winner': winner, 'player_score': final_player, 'banker_score': final_banker})
        return winner, winnings

def main():
    # Clear console
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(Fore.YELLOW + """
    ╔══════════════════════════════════════╗
    ║           BACCARAT GAME              ║
    ╚══════════════════════════════════════╝
    """ + Style.RESET_ALL)
    
    game = Baccarat()
    balance = 100
    initial_balance = balance
    
    try:
        while balance > 0:
            print(f"\n{Fore.YELLOW}Your balance: ${balance}{Style.RESET_ALL}")
            print(f"Session: {'▲' if balance > initial_balance else '▼'} ${abs(balance - initial_balance)}")
            
            if len(game.history) > 0:
                print("\nLast 5 results:", ' '.join([
                    Fore.GREEN + 'P' if h['winner'] == 'player' else
                    Fore.CYAN + 'B' if h['winner'] == 'banker' else
                    Fore.YELLOW + 'T' for h in game.history[-5:]
                ]) + Style.RESET_ALL)
            
            player_hand, banker_hand = game.deal_initial_cards()
            print(Fore.CYAN + "\nDealing cards..." + Style.RESET_ALL)
            time.sleep(1)
            game.display_hands(player_hand, banker_hand, hide_player_second=True)
            
            while True:
                bet_input = input(f"Enter your bet amount (Balance: ${balance}, 0 to quit): ").strip()
                if not bet_input.isdigit():
                    print("Invalid bet amount! Please enter a number.")
                    continue
                bet = int(bet_input)
                break
            
            if bet == 0:
                break
                
            if bet > balance:
                print("Insufficient funds!")
                continue
                
            while True:
                choice = input("Bet on (player/banker/tie): ").lower()
                if choice in ['player', 'banker', 'tie']:
                    break
                print("Invalid choice! Please choose player, banker, or tie.")
            
            winner, multiplier = game.play_game(choice, player_hand, banker_hand)
            winnings = bet * multiplier
            balance += winnings
            
            print(f"\nWinner: {winner}")
            if multiplier > 0:
                print(f"You won ${winnings}!")
            else:
                print(f"You lost ${bet}!")
                
            if len(game.deck.cards) < 6:
                print(Fore.YELLOW + "\n🔄 Shuffling new deck..." + Style.RESET_ALL)
                time.sleep(1)
                game = Baccarat()
                
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        print(f"\n{Fore.YELLOW}Game over! Final balance: ${balance}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
