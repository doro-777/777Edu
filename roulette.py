import random
import time
import os
from colorama import init, Fore, Back, Style

init(autoreset=True)

NUMBERS = {
    0: ('0', 'green'),
    32: ('32', 'red'), 15: ('15', 'black'), 19: ('19', 'red'), 4: ('4', 'black'),
    21: ('21', 'red'), 2: ('2', 'black'), 25: ('25', 'red'), 17: ('17', 'black'),
    34: ('34', 'red'), 6: ('6', 'black'), 27: ('27', 'red'), 13: ('13', 'black'),
    36: ('36', 'red'), 11: ('11', 'black'), 30: ('30', 'red'), 8: ('8', 'black'),
    23: ('23', 'red'), 10: ('10', 'black'), 5: ('5', 'red'), 24: ('24', 'black'),
    16: ('16', 'red'), 33: ('33', 'black'), 1: ('1', 'red'), 20: ('20', 'black'),
    14: ('14', 'red'), 31: ('31', 'black'), 9: ('9', 'red'), 22: ('22', 'black'),
    18: ('18', 'red'), 29: ('29', 'black'), 7: ('7', 'red'), 28: ('28', 'black'),
    12: ('12', 'red'), 35: ('35', 'black'), 3: ('3', 'red'), 26: ('26', 'black')
}

BETS = {
    'straight': {'desc': 'Single number (0-36)', 'payout': 35},
    'red': {'desc': 'Red numbers', 'payout': 1},
    'black': {'desc': 'Black numbers', 'payout': 1},
    'even': {'desc': 'Even numbers', 'payout': 1},
    'odd': {'desc': 'Odd numbers', 'payout': 1},
    '1-18': {'desc': 'Numbers 1-18', 'payout': 1},
    '19-36': {'desc': 'Numbers 19-36', 'payout': 1},
    '1st12': {'desc': 'First dozen (1-12)', 'payout': 2},
    '2nd12': {'desc': 'Second dozen (13-24)', 'payout': 2},
    '3rd12': {'desc': 'Third dozen (25-36)', 'payout': 2}
}

class RouletteWheel:
    def __init__(self):
        self.numbers = NUMBERS
        self.history = []
        self.stats = {'spins': 0, 'red': 0, 'black': 0, 'green': 0}
    
    def spin(self) -> int:
        result = random.randint(0, 36)
        self.history.append(result)
        self.stats['spins'] += 1
        self.stats[self.numbers[result][1]] += 1
        return result
    
    def check_win(self, bet_type: str, bet_value: any, result: int) -> bool:
        number, color = self.numbers[result]
        
        if bet_type == 'straight':
            return result == int(bet_value)
        elif bet_type in ['red', 'black']:
            return color == bet_type
        elif bet_type == 'even':
            return result != 0 and result % 2 == 0
        elif bet_type == 'odd':
            return result != 0 and result % 2 == 1
        elif bet_type == '1-18':
            return 1 <= result <= 18
        elif bet_type == '19-36':
            return 19 <= result <= 36
        elif bet_type == '1st12':
            return 1 <= result <= 12
        elif bet_type == '2nd12':
            return 13 <= result <= 24
        elif bet_type == '3rd12':
            return 25 <= result <= 36
            
        return False

    def display_wheel(self, result: int = None):
        print("\n" + "═" * 50)
        print(Fore.YELLOW + "🎯 Roulette Wheel" + Style.RESET_ALL)
        if result is not None:
            number, color = self.numbers[result]
            color_code = Fore.GREEN if color == 'green' else Fore.RED if color == 'red' else Fore.WHITE
            print(f"\nBall landed on: {color_code}{number} {color}{Style.RESET_ALL}")
        print("═" * 50)

def display_menu():
    print("\nBetting Options:")
    for bet_type, info in BETS.items():
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
            if bet_type == 'straight':
                bet_value = input("Enter number (0-36): ")
                if not bet_value.isdigit() or not 0 <= int(bet_value) <= 36:
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
    ║           ROULETTE             ║
    ╚════════════════════════════════╝
    """ + Style.RESET_ALL)
    
    wheel = RouletteWheel()
    balance = 100
    initial_balance = balance
    
    try:
        while balance > 0:
            print(f"\n{Fore.YELLOW}Balance: ${balance}")
            print(f"Session: {'▲' if balance > initial_balance else '▼'} ${abs(balance - initial_balance)}")
            
            if wheel.history:
                print("\nLast 5 spins:", ' '.join([
                    (Fore.GREEN if wheel.numbers[n][1] == 'green' else
                     Fore.RED if wheel.numbers[n][1] == 'red' else
                     Fore.WHITE) + wheel.numbers[n][0] + Style.RESET_ALL
                    for n in wheel.history[-5:]
                ]))
            
            display_menu()
            bet_type, bet_value, bet_amount = get_bet_input(balance)
            
            if bet_type is None:
                break
                
            balance -= bet_amount
            print(f"\n{Fore.CYAN}Spinning the wheel...{Style.RESET_ALL}")
            time.sleep(1)
            
            result = wheel.spin()
            wheel.display_wheel(result)
            
            if wheel.check_win(bet_type, bet_value, result):
                winnings = bet_amount * (BETS[bet_type]['payout'] + 1)
                balance += winnings
                print(f"{Fore.GREEN}You won ${winnings - bet_amount}!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}You lost ${bet_amount}!{Style.RESET_ALL}")
                
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    finally:
        print(f"\n{Fore.YELLOW}Game Over!")
        print(f"Final Balance: ${balance}")
        print(f"Total Spins: {wheel.stats['spins']}")
        print(f"Red: {wheel.stats['red']}")
        print(f"Black: {wheel.stats['black']}")
        print(f"Green: {wheel.stats['green']}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
