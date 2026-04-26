import pygame
from ui import text_input_screen, main_menu, leaderboard_screen, settings_screen, game_over_screen
from racer import play_game, WIDTH, HEIGHT
from persistence import save_score

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer TSIS3")

def main():
    username = text_input_screen(screen, "Enter your name:")
    while True:
        choice = main_menu(screen)
        if choice == "Play":
            while True:
                score, distance = play_game(screen, username)
                save_score(username, score, distance)
                action = game_over_screen(screen, score, distance, score)
                if action == "menu":
                    break
                # "retry" loops back
        elif choice == "Leaderboard":
            leaderboard_screen(screen)
        elif choice == "Settings":
            settings_screen(screen)
        elif choice == "Quit":
            break
    pygame.quit()

if __name__ == "__main__":
    main()
