class symbolTable():
    def __init__(self):
        self.symbolTable={"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"SCREEN":16384,"KBD":24576}
        for i in range(16):
            self.symbolTable["R"+str(i)]=i

    def addEntry(self,symbol,address):
        """Adds the symbol and address to table"""
        self.symbolTable[symbol]=address
    def contains(self,symbol):
        """checks if symbol in symbol table"""
        if symbol in self.symbolTable.keys():
            return True
        return False
    def getAddress(self,symbol):
        return int(self.symbolTable[symbol])
    def getAll(self):
        return self.symbolTable