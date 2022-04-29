"""
Main that controls how the the classes interact with each other
"""

from typing import BinaryIO

from symbolTable import symbolTable
from parser import Parser
from checkOutput import checkOutputs
from code import Code


def intialPass(filePath):
    """
    First pass through asm file to build symbol table with labels only
    :return: symbolTable object
    """
    parser2=Parser(filePath)
    commandCounter=1
    symbolTable1=symbolTable()

    while parser2.file.closed == False:
        # skip empty lines and comments
        parser2.advance()
        parser2.command = parser2.futureCommand

        if parser2.findCommandType()=="L_COMMAND":
            parser2.command=parser2.command.replace(")","")
            parser2.command=parser2.command.replace("(","")
            # Add a label entry in symbol table
            symbolTable1.addEntry(symbol=parser2.command.strip(),address=commandCounter)
        elif parser2.findCommandType()=="A_COMMAND"or parser2.findCommandType()=="C_COMMAND":
            commandCounter += 1
    return symbolTable1

def addUserDefinedVariables(symbolTable1, filePath):
    """
    Pass through the file to add user defined labels to the symbol table
    :return: symbolTable object: symbolTable with user-defined labels
    """
    parser4 = Parser(filePath)
    userDefinedAddress = 16
    while parser4.file.closed == False:
        parser4.advance()
        if parser4.findCommandType() == "A_COMMAND" or parser4.findCommandType() == "C_COMMAND":
            command = parser4.symbol()
            # if the command is not an A or L command and not in the symbol table
            if command != None and symbolTable1.contains(command) == False:
                symbolTable1.addEntry(symbol=command.replace("@", ""), address=userDefinedAddress)
                userDefinedAddress += 1
            parser4.command = parser4.futureCommand
        else:
            # skip when label is found
            parser4.command = parser4.futureCommand
            continue
    return symbolTable1

def secondPass(symbolTable1,filePath):
    """
    Second pass through the program
    Replace all A commands to labels with their decimal values from symbol table
    """
    parser3=Parser(filePath)
    symbolfile = open("outPut/symbolFile.asm", 'w')
    while parser3.file.closed == False:
        parser3.advance()
        parser3.removeComment()
        if parser3.findCommandType() == "A_COMMAND":
            command = parser3.command.replace("@", "").strip()
            if symbolTable1.contains(command):
                symbolAddress=symbolTable1.getAddress(command)
                new_command="@"+str(symbolAddress)+"\n"
                symbolfile.write(new_command)
                parser3.command = parser3.futureCommand
            else:
                symbolfile.write(parser3.command.strip()+"\n")
                parser3.command = parser3.futureCommand
        elif parser3.findCommandType() == "C_COMMAND":
            symbolfile.write(parser3.command.strip()+"\n")
            parser3.command = parser3.futureCommand
        else:
            # skip labels
            parser3.command=parser3.futureCommand

def main():
    """second pass through the list to retrieve values for labels and user defined variables
    and add them to the symbolFile.asm"""
    filePaths=["Add","Max","MaxL","Pong","PongL","Rect","RectL"]
    comparePaths=["Add","Max","MaxL","Pong","PongL","Rect","RectL"]
    for i in range(len(filePaths)):
        path=filePaths[i]
        comparePath=comparePaths[i]
        # construct the path to the file to read from
        filePath = "asmFiles/"+path+".asm"
        # Add labels to the symbol table
        symbolTable1=intialPass(filePath=filePath)
        # Add user defined variables to symbol table
        symbolTableWithVars=addUserDefinedVariables(symbolTable1,filePath)
        # Pass through the file and replace all symbols with decimal values
        secondPass(symbolTableWithVars,filePath)
        # Input is now from updated file
        inputFilePath="outPut/symbolFile.asm"
        # File to store final outputs
        outPutPath="outPut/"+path+".hack"
        outPutfile = open(outPutPath, 'w')  # type: BinaryIO

        # create parser
        parser1 = Parser(inputFilePath)
        # advance to start of instruction and run until we can not advance
        while parser1.file.closed == False:
            parser1.advance()
            if parser1.findCommandType() == "A_COMMAND":
                # # if A command is user defined
                # if parser1.symbol():
                #     constantDecimal = int(symbolTable1.symbolTable[parser1.symbol()])
                # # if A command is constant
                # else:
                constantDecimal = int(parser1.command.strip().replace("@",""))
                # convert to binary
                binary = bin(constantDecimal).replace("0b", "")
                paddingString = ""
                for i in range(len(binary), 16):
                    paddingString += "0"
                finalABinary = paddingString + binary
                # To append to end of opened output file
                outPutfile.write(finalABinary + "\n")
                parser1.command=parser1.futureCommand
            elif parser1.findCommandType() == "C_COMMAND":
                # make instance of code class
                code1 = Code(parser1)
                # get computation bits
                compBin = code1.comp()
                # get destination bits
                if ";" in parser1.command:
                    destBin="000"
                else:
                    destBin = code1.dest()
                # get jump bits
                jumpBin = code1.jump()
                # construct final C instruction
                finalCBinary = "111" + parser1.aBit + compBin + destBin + jumpBin
                # To append to end of opened file
                outPutfile.write(finalCBinary + "\n")
                parser1.command = parser1.futureCommand
        outPutfile.close()
        # compare output with expected hack translation
        compareFile="compare/"+comparePath+".hack"
        checkOutputs(outPutPath,compareFile)

if __name__=="__main__":
    main()