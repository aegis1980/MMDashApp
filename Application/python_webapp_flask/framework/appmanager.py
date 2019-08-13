"""

"""

import os
import importlib


APP_PATH = os.path.join(os.getcwd(),'python_webapp_flask')

app_layouts = {}
app_callbacks = {}

def dynamic_import(app_name):
    """
    imports app layout and callback modules for dash
    """

    ## TODO validation check that there is a valid layout, callback and app .py file (as a minimum) in module
    # there also needs to be a recursive check that 
    # ideally all this is done (once) when app uploaded
    app_path_str = os.path.join(APP_PATH,app_name)
    pkg = 'python_webapp_flask.' + app_name
    directory = os.fsencode(app_path_str)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".py"): 
            # TODO extract starts with
            if filename.startswith('layout'):
               app_layouts[app_name] = importlib.import_module('.layout', package = pkg)
            elif filename.startswith('callbacks'):
               app_callbacks[app_name] = importlib.import_module('.callbacks', package = pkg)
            else:
                #to do callbacks, app and others. maybe.
                continue
    return app_layouts


def check_module(module_name):
    """
    Checks if module can be imported without actually
    importing it
    """
    module_spec = importlib.util.find_spec(module_name)
    if module_spec is None:
        print('Module: {} not found'.format(module_name))
        return None
    else:
        print('Module: {} can be imported!'.format(module_name))
        return module_spec