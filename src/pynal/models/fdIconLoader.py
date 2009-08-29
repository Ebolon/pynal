"""
Finds icons by their name as specified by freedesktop.org

TODO:
- make usable
- make size optional
"""
import os
import user

data_dirs = os.environ["XDG_DATA_DIRS"].split(":")

theme = None

def find_icon(icon, size):
    """
    Search for an icon of the given name and size.

    Parameters:
    icon -- the name as specified by freedesktop.
    size -- the preferred size of the icon e.g. 32, 48, 128, scalable...

    Return:
    the path to the icon or None if no icon was found.
    """
    global theme
    if theme is None:
        theme = find_user_theme()

    filename = find_icon_helper(icon, size, theme)
    if filename is not None:
        return filename

    return lookup_fallback_icon(icon)

def find_icon_helper(icon, size, theme):
    """
    Find an icon within the specified theme, falling back to the theme's parents.

    Parameters:
    icon -- the name as specified by freedesktop.
    size -- the preferred size of the icon e.g. 32, 48, 128, scalable.
    theme -- the name of the theme in which to look for the icon.
    """
    filename = lookup_icon(icon, size, theme)
    if filename is not None:
        return filename

    parents = parent_themes(theme)
    if len(parents) > 0:
        themes = parents
    elif theme != "hicolor":
        themes = ["hicolor"]


    for parent in parents:
        filename = find_icon_helper(icon, size, parent)
        if filename is not None:
            return filename

    return None

def lookup_icon(icon, size, theme):
    """
    Find the icon for the given size and theme in all data_dirs.
    """
    for data_dir in data_dirs:
        theme_folder = os.path.join(data_dir, "icons", theme)
        if os.path.isdir(theme_folder):
            size_dirs = get_dirs_in_size(theme_folder, size)
            for icon_dir in size_dirs:
                search_dir = os.path.join(theme_folder, icon_dir)
                if not os.path.exists(search_dir):
                    continue

                icon_file = os.path.join(search_dir, icon + ".png")

                if os.path.isfile(icon_file):
                    return icon_file
        else:
            continue

def get_dirs_in_size(theme, size):
    result = []
    indexfile = open(os.path.join(theme, "index.theme"))
    for line in indexfile:
        if line.startswith("Directories"):
            dirs = [os.path.join(theme, item) for item in line.split("=")[1].split(",") if item.startswith(str(size))]
            break

    indexfile.close()
    return dirs

def parent_themes(theme):
    parents = None
    for data_dir in data_dirs:
        theme_folder = os.path.join(data_dir, "icons", theme)
        if not os.path.exists(theme_folder):
            continue

        indexfile = open(os.path.join(theme_folder, "index.theme"))
        for line in indexfile:
            if line.startswith("Inherits"):
                parents = line.split("=")[1].split(",")
                break
        indexfile.close()
    return parents

def find_user_theme():
    theme = None
    if kde_session():
        try:
            version = "kde" + os.environ["KDE_SESSION_VERSION"]
            config_file = os.path.join(user.home, "." + version, "share", "config", "kdeglobals")
                
            if os.path.isfile(config_file):
                file = open(config_file)
                for line in file:
                    if line.startswith("Theme"):
                        theme =  line.split("=")[1].strip()
                        break
                    
            if theme is None:
                #find system default
                global data_dirs
                for dir in data_dirs:
                    defaultdir = os.path.join(dir, "icons", "default." + version)
                    resolved = os.path.realpath(defaultdir)
                    if os.path.isdir(defaultdir):
                        theme = os.path.basename(resolved)
                        break
            
        except:
            pass # XXX: Stupid but will probably stand here until the end of days.
    elif gnome_session():
        pass # TODO: no idea how gnome does this.
    # TODO: xfce and others?

    return theme

def kde_session():
    try:
        os.environ["KDE_SESSION_VERSION"]
        return True
    except:
        return False

def gnome_session():
    return False
