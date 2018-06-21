#!/usr/bin/env python

################################################################################
# quizBarfun  - button and object helper classes 
#
# Copyright RHE 2018
#
# 18-05-09 - rhe - written
################################################################################





#Import Modules
import os
import pygame
#import profile
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
sound_dir = os.path.join(main_dir, 'qbSound')
image_dir = os.path.join(main_dir, 'qbImage')

hight = 800
length = 900


################################################################################
# Class buttonBasic - faoundational buttom support
################################################################################
class buttonBasic():
    ############################################################################
    # method: __init__() constructor
    ############################################################################
    def __init__ (self, pos=(0,0), mySound=None):

        self.spinIt = 0
        self.spinItDeg = 0
        self.moveIt = True
        self.pos  = pos
        self.home = pos        
        self.posX = 0
        self.posY = 0
        if not mySound == None:
            self.sound = self.load_sound(mySound)
        else:
            self.sound = None

    ############################################################################
    # method: _spin() spin object
    ############################################################################
    def _spin(self):
        "spin the button once"
        center = self.rect.center
        if not self.spinItDeg: 
            self.spinItDeg = self.spinIt * 360
        self.spinIt = self.spinIt + 12
        if self.spinIt >= self.spinItDeg:
            self.spinIt = 0
            self.spinItDeg = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.spinIt)
        self.rect = self.image.get_rect(center=center)


    ############################################################################
    # method: _walk() walk object to final position
    ############################################################################
    def _walk(self):
        "move toward final"
        if self.rect.topleft == self.pos:
            self.moveIt = False
        else:
            #self.spinIt = True
            x = self.pos[0] - self.rect.topleft[0]
            if x > 0:
                self.posX = min (5, x)
            elif x < 0:
                self.posX = min (-5, -x)
            else:
                self.posX = 0
                
            y = self.pos[1] - self.rect.topleft[1]
            if y > 0:
                self.posY = min (5 , y)
            elif y < 0:
                self.posY = min (-5, -y)
            else:
                self.posY = 0

            newpos = self.rect.move((self.posX, self.posY))
            self.rect = newpos
            #self.image = pygame.transform.flip(self.image, 1, 0)


    ############################################################################
    # method: goHome() move object to home position
    ############################################################################
    def goHome(self):
        self.pos  = self.home
        self.moveIt = True


    ############################################################################
    # method: move() move object position newPos
    ############################################################################
    def move(self, newPos):
        self.pos  = newPos
        self.moveIt = True
    
    
    ############################################################################
    # method: moveRel() move object relative as described by relX and relY
    ############################################################################
    def moveRel(self, relX, relY):
        relX = relX + self.pos[0]
        relY = self.pos[1]
        self.pos = (relX, relY)
        self.moveIt = True
        
        
    ############################################################################
    # method: updateBasic() foundational update support (spin / walk)
    ############################################################################
    def updateBasic(self):
        "spin if hit"
        if self.spinIt:
            self._spin()
        if self.moveIt:
            self._walk()
            

    ############################################################################
    # method: punchedBasic() foundational object trigger support
    ############################################################################
    def punchedBasic(self, count=1):
        "this will cause the button to start spinning"
        if not self.spinIt:
            self.sound.play()
            self.spinIt = count
            self.original = self.image


    ############################################################################
    # method: load_image() load image file
    ############################################################################
    def load_image(self, name, colorkey=(None)):
        "load image file"
        fullname = os.path.join(image_dir, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print ('Cannot load image:', fullname)
            raise SystemExit()
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()


    ############################################################################
    # method: load_sound() load sound file
    ############################################################################
    def load_sound(self, name):
        "load sound file"
        class NoneSound:
            def play(self): pass
        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()
        fullname = os.path.join(sound_dir, name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error:
            print ('Cannot load sound: %s' % fullname)
            raise SystemExit()
        return sound




        
################################################################################
# class: mousePic() - moves a mouse picture on the screen
################################################################################
class mousePic(pygame.sprite.Sprite, buttonBasic):
    """moves a mouse picture on the screen"""
    ############################################################################
    # method: __init__() constructor
    ############################################################################
    def __init__(self):
        buttonBasic.__init__(self, (0.0), None)
        self.moveIt = False
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        #self.image, self.rect = self.load_image('x_catgirl.png', -1)
        self.image, self.rect = self.load_image('x_squirrel.png', -1)
        self.punching = 0


    ############################################################################
    # method: update() - object update function
    ############################################################################
    def update(self):
        "move the mouse picture based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)


    ############################################################################
    # method: click() - MOUSEBUTTONDOWN: Look for collision
    ############################################################################
    def click(self, target):
        "returns true if the mouse picture collides with the target"
        hitbox = self.rect.inflate(0, 0)
        return hitbox.colliderect(target.rect)


    ############################################################################
    # method: unClick() - MOUSEBUTTONUP: collision check done
    ############################################################################
    def unClick(self):
        "called to pull the mouse picture back"
        self.punching = 0


################################################################################
# class: ButtonPat() - This putton initiates a lightBar pattern
################################################################################
class ButtonPat(pygame.sprite.Sprite, buttonBasic):
    """Pattern Button"""
    ############################################################################
    # method: __init__() constructor
    ############################################################################
    def __init__(self, pos=(100,100), name="*", pattern=None):
        buttonBasic.__init__(self, pos, 'w_beep2.ogg')
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        
        self.font = pygame.font.SysFont("Arial", 16)
        self.textSurf = self.font.render(name, 1, (255,0,0))
        
        self.image, self.rect = self.load_image('x_gem4.png', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [30/W, H+30])
        self.rect.topleft = (25, 50)
        self.Home = pos
        self.threadPattern = pattern
        
        
    ############################################################################
    # method: update() - object update function
    ############################################################################
    def update(self):
        self.updateBasic()


    ############################################################################
    # method: punched() - object punch or trigger function
    ############################################################################
    def punched(self):
        self.punchedBasic()


    ############################################################################
    # method: patternGet() - return threadPattern 
    ############################################################################
    def patternGet(self):
        return self.threadPattern
  
  
  
###############################################################################
# Class: ButtonQuestion - Big start question button
# Press to start a question
################################################################################
class ButtonQuestion(pygame.sprite.Sprite, buttonBasic):
    """Question Button"""
    def __init__(self, pos=(length -100, 20)):
        buttonBasic.__init__(self, pos, 'w_beep3.ogg')
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = self.load_image('question2.jpg', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (500, 0)


    ############################################################################
    # method: update() - object update function
    ############################################################################
    def update(self):
        self.updateBasic()


    ############################################################################
    # method: punched() - object punch or trigger function
    ############################################################################
    def punched(self):
        self.punchedBasic(3)



################################################################################
# class: ButtonSkip() - Skip Answer Button
################################################################################
class ButtonSkipPlayer(pygame.sprite.Sprite, buttonBasic):
    """Skip Answer Button"""
    ############################################################################
    # method: __init__() constructor
    ############################################################################
    def __init__(self, pos=(100, hight - 100)):
        buttonBasic.__init__(self, pos, 'w_beep3.ogg')
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = self.load_image('x_cat.png', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (100, 200)


    ############################################################################
    # method: update() - object update function
    ############################################################################
    def update(self):
        self.updateBasic()


    ############################################################################
    # method: punched() - object punch or trigger function
    ############################################################################
    def punched(self):
        self.punchedBasic()


################################################################################
# class: ButtonIncorrect() - Incorrect Answer Button
################################################################################
class ButtonIncorrect(pygame.sprite.Sprite, buttonBasic):
    """Incorrect Answer Button"""
    ############################################################################
    # method: __init__() constructor
    ############################################################################
    def __init__(self, pos=(100, hight - 100)):
        buttonBasic.__init__(self, pos, 'w_badswap.wav')
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = self.load_image('xa_wrong.png', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (length, hight / 2)


    ############################################################################
    # method: update() - object update function
    ############################################################################
    def update(self):
        self.updateBasic()


    ############################################################################
    # method: punched() - object punch or trigger function
    ############################################################################
    def punched(self):
        self.punchedBasic(2)


################################################################################
# class: ButtonSkip() - Skip Answer Button
################################################################################
class ButtonLightBarReset(pygame.sprite.Sprite, buttonBasic):
    """Reset the light bar Button"""
    ############################################################################
    # method: __init__() constructor
    ############################################################################
    def __init__(self, pos=(100, hight - 100)):
        buttonBasic.__init__(self, pos, 'w_beep3.ogg')
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = self.load_image('x_gem1.png', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (length, hight / 2)


    ############################################################################
    # method: update() - object update function
    ############################################################################
    def update(self):
        self.updateBasic()


    ############################################################################
    # method: punched() - object punch or trigger function
    ############################################################################
    def punched(self):
        self.punchedBasic()


################################################################################
# class: ButtonCorrect() - Correct Answer Button
################################################################################
class ButtonCorrect(pygame.sprite.Sprite, buttonBasic):
    """Correct Answer Button"""
    ############################################################################
    # method: __init__() constructor
    ############################################################################
    def __init__(self, pos=(length - 100, hight - 100)):
        buttonBasic.__init__(self, pos, 'w_match1.wav')
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = self.load_image('xa_correct.png', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (0,0)


    ############################################################################
    # method: update() - object update function
    ############################################################################
    def update(self):
        self.updateBasic()


    ############################################################################
    # method: punched() - object punch or trigger function
    ############################################################################
    def punched(self):
        self.punchedBasic(2)



