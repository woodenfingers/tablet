#!/usr/bin/python3

################################################################################
# quizBar main - LightBar / Flower button Quiz Game
#
# Copyright RHE 2018
#
# Other license:
# Attribution-NonCommercial-ShareAlike 3.0 United States (CC BY-NC-SA 3.0 US)
#  For non comercial use 
#  Image credits to Making Games with Python & Pygame - Albert Sweigart
#
# 18-05-09 - rhe - written - 1st prgame application
################################################################################


#Import Modules
import os
import time
import sys

# Path to core files
sys.path.append('../core1')

#import pygame
import pygame
from pygame.locals import *
from pygame.compat import geterror

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

#import core and game
from boxConfig import boxConfig
from lightBar import lightBar
from lightBar import playThread
from lightBar import playSwitchThread

from patternsDance import dancePat
from patternLib import patternLib
pat = patternLib()
val = dancePat()

from quizBarFun import buttonBasic
from quizBarFun import mousePic
from quizBarFun import ButtonPat
from quizBarFun import ButtonQuestion
from quizBarFun import ButtonSkipPlayer
from quizBarFun import ButtonIncorrect
from quizBarFun import ButtonLightBarReset
from quizBarFun import ButtonCorrect



main_dir = os.path.split(os.path.abspath(__file__))[0]
sound_dir = os.path.join(main_dir, 'qbSound')
image_dir = os.path.join(main_dir, 'qbImage')

hight = 800
length = 900
screenSize = (length, hight)




#classes for our game objects




class ButtonReset(pygame.sprite.Sprite, buttonBasic):
    """Reset Button"""
    def __init__(self, pos=(length/2, 20), p1=None, p2=None, p3=None, p4=None, p5=None, p6=None):
        buttonBasic.__init__(self, pos, 'BoxingBell.wav')
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = self.load_image('x_reset.png', 0)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (length, 0)
        self.player1 = p1
        self.player2 = p2
        self.player3 = p3
        self.player4 = p4
        self.player5 = p5
        self.player6 = p6

    def update(self):
        self.updateBasic()

    def punched(self):
        if self.player1:
            self.player1.scoreReset()
        if self.player2:
            self.player2.scoreReset()
        if self.player3:
            self.player3.scoreReset()
        if self.player4:
            self.player4.scoreReset()
        if self.player5:
            self.player5.scoreReset()
        if self.player6:
            self.player6.scoreReset()
        self.punchedBasic()





