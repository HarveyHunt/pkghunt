from PyQt4 import QtCore
from lib import database
import logging


class GenericThread(QtCore.QThread):
    # This class is a thread that inherits the QThread as a parent.
    # It is designed to work with a queue, as implemented by the application.
    def __init__(self, function, queue):
        QtCore.QThread.__init__(self)
        self.queue = queue
        self.function = function
        # Grab data from the queue.
        self.args = queue.get()

    def __del__(self):
        logging.debug("Killing thread " + str(self))

    def run(self):
        logging.debug("Running thread.")
        ret = self.function(*self.args)
        # Append the thread object so that it can be
        # deleted.
        ret.append(self)
        # Let the queue know that the task is done and push
        # the result to it. Self is appended to the return values
        # so that the caller can take care of clean up.
        self.queue.task_done()
        self.queue.put(ret)


class DatabaseThread(QtCore.QThread):
    def __init__(self, functionName, queue):
        QtCore.QThread.__init__(self)
        self.queue = queue
        self.args = queue.get()
        self.functionName = functionName
        self.db = database.Database(self.args[0])
        # As tuples don't support popping, removing the
        # first element with a slice is the best option.
        self.args = self.args[1:]

    def __del__(self):
        logging.debug("Killing thread " + str(self))

    def run(self):
        if self.functionName == "editPackage":
            self.db.editPackage(*self.args)
        elif self.functionName == 'deletePackage':
            self.db.deletePackage(*self.args)
        self.queue.task_done()
        # A null value is returned to prevent the main thread from stalling.
        self.queue.put(None)
