import random
import time
import os
from colorama import init, Fore, Back, Style

init(autoreset=True)

class GlassBridge:
    def __init__(self, bridge_length=18):
        self.bridge_length = bridge_length
        self.safe_path = [random.choice([0, 1]) for _ in range(bridge_length)]  # 0 for left, 1 for right
        self.current_position = -1
        self.revealed_panels = [[-1, -1] for _ in range(bridge_length)]  # -1: unknown, 0: broken, 1: safe

    def display_bridge(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.YELLOW + "\n🌉 GLASS BRIDGE GAME 🌉\n" + Style.RESET_ALL)

        # Bridge visualization
        for i in range(self.bridge_length):
            left_panel = self.get_panel_display(i, 0)
            right_panel = self.get_panel_display(i, 1)
            
            if i == self.current_position:
                print(f"{i+1:2d}. {left_panel} 🧍 {right_panel}")
            else:
                print(f"{i+1:2d}. {left_panel}   {right_panel}")

        print("\nStart 🏃" + "═" * (self.bridge_length * 3) + "🏁 Finish")
        
    def get_panel_display(self, position, side):
        if position < self.current_position:
            # Show broken or safe for passed panels
            if self.revealed_panels[position][side] == 0:
                return Fore.RED + "💔" + Style.RESET_ALL    # Broken glass
            else:
                return Fore.GREEN + "💎" + Style.RESET_ALL  # Safe glass
        elif position == self.current_position:
            return Fore.CYAN + "⬜" + Style.RESET_ALL      # Current position
        else:
            return Fore.WHITE + "⬜" + Style.RESET_ALL     # Unknown panels

    def make_choice(self) -> bool:
        """Returns True if the choice was successful, False if player fell"""
        while True:
            choice = input("\nChoose left (L) or right (R) panel: ").upper()
            if choice in ['L', 'R']:
                chosen_side = 0 if choice == 'L' else 1
                is_safe = (self.safe_path[self.current_position + 1] == chosen_side)
                
                # Update revealed panels
                self.revealed_panels[self.current_position + 1] = [
                    1 if side == self.safe_path[self.current_position + 1] else 0
                    for side in [0, 1]
                ]
                
                if is_safe:
                    self.current_position += 1
                    return True
                return False
            print("Invalid choice! Please enter L or R.")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.YELLOW + """
╔══════════════════════════════════════╗
║          GLASS BRIDGE GAME           ║
╚══════════════════════════════════════╝
        
Rules:
- Cross the bridge by choosing between left and right glass panels
- One panel is tempered glass (safe), the other will break
- Fall three times and you're eliminated!
        """ + Style.RESET_ALL)
        
        input("Press Enter to start...")
        
        lives = 3
        best_progress = 0
        game = GlassBridge()

        while lives > 0:
            game.display_bridge()
            print(f"\n❤️ Lives remaining: {lives}")

            if not game.make_choice():
                lives -= 1
                if lives > 0:
                    print(Fore.RED + "\n💥 The glass broke! You fell!" + Style.RESET_ALL)
                    best_progress = max(best_progress, game.current_position + 1)
                    game = GlassBridge()
                    time.sleep(2)
                continue
            
            # Check for victory
            if game.current_position == game.bridge_length - 1:
                game.display_bridge()
                print(Fore.GREEN + "\n🎉 Congratulations! You made it across safely!" + Style.RESET_ALL)
                break
                
            # Calculate progress percentage
            progress = ((game.current_position + 1) / game.bridge_length) * 100
            print(f"\nProgress: {progress:.1f}%")
        
        if lives == 0:
            print(Fore.RED + "\n☠️ Game Over! You've run out of lives!" + Style.RESET_ALL)
            print(f"Best progress: {(best_progress / game.bridge_length) * 100:.1f}%")
        
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    main()
