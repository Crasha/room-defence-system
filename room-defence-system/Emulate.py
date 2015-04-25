'''
Created on 13 Mar 2015

@author: donald.taylor2
'''

from DoorSystem import Model
from DoorSystem import GUI
from DoorSystem import Control


def main():
    model = Model.Model()
    
    controller = Control.Controller(model)
    gui = GUI.GUI(controller)
    #realController = Control.Controller(controllable)

if __name__ == '__main__':
    main()