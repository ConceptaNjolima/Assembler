import filecmp
import os.path
from difflib import Differ
import filecmp
from parser import Parser
from code import Code
#
def checkOutputs(filePath1,filePath2):
    #     # This needs checking
    # print(checkOutputs("Prog.hack","add-result.hack"))
    print(filecmp.cmp("outPut/Prog.hack", "compare/add-result.hack"))

    # To ask: Why are these not equal?
    with open('outPut/Prog.hack') as file_1, open('compare/add-result.hack') as file_2:
        differ = Differ()
        print(file_1.readlines())
        print(file_2.readlines())
        for line in differ.compare(file_1.readlines(), file_2.readlines()):
            print(line)



def main():
    # path to asm file
    filePath= "asmFiles/Add.asm"
    # open outpu file
    outPutfile=open("outPut/Prog.hack", 'w')
    # create parser
    parser1 = Parser(filePath)
    # advance to start of instruction and run until we can not advance
    while parser1.file.closed==False:
        # check command--To remove
        # parser1.command = "D=D+M"
        if parser1.findCommandType()=="A_COMMAND":
            constantDecimal=int(parser1.symbol())
            binary=bin(constantDecimal).replace("0b","")
            paddingString=""
            for i in range(len(binary),16):
                paddingString+="0"
            finalABinary=paddingString+binary
            print(finalABinary)
            # To append to end of opened file
            outPutfile.write(finalABinary+"\n")
            parser1.advance()
        elif parser1.findCommandType()=="C_COMMAND":
            # make instance of code class
            code1 = Code(parser1)
            compBin=code1.comp()
            destBin=code1.dest()
            jumpBin=code1.jump()
            print("compBin",compBin,"destBin",destBin,"jump",jumpBin)
            finalCBinary="111"+parser1.aBit+compBin+destBin+jumpBin
            print(finalCBinary)
            # To append to end of opened file
            outPutfile.write(finalCBinary + "\n")
            parser1.advance()
        else:
            parser1.advance()
    outPutfile.close()







    # print(parser1.lines)
    # print('advance from',parser1.advance())
    # # print("command_type:",parser1.findCommandType())
    # print("decimal",parser1.symbol())
    # # while parser1.hasMoreCommands():
    # #     print(parser1.command)
    # parser1.command="D=D+M"
    # code1=Code(parser1)
    # code1.dest()
    # code1.comp()
    # code1.jump()


if __name__=="__main__":
    main()