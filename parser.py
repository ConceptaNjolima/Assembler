import os.path


class Parser():
    """
    Reads an assembly language command,parses it, and accesses symbols and fields
    """
    def __init__(self,filePath):
        self.file=open(filePath,'r')
        self.filePath=filePath
        # self.lines=self.file.readlines()
        self.command=self.file.readline()
        self.aBit="0"
    def hasMoreCommands(self):
        """Checks if input has more commands"""
        # check THIS~!
        previousLine=""
        try:
            # check for comments is broken
            while "//" in self.command or self.command=="\r\n":
                # print("current command", self.command)
                # print(self.command.strip())
                # skip comments
                previousLine=self.command

                # commandIndex=nextLine.strip().index("//")
                # print(commandIndex)
                # # if comment is at start of line
                # if commandIndex==0:
                #     nextLine=self.file.next()
                #     print("left out", previousLine)
                # else:
                #     self.command=nextLine[0:commandIndex]
                #     break
                self.command = self.file.next()
                if "//" in self.command:
                    commandIndex = self.command.index("//")
                    if commandIndex==0:
                        # print("left out", self.command.strip())
                        continue
                    else:
                        commandLeft=self.command.strip()
                        # print("comment index",commandIndex)
                        self.command=self.command.strip()[0:commandIndex]
                        return True
                else:
                    return True
            self.command = self.file.next()
            return True
            # return True
        # self.command=nextLine
            # if self.command:
            #     # print("hasMorecommand= ", True)
            # return True
            # except StopIteration:
            #     return
        except:
            return False

    def advance(self):
        # line=self.command
        if self.hasMoreCommands():
            # nextCommand=line
            # print("advanced command",self.command)
            return self.command.strip()
        else:
            print("closing file")
            self.file.close()
    def findCommandType(self):
        """Determines if A,C or L command"""
        if "@" in self.command:
            return "A_COMMAND"
        elif "=" in self.command or ";" in self.command:
            return "C_COMMAND"
        elif "(" and ")" in self.command:
            return "L_COMMAND"

    def symbol(self):
        """Returns symbols or decimal of current symbol"""
        print("in symbol",self.command)
        if self.findCommandType()=="A_COMMAND":
            symbol=self.command[1:]
            print("in symbol",symbol.strip())
            return symbol.strip()
        elif self.findCommandType()=="L_COMMAND":
            # remove opening bracket
            symbol=self.command.strip("(")
            # remove second bracket
            symbol=symbol.strip(")")
            return symbol
        else:
            return
    def dest(self):
        destinationDictionary = {'0': "000",
                                 'M': "001",
                                 'D': "010",
                                 'MD': "011",
                                 'A': "100",
                                 'AM': "101",
                                 'AD': "110",
                                 'AMD': "111"}
        if self.findCommandType()=="C_COMMAND":
            if "=" in self.command:
                comp_list = self.command.strip().split("=")
            else:
                comp_list=self.command.strip().split(";")
            # print(comp_list)
            return destinationDictionary[comp_list[0]]
        else:
            return destinationDictionary['null']
    def comp(self):
        """Returns mnemonic when command is a computer command"""
        specialCase = ["0", "1", "-1", "D", "!D", "D+1", "D-1", "-D"]
        aIsFalse = {'0': '101010',
                    '1': '111111',
                    '-1': '111010',
                    'D': '001100',
                    'A': '110000',
                    '!D': '001101',
                    '!A': '110001',
                    '-D': '001111',
                    '-A': '110011',
                    'D+1': '011111',
                    'A+1': '110111',
                    'D-1': '001110',
                    'A-1': '110010',
                    'D+A': '000010',
                    'D-A': '010011',
                    'A-D': '000111',
                    'D&A': '000000',
                    'D|A': '010101'}
        aIsTrue = {
            'M': '110000',
            '!M': '110001',
            '-M': '110011',
            'M+1': '110111',
            'M-1': '110010',
            'D+M': '000010',
            'D-M': '010011',
            'M-D': '000111',
            'D&M': '000000',
            'D|M': '010101'}
        # '0': '101010',
        # '1': '111111',
        # '-1': '111010',
        # 'D': '001100',
        # '!D': '001101',
        # '-D': '001111',
        # 'D+1': '011111',
        # 'D-1': '001110',
        if self.findCommandType()=="C_COMMAND" and "=" in self.command:
            comp_list=self.command.strip().split("=")
            # print(comp_list)
            # if a=1
            if "A" in comp_list[1] or comp_list[1] in specialCase:
                self.aBit="0"
                return (aIsFalse[comp_list[1]])
            elif "M" in comp_list[1]:
                self.aBit="1"
                return (aIsTrue[comp_list[1]])
            else:
                return("000000")
        if self.findCommandType()=="C_COMMAND" and ";" in self.command:
            # For jump commands
            comp_list = self.command.split(";")
            self.aBit="0"
            print(comp_list)
            return aIsFalse[comp_list[0]]

    def jump(self):
        """Return the jump mnemonic"""
        jumpDictionary = {'null': "000",
                          "JGT": "001",
                          "JEQ": "010",
                          "JGE": "011",
                          "JLT": "100",
                          "JNE": "101",
                          "JLE": "110",
                          "JMP": "111"}
        if self.findCommandType() == "C_COMMAND" and ";" in self.command:
            comp_list = self.command.strip().split(";")
            # print(comp_list)
            return jumpDictionary[comp_list[1]]
        else:
            return jumpDictionary['null']
    def removeComment(self):
        if "//" in self.command:
            commandIndex = self.command.index("//")
            self.command = self.command.strip()[0:commandIndex].replace(" ","")

# end of Parser class








