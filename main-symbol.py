"""an assembler with symbol table"""
from typing import BinaryIO

from symbolTable import symbolTable
from parser import Parser
from main import checkOutputs
from code import Code


def intialPass(filePath):
    print("WITH NO VARS RUNNING")
    """first pass through code to build symbol table with labels only"""
    parser2=Parser(filePath)
    commandCounter=1
    userDefinedAddress=16
    symbolTable1=symbolTable()
    # print("INITAL PASS)")
    # parser2.advance()
    # parser2.command = parser2.futureCommand
    while parser2.file.closed == False:
        # skip empty lines and comments
        print("advancing in initial pass", parser2.command)
        parser2.advance()
        parser2.command = parser2.futureCommand
        # print("setting new command in initial pass", parser2.command)
        # print("initial pass command",parser2.command)
        if parser2.findCommandType()=="L_COMMAND":
            parser2.command=parser2.command.replace(")","")
            parser2.command=parser2.command.replace("(","")
            # print("L_command counter",parser2.command.strip(), commandCounter)
            symbolTable1.addEntry(symbol=parser2.command.strip(),address=commandCounter)
            # parser2.advance()
            # print("inital pass : comment", parser2.command, "future:", parser2.futureCommand)
        elif parser2.findCommandType()=="A_COMMAND"or parser2.findCommandType()=="C_COMMAND":
            commandCounter += 1
            print("not L command",parser2.command.strip(),commandCounter)
            # commandCounter += 1

            # parser2.advance()
            # parser2.command=parser2.futureCommand
            # parser2.advance()
            # print("inital pass :comment", parser2.command, "future:", parser2.futureCommand)
        # else:
        #     print("in else")
        #     parser2.command = parser2.futureCommand
        # elif parser2.findCommandType()=="L_COMMAND":
        #     # remove the () from label
        #     # print("label found")
        #     parser2.command=parser2.command.replace(")","")
        #     parser2.command=parser2.command.replace("(","")
        #     print("L_command counter", commandCounter)
        #     symbolTable1.addEntry(symbol=parser2.command.strip(),address=commandCounter)
            # Do we actually need this?
    # print("initial pass", symbolTable1.symbolTable)
    return symbolTable1

def addUserDefinedVariables(symbolTable1, filePath):
    """Pass through the file to add user defined labels to the symbol table """
    print("WITH VARS RUNNING")
    parser4 = Parser(filePath)
    userDefinedAddress = 16
    while parser4.file.closed == False:
        parser4.advance()
        if parser4.findCommandType() == "A_COMMAND" or parser4.findCommandType() == "C_COMMAND":
            command = parser4.symbol()
            print("A_C Command", command, userDefinedAddress, symbolTable1.contains(command))
            if command != None and symbolTable1.contains(command) == False:
                print("adding constant to symbol table",command)
                symbolTable1.addEntry(symbol=command.replace("@", ""), address=userDefinedAddress)
                userDefinedAddress += 1
            # elif parser4.findCommandType() == "A_COMMAND":
            #     # Non user-defined A commands
            parser4.command = parser4.futureCommand
        else:
            # skip when label is found
            parser4.command = parser4.futureCommand
            continue
    # print("inside add user vars",symbolTable1.symbolTable)
    return symbolTable1

def secondPass(symbolTable1,filePath):
    """
    Second pass through the program
    Replace all A commands to labels with their decimal values from symbol table
    """
    print("SECOND PASS")
    parser3=Parser(filePath)
    symbolfile = open("outPut/symbolFile.asm", 'w')
    while parser3.file.closed == False:
        parser3.advance()
        parser3.removeComment()
        print("second pass command",parser3.command)
        if parser3.findCommandType() == "A_COMMAND":
            command = parser3.command.replace("@", "").strip()
            print("A_command", command, symbolTable1.contains(command))
            if symbolTable1.contains(command):
                symbolAddress=symbolTable1.getAddress(command)
                new_command="@"+str(symbolAddress)+"\n"
                # print(new_command)
                symbolfile.write(new_command)
                parser3.command = parser3.futureCommand
            else:
                symbolfile.write(parser3.command.strip()+"\n")
                parser3.command = parser3.futureCommand
        elif parser3.findCommandType() == "C_COMMAND":
            symbolfile.write(parser3.command.strip()+"\n")
            parser3.command = parser3.futureCommand
        else:
            print("label found", parser3.command,parser3.futureCommand)
            parser3.command=parser3.futureCommand








def main():
    """second pass through the list to retrieve values for labels and user defined variables
    and add them to the symbolFile.asm"""
    filePaths=["Add","Max","MaxL","Pong","PongL","Rect","RectL"]
    comparePaths=["Add","Max","MaxL","Pong","PongL","Rect","RectL"]
    for i in range(len(filePaths)):
        path=filePaths[i]
        comparePath=comparePaths[i]
        filePath = "asmFiles/"+path+".asm"
        symbolTable1=intialPass(filePath=filePath)
        print("symbolTable with no vars",symbolTable1.symbolTable)
        symbolTableWithVars=addUserDefinedVariables(symbolTable1,filePath)
        print("symbolTable with vars", symbolTableWithVars.symbolTable)
        secondPass(symbolTableWithVars,filePath)
        inputFilePath="outPut/symbolFile.asm"
        outPutfile = open("outPut/Prog.hack", 'w')  # type: BinaryIO
        print("MAIN CALL")
        # create parser
        parser1 = Parser(inputFilePath)
        # advance to start of instruction and run until we can not advance
        while parser1.file.closed == False:
            # previousCommand= parser1.command
            # print("previous",previousCommand)
            parser1.advance()
            if parser1.findCommandType() == "A_COMMAND":
                if parser1.symbol():
                    constantDecimal = int(symbolTable1.symbolTable[parser1.symbol()])
                else:
                    constantDecimal = int(parser1.command.strip().replace("@",""))
                binary = bin(constantDecimal).replace("0b", "")
                paddingString = ""
                for i in range(len(binary), 16):
                    paddingString += "0"
                finalABinary = paddingString + binary
                print(finalABinary)
                # To append to end of opened file
                outPutfile.write(finalABinary + "\n")
                parser1.command=parser1.futureCommand
                # parser1.advance()
                # parser1.removeComment()
                # Removes repeated command for infinite looping at the end
                # if parser1.command.strip()==previousCommand.strip():
                #     parser1.advance()
            elif parser1.findCommandType() == "C_COMMAND":
                # make instance of code class
                code1 = Code(parser1)
                compBin = code1.comp()
                if ";" in parser1.command:
                    destBin="000"
                else:
                    destBin = code1.dest()
                jumpBin = code1.jump()
                print("abit",parser1.aBit,"compBin", compBin, "destBin", destBin, "jump", jumpBin)
                finalCBinary = "111" + parser1.aBit + compBin + destBin + jumpBin
                print(finalCBinary)
                # To append to end of opened file
                outPutfile.write(finalCBinary + "\n")
                parser1.command = parser1.futureCommand
                # parser1.advance()
                # parser1.removeComment()
                # Removes repeated command for infinite looping at the end
                # if parser1.command.strip()==previousCommand.strip():
                #     parser1.advance()
            # else:
            #     print("I am skipping",parser1.command)
            #     parser1.advance()
            #     parser1.removeComment()
        outPutfile.close()
        compareFile="compare/"+comparePath+".hack"
        checkOutputs("outPut/Prog.hack",compareFile)

if __name__=="__main__":
    main()