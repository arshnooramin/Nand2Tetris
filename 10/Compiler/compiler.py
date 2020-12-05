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
        # start by compiling class
        self._handleClass()
        # write assembled code to xml file
        fh.writeXMLFile(self._filePath, self._codeList)

    # method to update code list
    def _write(self, code):
        xml = '\t'*self._level; xml += code
        self._codeList.append(xml)

    def _error(self):
        sys.exit(self._tk.token() + \
            " not a valid jack grammar")
    
    # method to write the basic token xml
    def _writeXML(self):
        xml = '\t'*self._level
        xml += "<{type}> {token} </{type}>\n"\
              .format(token=self._tk.token(),\
                      type=types[self._tk.type()])
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
        else: self._error()
        if self._tk.type() == IDENTIFIER:
            self._writeXML()
        else: self._error()
        if self._tk.token() == '{':
            self._writeXML()
        else: self._error()
        # handle any class variables
        self._handleClassVar()
        # handle class subroutines
        self._handleSubroutine()
        if self._tk.token() == '}':
            self._writeXML()
        self._level -= 1
        self._write("</class>\n")

    # handle the compilation of class variables
    def _handleClassVar(self):
        # handle protection type
        while (self._tk.token() == 'static' or \
               self._tk.token() == 'field'):
            self._write("<classVarDec>\n")
            self._level += 1
            self._writeXML()
            # handle variable type
            if (self._tk.token() in vartypes or \
                self._tk.type() == IDENTIFIER):
                self._writeXML()
            else: self._error()
            # handle variable name
            if self._tk.type() == IDENTIFIER:
                self._writeXML()
            else: self._error()
            # if multiple variable names
            while self._tk.token() == ',':
                self._writeXML()
                if self._tk.type() == IDENTIFIER:
                    self._writeXML()
                else: self._error()
            # handle semicolon
            if self._tk.token() == ';':
                self._writeXML()
            else: self._error()
            self._level -= 1
            self._write("</classVarDec>\n")

    # handle the compilation of class subroutines
    def _handleSubroutine(self):
        # handle the method, constructor, function
        while (self._tk.token() == 'constructor' or \
              self._tk.token() == 'method' or \
              self._tk.token() == 'function'):
            self._write("<subroutineDec>\n")
            self._level += 1
            # writes the type of subroutine
            self._writeXML()
            # handle output type
            if (self._tk.token() in vartypes or \
                self._tk.token() == 'void' or \
                self._tk.type() == IDENTIFIER):
                self._writeXML()
            else: self._error()
            # handle subroutine name
            if self._tk.type() == IDENTIFIER:
                self._writeXML()
            else: self._error()
            # handle params if any
            self._handleParam()
            # handle subroutine body
            if self._tk.token() == '{':
                self._write("<subroutineBody>\n")
                self._level += 1
                self._writeXML()
            else: self._error()
            # handle var declarations
            self._handleVar()
            # handle statments
            self._handleStatement()
            if self._tk.token() == '}':
                self._writeXML()
            self._level -= 1
            self._write("</subroutineBody>\n")
            self._level -= 1
            self._write("</subroutineDec>\n")

    def _handleParam(self):
        if self._tk.token() == '(':
            self._writeXML()
            self._write("<parameterList>\n")
            self._level += 1
            while self._tk.token() != ')':
                # handle param type or name
                if (self._tk.token() in vartypes or \
                    self._tk.type() == IDENTIFIER or \
                    self._tk.token() == ','):
                    self._writeXML()
                else: self._error()
            # write closing bracket
            self._level -= 1
            self._write("</parameterList>\n")
            self._writeXML()
        else: self._error()
    
    def _handleVar(self):
        while self._tk.token() == 'var':
            self._write("<varDec>\n")
            self._level += 1
            self._writeXML
            # handle variable type
            if (self._tk.token() in vartypes or \
                self._tk.type() == IDENTIFIER):
                self._writeXML()
            else: self._error()
            # handle variable name
            if self._tk.type() == IDENTIFIER:
                self._writeXML()
            else: self._error()
            # if multiple variable names
            while self._tk.token() == ',':
                self._writeXML()
                if self._tk.type() == IDENTIFIER:
                    self._writeXML()
                else: self._error()
            # handle semicolon
            if self._tk.token() == ';':
                self._writeXML()
            else: self._error()
            self._level -= 1
            self._write("</varDec>\n")

    def _handleStatement(self):
        # handle multiple statements
        while self._tk.token() != '}':
            # if statement is a let statement
            if self._tk.token() == 'let':
                self._handleLet()
            elif self._tk.token() == 'if':
                self._handleIf()
            elif self._tk.token() == 'while':
                self._handleWhile()
            elif self._tk.token() == 'do':
                self._handleDo()
            elif self._tk.token() == 'return':
                self._handleReturn()
    
    def _handleLet(self):
        pass

    def _handleIf(self):
        pass

    def _handleWhile(self):
        pass

    def _handleDo(self):
        pass

    def _handleReturn(self):
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