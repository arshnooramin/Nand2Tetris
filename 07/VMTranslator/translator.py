import sys
from ctypes import *
from fhandler import FileHandler as fh

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
    
    # translate the .vm code by parsing
    def translate(self):
        pass
        # # populate the symbol table w/ loop markers
        # self.parse(self._firstPass)
        # # aseemble the code
        # self.parse(self._secPass)
        # # write assembled code to .hack file
        # fh.writeAsmFile(self._filePath, self._codeList)
    
    # parse through the code, remove unwanted chars
    def _parse(self):
        pass
        # for line in self._f:
        #     # remove the newline char '\n'
        #     line = line.strip()
        #     # remove whitespaces from lines
        #     line = fh.removeSpaces(line)
        #     # check if there is parseable code in line
        #     if not fh.isCommentOrEmpty(line):
        #         # apply assembly logic to it
        #         asmLogicFunc(line)
        # # reset the file cursor to the start of file
        # self._f.seek(0)
    
    # handle the arithmetic commands in line
    def _handleArithmetic(self, line):
        pass
    
    # handle the push/pop commands in line
    def _handlePushPop(self, line):
        pass

# main/executable section of the code
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(".asm file path not provided")
    
    filePath = sys.argv[1]

    # check to see if valid asm was provided
    if (not fh.fileExists(filePath)) or \
       (not fh.isVmFile(filePath)):
        sys.exit("Incorrect .vm file path")

    vm = Translator(filePath)
    vm.translate()



    
