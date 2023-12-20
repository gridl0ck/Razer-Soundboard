import os, threading, sys

from playsound import playsound
from tkinter import *
from tkinter.filedialog import askopenfilename
from pynput.keyboard import Listener
from functools import partial

# Global Variables
## Variables housing the sounds.
## TODO Change this to a dictionary

## Main window variable
window = Tk()

kb = None

## Sound Dictionary
## This dictionary maps the numpad 0-9 to their respective sounds based on their virtual key values.
sounds = {
    96:  None,
    97:  None,
    98:  None,
    99:  None,
    100: None,
    101: None,
    102: None,
    103: None,
    104: None,
    105: None
}

sound_keys = {
    "snd0" : 96,
    "snd1" : 97,
    "snd2" : 98,
    "snd3" : 99,
    "snd4" : 100,
    "snd5" : 101,
    "snd6" : 102,
    "snd7" : 103,
    "snd8" : 104,
    "snd9" : 105,
}

labels = {}
buttons = {}

# Function Definitions
## save_sounds saves all the sound locations to the disk in a txt file (saved_so they can be referenced
## at next launch if theyre configured.
def save_sounds():
    pass

## load_sounds looks for the saved_sounds.txt file and loads those paths into their respective variables.
def load_sounds():
    pass

## Plays the sound associatec with the key pressed.
## Launching the playsound function in a thread allows the sounds to be played immediately, and doesnt block the program.
def play_sound(key):
    global kb, window
    if not hasattr(key, 'vk'):
        pass

    else:
        if (96 <= key.vk <= 105) or key.vk == 110:
            if key.vk == 110:
                kb.stop()
                window.destroy()
            else:
                try:
                    sound = sounds[key.vk]
                    if sound:
                        threading.Thread(target=playsound, args=([sound]), daemon=True).start() #playsound(first_sound, False)
                except Exception as e:
                    pass

## Listener default keypress action
def key_press(key):
    play_sound(key)

## Listener default key-depress action
def key_release(key):
    pass

def err_popup(err_type, message):
    top = Toplevel(window)
    top.geometry("350x200")
    top.title(f"Error: {err_type}")
    Label(top, text=f"{err_type}: {message}").grid(column=0, row=0)
    top.wait_window()

## Allows the user to specify a sound file to play and associate it with a button
def clicked(btn, label):
    global sounds
    valid_file_extentions = ["pcm", "wav", "mp3", "aac", "ogg", "wma", "flac", "alac"]

    fileSelected = False
    fn = None
    while not fileSelected:
        fn = askopenfilename()
        print(fn)
        extension = fn.split(".")[-1].lower()

        if extension not in valid_file_extentions:
            err_popup("Invalid File Type", "Please select a standard audio file!")
        else:
            fileSelected = True
    sounds[sound_keys[f"snd{btn}"]] = fn
    label.configure(text=f"Current Sound for Key {btn}: {fn}")

## Sets up the gui to be able to configure and view the current sounds
def setup_window():
    global labels, buttons

    window.title("Numpad Soundboard")
    window.geometry('800x600')
    setup_labels()
    setup_buttons()


## Sets up the labels for each of the sounds
def setup_labels():
    global window, labels

    for i in range(0, 10):
        labels[f"lbl{i}"] = Label(window, text=f"Current Sound for key {i}: {sounds[i+96]}")
        labels[f"lbl{i}"].grid(column=0, row=i)




def setup_buttons():
    global window, buttons, labels
    for i in range(0,10):
        buttons[f"btn{i}"] = Button(window, text="Select File", fg="red", command=partial(clicked, i, labels[f"lbl{i}"]))
        buttons[f"btn{i}"].grid(column=1, row=i)

def main():
    global kb, window

    # Starts the listener before the GUI is initialized because if the the window main-loop is a blocking function
    kb = Listener(on_press=key_press, on_release=key_release)
    kb.start()

    setup_window()
    window.mainloop()

main()