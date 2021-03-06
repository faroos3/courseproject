
# this is where i will add and test the basic gui
try:
    # for Python2
    from Tkinter import *
    import Tkinter as tk
    from DiffWord import *  # added by Samad
    import time
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter as tk
    import time
# speech api
import speech_recognition as sr
from oauth2client.client import GoogleCredentials
from diffCheck import *


textFont1 = ("Courier New", 16, "normal")
sec = 0
# These are classes for each step in the QuoteR program

# general page class


class Page(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

    def show(self):
        self.lift()
    def drop(self):
        self.lower()

# This page will just be a welcome slide that
# outputs text and directs the user to the next page.


class WelcomePage(Page):
    def __init__(self, master):
        Page.__init__(self, master)
        # welcome label
        label = tk.Label(self, text="Welcome to QuoteR")
        # set font
        label.config(font=("Courier", 44))
        # formating
        label.pack(side="top", fill="both", expand=True)
        # label.configure(background='navajo white')

# this page has a text box where the user can input the correct version of the
# input in text format


class InputPage(Page):
    def __init__(self, master, fnout):
        Page.__init__(self, master)
        # text label and formatting
        label = tk.Label(self, text="Enter your text")
        label.config(font=("Courier", 44))
        label.grid(row=0, column=0, sticky="ns")
        # label.configure(background='white')

        # using .grid over pack for a more structured ui
        self.fnout = fnout
        self.mainFrame = tk.Frame(self)

        top = self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        self.mainFrame.grid(row=1, column=0, sticky="nsew")
        self.exit = tk.Button(self.mainFrame,
                              text="Save your text",
                              command=self.finish)
        self.exit.grid(row=4, column=0, sticky="ns")
        self.exit.config(font=("Courier", 16))

        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)

        vscrollbar = ScrollbarX(self.mainFrame)
        vscrollbar.grid(row=1, column=1, sticky="ns")
        hscrollbar = ScrollbarX(self.mainFrame, orient=tk.HORIZONTAL)
        hscrollbar.grid(row=2, column=0, sticky="ew")
        hscrollbar.grid(row=2, column=0, padx=(100, 0))

        self.textWidget = tk.Text(self.mainFrame,
                                  yscrollcommand=vscrollbar.set,
                                  xscrollcommand=hscrollbar.set,
                                  wrap=tk.NONE,
                                  height=24,
                                  width=84,
                                  font=textFont1)

        self.textWidget.grid(row=1, column=0, sticky="nsew")
        self.textWidget.grid(row=1, column=0, padx=(100, 0))

        hscrollbar["command"] = self.textWidget.xview
        vscrollbar["command"] = self.textWidget.yview

    def finish(self):
        fout = open(self.fnout, 'w')
        fout.write(self.textWidget.get("1.0", "end"))
        fout.close()


# this page will be where you begin your reciting
# and where the audio input will be
# entered into the file.
class ReadyPage(Page):
    def __init__(self, master):
        Page.__init__(self, master)

        def speechAPI():
            # self.drop()
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)

            # This is an alternative to goolge if we want, but it's also a
            # requirment for the google api
            """
            try:
                print("Sphinx thinks you said " + r.recognize_sphinx(audio))
            except sr.UnknownValueError:
                print("Sphinx could not understand audio")
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))
            """

            # recognize speech using Google Speech Recognition
            try:
                # right now , we are using the default API key
                # r.recognize_google
                # (audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")
                # will get a different one
                # instead of `r.recognize_google(audio)`
                print(
                    "Google Speech Recognition thinks you said " +
                    r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(
                    "Could not request results from Google Speech " +
                    " Recognition service; {0}".format(e))

            file2 = open("audioInput.txt", "w")
            try:
                file2.write(r.recognize_google(audio))
            except sr.UnknownValueError:
                file2.write(
                    "Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                file2.write(
                    "Could not request results from Google Speech" +
                    "Recognition service; {0}".format(e))

            file2.close()

        label = tk.Label(
            self, text="Ready?\n Click the button below to start reciting")
        label.config(font=("Courier", 32))
        label.grid(row=0, column=0, sticky="ns")

        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=1, column=0, sticky="nsew")

        top = self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        self.start = tk.Button(self.mainFrame, command=speechAPI, text="Start")
        self.start.config(font=("Courier", 16))
        self.start.grid(row=2, column=2, sticky="se")\
            # self.start.place(relx=0.5, rely=0.5, anchor=CENTER)

        # self.done = tk.Button(self.mainFrame,text="Done")
        # self.done.grid(row=3, column=4, sticky="ns")
        # self.done.config(font=("Courier", 16))
        # self.done.place(relx=.5, rely=.5, anchor=CENTER)

# we might time how long it takes for the speach to take place


class TimerPage(Page):
    def __init__(self, master):
        Page.__init__(self, master)
        label = tk.Label(self, text="Stay silent for 5 seconds\n when finished reciting on next page")
        label.config(font=("Courier", 32))
        label.pack(side="top", fill="both", expand=True)

# here both the output and the input text will be compared and differences
# will be highlighted


