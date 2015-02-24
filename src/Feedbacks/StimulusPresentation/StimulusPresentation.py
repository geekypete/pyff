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
        self.nCountdown = 0                 #N of secs to count down
        self.auditoryFeedback = True    #Auditory feedback provided
        self.preDelayTime =  1000         #Delay time before stimulus presentation in ms
        self.postDelayTime = 1000         #Delay time after stimulus presentation in ms
        self.stimTime = 500                   #Time to display the stimulus (word) in ms
        self.cueTime = 500                    #Time to display the cue (+) in ms
        self.cueFirst = True                   #Presents the cue first if true, else it presents the stimulus first 
        self.colorCue = True                 #If true it utilizes feedback to color the cue, otherwise the cue is presented as the same color as the stim
        self.cueSize = 400                     #Cue size in pixel height
        self.cueVal = 9                          #TTL code for the cue when colorCue==False
        self.redcueVal = 8                     #TTL code for the red cue when colorCue==True
        self.greencueVal = 7                  #TTL code for the green cue when colorCue==True
        self.wordPath = "C:/Documents and Settings/Stim2 Computer/My Documents/nonword.csv" #Filepath and filename for the word list with TTL codes
        self.bgcolor = 0, 0, 0                  #Background color tuple in the form (red, green, blue) where each value varies from 0 to 255
        self.screenPos = [200,200,1024,768] #Screen position where the first two values specify position origin and the second two values define resolution
        self.fullscreen = True                 #Sets the gui to fullscreen when True
        self.color = 255,255,255              #Color of stimulus and cue (when colorCue==False) in the form (red, green, blue) where each value varies from 0 to 255
        self.size = 125                            #Size of stimuli (word) in pixel height

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
        Initialize non-modifiable variables. Users should not modify variables within this region unless they are
        certain of what they are doing.
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
        """
        Tick increments the state between countdown, pre and post delay, cue presentation, and stimulus presentation.
        """
        if self.cueFirst:
            """ If last state is finished, proceed to next state"""
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

                self.currentTick = 0       
                self.state_finished = False
                
        else:
            """ If last state is finished, proceed to next state"""
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

                self.currentTick = 0       
                self.state_finished = False

    def play_tick(self):
        """
        Execute function associated with current state.
        """
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
        """
        Pause Feedback.
        """
            txt = self.font.render("PAUSE",self.ANTIALIAS,self.color)
            txt_rect = txt.get_rect(center=self.screenCenter)
            self.screen.blit(self.background,self.background_rect)
            self.screen.blit(txt, txt_rect)
            pygame.display.update()
            self.clock.tick(self.fps)
            
    def countdown(self):
        """
        Countdown at beginning of StimulusPresentation. nCountdown indicates number of seconds
        to countdown. (Ex. if nCountdown=0 then countdown does not occur, if nCountdown=5 then 
        countdown proceeds backwards from 5)
        """
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
        """
        Iterate through sequence list and display each stimulus in order. 
        """
        if self.currentTick == self.stimTime:
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
        """
        Display cue symbol. Vary color depending on feedback if colorCue==True.
        """
        if self.currentTick == self.cueTime:
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
            self.screen.blit(txt, txt_rect)
            pygame.display.update()
            self.currentTick += 1
    
    def predelay(self):
        """
        Delay prior to stimulus presentation. The TTL code for the currentStim is sent via parallel port now
        in order to compensate for communication lag.
        """
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
        """
        Delay after stimulus presentation. The TTL code for the cue is sent via parallel port now
        in order to compensate for communication lag.
        """
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
        """
        Executes upon completion of StimulusPresentation and closes pygame instance. 
        """
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