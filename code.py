from parser import Parser

class Code():
    """
    Sections of C instructions built from parser class
    """
    def __init__(self,parser):
        self.parser = parser

    def dest(self):
        """
        Get destination bits
        :return: dest: string
        """
        self.dest=self.parser.dest()
        return self.dest
    def comp(self):
        """
        Get computation bits
        :return: comp: string
        """
        self.comp=self.parser.comp()
        return self.comp
    def jump(self):
        """
        Get jump bits
        :return: jump: string
        """
        self.jump=self.parser.jump()
        return self.jump

