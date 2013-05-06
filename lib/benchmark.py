import time
import logging
# A rough function for measuring function performance.
# Can be called as a nice decorator: @timeFunction.

def timeFunction(func):
    
    def timed(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        endTime = time.time()
        if not kwargs:
            kwargs = 'No Kwargs'
        logging.debug('{0}{1}, {2}\n{3:.5f} Seconds'.format(func.__name__, args, kwargs, endTime - startTime))
        
        return result
    return timed
