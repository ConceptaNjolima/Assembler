import filecmp
import os.path
from difflib import Differ
import filecmp
from parser import Parser
from code import Code

def checkOutputs(filePath1,filePath2):
    """
    Check if two files have the same content
    """
    print(filecmp.cmp(filePath1, filePath2))
    with open(filePath1) as file_1, open(filePath2) as file_2:
        differ = Differ()
        # for line in differ.compare(file_1.readlines(), file_2.readlines()):
        #     print(line)
