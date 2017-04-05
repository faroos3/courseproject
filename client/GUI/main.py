
## this is where i will add and test the basic gui
try:
    # for Python2
    from Tkinter import *
    import Tkinter as tk
    import time
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter as tk
    import time
 
textFont1 = ("Courier New", 16, "normal")
sec = 0
##These are classes for each step in the QuoteR program

##general page class    
class Page(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self,master)
    def show(self):
        self.lift()
        
class WelcomePage(Page):
    def __init__(self, master):
        Page.__init__(self, master)
        label = tk.Label(self, text="Welcome to QuoteR")
        label.config(font=("Courier", 44))
        label.pack(side="top", fill="both", expand=True)
        
class InputPage(Page): 
    def __init__(self, master,fnout):
        Page.__init__(self, master)
        label = tk.Label(self, text="Enter your text")
        label.config(font=("Courier", 44)) 
        label.grid(row=0, column=0,sticky="ns")
       
        
        self.fnout = fnout
        self.mainFrame = tk.Frame(self)
 
        top=self.winfo_toplevel()
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
        app.destroy()
        
        
             

class ReadyPage(Page):
    def __init__(self, master):
        Page.__init__(self, master)
        label = tk.Label(self, text="Ready?\n Click the button below to start reciting ")
        label.config(font=("Courier", 32))
        label.pack(side="top", fill="both", expand=True)

class TimerPage(Page):
    def __init__(self, master):
        Page.__init__(self, master)
        label = tk.Label(self, text="Press stop when finished ")
        label.config(font=("Courier", 32))
        label.pack(side="top", fill="both", expand=True)   
       
    
             
          
      
    
        
class ProcessingPage(Page):
    def __init__(self,master):
        Page.__init__(self,master)
        label = tk.Label(self, text="Processing... ")
        label.config(font=("Courier", 32))
        label.pack(side="top", fill="both", expand=True)
        
class ComparisonPage(Page):
    def __init__(self,master):
        Page.__init__(self, master) 
        self.fnout = "input.txt"
        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=1, column=0, sticky="nsew")
 
        top=self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)        
       
        ##label = tk.Label(self, text="Your Text")
        ##label.config(font=("Courier", 22)) 
        ##label.grid(row=0, column=0)
        ##label2 = tk.Label(self, text="Your Audio Input")
        ##label2.config(font=("Courier", 22)) 
        ##label2.grid(row=0, column=1)
        

   
 
        
        self.exit = tk.Button(self.mainFrame,
                                   text="Load Input Text"
                                  )
        self.exit.grid(row=4, column=0, sticky="ns")
        self.exit.config(font=("Courier", 16)) 
        
        self.exit = tk.Button(self.mainFrame,
                                   text="Load Audio Text"
                                   )
        self.exit.grid(row=4, column=1, sticky="ns")
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
        
        file = open("input.txt")
        for line in file:
            self.textWidget.insert(END,line)
        file.close() 
        
        
        file2 = open("audioInput.txt")
        for line2 in file2:
            self.textWidget2.insert(END,line2)
        
        file2.close() 
        
        ##idea for the future
        ## make a command on each button that loads the input for each
        ## file
        ##ie it only inserts the stuff once you click the button
        ##so it gets an updated  version of each file
                 
    
        
 
       
        
       
        
        
class ScrollbarX(tk.Scrollbar):
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        tk.Scrollbar.set(self, low, high)
        

       
class MyFirstGUI(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.centerWindow()  
        tk.Frame.__init__(self,master)
        ## make pages
        p0 = WelcomePage(self)
        p1 = InputPage(self,inText)
        p2 = ReadyPage(self)
        p3 = TimerPage(self)
        p4 = ProcessingPage(self)
        p5 = ComparisonPage(self)
        
        ##make button frames
        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        container.configure(background='black')
        
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        
        ##place all the pages in the program
        p0.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1) 
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
         
        ##place all the buttons      
        b0 = tk.Button(buttonframe, text="Welcome", command=p0.lift)
        b1 = tk.Button(buttonframe, text="Input", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Ready", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Timer", command=p3.lift)
        b4 = tk.Button(buttonframe, text="Processing", command=p4.lift)
        b5 = tk.Button(buttonframe, text="Comparison", command=p5.lift)
        
        b0.pack(side="left")
        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        b5.pack(side="left")
                        
        ## show welcome page that will link to others
        p0.show()
        
        master.title("QuoteR")

## centers the window based on 1280 x 720 size, might change based on
## users screen later
    def centerWindow(self):
        
        w = 1280
        h = 720

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        
        
        x = (sw - w)/2
        y = (sh - h)/2
                
        
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y)) 
        

   
             
inText = "input.txt"
audioText = "audioInput.txt"
root = tk.Tk()
my_gui = MyFirstGUI(root)
my_gui.pack(side="top", fill="both", expand=True)

##root.wm_geometry("1024x768")
root.mainloop()