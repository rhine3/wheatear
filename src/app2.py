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

# Playing wav audio
import simpleaudio as sa

### Classes ###
class Application:
    def __init__(self, master=None, directory=None):
        self.master = master
        self.data_dir = directory
        
        #file positions
        self.files = listdir(directory)
        self.idx = 0
        self.scores = []
        
        #drawing things
        self.canvas = None
        self.ax = None
        
        # Create a self.frame with buttons
        self.frame = Tk.Frame()
        self.init_buttons()

    def init_buttons(self):
        self.startbutton = Tk.Button(self.frame, text="Start!", command=self.start)
        self.startbutton.pack(side="left")
        
        self.quitbutton = Tk.Button(self.frame, text="Quit", command=self.frame.quit)
        self.quitbutton.pack(side="right")
        
        print("HEY")
        self.frame.pack()
    
    def start(self):
        # erase start button
        self.startbutton.destroy()
        
        self.field = Tk.Entry(self.frame, text="Who??")
        self.field.pack(side="left")
        
        self.submitbutton = Tk.Button(self.frame, text="Submit", command=self.submit)
        self.submitbutton.pack(side="left")
        self.frame.pack()

        self.listen()
        return
    
    def submit(self):
        '''After the submit button is pressed, stop the song if necessary, 
        show result and allow user to move to next song'''
        
        self.submitbutton.destroy()
        self.play_obj.stop()
        
        # Handle and clear entry field input
        print(self.field.get())
        self.field.delete(0, 'end')
        
        # Create nextbutton
        self.nextbutton = Tk.Button(self.frame, text="Next", command=self.next)
        self.nextbutton.pack()
        
        self.frame.pack()
    
        
    def shuffle_filenames(self):
        #get filenames
        self.files = []
        # shuffle filenames

    def listen(self):
        # play self.files[self.idx]
        #assert it's an mp3 file
        filename = join(self.data_dir, self.files[self.idx])
        wave_obj = sa.WaveObject.from_wave_file(filename)
        self.play_obj = wave_obj.play()
    
    def next(self):
        self.nextbutton.destroy()
        
        # If index is longer than number of files, reshuffle files and start over
        if self.idx >= len(self.files):
            self.idx = 0
            self.shuffle_filenames()

        # Play the song
        self.listen()
        self.submitbutton = Tk.Button(self.frame, text="Submit", command=self.submit)
        self.submitbutton.pack(side="left")
        
        self.frame.pack()
    



### Scripts ###   
def main():
    root = Tk.Tk() # root window
    root.wm_title("Wheatear Song Quizzer")
    root.geometry("300x200+500+200") # dimensions & position
    
    directory = join(dirname(dirname(abspath(__file__))), "data")
    print(directory)
    appy = Application(root, directory)
    root.mainloop()
    
    
main()