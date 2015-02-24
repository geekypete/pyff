import sys,os,random,time,parallel,pygame,BCI
from FeedbackBase.MainloopFeedback import MainloopFeedback
from datetime import datetime

class StimulusPresentation(MainloopFeedback):
    """
    Implements the Stimulus Presentation . 
    """

    def init(self):
        """
        Initialize  user modifiable variables for stimulus presentation. 
        """
        self.nCountdown = 0                 # N of secs to count down
        self.auditoryFeedback = True    # Auditory feedback provided
        self.preDelayTime =  1000         
        self.postDelayTime = 1000
        self.stimTime = 500
        self.cueTime = 500
        self.cueFirst = True
        self.colorCue = True
        self.cueSize = 400
        self.cueVal = 9
        self.redcueVal = 8
        self.greencueVal = 7
        self.wordPath = "C:/Documents and Settings/Stim2 Computer/My Documents/nonword.csv"
        self.bgcolor = 0, 0, 0
        self.screenPos = [200,200,1024,768]
        self.fullscreen = True
        self.color = 255,255,255       # Color of symbol
        self.size = 125             # Size of symbol 

    def _init_pygame(self):
        """
        Initializes Pygame, opens a new screen filled with the specified background color.
        """
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.screenPos[0], self.screenPos[1])        
        pygame.init()
        pygame.display.set_caption('Stimulus Presentation')
        if self.fullscreen: 
            opts = pygame.FULLSCREEN
            self.screen = pygame.display.set_mode((self.screenPos[2],self.screenPos[3]),opts)
        else: 
            self.screen = pygame.display.set_mode((self.screenPos[2],self.screenPos[3]))
        self.background = pygame.Surface((self.screenPos[2],self.screenPos[3])) 
        self.background.fill(self.bgcolor)
        self.background_rect = self.background.get_rect(center = (self.screenPos[2]/2,self.screenPos[3]/2) )
        self.screen.blit(self.background,self.background_rect)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        self.font = pygame.font.Font(None, self.size)
        self.cueFont = pygame.font.Font(None, self.cueSize)
        pygame.mixer.init()

    def pre_mainloop(self):
        """
        """
        self._init_pygame()
        time.sleep(2)
        self.current = datetime.now()  
        self.ANTIALIAS = 1
        self.COUNTDOWN = 0
        self.fps = 60 
        self.CUE, self.PREDELAY, self.STIM, self.POSTDELAY= 1,2,3,4
        self.sequence =BCI.wordlist(os.path.normpath(self.wordPath))
        self.currentTick = 1            
        self.currentStim = 0            # Current number of stimulus    
        self.nSym = len(self.sequence)   # Number of symbols
        self.nStim = int(self.nSym)  # Total number of stimuli
        self.screenCenter = (self.screenPos[2]/2,self.screenPos[3]/2)
        self.state = self.COUNTDOWN
        self.state_finished = False
        self.p = parallel.Parallel()
        dir = os.path.dirname(sys.modules[__name__].__file__) # Get current dir
        self.sound = pygame.mixer.Sound(dir + "/Tone.wav")
        self.stimTime = BCI.fpsConvert((self.stimTime),self.fps) #BCI.fpsConvert(100,self.fps)               # How long the stimulus is displayed (in frames)
        self.preDelayTime = BCI.fpsConvert(self.preDelayTime,self.fps)     # How long to wait before response is accepted  # How long to wait before response is accepted 
        self.postDelayTime = BCI.fpsConvert(self.postDelayTime,self.fps)    
        self.cueTime = BCI.fpsConvert((self.cueTime),self.fps) 
   
    def tick(self):
        if self.cueFirst:
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
                
        else:
            # If last state is finished, proceed to next state
            if self.state_finished:
                if self.state == self.COUNTDOWN:
                    self.state = self.PREDELAY
                elif self.state == self.PREDELAY:
                    if self.currentStim == self.nStim:
                        self.on_stop()
                    else:
                        self.state = self.STIM
                elif self.state == self.STIM:
                    self.state = self.POSTDELAY
                elif self.state == self.POSTDELAY:
                    self.state = self.CUE
                elif self.state == self.CUE:
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
            #self.send_parallel(self.COUNTDOWN_END)
            # Finished counting, draw background
            self.state_finished = True
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            
        elif self.currentTick % self.fps == 0:
            #if self.currentTick == 0:        # the very first tick
                #self.send_parallel(self.COUNTDOWN_START)
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
            symbol = self.sequence[self.currentStim] [0]
            txt = self.font.render(symbol,self.ANTIALIAS,self.color)
            txt_rect = txt.get_rect(center=self.screenCenter)
            self.screen.blit(self.background,self.background_rect)
            self.screen.blit(txt, txt_rect)
            self.current = datetime.now()
            pygame.display.update()
            self.currentTick += 1
   
    def cue(self):
        if self.currentTick == self.cueTime:
            # Finished
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            self.state_finished = True
            self.currentStim += 1
        else:
            if self.colorCue==True:   
                if  self.sequence[self.currentStim-1] [2]>1:
                    txt = self.cueFont.render("+",self.ANTIALIAS,(255,0,0))
                else:
                    txt = self.cueFont.render("+",self.ANTIALIAS,(0,255,0))
            else:
                txt = self.cueFont.render("+",self.ANTIALIAS,self.color)
            txt_rect = txt.get_rect(center=self.screenCenter)
            self.screen.blit(self.background,self.background_rect)
            #print datetime.now() - self.current
            self.screen.blit(txt, txt_rect)
            #self.current = datetime.now()
            pygame.display.update()
            self.currentTick += 1
    
    def predelay(self):
        if self.currentTick == self.preDelayTime:
            # Finished
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            self.state_finished = True
        
        else:
            # Draw background
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            self.currentTick += 1
            if self.cueFirst:
                if self.currentTick ==self.preDelayTime-6:
                    self.send_parallel(int('{:07b}'.format(self.cueVal)[::-1],2))
            else:
                if self.currentTick == self.postDelayTime-6:
                    self.send_parallel(int('{:07b}'.format(self.sequence[self.currentStim-1] [1])[::-1],2))      
                if self.currentTick == BCI.fpsConvert(300,60):
                    self.sound.play()
                    print self.sound.get_length()
        
    def postdelay(self):
        if self.currentTick == self.postDelayTime:
            # Finished
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()
            self.state_finished = True
        
        else:
            # Draw background
            self.screen.blit(self.background,self.background_rect)
            pygame.display.update()

            if self.cueFirst:
                if self.currentTick == self.postDelayTime-6:
                    self.send_parallel(int('{:07b}'.format(self.sequence[self.currentStim-1] [1])[::-1],2))
                if self.currentTick == BCI.fpsConvert(300,60):
                    self.sound.play()
            else:
                if self.currentTick ==self.preDelayTime-6:
                    self.send_parallel(int('{:07b}'.format(self.cueVal)[::-1],2))
            self.currentTick += 1

    def post_mainloop(self):
        if self.auditoryFeedback:
            self.sound = None
            pygame.mixer.quit()
        pygame.quit()
        #self.send_parallel(self.RUN_END)
        
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
    a = StimulusPresentation()
    a.on_init()
    a.on_play()

  #  a.on_quit()
   # sys.exit()