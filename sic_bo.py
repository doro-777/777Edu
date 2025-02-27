import random
import time
import os
from colorama import init, Fore, Style

init(autoreset=True)

DICE_FRAMES = {
    1: ["""
 ┌─────────┐
 │         │
 │    ●    │
 │         │
 └─────────┘"""],
    
    2: ["""
 ┌─────────┐
 │  ●      │
 │         │
 │      ●  │
 └─────────┘"""],
    
    3: ["""
 ┌─────────┐
 │  ●      │
 │    ●    │
 │      ●  │
 └─────────┘"""],
    
    4: ["""
 ┌─────────┐
 │  ●   ●  │
 │         │
 │  ●   ●  │
 └─────────┘"""],
    
    5: ["""
 ┌─────────┐
 │  ●   ●  │
 │    ●    │
 │  ●   ●  │
 └─────────┘"""],
    
    6: ["""
 ┌─────────┐
 │  ●   ●  │
 │  ●   ●  │
 │  ●   ●  │
 └─────────┘"""]
}

BETS = {
    'small': {'desc': 'Sum 4-10 (excl. triples)', 'payout': 1},
    'big': {'desc': 'Sum 11-17 (excl. triples)', 'payout': 1},
    'odd': {'desc': 'Sum is odd', 'payout': 1},
    'even': {'desc': 'Sum is even', 'payout': 1},
    'triple': {'desc': 'All three dice show same number', 'payout': 30},
    'double': {'desc': 'Any two dice show same number', 'payout': 8},
    'total': {'desc': 'Exact sum of three dice (4-17)', 'payout': {
        4: 60, 5: 30, 6: 17, 7: 12, 8: 8, 9: 6, 10: 6,
        11: 6, 12: 6, 13: 8, 14: 12, 15: 17, 16: 30, 17: 60
    }},
    'single': {'desc': 'Chosen number appears on 1+ dice', 'payout': {
        1: 1, 2: 2, 3: 3  # Times appeared = payout
    }}
}

class SicBo:
    def __init__(self):
        self.history = []
        self.stats = {'rolls': 0, 'wins': 0, 'biggest_win': 0}
    
    def roll_dice(self) -> tuple:
        return tuple(random.randint(1, 6) for _ in range(3))
    
    def animate_roll(self):
        frames = 10
        for _ in range(frames):
            os.system('cls' if os.name == 'nt' else 'clear')
            temp_dice = [random.randint(1, 6) for _ in range(3)]
            self.display_dice(temp_dice)
            time.sleep(0.1)
    
    def display_dice(self, dice: list):
        dice_art = [DICE_FRAMES[d][0].split('\n') for d in dice]
        for i in range(len(dice_art[0])):
            print('  '.join(d[i] for d in dice_art))
    
    def check_win(self, bet_type: str, bet_value: any, result: tuple) -> float:
        total = sum(result)
        
        if bet_type == 'small':
            return 1 if 4 <= total <= 10 and len(set(result)) > 1 else 0
            
        elif bet_type == 'big':
            return 1 if 11 <= total <= 17 and len(set(result)) > 1 else 0
            
        elif bet_type == 'odd':
            return 1 if total % 2 == 1 else 0
            
        elif bet_type == 'even':
            return 1 if total % 2 == 0 else 0
            
        elif bet_type == 'triple':
            return 30 if len(set(result)) == 1 else 0
            
        elif bet_type == 'double':
            value_counts = [result.count(i) for i in set(result)]
            return 8 if 2 in value_counts else 0
            
        elif bet_type == 'total':
            return BETS[bet_type]['payout'].get(total, 0)
            
        elif bet_type == 'single':
            count = result.count(int(bet_value))
            return BETS[bet_type]['payout'].get(count, 0)
            
        return 0

def display_menu():
    print("\nBetting Options:")
    for bet_type, info in BETS.items():
        if bet_type == 'total':
            print(f"{bet_type}: {info['desc']} (Payout varies 6x-60x)")
        elif bet_type == 'single':
            print(f"{bet_type}: {info['desc']} (Payout 1x-3x)")
        else:
            print(f"{bet_type}: {info['desc']} (Pays {info['payout']}:1)")

def get_bet_input(balance: int) -> tuple:
    while True:
        try:
            bet_amount = int(input(f"\nEnter bet amount (1-{balance}, 0 to quit): "))
            if bet_amount == 0:
                return None, None, 0
            if not 0 < bet_amount <= balance:
                print(f"Please enter a bet between 1 and {balance}")
                continue
                
            bet_type = input("Enter bet type: ").lower()
            if bet_type not in BETS:
                print("Invalid bet type!")
                continue
                
            bet_value = None
            if bet_type == 'total':
                bet_value = input("Enter total sum (4-17): ")
                if not bet_value.isdigit() or not 4 <= int(bet_value) <= 17:
                    print("Invalid total!")
                    continue
                bet_value = int(bet_value)
            elif bet_type == 'single':
                bet_value = input("Enter number (1-6): ")
                if not bet_value.isdigit() or not 1 <= int(bet_value) <= 6:
                    print("Invalid number!")
                    continue
                bet_value = int(bet_value)
                
            return bet_type, bet_value, bet_amount
        except ValueError:
            print("Invalid input!")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + """
    ╔════════════════════════════════╗
    ║           SIC BO               ║
    ╚════════════════════════════════╝
    """ + Style.RESET_ALL)
    
    game = SicBo()
    balance = 100
    initial_balance = balance
    
    try:
        while balance > 0:
            print(f"\n{Fore.YELLOW}Balance: ${balance}")
            print(f"Session: {'▲' if balance > initial_balance else '▼'} ${abs(balance - initial_balance)}")
            
            if game.history:
                print("\nLast 5 rolls:", ' '.join(
                    f"{sum(roll)}({','.join(map(str, roll))})"
                    for roll in game.history[-5:]
                ))
            
            display_menu()
            bet_type, bet_value, bet_amount = get_bet_input(balance)
            
            if bet_type is None:
                break
                
            balance -= bet_amount
            print(f"\n{Fore.CYAN}Rolling dice...{Style.RESET_ALL}")
            game.animate_roll()
            
            result = game.roll_dice()
            game.history.append(result)
            game.stats['rolls'] += 1
            
            print(f"\n{Fore.CYAN}Final Result:{Style.RESET_ALL}")
            game.display_dice(result)
            print(f"Sum: {sum(result)}")
            
            multiplier = game.check_win(bet_type, bet_value, result)
            winnings = bet_amount * multiplier
            
            if multiplier > 0:
                balance += winnings
                game.stats['wins'] += 1
                game.stats['biggest_win'] = max(game.stats['biggest_win'], winnings - bet_amount)
                print(f"\n{Fore.GREEN}You won ${winnings - bet_amount}!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}You lost ${bet_amount}!{Style.RESET_ALL}")
                
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    finally:
        print(f"\n{Fore.YELLOW}Game Over!")
        print(f"Final Balance: ${balance}")
        print(f"Total Rolls: {game.stats['rolls']}")
        print(f"Wins: {game.stats['wins']}")
        print(f"Biggest Win: ${game.stats['biggest_win']}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
