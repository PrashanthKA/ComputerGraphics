# Kolandaiswami Arjunan, Prashanth
# 1001-110-082
# 2016-03-02
# Assignment_02

from tkinter import *
from math import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from threading import Timer
import sys
import time

class cl_widgets:
    def __init__(self,ob_root_window,ob_world=[]):
        self.ob_root_window=ob_root_window
        self.ob_world=ob_world
        self.menu=cl_menu(self)
        self.toolbar=cl_toolbar(self) #Draw and ToolBar Button 2
        self.rotateToolBar = cl_rotateToolBar(self,self.ob_root_window)
        self.zoomToolBar = cl_zoomToolBar(self,self.ob_root_window)
        # self.pannel_02 = cl_pannel_02(self) #Open Dialog and button2 button
        self.ob_canvas_frame=cl_canvas_frame(self)
        #self.status = cl_statusBar_frame(self)
        
        self.ob_world.add_canvas(self.ob_canvas_frame.canvas)
class cl_zoomToolBar:
    def __init__(self,master,ob_root_window):
        global m
        global m1
        global m2
        global m3
        self.ob_root_window=ob_root_window
        self.master=master
        fram1 = Frame(master.ob_root_window)
        Label(fram1, text="Scaled By:").grid(row=0,column=0, sticky=W)
        Label(fram1, text="X:").grid(row=0,column=1, sticky=W)
        m = StringVar()
        m.set(1.0)
        e = Entry(fram1, textvariable=m,width=5)
        e.grid(row=0,column=2)
        Label(fram1, text="Y:").grid(row=0,column=3, sticky=W)
        m1 = StringVar()
        m1.set(1.0)
        e = Entry(fram1, textvariable=m1,width=5)
        e.grid(row=0,column=4)
        Label(fram1, text="Z:").grid(row=0,column=5, sticky=W)
        m2 = StringVar()
        m2.set(1.0)
        e = Entry(fram1, textvariable=m2,width=5)
        e.grid(row=0,column=6)
        Label(fram1, text="Steps:").grid(row=0,column=7, sticky=W)

        m3 = StringVar()
        m3.set(1)
        e = Entry(fram1, textvariable=m3,width=5)
        e.grid(row=0,column=8)
        b1= Button(fram1, text="Scale", fg="red", command=self.scaleImage)
        b1.grid(row=0,column=9)
        fram1.pack()
    def scaleImage(self):
        tempScaleX = float(m.get())
        tempScaleY = float(m1.get())
        tempScaleZ = float(m2.get())
        tempSteps = int(m3.get())
        diffrenceX = tempScaleX-1
        diffrenceY = tempScaleY-1
        diffrenceZ = tempScaleZ-1
        for x in range(tempSteps):
            self.master.ob_world.scaleBy(self.master.ob_canvas_frame.canvas,1+diffrenceX/tempSteps,1+diffrenceY/tempSteps,1+diffrenceZ/tempSteps)
            self.master.ob_canvas_frame.canvas.update()


class cl_rotateToolBar:
    def __init__(self,master,ob_root_window):
        global v
        global v1
        global v2
        self.ob_root_window=ob_root_window
        self.master=master
        fram1 = Frame(master.ob_root_window)
        Label(fram1, text="Rotate around:").grid(row=0,column=0, sticky=W)
        v = IntVar()
        r1=Radiobutton(fram1,text = "x",variable=v,value=1)
        r1.select()
        r2=Radiobutton(fram1,text = "y",variable=v,value=2)
        r3=Radiobutton(fram1,text = "z",variable=v,value=3)
        r1.grid(row=0,column=2)
        r2.grid(row=0,column=3)
        r3.grid(row=0,column=4)
        Label(fram1, text="Rotate by:").grid(row=0,column=5, sticky=W)
        v1 = IntVar()
        v1.set(90)
        e = Entry(fram1, textvariable=v1,width=5)
        e.grid(row=0,column=6)
        Label(fram1, text="Steps:").grid(row=0,column=7, sticky=W)
        v2 = IntVar()
        v2.set(1)
        e = Entry(fram1, textvariable=v2,width=5)
        e.grid(row=0,column=8)
        b1= Button(fram1, text="Rotate", fg="red", command=self.rotateRadioCheck)
        b1.grid(row=0,column=9)
        fram1.pack()
    def rotateRadioCheck(self):
        rotateAround = v.get()
        rotateAroundBy = float(v1.get())
        rotateIn = int(v2.get())
        increamnetDegree = rotateAroundBy/rotateIn
        for x in range(rotateIn):
            self.master.ob_world.rotateBy(self.master.ob_canvas_frame.canvas,increamnetDegree,rotateAround)
            self.master.ob_canvas_frame.canvas.update()
        
    
