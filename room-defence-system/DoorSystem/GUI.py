'''
Created on 13 Mar 2015

@author: donald.taylor2
'''
from Tkinter import  Tk, Frame, BOTH, X, Y, LEFT, RIGHT, TOP, BOTTOM, CENTER, Button, StringVar
import Control
from Control import Controllable
import Tkinter
from Util import Observer
from Model import AuthStates, AlarmStates
from DoorSystem.Control import Flasher

class GUIController(Control.Controller):
    def __init__(self,model):
        Control.Controller.__init__(self,model)

class MyFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background="white")   
        self.parent = parent
        self.controller = controller #GUIController(controllable)
        self.controllable = controller.controllable
        self.initUI()
        
    def initUI(self):
        self.parent.title("Simple")
        self.pack(fill=BOTH, expand=1)
        self.fireFrame = Frame(self, background="lightgrey", height = 20)
        self.fireFrame.pack(fill=X, side=BOTTOM)
                   

        leftFrame = Frame(self, background="lightgrey" )
        leftFrame.pack(fill=Y, side = LEFT)

        rightFrame = Frame(self, background="lightgrey")
        rightFrame.pack(fill=Y, side = RIGHT)
        rightFill = Frame(rightFrame, background="lightgrey")
        rightFill.pack(side=TOP )

        centreFrame = Frame(self, background="lightgrey")
        centreFrame.pack(fill=BOTH, expand=True)
        clusterFrame = Frame(centreFrame, background="lightgrey", width = 80, height = 80)
        clusterFrame.pack(pady = 60)
        
        self.lights = []
        self.lights.append( Frame(clusterFrame, width=20, height=20, background="darkgrey") )
        self.lights[0].grid(row=0, column =0, padx = 10, pady = 10)
        self.lights.append( Frame(clusterFrame, width=20, height=20, background="darkgrey") )
        self.lights[1].grid(row=0, column =1, padx = 10, pady = 10)
        self.lights.append( Frame(clusterFrame, width=20, height=20, background="darkgrey") )
        self.lights[2].grid(row=0, column =2, padx = 10, pady = 10)

        camera = Frame(clusterFrame, width=25, height=25, background = "black") 
        camera.grid(row=1, column =1, padx = 10, pady = 10)
        
        self.lights.append( Frame(clusterFrame, width=20, height=20, background="darkgrey") )
        self.lights[3].grid(row=2, column =0, padx = 10, pady = 10)
        self.lights.append( Frame(clusterFrame, width=20, height=20, background="darkgrey") )
        self.lights[4].grid(row=2, column =2, padx = 10, pady = 10)
        
        self.cambuttons = Frame( clusterFrame, background="lightgrey")      
        self.cambuttons.grid( row = 3, column = 1)  
        accept = Button( self.cambuttons, text="Accept" , command= self.acceptButtonPress, width=5)
        accept.pack()
        reject = Button( self.cambuttons, text="Reject" , command= self.rejectButtonPress, width=5)
        reject.pack()
        fail = Button( self.cambuttons, text="Fail" , command= self.failButtonPress, width=5)
        fail.pack()
        self.cambuttons.grid_remove()            
        
        self.doorStateVar = StringVar()
        self.doorStateVar.set('Closed');
        doorSwitch = Tkinter.Checkbutton(leftFrame, text = "Door Closed", command = self.doorChange, onvalue = 'Closed', offvalue = 'Open', variable = self.doorStateVar)
        doorSwitch.pack()
        self.alarmRed = Frame(leftFrame, background='#A88', width=20, height=20)
        self.alarmRed.pack(side=BOTTOM, padx = 10, pady = 10)
        self.alarmGreen = Frame(leftFrame, background='#8A8', width=20, height=20)
        self.alarmGreen.pack(side=BOTTOM, padx = 10, pady = 10)
        
        userButton = Button(rightFrame, text = "Press", command = self.userButtonPress, padx = 20)
        userButton.bind('<Button-1>', self.userButtonDown)
        userButton.bind('<ButtonRelease-1>', self.userButtonUp)
        userButton.pack(side=BOTTOM)
        
        #self.pack(fill=BOTH, expand=1)       
    def acceptButtonPress(self):
        self.controllable.acceptAuth()
    def rejectButtonPress(self):
        self.controllable.rejectAuth()
    def failButtonPress(self):
        self.controllable.failAuth()
    
    def userButtonPress(self):
        self.controllable.userButtonPress()
    def userButtonUp(self,event):
        self.controllable.userButtonUp()
    def userButtonDown(self,event):
        self.controllable.userButtonDown()
    def doorChange(self):
        if ( self.doorStateVar.get() == 'Open' ) :
            self.controllable.doorOpen()
        else :
            self.controllable.doorClose()

class GUI(Observer.Observer):
    '''
    classdocs
    '''

    def __init__(self, controller):
        '''
        Constructor
        '''
        root = Tk()
        root.geometry("300x400+300+300")
        self.app = MyFrame(root,controller)
        controller.model.addObserver(self)
        self.flasher = Flasher()
        root.mainloop()
        
    def update(self, observable, arg):
        print "GUI sees change" , observable.currentState

        if observable.currentState.authState == AuthStates.Assess:
            self.ledsOff()
            self.app.cambuttons.grid()
            for l in self.app.lights:
                l.configure(background = 'white')
        elif observable.currentState.authState != AuthStates.Assess:
            self.app.cambuttons.grid_remove()
            for l in self.app.lights:
                l.configure(background = 'grey')
        if  observable.currentState.alarmState == AlarmStates.Disarmed:
            if observable.currentState.authState == AuthStates.Accept:
                self.flasher.flash(self.greenOnly, self.greenOnly, self.ledsOff, self.greenOnly, 3)
            else:
                self.flasher.flash(self.greenOnly, self.greenOnly, self.greenOnly, self.greenOnly, 3) 
        elif observable.currentState.alarmState == AlarmStates.Armed:
            if observable.currentState.authState == AuthStates.Reject:
                self.flasher.flash(self.redOnly, self.ledsOff, self.ledsOff, self.redOnly, 3)
            elif    observable.currentState.authState == AuthStates.Fail:
                self.flasher.flash(self.redOnly, self.greenOn, self.greenOnly, self.redOnly, 3)
            elif    observable.currentState.authState == AuthStates.NoAuth:
                self.flasher.flash(self.redOnly, self.greenOn, self.greenOnly, self.redOnly, 1)
            
        
        if  observable.currentState.alarmState == AlarmStates.Fire:
            self.fireOn()
        else:
            self.fireOff()
            
    def fireOn(self):
            self.app.fireFrame.configure(background = '#FF0')
        
    def fireOff(self):
            self.app.fireFrame.configure(background = 'lightgrey')

    def ledsOn(self):
        self.greenOn()
        self.redOn()

    def ledsOff(self):
        self.greenOff()
        self.redOff()
    def greenOnly(self):
        self.greenOn()
        self.redOff()
    def redOnly(self):
        self.redOn()
        self.greenOff()   
    def greenOn(self):
            self.app.alarmGreen.configure(background = '#4F4')
    def greenOff(self):
            self.app.alarmGreen.configure(background = '#8A8')           
    def redOn(self):
            self.app.alarmRed.configure(background = '#F44')
    def redOff(self):
            self.app.alarmRed.configure(background = '#A88')   

    def fireOn(self):    
            self.app.fireFrame.configure(background = '#FF0')
    def fireOff(self):    
            self.app.fireFrame.configure(background = 'lightgrey')

