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
        self.futureCommand=""
        self.aBit="0"
    def hasMoreCommands(self):
        """Checks if input has more commands"""
        # try:
        #     # self.futureCommand=self.file.next()
        #     # print("comment",self.command,"future:",self.futureCommand)
        #     # print(self.comment.strip().find("/"))
        #     # self.command = self.futureCommand.strip()
        #     # print("no comment",self.command)
        #     # return True
        #     commandIndex=self.command.strip().find("/")
        #     print("start command:",self.command)
        #     while commandIndex<=0:
        #         # Move to next line
        #         print("comment or empty line found:",self.command,"index",commandIndex,"future:",self.futureCommand)
        #         self.command=self.futureCommand.strip()
        #         self.futureCommand = self.file.next()
        #         commandIndex=self.command.strip().find("/")
        #     if commandIndex>0:
        #         print("command not comment:",self.command,"index",commandIndex)
        #         self.command=self.command[:commandIndex]
        #         self.futureCommand=self.futureCommand[:commandIndex]
        #         print("future comment with comment removed",self.command)
        #     # print("command",commandIndex,"future:",self.futureCommand)
        #     return  True
        # except:
        #     print("exception raised")
        #     return False

        previousLine=""
        try:
            # check for comments is broken
            self.futureCommand = self.file.next()
            self.command=self.command.strip()
            # print("command at start",self.command)
            while "//" in self.command or self.command=="" or self.command=="\r\n":
                # previousLine=self.command
                # print("comment", self.command, "future:", self.futureCommand)
                if self.command=="" or self.command=="\r\n":
                    print("empty line found")
                    # self.futureCommand = self.file.next()
                    self.command = self.futureCommand
                    self.futureCommand = self.file.next()
                    continue
                else:
                    commandIndex = self.command.strip().index("//")
                    print("comment index", commandIndex)
                    if commandIndex==0:
                        print("left out", self.command.strip())
                        self.command=self.futureCommand
                        self.futureCommand = self.file.next()
                    else:
                        commandLeft=self.command.strip()
                        print("command left",commandLeft[0:commandIndex])
                        self.command=self.command.strip()[0:commandIndex]
                        # self.futureCommand = self.file.next()
                        return True
                # else:
                #     # Is empty line
                #     self.command = self.futureCommand
                #     return True
            # self.futureCommand = self.file.next()
            # print(" outside while: comment", self.command, "future:", self.futureCommand)
            # print("outside while")
            return True
        except:
            return False

    def advance(self):
        """
        Check if the file has more commands.
        :return: command: string
        """
        # line=self.command
        self.removeComment()
        if self.hasMoreCommands():
            print("advanced command",self.command)
            return self.command.strip()
        else:
            print("closing file")
            self.file.close()
            return self.futureCommand.strip()
    def findCommandType(self):
        """
        Determines if the command is A, C or L command
        :return: string
        """
        if "@" in self.command:
            return "A_COMMAND"
        elif "=" in self.command or ";" in self.command:
            return "C_COMMAND"
        elif "(" and ")" in self.command:
            return "L_COMMAND"

    def symbol(self):
        """Returns symbols or decimal of current symbol"""
        if self.findCommandType()=="A_COMMAND":
            symbol=self.command.strip().replace("@","")
            # print("in symbol",symbol,symbol.isdigit())
            # if the A command is a constant
            if symbol.isdigit()==False:
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
        """
        Assign the values for the destination bits from the command
        :return: string
        """
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
        """
        Assign the computation bits from the command
        :return: string
        """
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
        """
        Return the jump mnemonic
        :return:string
        """
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








