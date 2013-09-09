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
        self.get_class(module)
    
    def get_class(self, module_name):
        response = self.response
        module = __import__("private.modules.Site.site")
        test = private.modules.Site.Site()
        response.write("<pre>"+pprint.PrettyPrinter().pformat(dir(module))+"</pre>")
        # response = self.response
        # module = __import__("site")
        # response.write("<pre>"+pprint.PrettyPrinter().pformat(dir(module))+"</pre>")
        # sys.path.insert(0, "private/modules/Site")
        # response.write("<pre>"+pprint.PrettyPrinter().pformat(sys.path)+"</pre>")
        # response.write("<pre>"+pprint.PrettyPrinter().pformat(dir(sys.path))+"</pre>")
        
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
    