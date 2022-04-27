chunkFile = open("asmFiles/chunk.asm", 'w')
readFile=open("asmFiles/Pong.asm","r")
for i in range(1000):
    chunkFile.write(readFile.next())
chunkFile.close()
readFile.close()

chunkOutFile = open("compare/chunk.hack", 'w')
readFile=open("compare/Pong.hack","r")
for i in range(1000):
    chunkOutFile.write(readFile.next())
chunkOutFile.close()
readFile.close()

