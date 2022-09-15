#import tkinter as tk
from tkinter import *
import time
import random
import threading


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        #self.root = Tk()
        #self.root.title("Typing speed app")
        #self.root.geometry("1280x720")

        #self.root.rowconfigure(0, weight=1)
        #self.root.columnconfigure(0, weight=1)

        #self.frame1 = Frame(self.root, bg="red")
        #self.frame2 = Frame(self.frame1, bg="green")
        #self.frame3 = Frame(self.root, bg="blue")

        #self.text = open("paragraphs.txt", "r").read().split("BREAK")
        
        #self.sample_label = Label(self.frame1, text=random.choice(self.text))
        #self.sample_label.place(x=100, y=200)
        #self.sample_label.grid(row=2, column=0)
        
        
        def test2():
            print('Ahoj')
            self.frame4 = Frame(self.root, bg="green")
            self.frame2.pack(fill="both", expand=True)
            

        #self.butt1 = Button(self.frame1, text='Test', command=test2)
        #self.butt1.place(x=600,y=550)
        #self.butt1.grid()

        #self.frame1.pack(fill="both", expand=True)

        self._frame = None
        self.switch_frame(StartPage)
        
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    

class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        #self..title("Typing speed app")
        self.geometry("1280x720")
        Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        Button(self, text="Open page one", command=lambda: master.switch_frame(PageOne)).pack()
        Button(self, text="Open page two", command=lambda: master.switch_frame(PageTwo)).pack()

class PageOne(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        Button(self, text="Return to start page", command=lambda: master.switch_frame(StartPage)).pack()

        self.text = open("paragraphs.txt", "r").read().split("BREAK")
        
        self.sample_label = Label(self, text=random.choice(self.text))
        self.sample_label.place(x=100, y=200)

class PageTwo(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        Button(self, text="Return to start page", command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()



#TODO 1) Menu with two typing mods: 1. basic test 2. training mod similiar to keybr.com
#TODO 2) Collect data from both mods and save it to .txt file, than make statistics from said data