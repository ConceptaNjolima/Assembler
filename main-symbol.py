"""an assembler with symbol table"""
from symbolTable import symbolTable
from parser import Parser
def intialPass():
    """first pass through code to build symbol table"""
    filepath="asmFiles/Max.asm"
    parser2=Parser(filepath)
    commandCounter=0
    symbolTable1=symbolTable()
    print("INITAL PASS)")
    while parser2.file.closed == False:
        # skip empty lines and comments
        parser2.advance()
        if parser2.findCommandType()=="A_COMMAND" or parser2.findCommandType()=="C_COMMAND" :
            commandCounter+=1
        elif "(" in parser2.command and ")" in parser2.command:
            # remove the () from label
            parser2.command=parser2.command.replace(")","")
            parser2.command=parser2.command.replace("(","")
            symbolTable1.addEntry(symbol=parser2.command.strip(),address=commandCounter)
        else:
            # Do we actually need this?
            parser2.advance()
    return symbolTable1

def secondPass(symbolTable1):
    """Second pass through the program"""
    filepath="asmFiles/Max.asm"
    parser3=Parser(filepath)
    RAM_address=16
    print("IN SECOND PASS")
    print("in second Pass",symbolTable1.symbolTable)
    while parser3.file.closed == False:
        parser3.advance()
        if parser3.findCommandType() == "A_COMMAND":
            command=parser3.command.replace("(","").replace(")","").replace("@","").strip()
            print("A_command", command, symbolTable1.contains(command))
            if symbolTable1.contains(command):
                print(symbolTable1.getAddress(command))
                parser3.command=symbolTable1.getAddress(command)
            else:
                # Be ware of shallow copies- might want to move this to initial pass so that no lists are passed around
                symbolTable1.addEntry(command.strip(),RAM_address)
                print("in second Pass",command.strip(), symbolTable1.symbolTable)
                RAM_address+=1









def main():
    """second pass through """
    symbolTable1=intialPass()
    print(symbolTable1)
    secondPass(symbolTable1)

if __name__=="__main__":
    main()