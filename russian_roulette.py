import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_dramatic(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def set_bullet_count():
    while True:
        try:
            print("\n" + "="*40)
            bullets = int(input("How many bullets do you want to load? (1-5): "))
            if 1 <= bullets <= 5:
                return bullets
            else:
                print("⚠ Please enter a number between 1 and 5!")
        except ValueError:
            print("⚠ Please enter a valid number!")

def russian_roulette():
    clear_screen()
    print("""
    ╔══════════════════════════════════╗
    ║     RUSSIAN ROULETTE GAME        ║
    ╚══════════════════════════════════╝
    """)
    print_dramatic("Warning: This is just a simulation game!\n")

    bullet_count = set_bullet_count()
    chambers = [False] * (6 - bullet_count) + [True] * bullet_count
    random.shuffle(chambers)

    print_dramatic("\nLoading the revolver...")
    print(f"[{bullet_count}] bullets loaded | [{'🔴' * bullet_count + '⚪' * (6-bullet_count)}]")
    
    print_dramatic("\nSpinning the cylinder...")
    print("*CLICK* *WHIRR* *CLICK*")

    round_number = 1
    while chambers:
        print(f"\n{'='*10} Round {round_number} {'='*10}")
        input("Press Enter to pull the trigger...")
        pulled_chamber = chambers.pop(0)

        if pulled_chamber:
            print("\n*BANG!*")
            print("""
               ______
            .-'      `-.
           /            \\
          |   X     X   |
          |      ^      |
          |     '-'     |
           \\    ==    /
            `-.____.-'
            
            💀 GAME OVER 💀
            """)
            break
        else:
            print("\n*click*")
            print("😌 You survived this round!")
            if chambers:
                print(f"Chambers remaining: {len(chambers)}")

        if not chambers:
            print("\n🎉 Congratulations! You've survived! 🎉")
            break
            
        round_number += 1

if __name__ == "__main__":
    while True:
        russian_roulette()
        play_again = input("\nWould you like to play again? (y/n): ").lower()
        if play_again != 'y':
            print("\nThanks for playing! Goodbye!")
            break