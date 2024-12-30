#from ramapp import models as my_model
from testapp import models as my_model
import inspect
def get_model_name():
    '''
    this function is getting the all models class name
    '''
    class_name = []
    for name,obj in inspect.getmembers(my_model):
        if inspect.isclass(obj):
            class_name.append(name)
    return class_name
