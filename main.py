# Import necessary libraries
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((350, 600))
clock = pygame.time.Clock()

# Define a flag to control the game loop
running = True

# Define a class for the Apple object


class Apple:
    def __init__(self, image, position, speed):
        """
        Initialize an Apple object.

        :param image: The image of the apple.
        :param position: The initial position of the apple.
        :param speed: The falling speed of the apple.
        """
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.speed = speed

    def move(self):
        """Move the apple down."""
        self.rect.y += self.speed


# Define game variables and constants
speed = 3
score = 0
TILESIZE = 32

# Load and scale the floor image
floor_image = pygame.image.load("assets\\floor.png").convert_alpha()
floor_image = pygame.transform.scale(floor_image, (TILESIZE*15, TILESIZE*5))
floor_rect = floor_image.get_rect(bottomleft=(0, screen.get_height()))

# Load and scale the player image
player_image = pygame.image.load('assets\player_static.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (TILESIZE, TILESIZE*2))
player_rect = player_image.get_rect(center=(screen.get_width()/2,
                                            screen.get_height() - floor_image.get_height() - (player_image.get_height()/2)))

# Load and scale the apple image
apple_image = pygame.image.load('assets\\apple.png').convert_alpha()
apple_image = pygame.transform.scale(apple_image, (TILESIZE, TILESIZE))

# Create a list to store Apple objects
apples = [
    Apple(apple_image, (100, 0), 3),
    Apple(apple_image, (300, 0), 3)
]

# Load font for displaying the score
font = pygame.font.Font('assets\PixeloidMono.ttf', TILESIZE//2)

# Load sound effects
pickup = pygame.mixer.Sound('assets\powerup.mp3')
pickup.set_volume(0.1)

# Define functions for drawing and updating the game


def draw():
    """
    Draw the game elements on the screen.
    """
    screen.fill('lightblue')
    screen.blit(floor_image, (floor_rect))
    screen.blit(player_image, (player_rect))

    for apple in apples:
        screen.blit(apple_image, apple.rect)

    score_text = font.render(f'Score: {score}', True, "white")
    score_rect = score_text.get_rect(
        center=(screen.get_width()/2, screen.get_height() - TILESIZE))
    screen.blit(score_text, score_rect)


def update():
    """
    Update the game logic and state.
    """
    global speed
    global score

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if player_rect.x <= 7:
            player_rect.x = 0
        else:
            player_rect.x -= 8

    if keys[pygame.K_RIGHT]:
        if player_rect.x < 318:
            player_rect.x += 8
        else:
            player_rect.x = 318

    # Create a falling effect for apples
    for apple in apples:
        apple.move()
        # If apple reaches the floor, respawn it at the top
        if apple.rect.colliderect(floor_rect):
            apples.remove(apple)
            apples.append(
                Apple(apple_image, (random.randint(50, 300), -50), speed))
        # If the player collects an apple, increase the score and play a sound
        elif apple.rect.colliderect(player_rect):
            apples.remove(apple)
            apples.append(
                Apple(apple_image, (random.randint(50, 300), -50), speed))
            score += 1
            pickup.play()
            speed += 0.1


# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    update()
    draw()

    clock.tick(60)
    pygame.display.update()