class quizMgr:
    def __init__(self):
        self.pointStart = 20
        self.points=self.pointStart
        self.player=None
        self.oSlot = 0
        self.order = [0,0,0,0,0,0,0,0,0,0]
        self.pSlot = 0
        self.pending = [0,0,0,0,0,0,0,0,0,0]
        self._initSlots()
        
        # light patterns
        self.threadPattern = pat.chasePattern21
        self.lightBarThread = None
        self.manualControl = lightBar(pat.allOffLight)
        self.slowdown = lightBar(pat.slowDown)
        self.correctLight = lightBar(pat.correctLight)
        self.inCorrectLight = lightBar(pat.inCorrectLight)



    def lightBarThreadStop(self):
        "Stop lChase thread"
        if not self.lightBarThread == None:
            self.lightBarThread.stop()
            self.lightBarThread = None



    def lightBarThreadStart(self):
        "Start lChase thread"
        self.lbAllOff()

        self.lightBarThread = playSwitchThread(self.threadPattern, 40)
        self.lightBarThread.tempoMinSet()
        self.lightBarThread.maskSet(0x7E)
        self.lightBarThread.timeWarpSet(100)
        self.lightBarThread.start()



    def lightBarThreadSet(self, pattern):
        self.threadPattern = pattern
        self.lightBarThreadStart()

    def slowdownStart(self):
        "Start slowdown thread"
        self.lbAllOff()
        self.slowdown.play()

    def lbCorrectStart(self):
        "Start lCorrect thread"
        self.lbAllOff()
        self.correctLight.play()

    
    def lbIncorrectStart(self):
        "Start inCorrectLight thread"
        self.lbAllOff()
        self.inCorrectLight.play()



    def lbAllOff(self):
        self.lightBarThreadStop()
        self.correctLight.stop()
        self.inCorrectLight.stop()
        time.sleep(.1)
        self.manualControl.maskSet(0xff)
        self.manualControl.allOff()



    def _initSlots(self):
        self.oSlot=0
        self.order = [0,0,0,0,0,0,0,0,0,0]
        self.pSlot=0
        self.pending = [0,0,0,0,0,0,0,0,0,0]


    def newQuestion(self):
        self.lightBarThreadStart()
        
        self.playerList.sort(key=lambda x: x._playerScore, reverse=True)
        for i in range(6):
            player = self.playerList[i]
            self.playerList[i].homeY = self.homeYList[i]

        self.points=self.pointStart
        self.player=None
        for player in self.order:
            if player != 0:
                player.done()
        for player in self.pending:
            if player != 0:
                player.done()
        self._initSlots()

        
        
    def answerCorrect(self):
        self.lbCorrectStart()

        player = self.order[0]
        if player != 0:
            player.scoreSet(self.points)
            self.Points = min(self.points, self.points - 5)
            #self.shiftLeft()
    
    
    def answerIncorrect(self):
        self.lbIncorrectStart()

        player = self.order[0]
        if player != 0:
            player.scoreSet(-5)
            #self.shiftLeft()
           
           
    def answerSkip(self):
        self.lightBarThreadStop()

        player = self.order[0]
        if player != 0:
            self.shiftLeft()


    def answerPenalty(self, penalty=0):
        self.lbIncorrectStart()

        player = self.order[0]
        if player != 0:
            player.scoreSet(penalty)
            

    def lbReset(self):
        self.lbAllOff()


    def lbResaltsReset(self):
        self.manualControl.maskSet(0x81)
        self.manualControl.relayPatternSet(0)
        
        
    def positionPlayer(self, player):
        if player.locatonGet() == 'home':
            player.select(self.oSlot)
            self.order[self.oSlot] = player
            player.move ((175 + int(self.oSlot) * 100 ,475))
            self.oSlot += 1
    

    def shiftLeft(self):
        player = self.order[0]
        loc = player.locatonGet()
        self.pending[self.pSlot] = player
        self.pSlot += 1
        player.select('waiting')
        player.move ((50, 150 + int(loc) * 100))
        
        self.order[0] = self.order[1]
        player = self.order[0]
        if player != 0:
            player.moveRel (-100, 0)
        
        self.order[1] = self.order[2]
        player = self.order[1]
        if player != 0:
            player.moveRel (-100, 0)
        
        self.order[2] = self.order[3]
        player = self.order[2]
        if player != 0:
            player.moveRel (-100, 0)
         
        self.order[3] = self.order[4]
        player = self.order[3]
        if player != 0:
            player.moveRel (-100, 0)
        
        self.order[4] = self.order[5]
        player = self.order[4]
        if player != 0:
            player.moveRel (-100, 0)
        
        self.order[5] = self.order[6]
        player = self.order[5]
        if player != 0:
            player.moveRel (-100, 0)
        
        self.order[6] = 0

        pass
    
    def selectPlayer(self):
        pass
    

class CourtFrame(pygame.sprite.Sprite, buttonBasic):
    """Players Frame"""

    def __init__(self, surface, image='xb_grass.png', plPlWdth=100, plPlHt=150, numPls=6):

        self.surface = surface
        self.plPlWidth = plPlWdth
        self.plPlHeight = plPlHt
        self.frameSize = (numPls * self.plPlWidth + 50, self.plPlHeight)
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        print ("FrameSize: " + repr(self.frameSize))

        self.image, self.rect = self.load_image(image, 0)
        self.image = pygame.transform.scale(self.image, (numPls * self.plPlWidth + 50, self.plPlHeight))
        self.frame = pygame.Surface((numPls * self.plPlWidth + 50, self.plPlHeight))
        self.frame.convert()

        self.frame.blit(self.image, (125, 450))
        pygame.display.flip()

        self.rect.topleft = (125, 450)

    def refresh(self):

        self.surface.blit(self.image, (125, 450))


