import time
import sys

class Logger:

    def __init__(self, level=5):
	self.setLogLevel(level)


    def Critical(self, msg):
	if(self.loggerLevel >= 1):
	    self.log(msg)

    def Severe(self, msg):
	if(self.loggerLevel >= 2):
	    self.log(msg)

    def Moderate(self, msg):
	if(self.loggerLevel >= 3):
	    self.log(msg)

    def Low(self, msg):
	if(self.loggerLevel >= 4):
	    self.log(msg)

    def Debug(self, msg):
	if(self.loggerLevel >= 5):
	    self.log(msg)

    def setLogLevel(self, level):
	self.loggerLevel = level

    def log(self, msg):
	print time.strftime("%H:%M:%S", time.gmtime()) + "---" + msg
	sys.stdout.flush()

if __name__ == "__main__":
    logger = Logger(5)

    logger.Debug("Hello World")
    logger.Low("Test log should display")

    logger.setLogLevel(3)
    time.sleep(2)
    logger.Debug("This shouldnt appear")

    logger.Moderate("This should appear")
    