class ComparisonPage(Page):
    def __init__(self, master):

        def loadInputText():
            file = open("input.txt")
            i = 0
            f1_words = get_words(file)

            for word in f1_words:
                i += 1
                if(i % 7 == 0):
                    self.textWidget.insert(END, str(word) + " \n")
                else:
                    self.textWidget.insert(END, str(word) + " ")

            file.close()

        def loadAudioText():
            file1 = open("input.txt")
            file2 = open("audioInput.txt")
            f1_words = get_words(file1)
            f2_words = get_words(file2)
            num_f1_words = len(f1_words)
            num_f2_words = len(f2_words)

            diffWords = get_DiffWords(f1_words, f2_words)
            i = 0
            j = 0
            for word in diffWords:
                if((num_f2_words == num_f1_words or num_f2_words > num_f1_words) and word.get_pos_in_derived() == -1):
                    continue
                if(num_f1_words > num_f2_words and word.get_pos_in_original() == -1):
                    continue
                else:
                    i += 1
                    if (word.isDiff()):
                        j += 1
                        # if(j%2 == 0):
                        if(i % 7 == 0):
                            self.textWidget2.tag_configure(
                                'color', foreground='red')
                            self.textWidget2.insert(
                                END, str(word) + " \n", 'color')
                        else:
                            self.textWidget2.tag_configure(
                                'color', foreground='red')
                            self.textWidget2.insert(
                                END, str(word) + " ", 'color')
                    else:
                        if(i % 7 == 0):
                            self.textWidget2.insert(END, str(word) + " \n")
                        else:
                            self.textWidget2.insert(END, str(word) + " ")

            # for line2 in file2:
            # self.textWidget2.insert(END,line2)

            file1.close()
            file2.close()

        Page.__init__(self, master)
        self.fnout = "input.txt"
        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=1, column=0, sticky="nsew")

        top = self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        # label = tk.Label(self, text="Your Text")
        # label.config(font=("Courier", 22))
        # label.grid(row=0, column=0)
        # label2 = tk.Label(self, text="Your Audio Input")
        # label2.config(font=("Courier", 22))
        # label2.grid(row=0, column=1)

        self.exit = tk.Button(self.mainFrame, command=loadInputText,
                              text="Load Input Text"
                              )
        self.exit.grid(row=4, column=0, sticky="ns")
        self.exit.config(font=("Courier", 16))

        self.exit2 = tk.Button(self.mainFrame, command=loadAudioText,
                               text="Load Audio Text"
                               )
        self.exit2.grid(row=4, column=1, sticky="ns")
        self.exit2.config(font=("Courier", 16))

        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)

        vscrollbar = ScrollbarX(self.mainFrame)
        vscrollbar.grid(row=1, column=1, sticky="ns")
        hscrollbar = ScrollbarX(self.mainFrame, orient=tk.HORIZONTAL)
        hscrollbar.grid(row=2, column=0, sticky="ew")
        hscrollbar.grid(row=2, column=0, padx=(100, 0))

        self.textWidget = tk.Text(self.mainFrame,
                                  yscrollcommand=vscrollbar.set,
                                  xscrollcommand=hscrollbar.set,
                                  wrap=tk.NONE,
                                  height=24,
                                  width=44,
                                  font=textFont1)

        self.textWidget.grid(row=1, column=0, sticky="nsew")
        self.textWidget.grid(row=1, column=0, padx=(100, 0))

        vscrollbar2 = ScrollbarX(self.mainFrame)
        vscrollbar2.grid(row=1, column=3, sticky="ns")
        hscrollbar2 = ScrollbarX(self.mainFrame, orient=tk.HORIZONTAL)
        hscrollbar2.grid(row=2, column=1, sticky="ew")
        hscrollbar2.grid(row=2, column=1, padx=(100, 0))

        self.textWidget2 = tk.Text(self.mainFrame,
                                   yscrollcommand=vscrollbar2.set,
                                   xscrollcommand=hscrollbar2.set,
                                   wrap=tk.NONE,
                                   height=24,
                                   width=44,
                                   font=textFont1)

        self.textWidget2.grid(row=1, column=1, sticky="nsew")
        self.textWidget2.grid(row=1, column=1, padx=(100, 0))

        hscrollbar["command"] = self.textWidget.xview
        vscrollbar["command"] = self.textWidget.yview
        hscrollbar2["command"] = self.textWidget2.xview
        vscrollbar2["command"] = self.textWidget2.yview

        # idea for the future
        # make a command on each button that loads the input for each
        # file
        # ie it only inserts the stuff once you click the button
        # so it gets an updated  version of each file

# scrollbar class


class ScrollbarX(tk.Scrollbar):
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        tk.Scrollbar.set(self, low, high)

# general class where all layers are palaced and buttons implemented


class MyFirstGUI(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.centerWindow()
        tk.Frame.__init__(self, master)
        # make pages
        p0 = WelcomePage(self)
        p1 = InputPage(self, inText)
        p2 = TimerPage(self)
        p3 = ReadyPage(self)
        p5 = ComparisonPage(self)

        # make button frames
        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        container.configure(background='black')

        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        # place all the pages in the program
        p0.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        

        # place all the buttons
        b0 = tk.Button(buttonframe, text="Welcome", command=p0.lift)
        b1 = tk.Button(buttonframe, text="Input", command=p1.lift)
        b3 = tk.Button(buttonframe, text="Ready", command=p3.lift)
        b2 = tk.Button(buttonframe, text="Instruct", command=p2.lift)
        b5 = tk.Button(buttonframe, text="Comparison", command=p5.lift)

        b0.pack(side="left")
        # b0.configure(background='blue')
        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b5.pack(side="left")

        # show welcome page that will link to others
        p0.show()

        master.title("QuoteR")

# centers the window based on 1280 x 720 size, might change based on
# users screen later
    def centerWindow(self):

        w = 1400
        h = 800

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2

        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))


# initialization and running
inText = "input.txt"
audioText = "audioInput.txt"
root = tk.Tk()
my_gui = MyFirstGUI(root)
root.tk_setPalette(background='navajo white', foreground='black',
                   activeBackground='black', activeForeground='white')
my_gui.pack(side="top", fill="both", expand=True)

# root.wm_geometry("1024x768")
root.mainloop()
