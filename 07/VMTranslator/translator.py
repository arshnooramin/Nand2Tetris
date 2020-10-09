import sys
from ctypes import *
from fhandler import FileHandler as fh
from cformat import CFormatter as cf

# the main assembler script that converts asm to hack
class Translator:
    # constructor takes file path as argument
    def __init__(self, filePath):
        # path to the asm file
        self._filePath = filePath
        # file read object
        self._f = open(filePath, 'r')
        # list of hack code w/ line as elem
        self._codeList = []
        # index to keep track of all the jumps
        self._jmpNum = 0
    
    # translate the .vm code by parsing
    def translate(self):
        # aseemble the code
        self.parse()
        # write assembled code to .hack file
        fh.writeAsmFile(self._filePath, self._codeList)
    
    # parse through the code, remove unwanted chars
    def parse(self):
        for line in self._f:
            # remove the newline char '\n'
            line = line.strip()
            # check if there is parseable code in line
            if not fh.isCommentOrEmpty(line):
                line = fh.removeInlineComments(line)
                # split commands from the line
                commands = line.split(" ")
                # get the type of command
                cmdtype = cf.commandType(commands[0])
                # if it's a push or pop command handle it
                if cmdtype == PUSH or cmdtype == POP:
                    self._handlePushPop(commands, cmdtype)
                # else if it's a arithmetic command handle it
                elif cmdtype == ARITHMETIC:
                    self._handleArithmetic(commands)
    
    # handle the arithmetic commands in line
    def _handleArithmetic(self, commands):
        outStr = ""
        # get the type of arithmetic command
        arithtype = cf.arithmeticType(commands[0])
        # if it's a normal operator handle it
        if arithtype == BI_OP:
            outStr = cf.writeOpAsm(commands[0])
        # if it's a unary operator handle it
        elif arithtype == UN_OP:
            outStr = cf.writeUnaryAsm(commands[0])
        # if it's a comparator handle it
        elif arithtype == COMP:
            outStr = cf.writeCompAsm(commands[0], self._jmpNum)
            self._jmpNum += 1
        self._codeList.append(outStr)
    
    # handle the push/pop commands in line
    def _handlePushPop(self, commands, ptype):
        outStr = ""
        if ptype == PUSH:
            outStr = cf.writePushAsm(commands[0], commands[1], commands[2])
        elif ptype == POP:
            outStr = cf.writePopAsm(commands[0], commands[1], commands[2])
        self._codeList.append(outStr)

# main/executable section of the code
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(".vm file path not provided")
    
    filePath = sys.argv[1]

    # check to see if valid asm was provided
    if (not fh.fileExists(filePath)) or \
       (not fh.isVmFile(filePath)):
        sys.exit("Incorrect .vm file path")

    tr = Translator(filePath)
    tr.translate()



    
