import sys
from ctypes import *
from fhandler import FileHandler as fh
from tokenizer import Tokenizer

# the main compiler class that converts jack tokens to xml
class Compiler:
    # constructor takes file path as argument
    def __init__(self, filePath):
        # instantiate tokenizer class
        self._tk = Tokenizer(filePath)
        # path to the jack file
        self._filePath = filePath
        # list of xml code w/ line as elem
        self._codeList = []
        # the parse tree level for indentation
        self._level = 0
    
    # compile the jack code by parsing
    def compile(self):
        # start by compiling class then make recursive calls
        self._handleClass()
        # write assembled code to xml file
        fh.writeXMLFile(self._filePath, self._codeList)

    # method to update code list
    def _write(self, code):
        xml = '\t'*self._level; xml += code
        self._codeList.append(xml)

    @staticmethod
    def _error():
        sys.exit("incorrect jack grammar")
    
    # method to write the basic token xml
    def _writeXML(self):
        xml = '\t'*self._level
        xml += "<{type}> {token} <{type}>\n"\
              .format(token=self._tk.token(),\
                      type=types[self._tk.tktype()])
        self._codeList.append(xml)
        self._tk.next()
    
    # handle compilation of a complete jack class
    def _handleClass(self):
        self._write("<class>\n")
        self._level += 1
        # check if the required grammar is correct
        if self._tk.token() == 'class':
            self._writeXML()
        # else exit with error
        else: Compiler._error()
        if self._tk.tktype() == IDENTIFIER:
            self._writeXML()
        else: Compiler._error()
        if self._tk.token() == '{':
            self._writeXML()
        else: Compiler._error()
        # handle any class variables recursively
        self._handleClassVar()
        # handle class subroutines
        self._handleSubRoutine()

    # handle the compilation of class variables
    def _handleClassVar(self):
       pass

    # handle the compilation of class subroutines
    def _handleSubRoutine(self):
       pass

# main/executable section of the code
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(".jack file path not provided")
    
    filePath = sys.argv[1]

    # check to see if valid jack file was provided
    if (not fh.fileExists(filePath)) or \
       (not fh.isJackFile(filePath)):
        sys.exit("Incorrect .jack file path")

    cp = Compiler(filePath)
    cp.compile()