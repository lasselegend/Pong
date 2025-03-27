import pygame
import random

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)

pygame.init()

# Start display window
size = (800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

#Fonts
font_large = pygame.font.SysFont('Calibri', 50, True, False)
font_small = pygame.font.SysFont('Calibri', 30, True, False)

# Function for title screen
def show_title_screen():   
    screen.fill(BLACK)
    
    title_text = font_large.render("Welcome to Pong", True, WHITE)
    prompt_text = font_small.render("Press any key to start", True, WHITE)

    title_rect = title_text.get_rect(center=(size[0] // 2, size[1] // 2 - 50))
    screen.blit(title_text, title_rect)

    prompt_rect = prompt_text.get_rect(center=(size[0] // 2, size[1] // 2 + 10))
    screen.blit(prompt_text, prompt_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Show title screen before the game starts
show_title_screen()

# Starting position of player
rect_x = 400
rect_y = 580
rect_change_x = 0

# Starting position of ball
# Speed of ball
# Score
ball_x, ball_y = random.randint(50, 750), 50
ball_change_x, ball_change_y = 5, 5
score = 0

# High score list (Top 3)
high_scores = [0, 0, 0]

# Draws player and restricts player from moving between edges of window
def drawrect(screen, x, y):
    if x <= 0:
        x = 0
    if x >= 700:
        x=700
    pygame.draw.rect(screen, GREEN, [x, y, 100, 20], border_radius=7)

# Main Game loop
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rect_change_x = -6
            elif event.key == pygame.K_RIGHT:
                rect_change_x = 6
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                rect_change_x = 0

    screen.fill(BLACK)

    rect_x += rect_change_x
    ball_x += ball_change_x
    ball_y += ball_change_y

    # Ball collision logic
    if ball_x < 0 or ball_x > 785:
        ball_change_x *= -1
    if ball_y < 0:
        ball_change_y *= -1
    elif ball_x > rect_x and ball_x < rect_x + 100 and 565 <= ball_y <= 580:
        ball_change_y *= -1
        score += 1

        if score % 5 == 0:
            ball_change_x += 1 if ball_change_x > 0 else -1
            ball_change_y += 1 if ball_change_y > 0 else -1

    # Player loses
    elif ball_y > 600:
        screen.fill(BLACK)
        font = pygame.font.SysFont('Calibri', 50, True, False)
        text = font.render("You Lose, Try again", True, WHITE)
        
        text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2 - 25))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)

        # Update highscore
        high_scores.append(score)
        high_scores = sorted(high_scores, reverse=True)[:3]

        # Resets Game
        ball_x = random.randint(50, 750)
        ball_y = 50
        ball_change_x = 5
        ball_change_y = 5
        score = 0

    # Draw new ball & paddle
    pygame.draw.circle(screen, WHITE, (ball_x + 7, ball_y + 7,), 7)
    drawrect(screen, rect_x, rect_y)

    # Display Current Score
    font = pygame.font.SysFont('Calibri', 20, False, False)
    text = font.render("Score = " + str(score), True, WHITE)
    screen.blit(text, [600, 100])

    # Display Top 3 scores
    font = pygame.font.SysFont('Calibri', 15, False, False)
    highscore_text = font.render("Top Scores:", True, WHITE)
    screen.blit(highscore_text, [600, 130])

    for i, hs in enumerate(high_scores):
        hs_text = font.render(f"{i+1}. {hs}", True, WHITE)
        screen.blit(hs_text, [600, 160 + i * 30])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()