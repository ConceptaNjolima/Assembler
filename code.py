from parser import Parser

class Code():
    def __init__(self,parser):
        self.parser = parser

    def dest(self):
        self.dest=self.parser.dest()
        return self.dest
    def comp(self):
        self.comp=self.parser.comp()
        return self.comp
    def jump(self):
        self.jump=self.parser.jump()
        return self.jump

