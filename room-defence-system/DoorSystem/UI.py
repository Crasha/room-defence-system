'''
Created on 13 Mar 2015

@author: donald.taylor2
'''
import Control
from Control import Controllable
from Util import Observer
from Model import AuthStates, AlarmStates
from DoorSystem.Control import Flasher
from time import sleep
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! Install, and remember to sudo")

import sys
sys.path.append('../pi-facerec-box')
import config, face, hardware
#from DoorSystem.facerec import config, face, hardware

import cv2
import subprocess

class UIController(Control.Controller):
    def __init__(self,model):
        Control.Controller.__init__(self,model)

if GPIO.RPI_REVISION == 1:
    userPin = 0
    doorPin = 1
    lightPins = [4,17,21,22,23]
else:
    userPin = 2
    doorPin = 3
    lightPins = [4,17,27,22,23]

greenPin = 25
redPin = 24

gunPin = 10

welcomeAudioFile = "welcome.mp3"
intruderAudioFile = "intruder.mp3"
sorryAudioFile = "sorry.mp3"

class UI(Observer.Observer):

    def __init__(self, controller):
        self.controller = controller #GUIController(controllable)
        self.controllable = controller.controllable
        controller.model.addObserver(self)
        self.flasher = Flasher()
        self.initUI()
        
    def initUI(self):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(userPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)	
	GPIO.setup(doorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)	
	GPIO.setup(gunPin, GPIO.OUT)	
	GPIO.setup(redPin, GPIO.OUT)	
	GPIO.setup(greenPin, GPIO.OUT)	
	GPIO.setup(lightPins, GPIO.OUT)	

        GPIO.add_event_detect(userPin, GPIO.FALLING, callback=self.userButtonUp, bouncetime=200)
        GPIO.add_event_detect(doorPin, GPIO.BOTH, callback=self.doorChange, bouncetime=200)

        GPIO.output(lightPins, GPIO.HIGH)
	sleep(0.5)
	GPIO.output(lightPins, GPIO.LOW)
	
        print 'Loading training data...'
        global model 
	model = cv2.createEigenFaceRecognizer()
        model.load(config.TRAINING_FILE)
        print 'Training data loaded!'
        # Initialize camer and box.
        global camera 
	camera = config.get_camera()

        
        #self.controllable.acceptAuth()
        #self.controllable.rejectAuth()
        #self.controllable.failAuth()
    
        #self.controllable.userButtonPress()
    def userButtonUp(self,*_):
        self.controllable.userButtonUp()
    def doorChange(self,*_):
	sleep(0.1)
	print GPIO.input(doorPin)
	if GPIO.input(doorPin):
            self.controllable.doorOpen()
	else :
            self.controllable.doorClose()


    def update(self, observable, arg):
        print "UI sees change" , observable.currentState

        if observable.currentState.authState == AuthStates.Assess:
            self.ledsOff()
	    GPIO.output(lightPins, 1)
	    image = camera.read()
            # Convert image to grayscale.
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

	    result = face.detect_single(image)
            if result is None:
                print 'Could not detect single face!  Check the image in capture.pgm' \
                        ' to see what was captured and try again with only one face visible.'              	
                self.playAudio( sorryAudioFile )
                self.controllable.failAuth()
            else:
                GPIO.output(lightPins, 0)
                sleep(0.2)
                GPIO.output(lightPins, 1)
                sleep(0.2)
                GPIO.output(lightPins, 0)
                sleep(0.2)
                GPIO.output(lightPins, 1)
	        x, y, w, h = result
                # Crop and resize image to face.
                crop = face.resize(face.crop(image, x, y, w, h))
                # Test face against model.
                label, confidence = model.predict(crop)
                print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
                      'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', 
                      confidence)
                if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
                  print 'Recognized face!'
                  self.playAudio( welcomeAudioFile )
                  self.controllable.acceptAuth()
                else:
                  print 'Did not recognize face!'
                  self.playAudio( intruderAudioFile )	
                  self.controllable.rejectAuth()		

        elif observable.currentState.authState != AuthStates.Assess:
	    GPIO.output(lightPins, 0)
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
	GPIO.output(greenPin,1)
    def greenOff(self):
	GPIO.output(greenPin,0)
    def redOn(self):
	GPIO.output(redPin,1)
    def redOff(self):
	GPIO.output(redPin,0)

    def fireOn(self):  
	GPIO.output(gunPin,1)  
	sleep(1)
	self.controllable.doorClose()  # don't keep firing
    def fireOff(self):    
	GPIO.output(gunPin,0)  

    def playAudio(self, file):
        cmd = ['mplayer', '-slave', '-quiet', file]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
