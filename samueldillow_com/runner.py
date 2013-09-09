import sys
import time
import traceback

_jackal = None

def run(environment, start_response):
    result = ""
    
    try:
        import jackal
        
        # Initialize Jackal 
        jackal = jackal.Jackal()
        # Pass the url to jackal
        result = jackal.handle(environment, start_response)
    except Exception as ex:
        # Get the last error
        error_name, error_type, stack_trace = sys.exc_info()
        # If there was an error, then print it
        result = "<pre>" + time.asctime() + " ERROR: " + str(error_type) + "\n" \
            + "\n" \
            + (traceback.format_exc()) \
            + "</pre>"
    return result