class ButtonPlayer(pygame.sprite.Sprite, buttonBasic):
    """Player Button"""
    def __init__(self, pos=(100,100), name="*", type=1):
        self._playerLocaton = 'home'
        self._playerScore = 0
        self.name = name
        buttonBasic.__init__(self, pos, 'w_beep2.ogg')
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        if type == 1:
            self.image, self.rect = self.load_image('x_RedSelector.png', 0)
        else:
            self.image, self.rect = self.load_image('x_Selector.png', 0)

        self._scroreTextUpdate()
        #self.rect.topleft = (25, 50)
        #print("pos[0] ", str(pos[0]) + " " + str(700 - pos[0]) + " pos[1] ", str(pos[1]) + " " + str(700 - pos[1]))
        #ORG self.rect.topleft = (25 + pos[1], 800 - pos[1])
        self.rect.topleft = (pos[1], pos[1])
        
        
        
    def update(self):
        self.updateBasic()

    def punched(self):
        self._playerScore += 10
        self._scroreTextUpdate()
        self.punchedBasic()
        self.scorePrint()
    
    def select(self, location):
        self._playerLocaton = location
        
    def locatonGet(self):
        return self._playerLocaton

    def done(self):
        self._playerLocaton = 'home'
        self.goHome()
        
    def scoreReset(self):
        self._playerScore = 0
        self._scroreTextUpdate()

    def scoreSet(self, score):
        self._playerScore += score
        self._scroreTextUpdate()

    def scorePrint(self):
        if self._playerScore:
            print("  Player: " + self.name + " " + str(self._playerScore))
        
    def scoreGet(self, score):
        self._scroreTextUpdate()
        return self._playerScore
        
    def _scroreTextUpdate(self):
        self.font = pygame.font.SysFont(None, 20)
        myTitle=str(self.name)
        self.textSurf = self.font.render(myTitle, 1, (0, 0, 255))
        self.font = pygame.font.SysFont(None, 30)
        scoreStr = '{:>4} '.format(self._playerScore)
        self.textScore = self.font.render(scoreStr, True, (0, 0, 255),(255,255,255))
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
        #RW = self.screen.get_width()
        #RH = self.screen.get_height()
        #print ('RW' + repr(RW))
        #print ('RH' + repr(RH))

        TW = self.textSurf.get_width()
        #TH = self.textSurf.get_height()
        self.image.blit(self.textSurf, [50/2 - TW/2, 2])
        self.image.blit(self.textScore, [2, 20])
        




def main():

    box=boxConfig()    
    
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    quiz = quizMgr()
    quiz.homeYList = [125, 225, 325, 425, 525, 625]
    quiz.playerList = [None, None, None, None, None, None]
    
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((screenSize))
    pygame.display.set_caption('QuizBar')
    pygame.mouse.set_visible(1)

#Create The Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))


#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("QuizBar", 1, (200, 200, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock       = pygame.time.Clock()
    myPtr       = mousePic()
    bIncorrect  = ButtonIncorrect((100, hight - 100))
    bLbReset    = ButtonLightBarReset((300, hight - 100))
    bCorrect    = ButtonCorrect((500, hight - 100))
    bQuestion   = ButtonQuestion((100, 150))
    bSkipPlayer = ButtonSkipPlayer((105, 620))
    bPlayer1    = ButtonPlayer((length -100, quiz.homeYList[0]), 'Green',   1)
    quiz.playerList[0] = bPlayer1
    bPlayer2    = ButtonPlayer((length -100, quiz.homeYList[1]), 'Blue',    2)
    quiz.playerList[1] = bPlayer2
    bPlayer3    = ButtonPlayer((length -100, quiz.homeYList[2]), 'White',   1)
    quiz.playerList[2] = bPlayer3
    bPlayer4    = ButtonPlayer((length -100, quiz.homeYList[3]), 'Red',     2)
    quiz.playerList[3] = bPlayer4
    bPlayer5    = ButtonPlayer((length -100, quiz.homeYList[4]), 'Yellow',  1)
    quiz.playerList[4] = bPlayer5
    bPlayer6    = ButtonPlayer((length -100, quiz.homeYList[5]), 'Antique', 2)
    quiz.playerList[5] = bPlayer6
    bReset      = ButtonReset((length -100, 20), bPlayer1, bPlayer2, bPlayer3, bPlayer4, bPlayer5, bPlayer6)
    bPat01      = ButtonPat(( 25, 50), 'waltz', val.waltz)
    bPat02      = ButtonPat((100, 50), 'vWaltz', val.vWaltz)
    bPat03      = ButtonPat((175, 50), 'FoxTrot', val.foxTrot)
    bPat04      = ButtonPat((250, 50), 'Q-step', val.quickstep)
    bPat05      = ButtonPat((325, 50), 'ChaCha', val.chaChaCha)
    bPat06      = ButtonPat((400, 50), 'Rumba', val.rumbaVal)
    bPat07      = ButtonPat((475, 50), 'vRumba', val.rumba)
    bPat08      = ButtonPat((550, 50), 'Chase1', pat.chasePattern12)
    bPat09      = ButtonPat((625, 50), 'Chase2', pat.chasePattern13)
    bPat10      = ButtonPat((700, 50), 'Chase3', pat.chasePattern21) 
    gameCourt   = CourtFrame(screen)
    allsprites  = pygame.sprite.Group((myPtr, bCorrect, bIncorrect, bReset, bLbReset, 
                                       bQuestion, bSkipPlayer,
                                       bPlayer1, bPlayer2, bPlayer3,
                                       bPlayer4, bPlayer5, bPlayer6,
                                       bPat01, bPat02, bPat03, bPat04, bPat05,
                                       bPat06, bPat07, bPat08, bPat09, bPat10))
    correctInPlay = False
    inCorrectInPlay = False

