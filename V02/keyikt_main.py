#!/usr/bin/env python

#######################################################################
#                            Aufgabe 1                                #
#######################################################################
import math
import pygame
from servo_ctrl import Steering, Motor

width = 400
height = 200

freq = 50  # Sets the frequency of input procession
delta = 1.0 / freq # time per step
acc = 2.6  # Max acceleration of the car (per sec.)
dec = -4.5  # Max deceleration of the car (per sec.)
frict = -1.0  # max friction
angle_acc = 300.0  # max change of angle (per sec.)

speed_cur = 0
angle_cur = 0

# Initialize motors for vehicle control
driving = Motor(1)
steering = Steering(2)
MOUSE_LEFT = 1
# Start pygame stuff

# start main pygame event processing loop here
pygame.display.init()

# set up the pygame screen environment
screen = pygame.display.set_mode((width, height))

# get a clock to generate frequent behaviour
clock = pygame.time.Clock()


# States of the keys
keystates = {'quit': False, 'simulated_mode': True, 'mouse_control_on': False, 'mouse_left': False, 'acc': False, 'dec': False, 'left': False, 'right': False}

# Exercises -----------------------------------------------


# 1. Update speed depending on pressed key 'w'/'s'
def keyboard_update_speed():
    final_acc = 0.0
    max_speed = 11.0  # in m/s
    global speed_cur
    if keystates['simulated_mode']:
        if 0 < speed_cur:
            if keystates['acc']:
                final_acc = acc * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
            if keystates['dec']:
                final_acc = dec * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
            if not keystates['acc'] and not keystates['dec'] and speed_cur > 0:
                final_acc = frict/2.0 * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (4.0 ** 2.0))))
            new_speed = speed_cur + final_acc * delta
            speed_cur = max(0, min(11, new_speed))
        elif 0 > speed_cur:
            if keystates['acc']:
                final_acc = dec * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
            if keystates['dec']:
                final_acc = acc * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
            if not keystates['acc'] and not keystates['dec'] and speed_cur < 0:
                final_acc = frict / 2.0 * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (4.0 ** 2.0))))
            new_speed = speed_cur - final_acc * delta
            speed_cur = max(-11, min(0, new_speed))
        else:
            final_acc = acc * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
            if keystates['acc']:
                speed_cur = speed_cur + final_acc * delta
            if keystates['dec']:
                speed_cur = speed_cur - final_acc * delta
    else:
        if keystates['acc'] and not speed_cur >= max_speed:
            speed_cur = 11
        elif keystates['dec']:
            speed_cur = -11
        if not keystates['acc'] and not keystates['dec']:
            speed_cur = 0


# 2. Update angle depending on pressed key 'a'/'d'
def keyboard_update_angle():
    global angle_cur
    max_angle = 45
    if keystates['simulated_mode']:
        if keystates['left'] and angle_cur > -max_angle:
            new_angle = angle_cur - angle_acc * delta
            angle_cur = max(-max_angle, new_angle)
        if keystates['right'] and angle_cur < max_angle:
            new_angle = angle_cur + angle_acc * delta
            angle_cur = min(max_angle, new_angle)
        if not keystates['left'] and not keystates['right']:
            if angle_cur < 0:
                new_angle = angle_cur + angle_acc * delta
                angle_cur = min(0, new_angle)
            elif angle_cur > 0:
                new_angle = angle_cur - angle_acc * delta
                angle_cur = max(0, new_angle)
    else:
        if keystates['left']:
            angle_cur = -45
        elif keystates['right']:
            angle_cur = 45
        else:
            angle_cur = 0


# 3. Calculate angle depending on mouse position
def mouse_update_angle(x):
    global angle_cur
    max_angle = 45
    angle_at_mouse_pos = (x / (width-1.0)) * max_angle * 2 - max_angle
    if keystates['simulated_mode']:
        if keystates['mouse_left']:
            if angle_at_mouse_pos >= 0:
                new_angle = angle_cur + angle_acc * delta
                angle_cur = min(angle_at_mouse_pos, new_angle)
            else:
                new_angle = angle_cur - angle_acc * delta
                angle_cur = max(angle_at_mouse_pos, new_angle)
        else:
            angle_cur = 0
    else:
        if keystates['mouse_left']:
            angle = max_angle if abs(angle_at_mouse_pos) > 10 else 0
            angle_cur = angle if angle_at_mouse_pos > 0 else -angle
        else:
            angle_cur = 0


