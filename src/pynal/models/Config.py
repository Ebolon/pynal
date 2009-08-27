'''
Contains configuration info for the running application.

Is stored in a file in the userspace (more like $XDG_CONFIG_HOME).
Reads and interprets the cmd line arguments.
'''
appname = "Pynal"
version = "0.1"

window_width = 600
window_height = 600

pdf_render_dpi = 150
       
def parse_args(args):
    """ Parse the list of arguments and do something useful, like pass. """
    pass

def load_config():
    """ Load the configuration file for the current user. """
    pass