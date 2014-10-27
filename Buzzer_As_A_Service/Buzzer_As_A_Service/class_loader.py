"""
This code is substantially taken from
https://lextoumbourou.com/blog/posts/dynamically-loading-modules-and-classes-in-python/
which was released under the MIT license is is freely available at
https://github.com/lextoumbourou/lextoumbourou.com/
"""

import pkgutil
import sys
import os

def get_class_name(mod_name):
    """Return the class name from a plugin name"""
    output = ""

    # Split on the _ and ignore the 1st word plugin
    words = mod_name.split("_")[1:]

    # Capitalise the first letter of each word and add to string
    for word in words:
        output += word.title()
    return output

def get_classes(mod_folder_path):
    path = mod_folder_path
    modules = pkgutil.iter_modules(path=[path])

    instanceList = []
    for loader, mod_name, ispkg in modules:
        # Ensure that module isn't already loaded
        if mod_name not in sys.modules:
            # Import module
            loaded_mod = __import__(path+"."+mod_name, fromlist=[mod_name])

            # Load class from imported module
            class_name = get_class_name(mod_name)
            loaded_class = getattr(loaded_mod, class_name)

            # Create an instance of the class
            instance = loaded_class()
            #instance.run()
	    instanceList.append(instance)
