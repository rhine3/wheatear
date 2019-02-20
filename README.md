# wheatear


To bundle Wheatear for use on a Mac:

- From the top folder of this repository, run `pyinstaller src/wheatear.py`
- This will create a folder `dist/wheatear`
- Within `dist/wheatear`, create a folder of your .wav files called `wavs/`
- Copy the `wavs/` directory into `dist/wheatear`
- Zip up the file

To use the app bundled with the above instructions:

- Unzip `wheatear.zip` and open the unzipped folder. 
- Ignore all the strangely named files. Click on the file called "wheatear" to open the user interface. The interface contains two windows: a graphical interface and a console/terminal. 
- The correct answer will appear in the terminal when a song initially starts; you can either choose to peek at the correct answer (to learn) or you can hide the terminal behind the GUI and quiz yourself.
- Type in the name exactly and press "submit" to guess an answer.

Writing down & committing to a guess, even if your guess is incorrect, has been shown to improve learning.
