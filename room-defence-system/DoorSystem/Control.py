'''
Created on 13 Mar 2015

@author: donald.taylor2
'''
from Util import Observer
import threading
from time import sleep
import time

class Controllable(object):
    '''
    classdocs
    '''
    def __init__(self, model):
        self.model = model
    def userButtonPress (self):
        pass
        #print "press"
    def userButtonDown (self):
        pass
    def userButtonUp (self):
        self.model.authRequested()
    def doorOpen (self):
        self.model.doorOpens()
    def doorClose (self):
        self.model.doorCloses()
    def acceptAuth(self):
        self.model.authAccepted()
    def rejectAuth(self):
        self.model.authRejected()
    def failAuth(self):
        self.model.authFailed()
        
class Controller(Observer.Observer):
    def __init__(self, model):
        self.controllable = Controllable(model)
        self.model = model
        self.model.addObserver(self)
    def update(self, observable, arg):
        print observable.currentState

def defpass(): pass
        
class Flasher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self )
        self.running = True
        self.reset = False
        self.timeout = time.clock()
        self.stopState2 = defpass 
        #self.lock = threading.Lock()
        self.start()
    def stop(self):
        self.reset = True
        self.running = False
    def flash(self, startState1, stopState1, startState2, stopState2, duration):
        self.startState1 = startState1        
        self.stopState1 = stopState1
        self.startState2 = startState2        
        self.stopState2 = stopState2
        #self.duration = duration
        self.timeout = time.time() + duration
        self.reset = True
    def run(self):
        while self.running :
            if time.time() < self.timeout:
                self.reset = False
            else:
                sleep(0.05)
                self.reset = True
            self.stopState2()
            if self.reset : continue
            self.startState1()
            if self.reset : continue
            sleep(0.2)
            self.stopState1()
            if self.reset : continue
            self.startState2()
            if self.reset : continue
            sleep(0.2)
            
            
