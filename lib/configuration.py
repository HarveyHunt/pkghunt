import configparser
import os
import logging

class Config():
    # It would be a lot nicer to inherit the RawConfigParser class,
    # but that causes issues with __del__, so I have instantiated it
    # within the class instead.
    def __init__(self):
        self.parser = configparser.RawConfigParser()
        if not os.path.exists('pkghunt.conf'):
            logging.warning("No configuration file found.")
            self.parser.add_section("General")
            # Craft some default values for the config.
            self.favouritesFile = os.sep.join([os.getcwd(), "favourites.ini"])
            self.databaseFile = os.sep.join([os.getcwd(), "packages.sqlite"])
            self.downloadPath = os.sep.join([os.getcwd(), "packages", ""])
            self.logFile = os.sep.join([os.getcwd(), "pkghunt.log"])
            self.makeLogFile = os.sep.join([os.getcwd(), "make.log"])
            self.loggingLevel = 1
            self.logToConsole = 2
            self.pipLogFile = os.sep.join([os.getcwd(), "pip.log"])
            self.terminalWaitTime = 5
            # Then add them to the parser.
            # I assign the member variables values first, so that they can
            # be accessed elsewhere. Otherwise, as no config file exists,
            # nothing is assigned to the member variables and so the program
            # will crash.
            self.parser.set("General", "favouritesFile", self.favouritesFile)
            self.parser.set("General", "databaseFile", self.databaseFile)
            self.parser.set("General", "downloadPath", self.downloadPath)
            self.parser.set("General", "logFile", self.logFile)
            self.parser.set("General", "makeLogFile", self.makeLogFile)
            self.parser.set("General", "loggingLevel", self.loggingLevel)
            self.parser.set("General", "logToConsole", self.logToConsole)
            self.parser.set("General", "pipLogFile", self.pipLogFile)
            self.parser.set("General", "terminalWaitTime", self.terminalWaitTime)
            # Write the configuration to the file.
            with open("pkghunt.conf", "w") as file:
                self.parser.write(file)
            logging.debug("Created a default configuration file.")
        else:
            # Read the values from the config file as it exists.
            self.parser.read("pkghunt.conf")
            self.favouritesFile = self.parser.get("General", "favouritesFile")
            self.databaseFile = self.parser.get("General", "databaseFile")
            self.downloadPath = self.parser.get("General", "downloadPath")
            self.logFile = self.parser.get("General", "logFile")
            self.makeLogFile = self.parser.get("General", "makeLogFile")
            self.loggingLevel = self.parser.getint("General", "loggingLevel")
            self.logToConsole = self.parser.getint("General", "logToConsole")
            self.pipLogFile = self.parser.get("General", "pipLogFile")
            self.terminalWaitTime = self.parser.get("General", "terminalWaitTime")

    def __del__(self):
        # Overload the pseudo-destructor in order to save the config settings.
        self.parser.set("General", "favouritesFile", self.favouritesFile)
        logging.debug("Favourites file is set to {0}".format(self.favouritesFile))
        self.parser.set("General", "databaseFile", self.databaseFile)
        logging.debug("Database file is set to {0}".format(self.databaseFile))
        self.parser.set("General", "downloadPath", self.downloadPath)
        logging.debug("Download path is set to {0}".format(self.downloadPath))
        self.parser.set("General", "logFile", self.logFile)
        logging.debug("Logfile set to {0}".format(self.logFile))
        self.parser.set("General", "makeLogFile", self.makeLogFile)
        logging.debug("Make log file is set to {0}".format(self.makeLogFile))
        self.parser.set("General", "loggingLevel", self.loggingLevel)
        logging.debug("Logging level set to {0}".format(self.loggingLevel))
        self.parser.set("General", "logToConsole", self.logToConsole)
        logging.debug("Log to console set to {0}".format(self.logToConsole))
        self.parser.set("General", "terminalWaitTime", self.terminalWaitTime)
        logging.debug("Terminal wait time set to {0}".format(self.terminalWaitTime))
        with open("pkghunt.conf", "w") as file:
            self.parser.write(file)