class cl_canvas_frame:
    def __init__(self, master):
        self.master=master
        self.canvas = Canvas(master.ob_root_window,width=640, height=640, highlightthickness=0, bg="yellow")
        self.canvas.pack(expand=YES, fill=BOTH)
        
        self.canvas.bind('<Configure>', self.canvas_resized_callback) 
        self.canvas.bind("<ButtonPress-1>", self.left_mouse_click_callback)
        #self.canvas.bind("<ButtonRelease-1>", self.left_mouse_release_callback)
        self.canvas.bind("<B1-Motion>", self.left_mouse_down_motion_callback)
        #self.canvas.bind("<ButtonPress-3>", self.right_mouse_click_callback)
        #self.canvas.bind("<ButtonRelease-3>", self.right_mouse_release_callback)
        #self.canvas.bind("<B3-Motion>", self.right_mouse_down_motion_callback)
        #self.canvas.bind("<Key>", self.key_pressed_callback)    
        self.canvas.bind("<Up>", self.up_arrow_pressed_callback)
        self.canvas.bind("<Down>", self.down_arrow_pressed_callback)
        self.canvas.bind("<Right>", self.right_arrow_pressed_callback)
        self.canvas.bind("<Left>", self.left_arrow_pressed_callback)     
        self.canvas.bind("<Shift-Up>", self.shift_up_arrow_pressed_callback)
        self.canvas.bind("<Shift-Down>", self.shift_down_arrow_pressed_callback)
        self.canvas.bind("<Shift-Right>", self.shift_right_arrow_pressed_callback)
        self.canvas.bind("<Shift-Left>", self.shift_left_arrow_pressed_callback)   
        self.canvas.bind("f", self.f_key_pressed_callback)  
        self.canvas.bind("b", self.b_key_pressed_callback)  
    def key_pressed_callback(self,event):
        print ('key pressed')      
    def up_arrow_pressed_callback(self,event):
        print ('pressed up')
        
    def down_arrow_pressed_callback(self,event):
        print ('pressed down')     
    def right_arrow_pressed_callback(self,event):
        print ('pressed right')       
    def left_arrow_pressed_callback(self,event):
        print ('pressed left')       
    def shift_up_arrow_pressed_callback(self,event):
        self.canvas.world.translate(0,.1,0,1)
    def shift_down_arrow_pressed_callback(self,event):
        pass
    def shift_right_arrow_pressed_callback(self,event):
        pass
    def shift_left_arrow_pressed_callback(self,event):
        pass
    def f_key_pressed_callback(self,event):

        print ("f key was pressed")
    def b_key_pressed_callback(self,event):
        
        print ("b key was pressed")         
    def left_mouse_click_callback(self,event):
        print ('Left mouse button was clicked')
        print ('x=',event.x, '   y=',event.y)
        
        
        self.x = event.x
        self.y = event.y  
        self.canvas.focus_set()
    def left_mouse_release_callback(self,event):
        print ('Left mouse button was released')
        print ('x=',event.x, '   y=',event.y)
        print ('canvas width', self.canvas.cget("width"))
        self.x = None
        self.y = None
        
    def left_mouse_down_motion_callback(self,event):
        print ('Left mouse down motion')
        print ('x=',event.x, '   y=',event.y)
        self.x = event.x
        self.y = event.y 
        
    def right_mouse_click_callback(self,event):
        
        self.x = event.x
        self.y = event.y   
    def right_mouse_release_callback(self,event):
        
        self.x = None
        self.y = None        
    def right_mouse_down_motion_callback(self,event):
        pass
    def canvas_resized_callback(self,event):
        self.canvas.config(width=event.width,height=event.height)
        #print 'canvas width height', self.canvas.cget("width"), self.canvas.cget("height")
        #print 'event width height',event.width, event.height
        
        self.canvas.pack(expand=YES, fill=BOTH)
        print ('canvas width', self.canvas.cget("width"))
        print ('canvas height', self.canvas.cget("height"))
        self.master.ob_world.redisplay(self.master.ob_canvas_frame.canvas,event)
class cl_pannel_01:

    def __init__(self, master):

        self.master=master
        frame = Frame(master.ob_root_window)
        frame.pack()
        
        self.var_filename = StringVar()
        self.var_filename.set('')
        self.button = Button(frame, text="Hello", fg="red", command=self.say_hi)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Ask for a string", command=self.ask_for_string)
        self.hi_there.pack(side=LEFT)
        
        self.hi_there = Button(frame, text="Ask for a float", command=self.ask_for_string)
        self.hi_there.pack(side=LEFT)
        self.file_dialog_button = Button(frame, text="Open File Dialog", fg="blue", command=self.browse_file)
        self.file_dialog_button.pack(side=LEFT)        

    def say_hi(self):
        print ( "hi there, everyone!")
    def ask_for_string(self):
        s=simpledialog.askstring('My Dialog', 'Please enter a string')
        print ( s)
    def ask_for_float(self):
        f=simpledialog.askfloat('My Dialog', 'Please enter a string')
        print ( f)
    def browse_file(self):
        self.var_filename.set(filedialog.askopenfilename(filetypes=[("allfiles","*"),("pythonfiles","*.txt")]))
        filename = self.var_filename.get()
        print(filename)
