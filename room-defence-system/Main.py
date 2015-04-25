'''
Created on 13 Mar 2015

@author: donald.taylor2
'''

from DoorSystem import Model
from DoorSystem import UI
from DoorSystem import Control
 

def main():
    model = Model.Model()
    
    controller = Control.Controller(model)
    ui = UI.UI(controller)
    #realController = Control.Controller(controllable)

if __name__ == '__main__':
    main()
