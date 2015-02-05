# nback_verbal.py -
# Copyright (C) 2009  Matthias Treder
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
A verbal n-back task. A sequence of symbols is successively presented 
on the screen. The participant's task is to indicate via a button press
(keyboard arrows or mouse button)
whether the current symbol matches the nth (e.g., first, second, or third)
symbol back in time.
"""

"""
Triggers: 10,11,12... for the symbols
+20, that is, 30,31,32 ... when it is a match with the n-th precursor
"""
import sys,os,random,time,parallel,pygame,BCI
from FeedbackBase.MainloopFeedback import MainloopFeedback
from datetime import datetime
class nback_verbal(MainloopFeedback):
    
  
 
    STIMTIME = 500
    CUETIME = 500
    PREDELAYTIME = 1000
    POSTDELAYTIME = 1000
    FPS = 60
    COUNTDOWN = 0
    COLOR = 255,255,255
    STIMSIZE = 125
    CUESIZE = 400
    CUEVAL = 9
    # Triggers
    RUN_START, RUN_END = 252,253
    COUNTDOWN_START, COUNTDOWN_END = 200,201
    FALSCH , RICHTIG = 7,8      # Response markers
    # States during running
    # First stimulus is shown, and after pre-response time
    # response is to be entered
    CUE, PREDELAY, STIM, POSTDELAY= 1,2,3,4
    
    # Antialising with the text
    ANTIALIAS = 1
      
    def init(self):
        random.seed()
        self.sequencealt =BCI.wordlist(os.path.normpath("C:/Documents and Settings/Stim2 Computer/My Documents/nonword.csv"))
        self.nMatch = 1                 # Number of nth matches for each symbol (should be less than half of nOccur)
        self.nOccur = 1                 # Total number of occurences of each symbol
        self.n = 1                      # Current symbol is matched with the nth symbol back
        # Timing 
        self.fps = self.FPS                   # Frames-per-second
        self.stimTime = BCI.fpsConvert((self.STIMTIME-50),self.fps) #BCI.fpsConvert(100,self.fps)               # How long the stimulus is displayed (in frames)
        self.predelayTime = BCI.fpsConvert(self.PREDELAYTIME,self.fps)     # How long to wait before response is accepted  # How long to wait before response is accepted 
        self.postdelayTime = BCI.fpsConvert(self.POSTDELAYTIME,self.fps)    
        self.cueTime = BCI.fpsConvert((self.CUETIME-50),self.fps) 
        self.nCountdown = 0           # N of secs to count down
        self.auditoryFeedback = True       # Auditory feedback provided
        # Triggers
     
        # Auditory settings
        #self.auditoryFeedback = False   # If yes, gives a beep when a wrong response is given
        # Graphical settings
        self.bgcolor = 0, 0, 0
        self.screenPos = [200,200,1024,768]
        self.fullscreen = True
        self.color = self.COLOR        # Color of symbol
        self.size = self.STIMSIZE               # Size of symbol 
        self.current = datetime.now()  
    def _init_pygame(self):
        # Initialize pygame, open screen and fill screen with background color 
        #os.environ['SDL_VIDEODRIVER'] = self.video_driver   # Set video driver
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.screenPos[0], self.screenPos[1])        
        pygame.init()
        pygame.display.set_caption('Stimulus Presentation')
        if self.fullscreen: 
            #use opts = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN to use doublebuffer and vertical sync
            opts = pygame.FULLSCREEN
            #self.screen = pygame.display.set_mode((480,480),pygame.FULLSCREEN)
            self.screen = pygame.display.set_mode((self.screenPos[2],self.screenPos[3]),opts)
        else: 
            self.screen = pygame.display.set_mode((self.screenPos[2],self.screenPos[3]))
        self.background = pygame.Surface((self.screenPos[2],self.screenPos[3])) 
        self.background.fill(self.bgcolor)
        self.background_rect = self.background.get_rect(center = (self.screenPos[2]/2,self.screenPos[3]/2) )
        self.screen.blit(self.background,self.background_rect)
        self.clock = pygame.time.Clock()
        #pygame.mouse.set_visible(False)
        self.font = pygame.font.Font(None, self.size)
        self.cueFont = pygame.font.Font(None, self.CUESIZE)
        # init sound engine
        pygame.mixer.init()

    def pre_mainloop(self):
        self.send_parallel(self.RUN_START)
        self._init_pygame()
        time.sleep(2)
        """ Internal variables """
        self.currentTick = 1            # Tick counter
        self.currentStim = 0            # Current number of stimulus    
        self.nSym = len(self.sequencealt)   # Number of symbols
        self.nStim = int(self.nSym)  # Total number of stimuli
        self.screenCenter = (self.screenPos[2]/2,self.screenPos[3]/2)
        # States
        self.state = self.COUNTDOWN
        self.state_finished = False
        self.p = parallel.Parallel()
        dir = os.path.dirname(sys.modules[__name__].__file__) # Get current dir
        if self.auditoryFeedback:
            self.sound = pygame.mixer.Sound(dir + "/sound18.wav")
        
         
    def tick(self):
        # If last state is finished, proceed to next state
        if self.state_finished:
            if self.state == self.COUNTDOWN:
                self.state = self.PREDELAY
            elif self.state == self.PREDELAY:
                self.state = self.CUE
            elif self.state == self.CUE:
                self.state = self.POSTDELAY
            elif self.state == self.POSTDELAY:
                if self.currentStim == self.nStim:
                    self.on_stop()
                else:
                    self.state = self.STIM
            elif self.state == self.STIM:
                self.state = self.PREDELAY

            self.currentTick = 0        # Reset tick count
            self.state_finished = False

    def play_tick(self):
        if self.checkWindowFocus():
            state = self.state
            if state == self.COUNTDOWN:
                self.countdown()
            elif state == self.PREDELAY:
                self.predelay()   
            elif state == self.POSTDELAY:
                self.postdelay()
            elif state == self.CUE:
                self.cue()      
            elif state == self.STIM:
                self.stim()

            # Keep running at the number of fps specified
            self.clock.tick(self.fps)

    def pause_tick(self):
            txt = self.font.render("PAUSE",self.ANTIALIAS,self.color)
            txt_rect = txt.get_rect(center=self.screenCenter)
            self.screen.blit(self.background,self.background_rect)
            self.screen.blit(txt, txt_rect)
            pygame.display.update()
            self.clock.tick(self.fps)
            
    def countdown(self):
        if self.currentTick/self.fps == self.nCountdown:
            self.send_parallel(self.COUNTDOWN_END)
            # Finished counting, draw background
            self.state_finished = True
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
        elif self.currentTick % self.fps == 0:
            if self.currentTick == 0:        # the very first tick
                self.send_parallel(self.COUNTDOWN_START)
            # New number
            count = self.nCountdown - (self.currentTick+1)/self.fps
            txt = self.font.render(str(count),self.ANTIALIAS,(0,255,0))
            txt_rect = txt.get_rect(center=self.screenCenter)
            self.screen.blit(self.background,self.background_rect)
            self.screen.blit(txt, txt_rect)
            pygame.display.update()
            self.currentTick += 1
        else:
            # Keep drawing the same number
            count = self.nCountdown - self.currentTick/self.fps
            txt = self.font.render(str(count),self.ANTIALIAS,(0,255,0))
            txt_rect = txt.get_rect(center=self.screenCenter)
            self.screen.blit(self.background,self.background_rect)
            self.screen.blit(txt, txt_rect)
            pygame.display.update()
            self.currentTick += 1
                          
    def stim(self):
        if self.currentTick == self.stimTime:
            # Finished
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            self.state_finished = True
        else:
            # Draw symbol
            #if self.currentTick == 0:
                #self.p.setData(0)
                #time.sleep(0.001)
                #self.p.setData(int('{:07b}'.format(self.sequencealt[self.currentStim] [1])[::-1],2))
                #print("%s = %s  " % (self.sequencealt[self.currentStim] [0], self.sequencealt[self.currentStim] [1]))
            #print self.currentTick
            symbol = self.sequencealt[self.currentStim] [0]
            #print self.sequencealt[self.currentStim] [1]
            txt = self.font.render(symbol,self.ANTIALIAS,self.color)
            txt_rect = txt.get_rect(center=self.screenCenter)
            self.screen.blit(self.background,self.background_rect)
            #print datetime.now() - self.current
            self.screen.blit(txt, txt_rect)
            self.current = datetime.now()
            #if self.currentTick == 0:
                #self.send_parallel(int('{:07b}'.format(self.sequencealt[self.currentStim] [1])[::-1],2))
                #self.p.setData(0)
                #time.sleep(0.01)
                #self.p.setData(int('{:07b}'.format(self.sequencealt[self.currentStim] [1])[::-1],2))
            pygame.display.update()
          
                #print("%s = %s  " % (self.sequencealt[self.currentStim] [0], self.sequencealt[self.currentStim] [1]))
                #self.p.setData(0)
            #time.sleep(1)
            #self.p.setData(int('{:07b}'.format(self.sequencealt[self.currentStim] [1])[::-1],2))
            self.currentTick += 1

    def cue(self):
        if self.currentTick == self.cueTime:
            # Finished
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            self.state_finished = True
            self.currentStim += 1
        else:
            #if self.currentTick == 0:
                #self.p.setData(0)
                #.sleep(0.005)
                #self.p.setData(int('{:07b}'.format(99)[::-1],2))
            # Draw symbol
            #symbol = self.sequencealt[self.currentStim] 
            #print "CUE CUE CUE CUE CUE"
            #if self.currentTick == 0:
                #self.send_parallel(int('{:07b}'.format(self.CUEVAL)[::-1],2))
                #self.p.setData(0)
                #time.sleep(0.01)
                #self.p.setData(int('{:07b}'.format(9)[::-1],2))    
            txt = self.cueFont.render("+",self.ANTIALIAS,self.color)
            txt_rect = txt.get_rect(center=self.screenCenter)
            self.screen.blit(self.background,self.background_rect)
            #print datetime.now() - self.current
            self.screen.blit(txt, txt_rect)
            #self.current = datetime.now()
            pygame.display.update()
            self.currentTick += 1
    
    def predelay(self):
        if self.currentTick == self.predelayTime:
            # Finished
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            self.state_finished = True
        
        else:
            # Draw background
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            self.currentTick += 1
            if self.currentTick ==self.predelayTime-6:
                self.send_parallel(int('{:07b}'.format(self.CUEVAL)[::-1],2))
                
            print 'Delay happening', self.currentTick
        
   
    def postdelay(self):
        if self.currentTick == self.postdelayTime:
            # Finished
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            self.state_finished = True
        
        else:
            # Draw background
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            if self.currentTick == self.postdelayTime-6:
                self.send_parallel(int('{:07b}'.format(self.sequencealt[self.currentStim] [1])[::-1],2))
            self.currentTick += 1
            
            print 'POSTDelay happening', self.currentTick
    


    def post_mainloop(self):
        if self.auditoryFeedback:
            self.sound = None
            pygame.mixer.quit()
        pygame.quit()
        self.send_parallel(self.RUN_END)
        
   
    
    def checkWindowFocus(self):
        """
        Return true if pygame window has focus. Otherwise display text
        and return false.
        """
        pygame.event.get()
        if not pygame.key.get_focused():
            txt = self.font.render("Click to start",self.ANTIALIAS,self.color)
            txt_rect = txt.get_rect(center=self.screenCenter)
            self.screen.blit(self.background,self.background_rect)
            self.screen.blit(txt, txt_rect)
            pygame.display.update()
            return False
        return True
        
        
    
if __name__ == "__main__":
    a = nback_verbal()
    a.on_init()
    a.on_play()

  #  a.on_quit()
   # sys.exit()
