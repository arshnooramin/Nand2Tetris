import sys
from ctypes import *
from fhandler import FileHandler as fh
from tokenizer import Tokenizer

# corresponding strings for each type
types = [
    "keyword", "symbol", "integerConstant",
    "stringConstant", "identifier"
]

# valid variable types
vartypes = [
    "int", "boolean", "char"
]

# valid keyword constants
keywords = [
    "true", "false", "null", "this"
]

# valid operations
operations = [
    "+", "-", "*", "/", "&", "|", 
    "<", ">", "="
]

# the main compiler class that converts jack tokens to xml
class Analyzer:
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
        fh.writeXMLFile(self._filePath, self._codeList)
        sys.exit(self._tk.token() + " " + types[self._tk.type()] + \
            " not a valid jack grammar")
    
    # method to write the basic token xml
    def _writeXML(self):
        xml = '\t'*self._level
        token = ''
        # xml for '<', '>', '&'
        if self._tk.token() == '<':
            token = '&lt;'
        elif self._tk.token() == '>':
            token = '&gt;'
        elif self._tk.token() == '&':
            token = '&amp;'
        else:
            token = self._tk.token()
        xml += "<{type}> {token} </{type}>\n"\
              .format(token=token,\
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
            self._handleParamList()
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

    # handle the compilation of subroutine parameter list
    def _handleParamList(self):
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
    
    # handle compilation of variables
    def _handleVar(self):
        while self._tk.token() == 'var':
            self._write("<varDec>\n")
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
            self._write("</varDec>\n")

    # handle compilation of statement(s)
    def _handleStatement(self):
        self._write("<statements>\n")
        self._level += 1
        # handle multiple statements
        while self._tk.token() != '}':
            # if statement is a let statement
            if self._tk.token() == 'let':
                self._handleLet()
            # if statement is a if statement
            elif self._tk.token() == 'if':
                self._handleIf()
            # if statement is a while statement
            elif self._tk.token() == 'while':
                self._handleWhile()
            # if statement is a do statement
            elif self._tk.token() == 'do':
                self._handleDo()
            # if statement is a return statement
            elif self._tk.token() == 'return':
                self._handleReturn()
        self._level -= 1
        self._write("</statements>\n")
    
    # handle compilation of let statements
    def _handleLet(self):
        self._write("<letStatement>\n")
        self._level += 1
        self._writeXML()
        # handle variable name
        if self._tk.type() == IDENTIFIER:
            self._writeXML()
        else: self._error()
        # check if array entry
        if self._tk.token() == '[':
            self._writeXML()
            # expect a expression
            self._handleExpression()
            if self._tk.token() == ']':
                self._writeXML()
            else: self._error()
        # handle the '=' sign
        if self._tk.token() == '=':
            self._writeXML()
        else: self._error()
        # expect expression
        self._handleExpression()
        # handle semicolon
        if self._tk.token() == ';':
            self._writeXML()
        else: self._error()
        self._level -= 1
        self._write("</letStatement>\n")

    def _handleIf(self):
        self._write("<ifStatement>\n")
        self._level += 1
        self._writeXML()
        if self._tk.token() == '(':
            self._writeXML()
        else: self._error()
        # expect a expression
        self._handleExpression()
        if self._tk.token() == ')':
            self._writeXML()
        else: self._error()
        if self._tk.token() == '{':
            self._writeXML()
        else: self._error()
        # expect statement(s)
        self._handleStatement()
        if self._tk.token() == '}':
            self._writeXML()
        else: self._error()
        # if else statement present
        if self._tk.token() == 'else':
            self._writeXML()
            if self._tk.token() == '{':
                self._writeXML()
            else: self._error()
            # expect statement(s)
            self._handleStatement()
            if self._tk.token() == '}':
                self._writeXML()
            else: self._error()
        self._level -= 1
        self._write("</ifStatement>\n")

    def _handleWhile(self):
        self._write("<whileStatement>\n")
        self._level += 1
        self._writeXML()
        if self._tk.token() == '(':
            self._writeXML()
        else: self._error()
        # expect a expression
        self._handleExpression()
        if self._tk.token() == ')':
            self._writeXML()
        else: self._error()
        if self._tk.token() == '{':
            self._writeXML()
        else: self._error()
        # expect statement(s)
        self._handleStatement()
        if self._tk.token() == '}':
            self._writeXML()
        else: self._error()
        self._level -= 1
        self._write("</whileStatement>\n")

    def _handleDo(self):
        self._write("<doStatement>\n")
        self._level += 1
        self._writeXML()
        # look-ahead token
        self._tk.next()
        # expect a subroutine call
        if (self._tk.token() == '(' or \
            self._tk.token() == '.'):
            # go back to curr token
            self._tk.prev()
            self._handleCall()
        else: self._error()
        # handle semicolon
        if self._tk.token() == ';':
            self._writeXML()
        else: self._error()
        self._level -= 1
        self._write("</doStatement>\n")    

    def _handleReturn(self):
        self._write("<returnStatement>\n")
        self._level += 1
        self._writeXML()
        # if not semicolon
        if not self._tk.token() == ';':
            # expect expression
            self._handleExpression()
            # handle semicolon
            if self._tk.token() == ';':
                self._writeXML()
            else: self._error()
        else: self._writeXML()
        self._level -= 1
        self._write("</returnStatement>\n")

    def _handleExpression(self):
        self._write("<expression>\n")
        self._level += 1
        # expect a term
        self._handleTerm()
        # if there is a operation
        while self._tk.token() in operations:
            self._writeXML()
            # expect a term after operation
            self._handleTerm()
        self._level -= 1
        self._write("</expression>\n")

    def _handleTerm(self):
        self._write("<term>\n")
        self._level += 1
        # if curr token identifier
        if self._tk.type() == IDENTIFIER:
            # look-ahead token
            self._tk.next()
            # check if array entry
            if self._tk.token() == '[':
                # go back to curr token
                self._tk.prev()
                self._writeXML(); self._writeXML()
                # expect expression
                self._handleExpression()
                if self._tk.token() == ']':
                    self._writeXML()
                else: self._error()
            # check if subroutine call
            elif (self._tk.token() == '(' or \
                self._tk.token() == '.'):
                # go back to curr token
                self._tk.prev()
                self._handleCall()
            # else variable name
            else:
                # go back to curr token
                self._tk.prev()
                self._writeXML()
        # else if constants
        elif (self._tk.type() == INTEGER or \
              self._tk.type() == STRING or \
              self._tk.token() in keywords):
            self._writeXML()
        # else if unary operation
        elif (self._tk.token() == '-' or \
              self._tk.token() == '~'):
            self._writeXML()
            # expect term, recursively handle it
            self._handleTerm()
        # else if (expression)
        elif self._tk.token() == '(':
            self._writeXML()
            # expect expression
            self._handleExpression()
            if self._tk.token() == ')':
                self._writeXML()
            else: self._error()
        else: self._error()
        self._level -= 1
        self._write("</term>\n")

    # handle compilation of a subroutine call
    def _handleCall(self):
        # handle subroutine/variable/class name
        if self._tk.type() == IDENTIFIER:
            self._writeXML()
        else: self._error()
        # if external class call
        if self._tk.token() == '.':
            self._writeXML()
            # expect name of ext subroutine call
            if self._tk.type() == IDENTIFIER:
                self._writeXML()
            else: self._error()
        # expect expression list
        self._handleExpressionList()
    
    # handle compilation of expression list
    def _handleExpressionList(self):
        if self._tk.token() == '(':
            self._writeXML()
            self._write("<expressionList>\n")
            self._level += 1
            while self._tk.token() != ')':
                if self._tk.token() == ',':
                    self._writeXML()
                else:
                    # handle param type or name
                    self._handleExpression()
            # write closing bracket
            self._level -= 1
            self._write("</expressionList>\n")
            self._writeXML()
        else: self._error()


# main/executable section of the code
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(".jack file path not provided")
    
    filePath = sys.argv[1]

    # check to see if valid jack file was provided
    if (not fh.fileExists(filePath)) or \
       (not fh.isJackFile(filePath)):
        sys.exit("Incorrect .jack file path")

    cp = Analyzer(filePath)
    cp.compile()