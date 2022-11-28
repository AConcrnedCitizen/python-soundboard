import pygame._sdl2.audio as sdl2_audio
import tkinter as tk
import pygame
from tkinter import Tk, ttk, filedialog
import sqlite3
import threading
import keyboard
import os
import shutil
db = "db.db"
device = "VoiceMeeter Input (VB-Audio VoiceMeeter VAIO)"
global song




def get_devices(capture_devices: bool = False) -> tuple([str, ...]):
    init_by_me = not pygame.mixer.get_init()
    if init_by_me:
        pygame.mixer.init()
    devices = tuple(sdl2_audio.get_audio_device_names(capture_devices))
    if init_by_me:
        pygame.mixer.quit()
    return devices

class playsound:
    def __init__(self, file_path: str):
        file_path = file_path
        
        self.file_path = file_path
        # starts the thread to play the sound
        threading.thread = threading.Thread(target=self.play)
        threading.thread.daemon = True
        threading.thread.start()

    def play(self):
        print("Play: {}\r\nDevice: {}".format(self.file_path, device))
        pygame.mixer.init(devicename=device)
        pygame.mixer.music.load(self.file_path)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()

def stopplaying():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print("Stopped")
    

class gui:
    def __init__(self):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM sounds")
        self.sounds = self.cur.fetchall()

        self.root = Tk()
        self.root.title("Soundboard")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c2f33")

        style = ttk.Style(self.root)
        self.root.tk.call('source', 'azure dark.tcl')
        style.theme_use('azure')

        self.soundButtons()
        self.stopButton() # 

        self.root.mainloop()

    def soundButtons(self):
        row = 0
        column = 0
        self.buttonSoundCanvas = tk.Canvas(self.root, width=1000, height=700, bg="#2c2f33")
        self.buttonSoundCanvas.place(x=25, y=0)

        for sound in self.sounds:
            # if sound == self.sounds[45]:
            #     break

            ttk.Button(self.buttonSoundCanvas,text=sound[0],command=lambda sound=sound: playsound(sound[1])).grid(row=row, column=column, padx=5, pady=5, ipadx=10, ipady=25)         

            row += 1
            if row == 5:
                column += 1
                row = 0

        
        ttk.Button(self.buttonSoundCanvas, text="+", command=addSound).grid(row=4, column=column, padx=5, pady=5, ipadx=10, ipady=25)


    def stopButton(self):
        ttk.Button(self.root, text="Stop", command=stopplaying).place(x=100, y=650)

class addSound:
    def __init__(self):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM sounds")
        self.sounds = self.cur.fetchall()

        self.root = tk.Toplevel()
        self.root.title("Add Sound")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c2f33")
        
        style = ttk.Style(self.root)
        style.theme_use('azure')

        # Entry for name, path and hotkey and adds it to the database
        ttk.Label(self.root, text="Name: ").place(x=50, y=100)
        self.nameEntry = ttk.Entry(self.root, width=30)
        self.nameEntry.place(x=100, y=100)

        self.pathtofile = ""

        while self.pathtofile == "":
            self.pathtofile = tk.filedialog.askopenfilename()

        # copys the file to the root directory
        shutil.copy(self.pathtofile, os.path.dirname(os.path.realpath(__file__)))

        ttk.Label(self.root, text="Hotkey: ").place(x=50, y=200)
        self.hotkeyEntry = ttk.Entry(self.root, width=30)
        self.hotkeyEntry.place(x=100, y=200)

        ttk.Button(self.root, text="Add", command=self.addSound).place(x=100, y=250)

        self.root.mainloop()


    def addSound(self):
        name = self.nameEntry.get()
        path = self.pathtofile.split("/")[-1]
        print(path)
        hotkey = self.hotkeyEntry.get()

        # if the name, path or hotkey is empty, it will not add it to the database
        if name == "" or path == "" or hotkey == "":
            print("Please fill in all the fields")
            return

        # if the hotkey, name or path is already in the database, it will not add it to the database
        for sound in self.sounds:
            if name == sound[0] or path == sound[1]:
                print("Name, path or hotkey already exists")
                return

        self.cur.execute("INSERT INTO sounds VALUES (?, ?)", (name, path))
        self.con.commit()
        id = self.cur.lastrowid
        self.cur.execute("INSERT INTO shortcuts VALUES (?, ?)", (hotkey, id))
        self.con.commit()
        self.root.destroy()

class shortcuts():
    def __init__(self):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.shortcuts = self.cur.execute("SELECT * FROM shortcuts").fetchall()
        self.start()

    def start(self):
        for shortcut in self.shortcuts:
            shortcut = list(shortcut)
            print(shortcut)
            self.cur.execute("SELECT path FROM sounds WHERE rowid = ?", str(shortcut[1]))
            sound = self.cur.fetchone()
            print("Shortcut: {} | Sound: {}".format(shortcut[0], sound[0]))
            keyboard.add_hotkey("print screen+" + shortcut[0], playsound, args=(sound[0],))

        keyboard.add_hotkey("esc", stopplaying)

threading.shortcut = threading.Thread(target=shortcuts)
threading.shortcut.daemon = True
threading.shortcut.start()

gui()