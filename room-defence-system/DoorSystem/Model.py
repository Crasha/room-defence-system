'''
Created on 13 Mar 2015

@author: donald.taylor2
'''

from StateMachine import State
from StateMachine import StateMachine
from Util.Observer import Observable

class Model(StateMachine, Observable):
    def __init__(self):
        StateMachine.__init__(self,ArmingNoAuth())
        Observable.__init__(self)
    def doorCloses(self):
        self.actionAndNotify(SysAct.doorCloses)
    def doorOpens(self):
        self.actionAndNotify(SysAct.doorOpens)
    def authRequested(self):
        self.actionAndNotify(SysAct.authRequested)
    def authOverriden(self):
        self.actionAndNotify(SysAct.authOverriden)
    def authAccepted(self):
        self.actionAndNotify(SysAct.authAccepted)
    def authRejected(self):
        self.actionAndNotify(SysAct.authRejected)
    def authFailed(self):
        self.actionAndNotify(SysAct.authFailed)
    def actionAndNotify(self,action):
        prevstate = self.currentState
        self.runAll([action])
        if prevstate != self.currentState:
            self.setChanged()
        self.notifyObservers()
        
        
#def enum(**enums):
#    return type('Enum', (), enums)
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

AuthStates = enum('NoAuth','Accept','Reject','Fail','Assess')
AlarmStates = enum('Armed','Disarmed','Fire')
                                
#abstract...
class SystemState(State):
    def __init__(self,alarmState,authState):
        self.alarmState = alarmState
        self.authState = authState
    def run(self):
        print "fire"
    def next(self, input):
            return Model.armingNoAuth
        


class ArmingNoAuth(SystemState):
    def __init__(self):
        SystemState.__init__(self, AlarmStates.Armed, AuthStates.NoAuth)
    def run(self):
        print "Armed noAuth"
    def next(self, input):
        if input == SysAct.doorOpens:
            return Model.firing
        elif input == SysAct.authRequested:
            return Model.armingAuthAssess
        return self
         
            
class ArmingAuthAssess(SystemState):
    def __init__(self):
        SystemState.__init__(self, AlarmStates.Armed, AuthStates.Assess)
    def run(self):
        print "Armed assess"
    def next(self, input):
        if input == SysAct.doorOpens:
            return Model.firing
        elif input == SysAct.authFailed:
            return Model.armingAuthFail
        elif input == SysAct.authRejected:
            return Model.armingAuthReject
        elif input == SysAct.authAccepted:
            return Model.disarmingAuthAccept
        return self

class ArmingAuthFail(SystemState):
    def __init__(self):
        SystemState.__init__(self, AlarmStates.Armed, AuthStates.Fail)
    def run(self):
        print "Armed fail"
    def next(self, input):
        if input == SysAct.doorOpens:
            return Model.firing
        elif input == SysAct.authRequested:
            return Model.armingAuthAssess
        return self

class ArmingAuthReject(SystemState):
    def __init__(self):
        SystemState.__init__(self, AlarmStates.Armed, AuthStates.Reject)
    def run(self):
        print "Armed reject"
    def next(self, input):
        if input == SysAct.doorOpens:
            return Model.firing
        elif input == SysAct.authRequested:
            return Model.armingAuthAssess
        return self

class DisarmingAuthAccept(SystemState):
    def __init__(self):
        SystemState.__init__(self, AlarmStates.Disarmed, AuthStates.Accept)
    def run(self):
        print "Disarmed accept"
    def next(self, input):
        if input == SysAct.doorOpens:
            return Model.disarmingNoAuth
        elif input == SysAct.doorCloses:
            return Model.armingNoAuth
        return self

class DisarmingNoAuth(SystemState):
    def __init__(self):
        SystemState.__init__(self, AlarmStates.Disarmed, AuthStates.NoAuth)
    def run(self):
        print "Disarmed accept"
    def next(self, input):
        if input == SysAct.doorCloses:
            return Model.armingNoAuth
        return self

class FiringNoAuth(SystemState):
    def __init__(self):
        SystemState.__init__(self, AlarmStates.Fire, AuthStates.NoAuth)
    def run(self):
        print "FIRE!"
    def next(self, input):
        if input == SysAct.doorCloses:
            return Model.armingNoAuth
        elif input == SysAct.timeout:
            return Model.disarmingNoAuth
        return self


Model.armingNoAuth = ArmingNoAuth();
Model.armingAuthAssess = ArmingAuthAssess();
Model.armingAuthFail = ArmingAuthFail();
Model.armingAuthReject = ArmingAuthReject();
Model.disarmingAuthAccept = DisarmingAuthAccept();
Model.disarmingNoAuth = DisarmingNoAuth();
Model.firing = FiringNoAuth();



class SysAct:
    def __init__(self, action):
        self.action = action
    def __str__(self): return self.action
    def __cmp__(self, other):
        return cmp(self.action, other.action)
    # Necessary when __cmp__ or __eq__ is defined
    # in order to make this class usable as a
    # dictionary key:
    def __hash__(self):
        return hash(self.action)

# Static fields; an enumeration of instances:
SysAct.doorCloses = SysAct("door closes")
SysAct.doorOpens = SysAct("door opens")
SysAct.authRequested = SysAct("auth requested")
SysAct.authOverriden = SysAct("auth overridden")
SysAct.authAccepted = SysAct("auth accepted")
SysAct.authRejected = SysAct("auth rejected")
SysAct.authFailed = SysAct("auth failed")
SysAct.timeout = SysAct("timeout")
