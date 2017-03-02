import time

class Logger:

    def __init__(self, level=5):
	self.setLogLevel(level)


    def logCritical(self, msg):
	if(self.loggerLevel >= 1):
	    self.log(msg)

    def logSevere(self, msg):
	if(self.loggerLevel >= 2):
	    self.log(msg)

    def logModerate(self, msg):
	if(self.loggerLevel >= 3):
	    self.log(msg)

    def logLow(self, msg):
	if(self.loggerLevel >= 4):
	    self.log(msg)

    def logDebug(self, msg):
	if(self.loggerLevel >= 5):
	    self.log(msg)

    def setLogLevel(self, level):
	self.loggerLevel = level

    def log(self, msg):
	print time.strftime("%H:%M:%S", time.gmtime()) + "---" + msg

if __name__ == "__main__":
    logger = Logger(5)

    logger.logDebug("Hello World")
    logger.logLow("Test log should display")

    logger.setLogLevel(3)
    time.sleep(2)
    logger.logDebug("This shouldnt appear")

    logger.logModerate("This should appear")
    
