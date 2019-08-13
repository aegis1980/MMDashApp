
import python_flask_app.framework.layouts as layouts


ID = ''
APP = ''


def process_pathname(pathname):
    """Validates pathname and extracts identifier(project) and app"""
    
    if pathname.endswith('/'): # not sure this would happen, but just in case
        pathname = pathname[:-1] #remove it

    bits_of_path = pathname.split('/')

    # www.mywebsite.com

    l = len(bits_of_path)
    if l == 0:# www.mywebsite.com
        return ROOT_NO_ID   
    elif l == 1:
        if is_valid_id(bits_of_path[0]): # www.mywebsite.com/valid_id
            ID = bits_of_path[0]
            return ROOT_WITH_ID
        elif is_valid_app(bits_of_path[0]):# www.mywebsite.com/valid_app
            APP = bits_of_path[0]
            return APP_NO_ID
        else: # www.mywebsite.com/gobbledygook
            return ROOT_NO_ID 
    elif l >= 2: #just ignore anything grtr than 2 for now
        if is_valid_id(bits_of_path[0]): # www.mywebsite.com/valid_id
            ID = bits_of_path[0]
            if is_valid_app(bits_of_path[1]):
                APP = bits_of_path[1]
                #TODO dynamically import module here and return layout.
                return
                #return APP_WITH_ID # ***GOLDEN TICKET*** www.mywebsite.com/valid_id/valid_app
            else:
                return ROOT_WITH_ID # www.mywebsite.com/valid_id/gobbledygook
        else: # www.mywebsite.com/gobbledygook/gobbledygook
            return ROOT_NO_ID 

def is_valid_id(id):
    if id == '007':
        return True
    else:
        return False

def is_valid_app(app):
    #TODO lookup of registered apps to id
    if app == 'cost' or app == 'pmv':
        return True
    else:
        return False