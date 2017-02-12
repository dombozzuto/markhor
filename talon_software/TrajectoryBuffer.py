class TrajectoryBuffer:

    _motProfTopBuffer = None
    _cap = None
    _in = 0
    _ou = 0
    _sz = 0
    _lastFront = None

    def Clear(self):
        self._sz = 0;
        self._in = 0;
        self._ou = 0;

    def Push(self, pt):
        self.Alloc()
        self._motProfTopBuffer.insert(self._in, pt)

        self._in += 1
        if(self._in >= self._cap):
            self._in = 0
        self._sz += 1

    def Front(self):
        self.Alloc()
        try:
            self._lastFront = self._motProfTopBuffer[self._ou]
        except:
            return None
        return self._lastFront

    def Pop(self):
        self._ou += 1
        if(self._ou >= self._cap):
            self._ou = 0
        self._sz -= 1

    def GetNumTrajectories(self):
        return self._sz

    def IsEmpty(self):
        return self._sz == 0

    def __init__(self, cap):
        if(cap < 1):
            cap = 1
        self._cap = cap

    def Alloc(self):
        if(self._motProfTopBuffer == None):
            self._motProfTopBuffer = []

##t = TrajectoryBuffer(512)
##print t.IsEmpty()
##t.Push("pt1")
##print t.IsEmpty()
##print t.Front()
##t.Push("pt2")
##print t.Front()
##print t.GetNumTrajectories()
##t.Pop()
##print t.Front()
##t.Pop()
##print t.IsEmpty()
##print t.Front()


    
