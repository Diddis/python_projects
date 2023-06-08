# -*- coding: utf-8 -*-

"""
# This is a trivia game called "Non-linear history". It will test your knowledge
# of the people behind your most loved statistical concepts. Click on a point in 
# the figure to answer a question. When you answer a question correctly, a point
# on the figure will turn a different color. When you answer incorrectly, the point
# will move away from the line and threaten your linearity. Your final score will 
# reflect how correlated your final points are.

# pip install Pillow
# pip install pygame

"""

from tkinter import *
import PIL.Image
from PIL import ImageTk
import sys, os
import pygame


class NonLinearTrivia:
    '''The trivia game.'''
    
    def __init__(self):
        '''Return a Non Linear Trivia game object.'''

        self._initializeVariables()
        self._initializeGUI()
        self._initializeData()
        self._initializeMusic() 
        self._initializeFrames()
    
    
    def start(self):
        '''Start the game by opening the display window.'''

        print("Start")
        self._musicOn()
        self._drawIntroWindow()
        self._display.mainloop()


    def _initializeVariables(self):
        '''Set score, key to questions and answers dictionaries, and game colors.'''

        self._score = 0
        self._questions = { 0:True, 1:True, 2:True, 3:True, 4:True, 5:True }
        self._answers =   { 0:True, 1:True, 2:True, 3:True, 4:True, 5:True }
        
        self._colors = {
            "dk_yellow": "#ecba14",
            "md_green":  "#33a02c",
            "lt_teal":   "#277575",
            "white":     "#ffffff",
            "lt_gray":   "#1a1a1a"
        }


    def _initializeGUI(self):
        '''Create the root object.'''
    
        self._root = Tk()
        self._root.title("Non-Linear History")
        self._root.resizable(0,0)	
        self._root.geometry("900x605")
        self._root.protocol("WM_DELETE_WINDOW", self.__exit__)
        self._display = Canvas(self._root)

    
    def _initializeData(self):
        '''Open the questions and answers.'''
        
        try:
            self._openQAfile = open("Questions.dta")
            self._QAfile = self._openQAfile.readlines()
            self._openQAfile.close()
        except:
            print("Sorry, there was a problem opening the questions.")
            self.__exit__()
    
    
    def _initializeFrames(self):
        '''Declare the four frames that hold the intro, instructions, game board, and final score.'''
        
        self._introFrame = Frame(self._root, bg=self._colors["white"])
        self._instructionsFrame = Frame(self._root, bg=self._colors["white"])
        self._boardFrame = Frame(self._root, bg=self._colors["white"])
        self._questionFrame = Frame(self._root, bg=self._colors["white"])


    def _initializeMusic(self):
        '''Play music with pygame mixer when game opens.
        Except: the program continues even if the music does not start.'''
        
        self._music = None
        
        try:
            # Initialize pygame and define the values for frequency, size, 
            # channels and buffer size. 
            pygame.mixer.pre_init(44100, 16, 2, 4096)
            pygame.init()
            self._music = pygame.mixer.Sound("tune.wav")
        except:
            pass

    
    def _musicOn(self):
        '''Turn on music and play indefinitely.'''

        self._music.play(loops=-1)
        

    def _musicOff(self):
        '''Stop the music and shut down pygame mixer.'''
        
        self._music.stop()
        pygame.mixer.quit
        

    def _drawButton(self, canvas, buttonText, buttonCommand):
        '''Template for buttons.'''
        
        return Button(canvas, text=buttonText, font=("candara", 18, "bold"), 
                      width=15, bg=self._colors["dk_yellow"], fg=self._colors["white"], 
                      command=buttonCommand)
    

    def _drawIntroWindow(self):
        '''Draw intro canvas. Place in _introFrame.'''
        
        self._introFrame.grid(row=0, column=0, sticky=N+E+W+S)
        self._introCanvas = Canvas(self._introFrame, bg=self._colors["white"])   
        self._introCanvas.grid(sticky=N+S+E+W, padx=15, pady=15)

        # Text label for the name of the game.
        self._introTitle = StringVar()
        self._introTitle.set("NON-LINEAR HISTORY")
        self._titleLabel = Label(self._introCanvas, textvariable=self._introTitle, 
                                 bg=self._colors["white"], fg=self._colors["dk_yellow"], 
                                 font=("candara", 45, "bold"))
        self._titleLabel.grid(row=0, column=0, pady=55)
    
    
        self._playButton = self._drawButton(self._introCanvas, "PLAY", self._drawGameBoard)
        self._playButton.grid(row=1, column=0, padx=30, pady=140, sticky=S) 
        
        self._playButton = self._drawButton(self._introCanvas, "INSTRUCTIONS", self._drawInstructionWindow)
        self._playButton.grid(row=1, column=0, padx=30, pady=85, sticky=S) 
        
        self._playButton = self._drawButton(self._introCanvas, "EXIT", self.__exit__)
        self._playButton.grid(row=1, column=0, padx=30, pady=30, sticky=S)         

        

    def _drawInstructionWindow(self):
        '''Draw the instruction window. Place in _instructionsFrame.'''
    
        self._instFrame = Toplevel(self._instructionsFrame, bg=self._colors["white"])
        self._instFrame.geometry("900x605")
        
        # Create a text label for title.
        self._instrLabel = StringVar()
        self._instrLabel.set("INSTRUCTIONS")
        self._titleLabel = Label(self._instFrame, textvariable=self._instrLabel, 
                           bg=self._colors["white"], fg=self._colors["dk_yellow"], font=("candara", 25, "bold"))
        self._titleLabel.grid(row=0, column=0, pady=45)    
         
        # Define the instructions text. 
        self._text = ("Test your knowledge on the history of your favorite statistical concepts. To read a "
        "question, click on a point on the linear graph. If you answer correctly, the point on the line "
        "will turn yellow. If you answer incorrectly, the point will be moved away from the line and "
        "threaten your linearity. A score of 1.00 is perfect while 0.00 means you guessed incorrectly "
        "every time. Good luck!")
        
        # Create a message widget to hold the instructions text.
        self._insText = StringVar()
        self._insText.set(self._text)
        self._textLabel = Message(self._instFrame, font=("bodoni mt", 15), width=775, 
                                 bg=self._colors["white"], fg=self._colors["lt_gray"], 
                                 textvariable=self._insText)
        self._textLabel.grid(row=1, column=0, pady=0, padx=30, sticky=E+W)  

        self._playButton = self._drawButton(self._instFrame, "BACK TO HOME", 
                                            self._instFrame.destroy)
        self._playButton.grid(row=2, column=0, padx=30, pady=15, sticky=S)          
    
    
    def _drawGameBoard(self):
        '''Draw the gameboard. Place in _boardFrame.'''
        
        def fillcolor(number):
            ''' Assign rules for coloring the dots on the game board. '''
            
            if self._answers[number]==False & self._questions[number]==False:
                return self._colors["lt_gray"]
            elif self._answers[number]==True & self._questions[number]==True:
                return self._colors["dk_yellow"]
            else:
                return self._colors["white"]
            
                
        self._boFrame = Toplevel(self._boardFrame, bg=self._colors["white"])
        self._boFrame.geometry("900x605")
        
        # Draw board.
        self._boardCanvas = Canvas(self._boFrame, bg=self._colors["white"], width=700, height=550)   
        self._boardCanvas.grid(row=0, column=0)
        
        self._boardCanvas.create_line(100, 450, 625, 450, fill=self._colors["lt_gray"], width=7)
        self._boardCanvas.create_line(100, 50, 100, 450, fill=self._colors["lt_gray"], width=7)
        
        self._boardCanvas.create_oval((135, 365, 195, 425) if self._answers[0] else (135, 335, 195, 395), 
                                      outline=self._colors["lt_teal"], fill=fillcolor(0), width=5, tags="oval0")
        self._boardCanvas.create_oval((210, 320, 270, 380) if self._answers[1] else (210, 220, 270, 280), 
                                      outline=self._colors["lt_teal"], fill=fillcolor(1), width=5, tags="oval1")
        self._boardCanvas.create_oval((285, 275, 345, 335) if self._answers[2] else (285, 375, 345, 435), 
                                      outline=self._colors["lt_teal"], fill=fillcolor(2), width=5, tags="oval2")
        self._boardCanvas.create_oval((360, 230, 420, 290) if self._answers[3] else (360, 180, 420, 240), 
                                      outline=self._colors["lt_teal"], fill=fillcolor(3), width=5, tags="oval3")
        self._boardCanvas.create_oval((435, 185, 495, 245) if self._answers[4] else (435, 215, 495, 275), 
                                      outline=self._colors["lt_teal"], fill=fillcolor(4), width=5, tags="oval4")
        self._boardCanvas.create_oval((510, 140, 570, 200) if self._answers[5] else (510, 40, 570, 100), 
                                      outline=self._colors["lt_teal"], fill=fillcolor(5), width=5, tags="oval5")
        
        self._boardCanvas.tag_bind("oval0", "<Button-1>", lambda x: [self._askQuestion(0), self._boFrame.destroy()])
        self._boardCanvas.tag_bind("oval1", "<Button-1>", lambda x: [self._askQuestion(1), self._boFrame.destroy()])
        self._boardCanvas.tag_bind("oval2", "<Button-1>", lambda x: [self._askQuestion(2), self._boFrame.destroy()])
        self._boardCanvas.tag_bind("oval3", "<Button-1>", lambda x: [self._askQuestion(3), self._boFrame.destroy()])
        self._boardCanvas.tag_bind("oval4", "<Button-1>", lambda x: [self._askQuestion(4), self._boFrame.destroy()])
        self._boardCanvas.tag_bind("oval5", "<Button-1>", lambda x: [self._askQuestion(5), self._boFrame.destroy()])
        
        
        if all(value == False for value in self._questions.values()):  
            self._scoreLabel = StringVar()
            self._scoreLabel.set("SCORE " + str(self._score))
            self._titleLabel = Label(self._boFrame, textvariable=self._scoreLabel, 
                               bg=self._colors["white"], fg=self._colors["lt_teal"], font=("candara", 45, "bold"))
            self._titleLabel.grid(row=0, column=0, padx=135, pady=10, sticky=N+W) 
            
            self._playButton = self._drawButton(self._boFrame, "EXIT", self.__exit__)
            self._playButton.grid(row=0, column=0, padx=30, pady=5, sticky=S)  
        
                    
        
    def _drawQuestion(self, questionID):
        '''Show the questions.'''
        
        offset = 5 * questionID
        questionAnswer = int(self._QAfile[offset+4])
        
        self._questFrame = Toplevel(self._questionFrame, bg=self._colors["md_green"])
        self._questFrame.geometry("900x605")
        
        
        Message(self._questFrame, font=("bodoni mt", 16), width=450, bg=self._colors["lt_gray"], 
                fg=self._colors["md_green"], text=self._QAfile[offset][1:]).grid(row=0, column=0, padx=100, pady=35, sticky=N+E+W)
        
        Button(self._questFrame, text=self._QAfile[offset+1][3:], font=("bodoni mt", 16, "bold"), 
               width=40, height=1, anchor="n", bg=self._colors["dk_yellow"], fg=self._colors["md_green"], 
               command=lambda: [self._updateScore(questionAnswer, 0, questionID), self._questFrame.destroy()]).grid(row=1, column=0, padx=100, pady= 3, sticky=S+W)
        Button(self._questFrame, text=self._QAfile[offset+2][3:], font=("bodoni mt", 16, "bold"), 
               width=40, height=1, anchor="n", bg=self._colors["dk_yellow"], fg=self._colors["md_green"], 
               command=lambda: [self._updateScore(questionAnswer, 1, questionID), self._questFrame.destroy()]).grid(row=2, column=0, padx=100, pady= 3, sticky=S+W)
        Button(self._questFrame, text=self._QAfile[offset+3][3:], font=("bodoni mt", 16, "bold"), 
               width=40, height=1, anchor="n", bg=self._colors["dk_yellow"], fg=self._colors["md_green"], 
               command=lambda: [self._updateScore(questionAnswer, 2, questionID), self._questFrame.destroy()]).grid(row=3, column=0, padx=100, pady= 3, sticky=S+W)
               
            
            
    def _askQuestion(self, questionID):
        '''Ask the questions.'''
        
        if self._questions[questionID]: 
            self._questions[questionID] = False
        
        self._drawQuestion(questionID)
               
    

    def _updateScore(self, questionAnswer, playerAnswer, questionID):
        '''Update the score.'''
        
        if questionAnswer == playerAnswer:
            self._score += 1
            self._answers[questionID] = True
        else:
            self._answers[questionID] = False
                        
        self._drawGameBoard()
        
    
    def __exit__(self):
        '''Exit the game by calling shutdownMusic method and closing the tkinter window.'''

        print("Exiting")
        self._musicOff()
        pygame.mixer.quit
        self._root.destroy()




def main():
    '''Create an instance of the trivia game and call its start method. When
    done, delete the game.'''
    
    game = NonLinearTrivia()
    game.start()
    del game


if __name__ == "__main__": main()