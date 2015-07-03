from Tkinter import *
import tkFont
from PIL import Image, ImageTk
import tkMessageBox
from time import sleep
from random import uniform
import datetime

APP_BG_COLOR = "#FF9200"
UPPER_BG_COLOR = "#0B61A4"
global logging
logging = False

class base_gui(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background=UPPER_BG_COLOR)
        self.parent = parent

        self.parent.title("Proxy Server")
        self.pack(fill=BOTH, expand=1)
        self.center_window(300, 350)
        self.root = parent
        self.start_gui()

    def start_gui(self):
        self.build_top_frame(300, 150)
        self.create_init_button()
        self.build_logging_frame(250, 150)
        self.create_logging_section()

    """
    injects the logging info into the logging text placeholder

    :param string info          information to display as a row
    :param list info            information to display each row as item in list

    """
    def insert_log(self, info):
        global logging

        #Possible errors
        self.loggingText.config(state=NORMAL)
        try:
            self.loggingText.insert(END,"\n"+ datetime.datetime.now().strftime("%H:%M:%S")+": \n" + info)
            # Cool writing -> Adds a typing like animation to the logging box. Working but with minor problems
            # if type(info) is not list:
            #
            #     self.loggingText.insert(END,"\n"+ datetime.datetime.now().strftime("%H:%M:%S")+": \n")
            #     for letter in info:
            #         self.loggingText.insert(END, letter)
            #         self.parent.update()
            #         sleep(uniform(0.2, 0.3)/10.0)
            #     logging = False
            #
            # else:
            #     for info_text in info:
            #
            #         self.loggingText.insert(END,"\n"+ datetime.datetime.now().strftime("%H:%M:%S")+":\n")
            #         for letter in info_text:
            #             self.loggingText.insert(END, letter)
            #             self.parent.update()
            #             sleep(uniform(0.2, 1)/10.0)
            #         logging = False
        except():
            self.loggingText.insert(INSERT, "Error displaying logging info.\n")
            logging = False
       # self.loggingText.config(state=DISABLED)

    def center_window(self, width, height):

        w = width
        h = height

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))



    def build_top_frame(self, width, height):
        #Setting the top frame with the main button
        self.topFrame = Frame(self.root, width=width, height=height, bg=UPPER_BG_COLOR)
        self.topFrame.pack_propagate(0)
        self.topFrame.grid_propagate(False) #disables resizing of frame
        self.topFrame.columnconfigure(0, weight=1) #enables button to fill frame
        self.topFrame.rowconfigure(0,weight=1) #any positive number would do the trick
        self.topFrame.grid(row=0, column=1) #put frame where the button should be
        self.topFrame.pack(side=TOP)

    def create_init_button(self):
        #Create button font
        self.helv36 = tkFont.Font(self.root, family='Tahoma', size=20, weight='bold')

        #Configuring the image in the main button
        self.image = Image.open("plug_proxy_gui.png")
        self.photo = ImageTk.PhotoImage(self.image)

        #Configuring the main button
        self.startButton = Button(self.topFrame, text="Start Proxy", image=self.photo, compound="bottom", font=self.helv36)
        self.startButton.grid(row=0, column=0, sticky="w")
        self.startButton.pack()
        self.startButton.place(in_=self.topFrame, anchor="c", relx=.5, rely=.5)


    def build_logging_frame(self, width, height):
        #Creating the logging frame
        self.loggingFrame = Frame(self.root, width=width, height=height, bg=APP_BG_COLOR)
        self.loggingFrame.grid_propagate(False)
        self.loggingFrame.columnconfigure(0, weight=1)
        self.loggingFrame.rowconfigure(1, weight=1)
        self.loggingFrame.grid(row=2, column=2)
        self.loggingFrame.pack(side=BOTTOM, pady=10)

    def create_logging_section(self):
        #Configuring the logging label('Logging Info').
        self.loggingLabel = Label(self.loggingFrame,bg=APP_BG_COLOR, text="Logging Info: ", anchor=W, justify=LEFT)
        self.loggingLabel.pack(side=LEFT,fill=X, expand=True, anchor=W)
        self.loggingLabel.grid(row=0, column=0, sticky=W)


        self.log_font = tkFont.Font(self.root, size=7)

        #Creating the main logging text
        self.loggingText = Text(self.loggingFrame, height=9, fg="#00CC00", bg="black", font=self.log_font)
        #self.loggingText.config(state=DISABLED)
        self.loggingText.grid(row=2)
        self.loggingText.grid_propagate(False)
        self.loggingText.columnconfigure(0, weight=1)
        self.loggingText.rowconfigure(1, weight=1)


         # add a vertical scroll bar to the text area

        self.scr = Scrollbar(self.loggingText)
        self.scr.config(command=self.loggingText.yview)
        self.loggingText.config(yscrollcommand=self.scr.set)

        self.scr.grid(row=0, sticky=E)
        #self.scroll.grid(row=2, sticky=E)
        #self.loggingText['yscrollcommand'] = self.scrollb.set



def main():
    #Setting GUI root
    root = Tk()
    root.configure(bg=APP_BG_COLOR)
    global gui
    gui = base_gui(root)
    gui.startButton.bind("<Button-1>", button_click)

    gui.insert_log("GUI started successfully!")
    root.mainloop()



def button_click(event):
    global pro
    if(" ".join(gui.startButton.config('text')[-1]) != "Stop Proxy"):
        image = Image.open("plug_proxy_gui_x.png")
        photo = ImageTk.PhotoImage(image)
        gui.startButton.config(text="Stop Proxy", image=photo, compound="bottom")
        gui.startButton.image = photo
        gui.insert_log("Beginning proxy initialization...")
        import main
        main.gui = gui
        import thread
        th = thread.start_new_thread(main.main,())

    else:
        image = Image.open("plug_proxy_gui.png")
        photo = ImageTk.PhotoImage(image)
        gui.startButton.config(text="Start Proxy", image=photo, compound="bottom")
        gui.startButton.image = photo
        gui.insert_log("Stopping proxy server...")
        sys.exit()






if __name__ == '__main__':
    main()
