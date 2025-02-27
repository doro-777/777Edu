import random
import time
import os
from colorama import init, Fore, Style

init(autoreset=True)

SYMBOLS = {
    '7': (Fore.RED + '７' + Style.RESET_ALL, 10),
    'BAR': (Fore.YELLOW + '█' + Style.RESET_ALL, 5),
    'BELL': (Fore.YELLOW + '🔔' + Style.RESET_ALL, 4),
    'CHERRY': (Fore.RED + '●' + Style.RESET_ALL, 3),
    'LEMON': (Fore.YELLOW + '©' + Style.RESET_ALL, 2),
}

PAYLINES = {
    ('7', '7', '7'): 100,
    ('BAR', 'BAR', 'BAR'): 50,
    ('BELL', 'BELL', 'BELL'): 40,
    ('CHERRY', 'CHERRY', 'CHERRY'): 30,
    ('LEMON', 'LEMON', 'LEMON'): 20,
    ('CHERRY', 'CHERRY', '*'): 5,
    ('CHERRY', '*', '*'): 2,
}

class SlotMachine:
    def __init__(self):
        self.symbols = list(SYMBOLS.keys())
        self.stats = {'spins': 0, 'wins': 0, 'biggest_win': 0}
        
    def spin(self) -> tuple:
        return tuple(random.choice(self.symbols) for _ in range(3))
    
    def calculate_win(self, result: tuple, bet: int) -> int:
        for pattern, multiplier in PAYLINES.items():
            matches = 0
            for i, symbol in enumerate(pattern):
                if symbol == '*' or symbol == result[i]:
                    matches += 1
                else:
                    break
            if matches == len(pattern):
                return bet * multiplier
        return 0
    
    def display_spin_animation(self):
        frames = ['| • ◦ ◦ |', '| ◦ • ◦ |', '| ◦ ◦ • |']
        for _ in range(2):  # Two complete cycles
            for frame in frames:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\n\n\n{Fore.CYAN}{frame}", end='')
                time.sleep(0.1)
        print("\r", end='')
    
    def display_result(self, result: tuple):
        symbols_display = [SYMBOLS[s][0] for s in result]
        
        print(f"""
╔═══╦═══╦═══╗
║ {symbols_display[0]} ║ {symbols_display[1]} ║ {symbols_display[2]} ║
╚═══╩═══╩═══╝""")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + """
    ╔════════════════════════════════╗
    ║         SLOT MACHINE           ║
    ╚════════════════════════════════╝
    """ + Style.RESET_ALL)
    
    print("PAYTABLE:")
    for symbols, payout in PAYLINES.items():
        symbols_str = ' '.join(SYMBOLS[s][0] if s != '*' else '*' for s in symbols)
        print(f"{symbols_str}: {payout}x")
    
    machine = SlotMachine()
    balance = 100
    initial_balance = balance
    
    try:
        while balance > 0:
            print(f"\n{Fore.YELLOW}Balance: ${balance}")
            print(f"Session: {'▲' if balance > initial_balance else '▼'} ${abs(balance - initial_balance)}")
            
            while True:
                bet_input = input(f"Enter bet amount (1-{balance}, 0 to quit): ").strip()
                if not bet_input.isdigit():
                    print("Invalid bet amount! Please enter a number.")
                    continue
                bet = int(bet_input)
                if bet == 0:
                    raise KeyboardInterrupt
                if 0 < bet <= balance:
                    break
                print(f"Please enter a bet between 1 and {balance}")
            
            balance -= bet
            machine.stats['spins'] += 1
            
            input("Press Enter to pull the lever...")
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{Fore.YELLOW}Balance: ${balance}")
            print(f"Session: {'▲' if balance > initial_balance else '▼'} ${abs(balance - initial_balance)}\n")
            
            machine.display_spin_animation()
            
            result = machine.spin()
            machine.display_result(result)
            
            win_amount = machine.calculate_win(result, bet)
            balance += win_amount
            
            if win_amount > 0:
                machine.stats['wins'] += 1
                machine.stats['biggest_win'] = max(machine.stats['biggest_win'], win_amount)
                print(f"\n{Fore.GREEN}You won ${win_amount}!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}No win this time!{Style.RESET_ALL}")
                
    except KeyboardInterrupt:
        print("\nCashing out...")
    finally:
        print(f"\n{Fore.YELLOW}Game Over!")
        print(f"Final Balance: ${balance}")
        print(f"Spins: {machine.stats['spins']}")
        print(f"Wins: {machine.stats['wins']}")
        print(f"Biggest Win: ${machine.stats['biggest_win']}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
