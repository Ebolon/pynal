'''
Contains configuration info for the running application.

Is stored in a file in the userspace (more like $XDG_CONFIG_HOME).
Reads and interprets the cmd line arguments.
'''
class Config():
   def __init__(self, args):
       self.parse_args(args)
        
       self.appname = "Pynal"
       
   def parse_args(self, args):
       """ Parse the list of arguments and do something useful, like pass. """
       pass
