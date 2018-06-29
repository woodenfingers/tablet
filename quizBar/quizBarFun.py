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
        self.homeY = self.pos[1]
        self.posX = 0
        self.posY = 0
        self.sound = None
        self.bSound0 = None
        self.bSound1 = None
        self.bSound2 = None
        self.bSound3 = None
        self.bSound4 = None
        self.bSound5 = None
        self.bSound6 = None
        self.bSound7 = None
        self.bSoundCount = 0
        self.bSoundList = [self.bSound0, self.bSound1,
                           self.bSound2, self.bSound3,
                           self.bSound4, self.bSound5,
                           self.bSound6, self.bSound7]
        
        if mySound:
            self.sound = self.load_sound(mySound)
            self.bSound0 = self.sound
            self.bSound1 = self.sound
            self.bSound2 = self.sound
            self.bSound3 = self.sound
            self.bSound4 = self.sound
            self.bSound5 = self.sound
            self.bSound6 = self.sound
            self.bSound7 = self.sound

        self.initSoundlist(self.bSound0, self.bSound1,
                           self.bSound2, self.bSound3,
                           self.bSound4, self.bSound5,
                           self.bSound6, self.bSound7)
    
    
    ############################################################################
    # method: initSoundlist initialize the sound list
    ############################################################################
    def initSoundlist(self, s0, s1, s2, s3, s4, s5, s6, s7):
        self.bSoundList[0] = s0
        self.bSoundList[1] = s1
        self.bSoundList[2] = s2
        self.bSoundList[3] = s3
        self.bSoundList[4] = s4
        self.bSoundList[5] = s5
        self.bSoundList[6] = s6
        self.bSoundList[7] = s7
        
        self.bSoundCount = 0


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
        self.pos  = (self.home[0], self.homeY)
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
    # methcatod: punchedBasic() foundational object trigger support
    ############################################################################
    def punchedBasic(self, count=1):
        "this will cause the button to start spinning"
        if not self.spinIt:
            sound = self.bSoundList[self.bSoundCount & 0x7]
            if sound:
                sound.play()
            self.bSoundCount += 1
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
        buttonBasic.__init__(self, (0,0), None)
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
        buttonBasic.__init__(self, pos, None)
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = self.load_image('x_cat.png', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (100, 200)
        self.cSound1 = buttonBasic.load_sound(self, 'Cat-Scream.wav')
        self.cSound2 = buttonBasic.load_sound(self, 'DogGrowlThenBark-SoundBible.com-224495057.wav')
        self.cSound3 = buttonBasic.load_sound(self, 'MonsterLaugh-SoundBible.com-542163030.wav')
        self.cSound4 = buttonBasic.load_sound(self, 'TyrannosaurusRex-SoundBible.com-45786848.wav')
        self.cSound5 = buttonBasic.load_sound(self, 'Evil_Laugh_1-Timothy-64737261.wav')
        self.catCount = 0
        self.soundList=(self.cSound2, self.cSound1, self.cSound1, self.cSound5,
                        self.cSound3, self.cSound1, self.cSound4, self.cSound1)
        self.penaltyPoints=(0, -7, 0, 11, 2,- 23, 0, -27)

    ############################################################################
    # method: update() - object update function
    ############################################################################
    def update(self):
        self.updateBasic()


    ############################################################################
    # method: punched() - object punch or trigger function
    ############################################################################
    def punched(self):
        self.soundList[self.catCount & 0x07].play()
        self.catCount += 1        
        self.punchedBasic()


    ############################################################################
    # method: punched() - object punch or trigger function
    ############################################################################
    def punchedQuiet(self):
        self.punchedBasic()
        
        
    ############################################################################
    # method: penaltyGet() - Return Pentalty 
    ############################################################################
    def penaltyGet(self):
        return self.penaltyPoints[self.catCount & 0x07]


################################################################################
# class: ButtonIncorrect() - Incorrect Answer Button
################################################################################
class ButtonIncorrect(pygame.sprite.Sprite, buttonBasic):
    """Incorrect Answer Button"""
    ############################################################################
    # method: __init__() constructor
    ############################################################################
    def __init__(self, pos=(100, hight - 100)):
        buttonBasic.__init__(self, pos, None)
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = self.load_image('xa_wrong.png', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (length, hight / 2)
        self.bSound1 = buttonBasic.load_sound(self, 'w_badswap.wav')
        self.bSound2 = buttonBasic.load_sound(self, 'Sad_Trombone-Joe_Lamb-665429450.wav')
        self.bSound3 = buttonBasic.load_sound(self, 'Smashing-Yuri_Santana-1233262689.wav')
        self.bSound4 = buttonBasic.load_sound(self, 'StrangeSlip-SoundBible.com-223009506.wav')
        self.initSoundlist (self.bSound1, self.bSound2, self.bSound3, self.bSound4,
                            self.bSound2, self.bSound3, self.bSound4, self.bSound1)


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
# class: ButtonLightBarReset() - Skip Answer Button
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
        #buttonBasic.__init__(self, pos, 'w_match1.wav')
        buttonBasic.__init__(self, pos, None)
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = self.load_image('xa_correct.png', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (0,0)
        self.bSound1 = buttonBasic.load_sound(self, 'Computer_Magic-Microsift-1901299923.wav')
        self.bSound2 = buttonBasic.load_sound(self, '1_person_cheering-Jett_Rifkin-1851518140.wav')
        self.bSound3 = buttonBasic.load_sound(self, 'Yes-SoundBible.com-1345875982.wav')
        self.bSound4 = buttonBasic.load_sound(self, 'KidsCheering-SoundBible.com-681813822.wav')
        self.bSound5 = buttonBasic.load_sound(self, 'ScreamOfJoy-SoundBible.com-1639390065.wav')
        self.initSoundlist(self.bSound1, self.bSound2, self.bSound3, self.bSound4,
                           self.bSound5, self.bSound3, self.bSound4, self.bSound1)


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



