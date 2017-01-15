'''
Control an AR Parrot Drone with a Playstation 4 Controller

MIT License

Copyright (c) 2016 Jacob Laney

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import pygame
import pydrone

##### connect to drone ####
# TODO add functionality to check for connection
drone = pydrone.DroneController()

#### init the display ####
pygame.init()
WIDTH = 600
HEIGHT = 400
size = [WIDTH, HEIGHT] # size of window in pixels [width,height]
DISPLAY = pygame.display.set_mode(size)

#### some colors that can be used for the display ####
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#### init ps4 controller ####
pygame.joystick.init()
try:
    controller = pygame.joystick.Joystick(0)
    controller.init()
except:
    print "#### Please connect a ps4 controller! ####"
    exit()
print "#### CONNECTED TO PS4 CONTROLLER ####"

##### reduces ps4 controller joystick sensitivity ####
def smooth_axis_input(value):
    if abs(value) < 0.1:
        return 0.0
    return value

#### process pygame event queue ####
def handle_events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            print "QUIT"
            return True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_SPACE:
                drone.kill()
                print "#### Trying to kill drone! ####"
        if e.type == pygame.JOYBUTTONUP:
            if e.button == 1: # X button
                if drone.isFlying == False:
                    print "#### TAKING OFF ####"
                    drone.liftoff()
                else:
                    print "#### LANDING ####"
                    drone.land()
            elif e.button == 13: # touchpad
                drone.kill();
    (x,y) = controller.get_hat(0)
    if x == -1:
        if drone.latSpeed - 1 > 0:
            drone.latSpeed -= 1
    if x == 1:
        if drone.latSpeed + 1 < 11:
            drone.latSpeed += 1
    if y == 1:
        if drone.vertSpeed + 1 < 11:
            drone.vertSpeed += 1
    if y == -1:
        if drone.vertSpeed - 1 > 0:
            drone.vertSpeed -= 1
    return False

#### process moving the drone ####
def handle_movement():
    #### MOVE ####
    value = smooth_axis_input(controller.get_axis(0))
    drone.set_left_right(value)
    value = smooth_axis_input(controller.get_axis(1))
    drone.set_front_back(value)
    #### UP and DOWN ####
    value = smooth_axis_input(controller.get_axis(3))
    drone.set_vertical_speed(value * -1 * 5)
    #### ROTATE
    value = smooth_axis_input(controller.get_axis(2))
    drone.set_angular_speed(value)
    #### Tell the drone to move ####
    if drone.isFlying:
        drone.move()
    #### slow down ####

#### draw the pygame window ####
def draw():
    DISPLAY.fill(WHITE)

    if drone.isFlying:
        pygame.draw.rect(DISPLAY, GREEN, (0, 0, WIDTH, HEIGHT/10))
    else:
        pygame.draw.rect(DISPLAY, RED, (0, 0, WIDTH, HEIGHT/10))

    # output speed information
    font = pygame.font.SysFont("impact", 25)
    latLabel = font.render("Lateral Speed:  {}".format(drone.latSpeed), 1, BLUE)
    vertLabel = font.render("Vertical Speed:  {}".format(drone.vertSpeed), 1, BLUE)
    rotLabel = font.render("Rotational Speed:  {}".format(drone.rotSpeed), 1, BLUE)
    DISPLAY.blit(latLabel, (10, HEIGHT/10 + 30 * 1))
    DISPLAY.blit(vertLabel, (10, HEIGHT/10 + 30 * 2))
    DISPLAY.blit(rotLabel, (10, HEIGHT/10 + 30 * 3))

    # draw joysticks
    pygame.draw.rect(DISPLAY, BLACK, (0, HEIGHT / 2, WIDTH, HEIGHT / 2))
    pygame.draw.circle(DISPLAY, BLUE, (WIDTH/4, 3*HEIGHT/4), 60, 5)
    pygame.draw.circle(DISPLAY, BLUE, (int(WIDTH/4 + controller.get_axis(0) * 20), int(3*HEIGHT/4 + controller.get_axis(1) * 20)), 40)
    pygame.draw.circle(DISPLAY, BLUE, (3*WIDTH/4, 3*HEIGHT/4), 60, 5)
    pygame.draw.circle(DISPLAY, BLUE, (int(3*WIDTH/4 + controller.get_axis(2) * 20), int(3*HEIGHT/4 + controller.get_axis(3) * 20)), 40)

    pygame.display.update()

####################################################
####                MAIN LOOP
####################################################
while True:
    if handle_events() == True:
        break
    handle_movement()  # tell the drone to move
    draw()  # draw the GUI
    pygame.time.Clock().tick(40) # make sure loop does not exceed 40 fps
