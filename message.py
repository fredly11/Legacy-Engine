####################################################################
##                                                                ##
##               message.py                                       ##
##                  Tos                                           ##
##               6/17/2017                                        ##
##                                                                ##
##      This is the message bus module for                        ##
##  Legacy Engine. Further documentation to follow                ##
##                                                                ##
####################################################################

#Imports
from collections import deque as dq
import time

class Messenger:
    """Manages messages sent between modules.


    Arguments:
    modules -- The modules that interact with the message bus.

    As of v0.01:
    -posts messages to a number of deques on command.
    -sends messages from those deques on command.
    -can add modules to the list on command.
    -prints errors to idle console.
    -performs very very fast when not printing to idle.

    TODO:
    -hook to custom console
    -build other module classes to interact with it.
    """

    def __init__(self, modules = []):
        self.modules = modules
        self.box_1 = dq([])
        self.box_2 = dq([])
        self.box_3 = dq([])
        self.box_now = dq([])

    def postMessage(self, message, priority):
        """Places a message in a box.


        Arguments:
        message  -- The message.
        priority -- Which box it goes in.

        As of v0.01:
        -places message in appropriate box
        -processes immediate messages upon posting.

        TODO:
        -hook to console, print error message there.
        -possibly redo the method for processing
         immediate messages.

        Speed: .000001
        """
 #       t0 = time.time()
        if priority == "now":
            self.box_now.append(message)
            self.processMessages("now")
        elif priority == 1:
            self.box_1.append(message)
        elif priority == 2:
            self.box_2.append(message)
        elif priority == 3:
            self.box_3.append(message)
        else:
            print("Error: unable to post message.")
#        t1 = time.time()
#        print(t1-t0)

    def processMessages(self, priority, limit = 0):
        """Sends each message in a given box to all modules.


        Arguments:
        priority -- Which box to pull from.
        limit    -- How many messages to process this frame.
                    0 pulls all messages from the box.

        As of v0.01:
        -pulls a given number of messages from a given box.
        -prevents crashes due to poping an empty deque.

        TODO:
        -fine tune engine to prevent overdrawing a deque.
        -hook to console, print errors there.
    
        Speed: .000005
        """
#        t0 = time.time()        
        box = None
        if priority == "now":
            box = self.box_now
        elif priority == 1:
            box = self.box_1
        elif priority == 2:
            box = self.box_2
        elif priority == 3:
            box = self.box_3

        if limit == 0:
            limit = len(box)

        while limit > 0:
            try:
                limit -= 1
                message = box.popleft()
                for x in self.modules:
                    x.recieve(message)
            except:
                print("Inefficiency detected: Excess messaging attempts.")
#        t1 = time.time()
#        print(t1-t0)

    def addModule(self, module):
        """Adds a module to the messaging list.


        Arguments:
        module  -- The module to add to the list.

        As of v0.01:
        -

        TODO:
        -

        Speed: .000003 
        """

#        t0 = time.time()
        if module not in self.modules:
            self.modules.append(module)
            #debug only:
            #for x in self.modules:
#                print(x.name)
#        t1 = time.time()
#        print(t1-t0)
        
class DummyModule:

    
    """A dummy module for testing purposes.

    Arguments:
    name     -- the dummy's name.
    triggers -- things that trigger the dummy.
    
    As of v0.01:
    -does dumb stuff

    TODO:
    -likely keep doing dumb stuff.

    """
    
    def __init__(self, name, triggers = [] ):
        self.name = name
        self.triggers = triggers

    def recieve(self, message):
        if message in self.triggers:
            print(message)
            print("recieved by " + self.name)

if __name__ == '__main__':
    """Uses the dummy class to test the message bus."""
    bus = Messenger()

    dummy_1 = DummyModule("One", ["Put your left foot in", "Put your left foot out"])
    dummy_2 = DummyModule("Two", ["Shake it all about", "Do the hokey pokey"])
    dummy_3 = DummyModule("Three", ["Put your left foot out", "Do the hokey pokey"])

    bus.addModule(dummy_1)
    bus.addModule(dummy_2)
    bus.addModule(dummy_3)

    bus.postMessage("Put your left foot in", 1)
    bus.postMessage("Put your left foot out", 1)
    bus.postMessage("Put your left foot in", 1)
    bus.postMessage("Do the hokey pokey", "now")
    bus.postMessage("Shake it all about", 2)
    bus.postMessage("Put your left foot out", 3)

    bus.processMessages(1)
    bus.processMessages(2)
    bus.processMessages(3)
        
