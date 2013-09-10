import pprint
import sys

# ==================================================
# 
# 
# Jackal
# 
# 
# ==================================================
class Jackal():
    default_module = "Site"
    default_action = "index"
    
    def __init__(self):
        # Make a response buffer
        self._response = Response()
        sys.path += [
            'private/modules',
            'jackal/modules',
        ]
        
    def call(self, *args):
        # Get the class response object
        response = self.response
        # Initialize the module / action 
        module = action = None
        # Make uri into a list to hold the segments
        uri = list()
        # Go through the arguments until we have a module and method
        for argument in args:
            # Don't process non-string arguments
            if(isinstance(argument, str)):
                # Split the argument by '/' and remove empties
                argument = filter(None, argument.split('/'))
                while len(argument):
                    uri += [argument.pop(0)]
        # Pad uri so that pops won't fail
        uri += ['', '', '']
        # Get module from uri
        module = uri.pop(0) or Jackal.default_module
        # Get action from uri
        action = uri.pop(0) or Jackal.default_action
        # Tail is whatever is left in the uri (minus any empties)
        tail = filter(None, uri)
        # Get the module (class) that we're going to call
        instance = self.get_class(module)
        # Execute the action on the instance
        self.execute_method(instance, action, uri)
        
    def execute_method(self, instance, method_name, parameters):
        getattr(instance, method_name)(self, parameters)
    
    def get_class(self, module_name):
        # Build a path to the module (one-time-use, but written for cleanliness of code)
        path_to_module = ".".join(["private.modules", module_name.capitalize(), module_name.lower()])
        # Load the python module that the class is in
        module = __import__(path_to_module, globals(), locals(), ["Site"], -1)
        # Instantiate the class
        instance = getattr(module, module_name.capitalize())()
        return instance
    
    def handle(self, environment, start_response):
        # Get the Jackal response object
        response = self.response
        # Perform the call
        self.call(environment["PATH_INFO"])
        # Ensure a response is written (for debugging, basically)
        if response.length == 0: response.write("(Empty response)")
        # Convert the response into a string and return it
        return response.getvalue()
    
    @property 
    def response(self): return self._response
    @response.setter
    def response(self, value): self._response = value

# ==================================================
# 
# 
# Response
# 
# 
# ==================================================
import StringIO
class Response(StringIO.StringIO):
    # ==================================================
    # length
    # --------------------------------------------------
    # Returns the current length of the underlying buffer
    # ==================================================
    @property
    def length(self): return self.tell()
    