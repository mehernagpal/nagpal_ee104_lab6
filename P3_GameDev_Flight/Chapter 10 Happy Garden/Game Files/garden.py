# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 17:06:18 2023

@author: mehernagpal
"""

# Import necessary libraries
from random import randint
import time
import pgzrun
import pygame
import pgzero
from pgzero.builtins import Actor

# Define screen dimensions and center positions
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Initialize game state variables
game_over = False
finalized = False
garden_happy = True
fangflower_collision = False
time_elapsed = 0
start_time = time.time()

# Randomize rain outcome
raining = randint(0, 1)

# Create and position the cow actor
cow = Actor("cow")
cow.pos = 100, 500

# Initialize lists for flowers, wilted flowers, fangflowers, and their velocities
flower_list = []
wilted_list = []
fangflower_list = []
fangflower_vy_list = []
fangflower_vx_list = []

# Draw function for rendering the game screen
def draw():
    global game_over, time_elapsed, finalized
    if not game_over:
        screen.clear()

        # Draw the garden background with or without rain
        if not raining:
            screen.blit("garden", (0, 0))
        else:
            screen.blit("garden-raining", (0, 0))
        
        # Draw cow, flowers, and fangflowers
        cow.draw()
        for flower in flower_list:
            flower.draw()
        for fangflower in fangflower_list:
            fangflower.draw()

        # Display time elapsed
        time_elapsed = int(time.time() - start_time)
        screen.draw.text(
            "Garden happy for: " +
            str(time_elapsed) + " seconds",
            topleft=(10, 10), color="black"
        )
    else:
        # Game over screen
        if not finalized:
            cow.draw()
            screen.draw.text(
                "Garden happy for: " +
                str(time_elapsed) + " seconds",
                topleft=(10, 10), color="black"
            )
            if (not garden_happy):
                screen.draw.text(
                    "GARDEN UNHAPPY—GAME OVER!", color="black",
                    topleft=(10, 50)
                )
                finalized = True
            else:
                screen.draw.text(
                    "FANGFLOWER ATTACK—GAME OVER!", color="black",
                    topleft=(10, 50)
                )
                finalized = True
    return

# Function to create a new flower and add it to the lists
def new_flower():
    global flower_list, wilted_list
    flower_new = Actor("flower")
    flower_new.pos = randint(50, WIDTH - 50), randint(150, HEIGHT - 100)
    flower_list.append(flower_new)
    wilted_list.append("happy")
    return

# Function to add flowers to the game
def add_flowers():
    global game_over
    if not game_over:
        new_flower()
        clock.schedule(add_flowers, 2)
    return

# Check wilted flowers duration
def check_wilt_times():
    global wilted_list, game_over, garden_happy
    if wilted_list:
        for wilted_since in wilted_list:
            if (not wilted_since == "happy"):
                time_wilted = int(time.time() - wilted_since)
                if (time_wilted) > 10.0:
                    garden_happy = False
                    game_over = True
                    break
    return

# Function to wilt a random flower
def wilt_flower():
    global flower_list, wilted_list, game_over
    if not game_over:
        if flower_list:
            rand_flower = randint(0, len(flower_list) - 1)
            if (flower_list[rand_flower].image == "flower"):
                flower_list[rand_flower].image = "flower-wilt"
                wilted_list[rand_flower] = time.time()
            clock.schedule(wilt_flower, 3)
    return

# Function to check if the cow is colliding with a wilted flower and restore it
def check_flower_collision():
    global cow, flower_list, wilted_list
    index = 0
    for flower in flower_list:
        if (flower.colliderect(cow) and flower.image == "flower-wilt"):
            flower.image = "flower"
            wilted_list[index] = "happy"
            break
        index = index + 1
    return

# Function to check if the cow is colliding with a fangflower and end the game
def check_fangflower_collision():
    global cow, fangflower_list, fangflower_collision, game_over
    for fangflower in fangflower_list:
        if fangflower.colliderect(cow):
            cow.image = "zap"
            game_over = True
            break
    return

# Function to generate a random velocity for fangflowers
def velocity():
    random_dir = randint(0, 1)
    random_velocity = randint(2, 3)
    if random_dir == 0:
        return -random_velocity
    else:
        return random_velocity

# Function to mutate a random flower into a fangflower
def mutate():
    global flower_list, fangflower_list, fangflower_vy_list
    global fangflower_vx_list, game_over
    if not game_over and flower_list:
        rand_flower = randint(0, len(flower_list) - 1)
        fangflower_pos_x = flower_list[rand_flower].x
        fangflower_pos_y = flower_list[rand_flower].y
        del flower_list[rand_flower]
        fangflower = Actor("fangflower")
        fangflower.pos = fangflower_pos_x, fangflower_pos_y
        fangflower_vx = velocity()
        fangflower_vy = velocity()
        fangflower = fangflower_list.append(fangflower)
        fangflower_vx_list.append(fangflower_vx)
        fangflower_vy_list.append(fangflower_vy)
        clock.schedule(mutate, 10)
    return

# Function to update fangflower positions based on their velocities
def update_fangflowers():
    global fangflower_list, game_over
    if not game_over:
        index = 0
        for fangflower in fangflower_list:
            fangflower_vx = fangflower_vx_list[index]
            fangflower_vy = fangflower_vy_list[index]
            fangflower.x = fangflower.x + fangflower_vx
            fangflower.y = fangflower.y + fangflower_vy
            if fangflower.left < 0:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.right > WIDTH:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.top < 150:
                fangflower_vy_list[index] = -fangflower_vy
            if fangflower.bottom > HEIGHT:
                fangflower_vy_list[index] = -fangflower_vy
            index = index + 1
    return
    #pass

# Function to reset the cow's image after watering
def reset_cow():
    global game_over
    if not game_over:
        cow.image = "cow"
    return
   # pass

add_flowers()
wilt_flower()

# Function to update game logic
def update():
    global score, game_over, fangflower_collision
    global flower_list, fangflower_list, time_elapsed
    fangflower_collision = check_fangflower_collision()
    check_wilt_times()
    if not game_over:
        if keyboard.space:
            cow.image = "cow-water"
            clock.schedule(reset_cow, 0.5)
            check_flower_collision()
        if keyboard.left and cow.x > 0:
            cow.x -= 5
        elif keyboard.right and cow.x < WIDTH:
            cow.x += 5
        elif keyboard.up and cow.y > 150:
            cow.y -= 5
        elif keyboard.down and cow.y < HEIGHT:
            cow.y += 5
        
        # Spawn fangflowers after 15 seconds and update their positions
        if time_elapsed > 15 and not fangflower_list:
            mutate()
        update_fangflowers()
    #pass


pgzrun.go()