#Flappy Pipes


#It's Flappy Bird except with an AI bird, and we control the pipes and attempt to make the AI lose.


#Prototype Code for working pipes moving right->left

# ***************************************************************************************
# Import the pygame module

import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# importing the images of birds, pipes
bird1 = pygame.transform.scale2x(pygame.image.load('imgs/bird2.png'))
bird2 = pygame.transform.scale2x(pygame.image.load('imgs/bird2.png'))
bird3 = pygame.transform.scale2x(pygame.image.load('imgs/bird3.png'))

PIPE_IMG = pygame.transform.scale2x(pygame.image.load('imgs/pipe.png'))
BIRD_IMGS = [bird1, bird2, bird3]

clock = pygame.time.Clock()
x1 = 0
x2 = 0
speed = 250.
frame_no = 0

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pipeVelX = 4

# cloud image
image = pygame.image.load('cloud.png')
pygame.Surface.set_colorkey(image, [47, 148, 168])

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        
        # Pipe border
        self.surfB = pygame.Surface((52, 502))
        self.surfB.fill((0, 0, 0))
        self.rectB = self.surfB.get_rect(
            center =(
                SCREEN_WIDTH,
                0)
            )
        
        # Pipe
        self.surf = pygame.Surface((50, 500))
        self.surf.fill((17, 168, 42))
        self.rect = self.surf.get_rect(
            center =(
                SCREEN_WIDTH,
                0)
            )
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:                
            self.rect.move_ip(0, 10)
        
        # left and right
        #if pressed_keys[K_LEFT]:
        #    self.rect.move_ip(-1, 0)
        #if pressed_keys[K_RIGHT]:
        #    self.rect.move_ip(1, 0)
            
            
        #if self.rect.left < 0:
        #    self.rect.left = 0
        #if self.rect.right > SCREEN_WIDTH:
        #    self.rect.right = SCREEN_WIDTH
        if self.rect.right <= 0:
            self.rect.left = SCREEN_WIDTH
        if self.rect.top <= -500:
            self.rect.top = -500
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
        
        if self.rectB.center != self.rect.center:
            self.rectB.center = self.rect.center


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        
        # Pipe border
        self.surftopB = pygame.Surface((52, 502))
        self.surftopB.fill((0, 0, 0))
        self.rectB = self.surftopB.get_rect(
            center =(
                SCREEN_WIDTH,
                SCREEN_HEIGHT)
            )
        
        # Pipe
        self.surftop = pygame.Surface((50, 500))
        self.surftop.fill((17, 168, 42))
        self.rect = self.surftop.get_rect(
            center =(
                SCREEN_WIDTH,
                SCREEN_HEIGHT)
            )
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:                
            self.rect.move_ip(0, 10)
        if self.rect.right <= 0:
            self.rect.left = SCREEN_WIDTH
        if self.rect.top <= 100:
            self.rect.top = 100
        if self.rect.bottom >= 600 + 500:
            self.rect.bottom = 600 + 500
            
        if self.rectB.center != self.rect.center:
            self.rectB.center = self.rect.center
            
    def collide(self, bird):  # for checking collision of the bird with the pipes
        bird_mask = bird.get_mask()
        
        # current position of pipe
        
        # compare overlap of bird position and pipe
        # overlap = bird_mask.overlap(pygame.mask.from_surface(self.surftop), offset)
        # print(overlap)
        
        # if there is overlap return true
        if overlap:
            return True
        return False
            
# CLASS BIRD
class Bird:
    ROTATION_VEL = 20
    MAX_ROTATION = 25
    ANIMATION_TIME = 5
    IMGS = BIRD_IMGS

    def __init__(self, x, y):  # constructor for class bird
        self.x = x
        self.y = y
        self.height = self.y
        self.frame_count = 0
        self.tilt = 0
        self.vel = 0
        self.img_number = 0  # image in which the bird's wings are upwards
        self.img = self.IMGS[0]  # image in which the bird's wings are upwards

    def jump(self):
        self.vel = -9  # negative velocity refers to jump upwards
        self.frame_count = 0  # reset the frames
        self.height = self.y  # reset the height

    def move(self):
        self.frame_count += 1  # update the frames when the bird moves
        # d > 0 means downwards and d<0 means upwards and same for velocity also
        # and also bird is just moving in y direction and not in x direction
        d = self.vel * self.frame_count + 1.5 * self.frame_count ** 2  # frame count also works as time
        if d >= 16: # if the bird is falling and it falls more than 16 pixels then stop falling and face straight moving
            d = 16
        # if d < 0:   # just for tuning so that upward movement is seen clear
        #     d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:  # (d<0) this is the case when when bird is going upward
            if self.tilt < self.MAX_ROTATION:  # so making a tilt angle of max rotation
                self.tilt = self.MAX_ROTATION

        else:
            if self.tilt > -90:  # if the tilt is greater than -90 then keep on reducing it till it reaches -90 to show
                self.tilt -= self.ROTATION_VEL  # the arc like falling

    def draw(self, win):
        self.img_number += 1

        # below work is done to show the flapping of the bird
        # animation time is that for how much time bird should be in one image state
        if self.img_number < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_number < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_number < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_number < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_number < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_number = 0

        if self.tilt < -80:  # when the bird is nose diving it should not flap its wings
            self.img = self.IMGS[1]
            self.img_number = self.ANIMATION_TIME * 2  # reset the image number so that next image should be IMG[2]

        rotated_image = pygame.transform.rotate(self.img, self.tilt)  # just rotating the image around its center
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect)

    def get_mask(self):  # getting the mask of the bird means the contour of bird to check its collision with any pipe
        return pygame.mask.from_surface(self.img)
    




# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Instantiate player. Right now, this is just a rectangle.
player = Player()
player2 = Player2()
bird = Bird(200, 200)


# Variable to keep the main loop running
running = True
moving = True

# clock for bird dropping
clock = pygame.time.Clock()

    
# Main loop
n=0
while running:
    clock.tick(100)
    # for loop through the event queue
    
    for event in pygame.event.get():
        
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
                moving = False
            
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
            moving = False
     


        
    

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()


    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    player2.update(pressed_keys)
    
    # Fill the screen with black
    screen.fill((126, 219, 242))
    
    # add clouds
    screen.blit(image, (50, 50))
    screen.blit(image, (375, 50))
    screen.blit(image, (150, 100))
    screen.blit(image, (475, 100))
    
    
    # add players + borders
    screen.blit(player2.surftopB, player2.rectB)
    screen.blit(player.surfB, player.rectB)
    screen.blit(player2.surftop, player2.rect)
    screen.blit(player.surf, player.rect)
    
    # add bird
    bird.draw(screen)
    
    # make bird jump
    
    if n % 10 == 0:
        bird.jump()
    else:
        bird.move()
    n=n+1
    
    #player2.collide(bird)
    

    pygame.display.flip()
    
    player2.rect.move_ip(-4, 0)
    player.rect.move_ip(-4, 0)
    clock.tick(30)

pygame.quit()

#***************************************************************************************