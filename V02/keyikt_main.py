#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1                                #
#######################################################################
import math
import threading
import time
import pygame

width = 400
height = 200

freq = 50  # Sets the frequency of input procession
delta = 1.0 / freq # time per step
acc = 2.6  # Max acceleration of the car (per sec.)
dec = -4.5  # Max deceleration of the car (per sec.)
frict = -1  # max friction
angle_acc = 300  # max change of angle (per sec.)

speed_cur = 0
angle_cur = 0



# Start pygame stuff

# start main pygame event processing loop here
pygame.display.init()

# set up the pygame screen environment
screen = pygame.display.set_mode((width, height))

# get a clock to generate frequent behaviour
clock = pygame.time.Clock()


# States of the keys
keystates = {'quit': False, 'acc': False, 'dec': False}

# Exercises -----------------------------------------------


# 1. Update speed
def update_speed():
    final_acc = 0.0
    max_speed = 11.0  # in m/s
    global speed_cur
    if keystates['acc'] and not speed_cur >= max_speed:
        final_acc = acc * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
    if keystates['dec'] and speed_cur > 0:
        final_acc = acc * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
    if not keystates['acc'] and not keystates['dec'] and speed_cur > 0:
        final_acc = frict/2.0 * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (4.0 ** 2.0))))
    new_speed = speed_cur + final_acc * delta
    speed_cur = max(0, min(11, new_speed))

# OLD CODE (with threading) - Start ----------------------
# # 1. acceleration
# def increase_speed():
#     max_speed = 11 # in m/s
#     global speed_cur
#     while keystates['acc'] and not speed_cur >= max_speed:
#         speed_after_acc = speed_cur + acc * delta
#         speed_cur = speed_after_acc if max_speed > speed_after_acc else max_speed
#         time.sleep(delta)
#
#
# # 1. deceleration
# def decrease_speed():
#     global speed_cur
#     while keystates['dec'] and not speed_cur <= 0:
#         speed_after_dec = speed_cur + dec * delta
#         speed_cur = speed_after_dec if 0 < speed_after_dec else 0
#         time.sleep(delta)
#
#
# # 1. friction
# def speed_after_friction():
#     global speed_cur
#     while not keystates['acc'] and not keystates['dec'] and not speed_cur <= 0:
#         speed_after_acc = speed_cur - frict * delta
#         speed_cur = speed_after_acc if 0 < speed_after_acc else 0
#         time.sleep(delta)
# OLD CODE - End -----------------------------------------
# --------------------------------------------------------


running = True
try:
    while running:
        # set clock frequency
        clock.tick(freq)
        
        # save the last speed 4 analysis
        last = speed_cur
     
        # process input events
        for event in pygame.event.get():
        
            # exit on quit
            if event.type == pygame.QUIT:
                running = False

            # check for key down events (press)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    keystates['quit'] = True
                # Start acceleration
                if event.key == pygame.K_w:
                    keystates['acc'] = True
                    pygame.event.set_blocked(pygame.KEYDOWN)
                # Start deceleration
                if event.key == pygame.K_s:
                    keystates['dec'] = True
                    pygame.event.set_blocked(pygame.KEYDOWN)
                # Reset speed
                if event.key == pygame.K_r:
                    speed_cur = 0
                print("Keydown")

            # check for key up events (release)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    keystates['quit'] = False
                # Stop acceleration
                if event.key == pygame.K_w:
                    keystates['acc'] = False
                    pygame.event.set_allowed(pygame.KEYDOWN)
                # Stop deceleration
                if event.key == pygame.K_s:
                    keystates['dec'] = False
                    pygame.event.set_allowed(pygame.KEYDOWN)

        # do something about the key states here, now that the event queue has been processed
        if keystates['quit']:
            running = False
        # update speed depending on keystates
        update_speed()
        print("({},{} --> {})".format(speed_cur, angle_cur, (speed_cur - last) / delta))
    
except KeyboardInterrupt:
    print("Exiting through keyboard event (CTRL + C)")


# gracefully exit pygame here
pygame.quit()
