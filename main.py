import pygame
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 960, 640
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPS Smasher")

# Fonts
font_large = pygame.font.Font('Splatch.ttf', 80)
font_small = pygame.font.SysFont('arial', 40)

# Sounds
click_sound = pygame.mixer.Sound('cutting-paper-with-scissors-69879.mp3')
win_sound = pygame.mixer.Sound('scissors-43842.mp3')
lose_sound = pygame.mixer.Sound('scissors-274671.mp3')
draw_sound = pygame.mixer.Sound('scissors-89742.mp3')

# Load images
bg = pygame.image.load("background.jpg")
r_btn = pygame.image.load("r_button.png").convert_alpha()
p_btn = pygame.image.load("p_button.png").convert_alpha()
s_btn = pygame.image.load("s_button.png").convert_alpha()
rock_img = pygame.image.load("rock.png").convert_alpha()
paper_img = pygame.image.load("paper.png").convert_alpha()
scissors_img = pygame.image.load("scissors.png").convert_alpha()
replay_btn_img = pygame.image.load("replay.png").convert_alpha()

# Game Button Class
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# RPS Game Class
class RpsGame:
    def __init__(self):
        self.running = True
        self.player_choice = None
        self.computer_choice = None
        self.result = ""
        self.player_score = 0
        self.computer_score = 0

        # Buttons
        self.rock_btn = Button(30, 500, r_btn)
        self.paper_btn = Button(330, 500, p_btn)
        self.scissors_btn = Button(640, 500, s_btn)
        self.replay_btn = Button(820, 20, replay_btn_img)

    def draw_choices(self):
        if self.player_choice:
            screen.blit(self.get_image(self.player_choice), (120, 200))
        if self.computer_choice:
            screen.blit(self.get_image(self.computer_choice), (600, 200))

    def get_image(self, choice):
        return {
            "rock": rock_img,
            "paper": paper_img,
            "scissors": scissors_img
        }[choice]

    def get_computer_choice(self):
        return random.choice(["rock", "paper", "scissors"])

    def check_winner(self):
        p = self.player_choice
        c = self.computer_choice
        if p == c:
            draw_sound.play()
            self.result = "It's a Draw!"
        elif (p == "rock" and c == "scissors") or \
             (p == "scissors" and c == "paper") or \
             (p == "paper" and c == "rock"):
            self.player_score += 1
            win_sound.play()
            self.result = "You Win!"
        else:
            self.computer_score += 1
            lose_sound.play()
            self.result = "You Lose!"

    def reset_round(self):
        self.player_choice = None
        self.computer_choice = None
        self.result = ""

    def draw_ui(self):
        screen.blit(bg, (0, 0))
        self.rock_btn.draw(screen)
        self.paper_btn.draw(screen)
        self.scissors_btn.draw(screen)
        self.replay_btn.draw(screen)

        # Score
        score_text = font_large.render(f"{self.player_score} : {self.computer_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 60))
        screen.blit(score_text, score_rect)

        # Result
        if self.result:
            result_text = font_small.render(self.result, True, WHITE)
            result_rect = result_text.get_rect(center=(WIDTH // 2, 140))
            screen.blit(result_text, result_rect)

    def game_loop(self):
        clock = pygame.time.Clock()

        while self.running:
            screen.fill(BLACK)
            self.draw_ui()
            self.draw_choices()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    click_sound.play()

                    if self.rock_btn.is_clicked(pos):
                        self.play_round("rock")
                    elif self.paper_btn.is_clicked(pos):
                        self.play_round("paper")
                    elif self.scissors_btn.is_clicked(pos):
                        self.play_round("scissors")
                    elif self.replay_btn.is_clicked(pos):
                        self.player_score = 0
                        self.computer_score = 0
                        self.reset_round()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

    def play_round(self, choice):
        self.player_choice = choice
        self.computer_choice = self.get_computer_choice()
        self.check_winner()

# Run the game
if __name__ == "__main__":
    game = RpsGame()
    game.game_loop()
