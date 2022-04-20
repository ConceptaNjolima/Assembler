def createSymbolTable():
    pass
def parseInput(filePath):
    #Open the asm file passed in as path
    fileRead=open(filePath,'r')
    lines=fileRead.readlines()
    resultWrite = open("read.txt", "w")
    for line in lines:
        # For each line, try translating it as A or C instruction
        resultWrite.write(line)
    fileRead.close()
    resultWrite.close()

def translateA(instruction):
    # convert the decimal to binary
    pass
def translateC(instruction):
    # Check if contains jump
    # separate the two section, compute part and jump part
    pass
def translateInstruction(instruction):
    if "@" in instruction:
        #remove the @ symbol
        translateA(instruction[1:])
    else:
        #remove the first three parts of the instruction
        translateC(instruction[3:])
    pass
def main():
    filePath="~/Users/conceptanjolima/Desktop/nand2tetris/projects/06/add"
    #parseInput(filePath)
    fileRead = open(filePath, 'r')
    lines = fileRead.readlines()
    print("lines",lines)

main()
