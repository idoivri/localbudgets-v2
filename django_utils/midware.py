import traceback
import sys

class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        # Print the familiar Python-style traceback to stderr
        traceback.print_exc()