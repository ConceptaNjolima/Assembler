"""an assembler with symbol table"""
from typing import BinaryIO

from symbolTable import symbolTable
from parser import Parser
from main import checkOutputs
from code import Code


def intialPass():
    print("WITH NO VARS RUNNING")
    """first pass through code to build symbol table"""
    filepath="asmFiles/Max.asm"
    parser2=Parser(filepath)
    commandCounter=0
    userDefinedAddress=16
    symbolTable1=symbolTable()
    # print("INITAL PASS)")
    while parser2.file.closed == False:
        # skip empty lines and comments
        parser2.advance()
        # print("initial pass command",parser2.command)
        if parser2.findCommandType()=="L_COMMAND":
            # remove the () from label
            # print("label found")
            parser2.command=parser2.command.replace(")","")
            parser2.command=parser2.command.replace("(","")
            print("L_command counter",parser2.command.strip(), commandCounter)
            symbolTable1.addEntry(symbol=parser2.command.strip(),address=commandCounter)
        elif parser2.findCommandType()=="A_COMMAND"or parser2.findCommandType()=="C_COMMAND":
            print("not L command",parser2.command.strip(),commandCounter)
            commandCounter+=1
            # else:
            #     commandCounter+=1
        # elif parser2.findCommandType()=="L_COMMAND":
        #     # remove the () from label
        #     # print("label found")
        #     parser2.command=parser2.command.replace(")","")
        #     parser2.command=parser2.command.replace("(","")
        #     print("L_command counter", commandCounter)
        #     symbolTable1.addEntry(symbol=parser2.command.strip(),address=commandCounter)
            # Do we actually need this?
    return symbolTable1

def addUserDefinedVariables(symbolTable1):
    print("WITH VARS RUNNING")
    filepath = "asmFiles/Max.asm"
    parser4 = Parser(filepath)
    userDefinedAddress = 16
    while parser4.file.closed == False:
        parser4.advance()
        if parser4.findCommandType() == "A_COMMAND" or parser4.findCommandType() == "C_COMMAND":
            command = parser4.symbol()
            # notNumber=True
            print("A_C Command", command, userDefinedAddress, symbolTable1.contains(command))
            # try:
            #     intValue=int(command)
            # except:
            #     notNumber=False
            # if parser2.findCommandType()=="A_command" and command.isdigit():
            #     continue
            if command != None and symbolTable1.contains(command) == False:
                print("adding constant to symbol table",command)
                symbolTable1.addEntry(symbol=command.replace("@", ""), address=userDefinedAddress)
                userDefinedAddress += 1
    print("inside add user vars",symbolTable1.symbolTable)
    return symbolTable1

def secondPass(symbolTable1):
    """Second pass through the program"""
    filepath="asmFiles/Max.asm"
    parser3=Parser(filepath)
    # print("IN SECOND PASS")
    # print("in second Pass",symbolTable1.symbolTable)
    symbolfile = open("outPut/symbolFile.asm", 'w')
    while parser3.file.closed == False:
        parser3.advance()
        parser3.removeComment()
        # print("second pass command",parser3.command)
        if parser3.findCommandType() == "A_COMMAND":
            # command=parser3.command.replace("(","").replace(")","").replace("@","").strip()
            command = parser3.command.replace("@", "").strip()
            print("A_command", command, symbolTable1.contains(command))
            if symbolTable1.contains(command):
                symbolAddress=symbolTable1.getAddress(command)
                new_command="@"+str(symbolAddress)+"\n"
                # print(new_command)
                symbolfile.write(new_command)
                # continue
            else:
                symbolfile.write(parser3.command.strip()+"\n")
        elif parser3.findCommandType() == "C_COMMAND":
            # print("c-command second pass")
            symbolfile.write(parser3.command.strip()+"\n")
            # continue
        else:
            continue








def main():
    """second pass through """
    symbolTable1=intialPass()
    symbolTableWithVars=addUserDefinedVariables(symbolTable1)
    print("symbolTable with no vars",symbolTable1.symbolTable)
    print("symbolTable with vars", symbolTableWithVars.symbolTable)
    secondPass(symbolTableWithVars)
    inputFilePath="outPut/symbolFile.asm"
    outPutfile = open("outPut/Prog.hack", 'w')  # type: BinaryIO
    # create parser
    parser1 = Parser(inputFilePath)
    # advance to start of instruction and run until we can not advance
    while parser1.file.closed == False:
        # check command--To remove
        # parser1.command = "D=D+M"
        # parser1.advance()
        # parser1.removeComment()
        # This helps when the final command is repeated for infinite loop
        previousCommand= parser1.command
        print("previous",previousCommand)
        if parser1.findCommandType() == "A_COMMAND":
            # constantDecimal = int(symbolTable1.symbolTable[parser1.symbol()])
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
            parser1.advance()
            parser1.removeComment()
            # Removes repeated command for infinite looping at the end
            if parser1.command.strip()==previousCommand.strip():
                parser1.advance()
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
            parser1.advance()
            parser1.removeComment()
            # Removes repeated command for infinite looping at the end
            if parser1.command.strip()==previousCommand.strip():
                parser1.advance()
        else:
            parser1.advance()
            parser1.removeComment()
    outPutfile.close()

    # mainCall("outPut/symbolFile.asm")
    checkOutputs("outPut/Prog.hack","compare/Max.hack")

if __name__=="__main__":
    main()