#Main Loop
    going = True
    while going:
        clock.tick(60)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    going = False
                    
                elif event.unicode == 'c'or event.key == 275:
                    quiz.slowdownStart()
                    quiz.answerCorrect()
                    bCorrect.punched()
                    #bSkipPlayer.punched()
                    quiz.answerSkip()
                    
                elif event.unicode == 'x'or event.key == 276:
                    quiz.slowdownStart()
                    quiz.answerIncorrect()
                    bIncorrect.punched()
                    bSkipPlayer.punchedQuiet()
                    quiz.answerSkip()

                elif event.unicode == 's'or event.key == 273:
                    bSkipPlayer.punchedQuiet()
                    quiz.answerSkip()

                elif event.key == 274:
                    bLbReset.punched()
                    quiz.lbResaltsReset()
                    
                elif event.unicode == 'q' or event.unicode == '?' or event.key == 13 or event.key == 271:
                    bQuestion.punched()
                    quiz.newQuestion()
                    print ("\nScoreboard:")
                    bPlayer1.scorePrint()
                    bPlayer2.scorePrint()
                    bPlayer3.scorePrint()
                    bPlayer4.scorePrint()
                    bPlayer5.scorePrint()
                    bPlayer6.scorePrint()
                    
                elif event.unicode == 'R':
                    bReset.punched()
                    quiz.newQuestion()


                elif event.unicode == '1':
                    quiz.positionPlayer(bPlayer1)

                elif event.unicode == '2':
                    quiz.positionPlayer(bPlayer2)

                elif event.unicode == '3':
                    quiz.positionPlayer(bPlayer3)

                elif event.unicode == '4':
                    quiz.positionPlayer(bPlayer4)

                elif event.unicode == '5':
                    quiz.positionPlayer(bPlayer5)

                elif event.unicode == '6':
                    quiz.positionPlayer(bPlayer6)

                # ignore shift, right control left control or alt
                elif event.key == 304 or event.key == 305 or event.key == 306 or event.key == 308:
                    continue

                else:
                    # DEBUG, print event
                    print(str(event.key) + " " + str(event))
            
            elif event.type == MOUSEBUTTONDOWN:
                done = False
                for button in allsprites:
                    if button != myPtr and done == False:
                        if myPtr.click(button):
                            if button == bQuestion:
                                quiz.newQuestion()
                                print ("\nScoreboard:")
                                bPlayer1.scorePrint()
                                bPlayer2.scorePrint()
                                bPlayer3.scorePrint()
                                bPlayer4.scorePrint()
                                bPlayer5.scorePrint()
                                bPlayer6.scorePrint()
                            elif button == bCorrect:
                                if not correctInPlay:
                                    correctInPlay = True
                                    quiz.answerCorrect()
                                    quiz.answerSkip()
                                    correctInPlay = False
                                else:
                                    print("Ignoring: Correct play in progress")
                            elif button == bIncorrect:
                                if not inCorrectInPlay:
                                    inCorrectInPlay=True
                                    quiz.answerIncorrect()
                                    bSkipPlayer.punchedQuiet()
                                    quiz.answerSkip()
                                    inCorrectInPlay = False
                                else:
                                    print("Ignoring: Correct play in progress")
                            elif button == bLbReset:
                                quiz.lbResaltsReset()
                                correctInPlay = False
                                inCorrectInPlay = False
                                print ("\nScoreboard:")
                                bPlayer1.scorePrint()
                                bPlayer2.scorePrint()
                                bPlayer3.scorePrint()
                                bPlayer4.scorePrint()
                                bPlayer5.scorePrint()
                                bPlayer6.scorePrint()
                            elif button == bSkipPlayer:
                                 quiz.answerPenalty(bSkipPlayer.penaltyGet())
                                 quiz.answerSkip()
                            elif button == bPat01 or button == bPat02 or button == bPat03 or button == bPat04 or button == bPat05 or button == bPat06 or button == bPat07 or button == bPat08 or button == bPat09 or button == bPat10:
                                 #quiz.lightBarThreadSet(button.patternGet())
                                 quiz.lightBarThreadSet(button.threadPattern)
                                 


                                
                            button.punched()
                            done = True

            elif event.type == MOUSEBUTTONUP:
                myPtr.unClick()
            #else:
                #print(str(event))

        #Move or spin Players
        allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        gameCourt.refresh()
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

#Game Over
    

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
    #profile.run('main()')
