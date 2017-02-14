class MessageQueue():
    
    def __init__(self):
        self.queue = []
        
    def getSize(self):
        return len(self.queue)
    
    def isEmpty(self):
        return len(self.queue) == 0
    
    def makeEmpty(self):
        self.queue = []
    
    def add(self, msg):
        self.queue.append(msg)
        
    def peek(self):
        if(self.isEmpty()):
            return None
        else:
            return self.queue[0]
        
    def getNext(self):
        if(self.isEmpty()):
            return None
        else:
            msg = self.queue.pop(0)
            return msg