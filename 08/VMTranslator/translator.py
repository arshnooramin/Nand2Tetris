import sys
from ctypes import *
from fhandler import FileHandler as fh
from cformat import CFormatter

# the main assembler script that converts asm to hack
class Translator:
    # constructor takes file path as argument
    def __init__(self, filePath, cf):
        # path to the asm file
        self._filePath = filePath
        # file read object
        self._f = open(filePath, 'r')
        # list of hack code w/ line as elem
        self._codeList = []
        # the code formatter object
        self._cf = cf
    
    # handle and add init code to the list
    def handleInit(self):
        # write the init code
        outStr = self._cf.writeInitAsm() + \
            self._cf.writeCallAsm("Sys.init", 0)
        # add it to code list
        self._codeList.append(outStr)
    
    # translate the .vm code by parsing
    def translate(self):
        # assemble the code
        self.parse()
        # write assembled code to .asm file
        fh.writeAsmFile(self._filePath, self._codeList)
    
    # parse through the code, remove unwanted chars
    def parse(self):
        for line in self._f:
            # remove the newline char '\n'
            line = line.strip()
            # check if there is parseable code in line
            if not fh.isCommentOrEmpty(line):
                writeStr = ""
                # remove in-line comments from each line
                line = fh.removeInlineComments(line)
                # split commands from the line
                commands = line.split(" ")
                # get the type of command
                cmdtype = self._cf.commandType(commands[0])
                # if it's a push or pop command handle it
                if cmdtype == PUSH or cmdtype == POP:
                    writeStr = self._handlePushPop(commands, cmdtype)
                # else if it's a arithmetic command handle it
                elif cmdtype == ARITHMETIC:
                    writeStr = self._handleArithmetic(commands)
                # else if it's a label command handle it
                elif cmdtype == LABEL:
                    writeStr = self._cf.writeLabelAsm(commands[1])
                # else if it's a goto command handle it
                elif cmdtype == GOTO:
                    writeStr = self._cf.writeGotoAsm(commands[1])
                # else if it's a if-goto command handle it
                elif cmdtype == IF:
                    writeStr = self._cf.writeIfGotoAsm(commands[1])
                # else if it's a call command handle it
                elif cmdtype == CALL:
                    writeStr = self._cf.writeCallAsm(commands[1], int(commands[2]))
                # else if it's a return command handle it
                elif cmdtype == RETURN:
                    writeStr = self._cf.writeReturnAsm()
                # else if it's a function command handle it
                elif cmdtype == FUNCTION:
                    writeStr = self._cf.writeFunctionAsm(commands[1], int(commands[2]))
                # add it to the code list
                self._codeList.append(writeStr)
                print(line)
                print(self._codeList)
    
    # handle the arithmetic commands in line
    def _handleArithmetic(self, commands):
        outStr = ""
        # get the type of arithmetic command
        arithtype = self._cf.arithmeticType(commands[0])
        # if it's a normal operator write asm code for it
        if arithtype == BI_OP:
            outStr = self._cf.writeOpAsm(commands[0])
        # if it's a unary operator write asm code for it
        elif arithtype == UN_OP:
            outStr = self._cf.writeUnaryAsm(commands[0])
        # if it's a comparator write asm code for it
        elif arithtype == COMP:
            outStr = self._cf.writeCompAsm(commands[0])
        return outStr
    
    # handle the push/pop commands in line
    def _handlePushPop(self, commands, ptype):
        outStr = ""
        segment = commands[1]; index = int(commands[2])
        segtype = self._cf.pushPopType(segment)
        # if it's a group 1 command write asm code for it
        if segtype == GROUP_1:
            outStr = self._cf.writePushPopAsm1(ptype, segment, index)
        elif segtype == STATIC:
            outStr = self._cf.writeStaticPushPopAsm(fh.getVmFileName(self._filePath), ptype, index)
        # if it's a group 2 command write asm code for it
        elif segtype == GROUP_2:
            outStr = self._cf.writePushPopAsm2(ptype, segment, index)
        # if it's a constant command write asm code for it
        elif segtype == CONSTANT:
            outStr = self._cf.writeConstantPushPopAsm(index)
        return outStr

    # getter method for codelist attribute
    def getCodeList(self):
        return self._codeList

# main/executable section of the code
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(".vm file path not provided")
    
    fileDir = sys.argv[1]

    # check to see if the directory is valid
    if not fh.dirExists(fileDir):
        sys.exit("Incorrect file directory!")

    # get the file paths for all vm files in directory
    filePaths = fh.getVmFiles(fileDir)

    # the cformatter object
    cf = CFormatter()

    # intialize the code list for each file
    codeList = []
    # iterate over each file path
    for i, filePath in enumerate(filePaths):
        tr = Translator(filePath, cf)
        if i == 0:
            tr.handleInit()
        # assemble the code
        tr.parse()
        # store current codelist in the combined one
        codeList += tr.getCodeList()

    # write assembled code to .asm file
    fh.writeAsmFile(fileDir, codeList)




    
