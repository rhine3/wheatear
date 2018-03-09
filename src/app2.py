'''
application.py
by Tessa Rhinehart

A Python3 GUI for inspecting spectrograms
'''

import matplotlib
matplotlib.use('TkAgg')

### Imports ###
# GUI: TkInterface
import tkinter as Tk
import tkinter.filedialog as fd

# Plotting MPL figures with tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

# Default mpl key bindings
from matplotlib.backend_bases import key_press_handler

# Own utils for creating and saving spectrograms and saving wave files
from spectrogram_utils import make_spectrogram, save_spectrogram

# File inspection
from os import listdir
from os.path import splitext, dirname, abspath, join

# Shuffle
from numpy.random import shuffle

# Playing wav audio
import simpleaudio as sa

### Classes ###
class Application:
    def __init__(self, master=None, directory=None):
        self.master = master
        self.data_dir = directory
        
        # For incrementing through files
        self.files = listdir(directory)
        self.shuffle_filenames()
        self.idx = 0
        self.scores = []
        
        #drawing things
        self.canvas = None
        self.ax = None
        
        # Create a self.frame with buttons
        self.init_grid()

    def init_grid(self):

        # So that everything will be centered in window
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(4, weight=1)

        self.welcome = Tk.Label(self.master, text="Go Wheatears!")
        self.welcome.grid(column=1, columnspan=3)

        self.startbutton = Tk.Button(self.master, text="Start!", command=self.start)
        self.startbutton.grid(row=2, column=2)
        
        self.quitbutton = Tk.Button(self.master, text="Quit", width=6, command=self.master.quit)
        self.quitbutton.grid(row=2, column=3)
 
        self.result = Tk.Label(self.master, text="")
        self.result.grid(row=3, column=1, columnspan=3, sticky='W')       

        self.answer = Tk.Label(self.master, text="")
        self.answer.grid(row=4, column=1, columnspan=3, sticky='W')
        
        self.response = Tk.Label(self.master, text="")
        self.response.grid(row=5, column=1, columnspan=3, sticky='W')

    def start(self):
        # Change "start" button to "submit" button
        self.startbutton.destroy()
        self.make_submitbutton()
        
        # Add entry field
        self.field = Tk.Entry(self.master, width=20)
        self.field.grid(row=2, column=1)
                
        self.listen()
    
    def make_submitbutton(self):
        self.submitbutton = Tk.Button(self.master, text="Submit", command=self.submit, width=6)
        self.submitbutton.grid(row=2, column=2)    

    def make_nextbutton(self):
        self.nextbutton = Tk.Button(self.master, text="Next", command=self.next, width=6)
        self.nextbutton.grid(row=2, column=2)
    
    def submit(self):
        '''After the submit button is pressed, stop the song if necessary, 
        show result and allow user to move to next song'''
        
        # Change "submit" button to "next" button
        self.submitbutton.destroy()
        self.make_nextbutton()

        # Compare entry field input & correct answer
        if not self.compare():
            self.result['text'] = 'Incorrect.'
            self.answer['text'] = 'Correct answer: ' + self.species
            self.response['text'] = 'Your answer: ' + self.field.get()
        else:
            self.result['text'] = 'Correct!'
            self.answer['text'] = 'Correct answer: ' + self.species
        self.field.delete(0, 'end')

    def shuffle_filenames(self):
        shuffle(self.files)

    def listen(self):
        # play self.files[self.idx]
        # WANTED: assert it's a wav file
        self.species = self.files[self.idx].split('(')[0]
        print(self.species)

        filename = join(self.data_dir, self.files[self.idx])
        wave_obj = sa.WaveObject.from_wave_file(filename)

        self.play_obj = wave_obj.play()
        
    def next(self):
        # Replace "next" button with "submit" button
        self.nextbutton.destroy()
        self.make_submitbutton()

        # Refresh response text
        self.result['text'] = ''
        self.answer['text'] = ''        
        self.response['text'] = ''
        
        # If next index is longer than number of files, reshuffle files and start over
        self.idx += 1
        if self.idx >= len(self.files):
            self.idx = 0
            self.shuffle_filenames()

        # Stop the previous song and play the new song
        if self.play_obj.is_playing():
            self.play_obj.stop()
        self.listen()

    def strip(self, stringy):
        return ''.join(e for e in stringy if e.isalnum()).upper()

    def compare(self):
        response = self.strip(self.field.get())
        species = self.strip(self.species)

        if response == species:
            return True
        return False


### Scripts ###   
def main():
    root = Tk.Tk() # root window
    root.wm_title("Wheatear Song Quizzer")
    root.geometry("400x150+500+200") # dimensions & position
    
    directory = join(dirname(dirname(abspath(__file__))), "wavs")
    print(directory)
    appy = Application(root, directory)
    root.mainloop()
    
    
main()