# 3. Calculate speed depending on mouse position
def mouse_update_speed(y):
    global speed_cur
    max_speed = 11
    max_speed_on_mouse_pos = -((y / (height-1.0)) * max_speed * 2 - max_speed)
    if keystates['simulated_mode']:
        if keystates['mouse_left']:
            if speed_cur <= max_speed_on_mouse_pos:
                if speed_cur >= 0:
                    final_acc = acc * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
                    speed_cur = min(speed_cur + final_acc * delta, max_speed_on_mouse_pos)
                elif speed_cur < 0:
                    final_acc = dec * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
                    speed_cur = min(speed_cur - final_acc * delta, max_speed_on_mouse_pos)
            else:
                if speed_cur > 0:
                    final_acc = dec * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
                    speed_cur = max(speed_cur + final_acc * delta, 0)
                elif speed_cur <= 0:
                    final_acc = acc * (1.0 - (1.0 / 2.0) * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (2.5 ** 2.0)))))
                    speed_cur = max(speed_cur - final_acc * delta, max_speed_on_mouse_pos)

        else:
            friction = frict/2.0 * (1.0 + math.erf((abs(speed_cur) - max_speed / 2.0) / math.sqrt(2.0 * (4.0 ** 2.0))))
            speed_cur = max(speed_cur + friction * delta, 0)
    else:
        if keystates['mouse_left']:
            speed_cur = max_speed if max_speed_on_mouse_pos > 0 else -max_speed
        else:
            speed_cur = 0

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT:
                    keystates['mouse_left'] = True
            # check for key down events (press)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    keystates['quit'] = True
                # Reset speed
                if event.key == pygame.K_r:
                    speed_cur = 0
                    angle_cur = 0
                    keystates['mouse_control_on'] = False
                    print("Reset...")
                    continue
                # toggle between actual control and simulated mode
                if event.key == pygame.K_t:
                    keystates['simulated_mode'] = not keystates['simulated_mode']
                # Start mouse control
                if event.key == pygame.K_m:
                    keystates['mouse_control_on'] = True
                    print ("Starting mouse control...")
                # Start acceleration
                if event.key == pygame.K_w:
                    keystates['acc'] = True
                    # pygame.event.set_blocked(pygame.KEYDOWN)
                    pygame.event.set_allowed(pygame.KEYDOWN)
                # Start deceleration
                if event.key == pygame.K_s:
                    keystates['dec'] = True
                    # pygame.event.set_blocked(pygame.KEYDOWN)
                # Start left turn
                if event.key == pygame.K_a:
                    keystates['left'] = True
                # Start right turn
                if event.key == pygame.K_d:
                    keystates['right'] = True
                print("Keydown")

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_LEFT:
                    keystates['mouse_left'] = False
            # check for key up events (release)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    keystates['quit'] = False
                # Stop acceleration
                if event.key == pygame.K_w:
                    keystates['acc'] = False
                # Stop deceleration
                if event.key == pygame.K_s:
                    keystates['dec'] = False
                # Stop left turn
                if event.key == pygame.K_a:
                    keystates['left'] = False
                # Stop right turn
                if event.key == pygame.K_d:
                    keystates['right'] = False

        # Quit the input processing
        if keystates['quit']:
            running = False
        if keystates['mouse_control_on']:
            # update depending on keystates
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_update_angle(mouse_x)
            mouse_update_speed(mouse_y)
        else:
            # update depending on keystates
            keyboard_update_speed()
            keyboard_update_angle()

        driving.set_speed(speed_cur)
        steering.set_angle(angle_cur)

        print("({},{} --> {})".format(speed_cur, angle_cur, (speed_cur - last) / delta))
    
except KeyboardInterrupt:
    print("Exiting through keyboard event (CTRL + C)")


# gracefully exit pygame here
pygame.quit()
