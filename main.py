'''
-------------------------------------------------------------------------------
Name:	main.py

Purpose: Tech ICS2O1 2021 CPT - Snake Game 

Author:	Hong.C

Created:	date in 01/14/2021
------------------------------------------------------------------------------
'''

import pygame
import time
import random

pygame.init() 

# Define some colors
BLACK      = (   0,   0,   0)
WHITE      = ( 255, 255, 255)
GREEN      = (   0, 255,   0)
DARK_GREEN = (   6, 107,   6)
RED        = ( 255,   0,   0)
GREY       = (  82,  82,  82)

# Set the width and height of the screen [width, height]
screen_width = 700
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
 
pygame.display.set_caption("Antivirus Snake")
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Defining Variables
head_x = 350
head_y = 250
head_x_velocity = 0
head_y_velocity = 0
head_width = 15
head_height = 15

intro_x = 1
intro_y = 1
intro_x_velocity = 15
intro_y_velocity = 5
intro_width = 700
intro_height = 500
intro_go = False

body = 10
snake_speed = 15

paragraph_x = 4
paragraph_y = 4
paragraph_x_velocity = 15
paragraph_y_velocity = 5
paragraph_go = False

font_style = pygame.font.SysFont(None, 40)
font = pygame.font.SysFont(None, 40)

game_over_sfx = pygame.mixer.Sound("retro_game_over.wav")
food_sfx = pygame.mixer.Sound("human_eating.wav")
boop_sfx = pygame.mixer.Sound("boop.wav")
game_winner = pygame.mixer.Sound("game_winner.wav")

boop_play = boop_sfx.play()

score_font = pygame.font.SysFont("comicsansms", 30)

game_winner_font = pygame.font.SysFont('Oswald',21, True, False)
game_winner_text = game_winner_font.render("Congratulations! You have beaten the antivirus snake! Keep Going!", True, BLACK)

#Defining Functions
def user_score(score):
    value = score_font.render("Score:  " + str(score), True, WHITE)
    screen.blit(value, [4, 0])

def our_snake(body, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], body, body])

def message(msg, colour):
    mesg = font_style.render(msg, True, colour)
    screen.blit(mesg, [80, 230])

def paragraph(msg, colour):
    paragraph_y = 4
    paragraph_velocity = 5
    paragraph_go = False
    msg_list = msg.split("\n")
    for line in msg_list:
        mesg = font.render(line, True, colour)
        screen.blit(mesg, [paragraph_x,paragraph_y])
        paragraph_y += 25

def gameLoop():
    game_over = False
    game_close = False
    global intro_go
    global paragraph_go
    global intro_x
    global intro_y
    global paragraph_x
    global paragraph_y

    head_x = screen_width / 2
    head_y = screen_height / 2
    
    head_x_velocity = 0
    head_y_velocity = 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, screen_width - body) / 10.0) * 10.0
    food_y = round(random.randrange(0, screen_height - body) / 10.0) * 10.0

# -------- Main Program Loop -----------
    while not game_over:

        # Game Over Loop
        while game_close == True:
            screen.fill(RED)
            message("Game Over! Press 1-Quit or 2-Play Again", BLACK)
            user_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        boop_sfx.play()
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_2:
                        boop_sfx.play()
                        gameLoop()

        #Detecting the input of the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("User asked to quit.")
                game_over = True 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    head_x_velocity = -body
                    head_y_velocity = 0
                elif event.key == pygame.K_RIGHT:
                    head_x_velocity = body
                    head_y_velocity = 0
                elif event.key == pygame.K_DOWN:
                    head_x_velocity = 0
                    head_y_velocity = body
                elif event.key == pygame.K_UP:
                    head_x_velocity = 0
                    head_y_velocity = -body
                elif event.key == pygame.K_SPACE:
                    intro_go = not intro_go
                    paragraph_go = not paragraph_go

            #Movement for intro screen
            if intro_go:
                intro_x += intro_x_velocity

            if paragraph_go:
                paragraph_x += paragraph_x_velocity
            
        #Game over if snake hits wall   
        if head_x >= screen_width or head_x < 0 or head_y >= screen_height or head_y < 0:
            game_over_sfx.play()    
            game_close = True
            
        head_x += head_x_velocity
        head_y += head_y_velocity

        #Background
        screen.fill(GREY)

        #Game winning text; if user score is 20 or more, you win
        if (snake_length - 1) >= 20 and game_close == False:
            screen.blit(game_winner_text, [150, 10])

        #Displaying the food
        pygame.draw.rect(screen, RED, [food_x, food_y, body, body])

        #How the snake body connects to the snake head
        snake_head = []
        snake_head.append(head_x)
        snake_head.append(head_y)
        snake_list.append(snake_head)

        #If the snake hits it's own body the game is over
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_over_sfx.play()
                game_close = True

        #User Score
        our_snake(body, snake_list)
        user_score(snake_length - 1)

        #What happens when the snake head hits one of the food blocks
        if head_x == food_x and head_y == food_y:
            food_sfx.play()
            food_x = round(random.randrange(0, screen_width - body) / 10.0) * 10.0
            food_y = round(random.randrange(0, screen_height - body) / 10.0) * 10.0

            snake_length += 1

        #Introduction
        if intro_x < 700:
            pygame.draw.rect(screen, WHITE, [intro_x, intro_y, intro_width, intro_height])
            text = "Welcome to the Antivirus Snake! A computer has\nbeen infected with malware and you have inserted\nthe Anti Virus Snake into the computer. To get rid\nof the malware, you must achieve a score of 20 or\ngreater in order for the antivirus snake to become\nsuccesful. If you reach a score past 20, keep going\nas the Anti Virus Snake will install antivirus and\nmalware protection programs. The higher the\nscore, the more protected the computer is from\nviruses. \n \nUse the arrow keys to move and hold Space Bar\nto dismiss this screen."
            paragraph(text, BLACK)
        
        # Limit FPS
        clock.tick(snake_speed)

        #Display Update
        pygame.display.update()

    # Close the window and quit.
    pygame.quit()
    quit()

gameLoop()