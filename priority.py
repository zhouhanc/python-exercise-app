#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
    @
    @Description:   This GUI application helps one set priority and 
    @               check if one finishes all tasks in the end
    @
    @
    @Author:        Zhouhan Chen
    @Last modified: 02/05/2015 Beijing Time

    Issue: When make executable file, change the path of image
"""



import time
from datetime import datetime 
import datetime
import Tkinter 
from Tkinter import *
import tkMessageBox as box
from  PIL import Image, ImageTk
from subprocess import call
from pymongo import MongoClient
#call(["ls", "-l"])

global rownum
rownum = 4
# each color represents a level of priority
pri_color = {1: "#FF0000", 2: "#FF7F00", 3: "#FFFF00", 4: "#00FF00", 5: "#80FF00", 6:"#00FFBF", 6:"#00BFFF", 7:"#0040FF", 8:"#4000FF",
             9: "#4000FF", 10: "white" };
# all_labels store label object
all_labels = []
# connect to our database
client = MongoClient()
db = client.priority
collection = db.tasks

def resource_path(filename):
    #filename = 'myfilesname.type'
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller >= 1.6
        os.chdir(sys._MEIPASS)
        filename = os.path.join(sys._MEIPASS, filename)
    elif '_MEIPASS2' in os.environ:
        # PyInstaller < 1.6 (tested on 1.5 only)
        chdir(os.environ['_MEIPASS2'])
        filename = os.path.join(os.environ['_MEIPASS2'], filename)    

    else: 
        os.chdir(dirname(sys.argv[0]))
        filename = os.path.join(dirname(sys.argv[0]), filename)
    return filename


class Newlabel:
    """Newlabel is a wrapper for label widget, 
       Each object is able to draw a label on 
       canvas, as well as update its priority, 
       change its position on canvas 
    """
    def __init__(self, priority, row, message):
        
        self.priority = priority
        self.row = row
        self.finish = False
        self.message = message
        self.createtime = datetime.datetime.utcnow()
        self.create();
        

        
    def create(self):
        global rownum
        # 30 is the default font
        font = "Helvetica 30 bold italic"
        if (len(self.message) > 30):
            font = "Helvetica 20 bold italic"
        # add a button
        self.button = Button(root, text ="To do", command = self.updateStatus)
        self.button.grid(row = self.row, column = 0 ,sticky= N)

        # add a label
        self.label = Label(root, fg= pri_color[self.priority],
                                 text = self.message, 
                                 font = font,
                                 bg = "black"
                           )
        self.label.grid(row = self.row, column = 1, columnspan = 4 ,sticky= N + W)
        rownum += 1
        


    def updateStatus(self):
        # set priority to 10 (finished)
        if not self.finish:

            # create a json structure 
            newtask = {
                "createtime": self.createtime,
                "finishtime": datetime.datetime.utcnow(),
                "message": self.message,
                "priority": self.priority
            }
            # store the task into our database first
            collection.insert(newtask)

            self.finish = True
            self.priority = 10
            self.button.config(text = "Done!") 
            self.label.config(fg = "white")
            auto_Rank()
            self.popupWindow()

        # when button is clicked twice, delete the button and label
        else:

            self.label.destroy()
            self.button.destroy()
            all_labels.remove(self)


    def popupWindow(self):
        prompt = "I'm a slow walker, but I never walk back. \n -Abraham Lincoln "         
        box.showinfo("Keep Going", prompt, parent = root)  


    def modify(self):
        # self.label.destroy()    
        # self.label = Label(root, fg= pri_color[self.priority],
        #                          text = self.message, 
        #                          font = "Helvetica 30 bold italic",
        #                          bg = "black"
        #                    )
        self.label.grid(row = self.row, columnspan = 4 ,sticky= N + W )            
        self.button.grid(row = self.row, column = 0 ,sticky= N )

    def getPriority(self):
        return self.priority

    def getRow(self):
        return self.row

    def getStatus(self):
        return self.finish
 

def main():

    global root
    root = Tk()
    root.title('priority')
    root.attributes("-alpha", 1)
    root.wm_attributes("-topmost", 1)


    root.geometry("960x600+300+300")
    
    # add a background image
    #"/Users/zc/Documents/web_development/NO_procrastination/dist/priority.app/Contents/Resources/lib/python2.7/
    image = Image.open("/Users/zc/Documents/web_development/NO_procrastination/Inspirational.jpg")
    photo = ImageTk.PhotoImage(image)



    # leftframe = Frame(root)
    # leftframe.pack()

    # rightframe = Frame(root)
    # rightframe.pack()

    
 #    root.rowconfigure(0, pad=3)
 #    root.rowconfigure(1, pad=3)
 #    root.rowconfigure(2, pad=3)
 #    root.rowconfigure(3, pad=3)
 #    root.rowconfigure(4, pad=3)
 #    root.columnconfigure(0, pad=3)
	# root.columnconfigure(1, pad=3)
	# root.columnconfigure(2, pad=3)
	# root.columnconfigure(3, pad=3)

    # dispaly background image
    pic = Label(root, 
                        font = "Helvetica 40 bold italic",
                        relief = RAISED, 
                        image = photo,
                        text = "Program starting...", 
                        bg = "black" )
                        #compound=Tkinter.CENTER)
    pic.image = photo
    pic.grid(rowspan = 40, columnspan = 10)        

    # name of application
    title = Label(root, fg="red",
    					text = "Priority Manager", 
                               font = "Helvetica 30 bold italic",
                               bg = "black"
                               )

    title.grid(row = 0, columnspan = 3, sticky= E, padx=45, pady=5)

    # get current data

    time_label = Label( root, text=time.strftime("%H : %M : %S"),
                        fg = "light green",
                        bg = "#2E2E2E",
                        font = "Helvetica 40 bold italic"
                        )

    time_label.grid(row = 0, column = 3, columnspan = 3, sticky= N + W, pady=5)


    # button to add tasks
    add_bt = Button(root, text="Add", foreground = "red", command = lambda:add_label( start_hour.get(), entry.get()), 
                    bg = "black", fg = "red" )
    add_bt.grid(row = 1, column=1)

    #remove_bt = Button(root, text="REMOVE", bg = "black", foreground = "red"  )
    #remove_bt.grid(row = 1, column = 3)

    # prompt right to the button
    select_prompt = Label(root, fg="green",
                        text = "Select Priority", 
                               font = "Helvetica 20",
                               bg = "black"
                               )
    select_prompt.grid(row = 1, column = 3)


    # add scale to specify priority  
    start_hour_var = IntVar()
    start_hour_var = 5
    start_hour = Scale( root, variable = start_hour_var, orient=HORIZONTAL, 
                        resolution = 1, from_ = 1, to = 10,
                        sliderlength = 20, length = 200,
                        bg = "black", fg = "green", showvalue = start_hour_var
                        )

    start_hour.grid(row = 2, column = 3, columnspan = 3, sticky = W + N)


    # add entry to receive string
    entry = Entry(root, bd =5, bg = "yellow", highlightcolor = "red")
    entry.grid(row = 2, column = 0 ,columnspan = 3, sticky= N , pady = 2)
    timer_update(time_label);



    root.mainloop()  


# rownum starts at 4
def add_label(priority, msg):
    # the screen can only hold no more than 10 tasks
    if (rownum < 14):
        newlabel = Newlabel(priority, rownum, msg)
        all_labels.append(newlabel)
    # rank all labels according to its priority    
    auto_Rank()
    # force the user to login and do the word
    #time.sleep(3)

    # user experience not good enough
    # call("/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend", shell=True)
    


def timer_update(label):
  def count():

    # How to delete the window?
    # if t == 0:
    #     pass
    # else:    
    #     window_Destory(t, datetime.now().second)
    currentSecond= datetime.datetime.now().second
    currentMinute = datetime.datetime.now().minute
    currentHour = datetime.datetime.now().hour
    label.config(   text=time.strftime("%H : %M : %S"))
    label.after(1000, count)

  count()




# rank each task according to its priority
def auto_Rank():

    for x in xrange(len(all_labels) - 1):
        print(str(x) + "this is x")
        for y in xrange(x + 1, len(all_labels)):
            print(str(y) + "this is y")
            print(all_labels[x].priority, "x priority")
            print(all_labels[y].priority, "y priority")
            print(all_labels[x].row)
            print(all_labels[y].row)
            if ((all_labels[x].priority < all_labels[y].priority) and (all_labels[x].row > all_labels[y].row) ) or ( (all_labels[x].priority > all_labels[y].priority) and (all_labels[x].row < all_labels[y].row)  ):
                print("try to make the swap")
                temp = all_labels[x].row
                all_labels[x].row = all_labels[y].row
                all_labels[y].row = temp

                all_labels[x].modify()
                all_labels[y].modify()

# original code
        # for y in xrange(0, len(all_labels) - 1):
        #     print(str(y) + "this is y")
        #     print(all_labels[x].priority)
        #     print(all_labels[y].priority)
        #     print(all_labels[x].row)
        #     print(all_labels[y].row)
        #     if (all_labels[x].priority < all_labels[y].priority) and (all_labels[x].row > all_labels[y].row):
        #         print("try to make the swap")
        #         temp = all_labels[x].row
        #         all_labels[x].row = all_labels[y].row
        #         all_labels[y].row = temp

        #         all_labels[x].modify()
        #         all_labels[y].modify()

if __name__ == '__main__':
    #thread.start_new_thread( main, () )
    main()  
 