class cl_pannel_02:

    def __init__(self, master):

        self.master=master
        frame = Frame(master.ob_root_window)
        frame.pack()
        self.button = Button(frame, text="Open Dialog", fg="blue", command=self.open_dialog_callback)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="button 2", command=self.button2_callback)
        self.hi_there.pack(side=LEFT)
        

    def open_dialog_callback(self):
        d = MyDialog(self.master.ob_root_window)
        print ( d.result)
        print ( "mydialog_callback pressed!"   )     

    def button2_callback(self):
        print ( "button2 pressed!")
class MyDialog(simpledialog.Dialog):
    def body(self, master):

        Label(master, text="Integer:").grid(row=0, sticky=W)
        Label(master, text="Float:").grid(row=1, column=0 ,sticky=W)
        Label(master, text="String:").grid(row=1, column=2 , sticky=W)
        self.e1 = Entry(master)
        self.e1.insert(0, 0)
        self.e2 = Entry(master)
        self.e2.insert(0, 4.2)
        self.e3 = Entry(master)
        self.e3.insert(0, 'Default text')

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=1, column=3)
        
        
        self.cb = Checkbutton(master, text="Hardcopy")
        self.cb.grid(row=3, columnspan=2, sticky=W)


    def apply(self):
        try:
            first = int(self.e1.get())
            second = float(self.e2.get())
            third=self.e3.get()
            self.result = first, second, third
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input",
                "Illegal values, please try again"
            )


#class StatusBar:

    #def __init__(self, master):
        #self.master=master
        #self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        #self.label.pack(fill=X)

    #def set(self, format, *args):
        #self.label.config(text=format % args)
        #self.label.update_idletasks()

    #def clear(self):
        #self.label.config(text="")
        #self.label.update_idletasks()       

class cl_statusBar_frame:

    def __init__(self, master):
        self.master=master
        status = StatusBar(master.ob_root_window)
        status.pack(side=BOTTOM, fill=X)
        status.set('%s','This is the status bar')


    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
class cl_menu:
    def __init__(self, master):
        
        self.master=master
        self.menu = Menu(master.ob_root_window)
        master.ob_root_window.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.menu_callback)
        self.filemenu.add_command(label="Open...", command=self.menu_callback)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.menu_callback)
        self.dummymenu = Menu(self.menu)
        self.menu.add_cascade(label="Dummy", menu=self.dummymenu)
        self.dummymenu.add_command(label="Item1", command=self.menu_item1_callback)
        self.dummymenu.add_command(label="Item2", command=self.menu_item2_callback)
        
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.menu_help_callback)        

    def menu_callback(self):
        print ("called the menu callback!")
                        
    def menu_help_callback(self):
        print ("called the help menu callback!") 
    def menu_item1_callback(self):
        print ("called item1 callback!")    

    def menu_item2_callback(self):
        print ("called item2 callback!")    
class cl_toolbar:
    def __init__(self, master):
        
        self.master=master
        self.toolbar = Frame(master.ob_root_window)
        self.button = Button(self.toolbar, text="Draw", width=16, command=self.toolbar_draw_callback)
        self.button.pack(side=LEFT, padx=2, pady=2)
        

        self.button = Button(self.toolbar, text="Load", width=16, command=self.toolbar_callback)
        self.button.pack(side=RIGHT, padx=2, pady=2)

        self.toolbar.pack(side=TOP, fill=X)
    def toolbar_draw_callback(self):
        self.master.ob_world.create_graphic_objects(self.master.ob_canvas_frame.canvas)
        #temp_canvas=self.master.ob_canvas_frame.canvas
        #line1=temp_canvas.create_line(0,0,temp_canvas.cget("width"),temp_canvas.cget("height"))
        #line2=temp_canvas.create_line(temp_canvas.cget("width"),0,0,temp_canvas.cget("height"))
        #oval=temp_canvas.create_oval(int(0.25*int(temp_canvas.cget("width"))),
            #int(0.25*int(temp_canvas.cget("height"))),
            #int(0.75*int(temp_canvas.cget("width"))),
            #int(0.75*int(temp_canvas.cget("height"))))

        print ( "called the draw callback!")
    
    def toolbar_callback(self):
        
        #load file code
        print("Load button clicked")
        # fileToBeRead = askopenfilename(mode = 'r')
        fileToBeRead = filedialog.askopenfilename()
        if(fileToBeRead):
            fl_obj = open(fileToBeRead,'r')
            
            mainVectorList = []
            mainFaceList = []
            mainViewPort = []
            mainWindow = []
            for line in fl_obj:
                if line[0] == 'v':
                    tempLine = line[2:-1]
                    splitStr = tempLine.rsplit()
                    mainVectorList.append(splitStr)
                elif line[0]=='f':
                    tempLine = line[2:-1]
                    splitStr = tempLine.rsplit()
                    mainFaceList.append(splitStr)
                elif line[0]=='s':
                    tempLine = line[2:-1]
                    mainViewPort = tempLine.rsplit()
                elif line[0]=='w':
                    tempLine = line[2:-1]
                    mainWindow = tempLine.rsplit()
            
            self.master.ob_world.plotFace2D(self.master.ob_canvas_frame.canvas,mainVectorList,mainFaceList,mainWindow,mainViewPort)