from fhandler import FileHandler as fh
from ctypes import *

# parses the input jack code and tokenizes it
class Tokenizer:
    # jack lang keywords
    _keywords = [
        'class', 'constructor', 'function', 'method',
        'field', 'static', 'var', 'int', 'char', 'boolean',
        'void', 'true', 'false', 'null', 'this', 'let',
        'do', 'if', 'else', 'while', 'return'
    ]
    # jack lang symbols
    _symbols = [
        '{', '}', '(', ')', '[', ']', '.', ',', 
        ';', '+', '-', '*', '/', '&', '|', '<', 
        '>', '=', '~'
    ]

    # constructor takes file path as argument
    def __init__(self, filePath):
        # path to the jack file
        self._filePath = filePath
        # file read object
        self._f = open(filePath, 'r') 
        # list of tokens
        self._tokenList = []
        # list of token types
        self._typeList = []
        # current line being analyzed
        self._code = ""
        # pointer for iterator
        self._idx = 0

        # parse the code and tokenize
        self._firstParse(); self._secParse()

    # getter method for token
    def token(self):
        return self._tokenList[self._idx]
    
    # getter method for token type
    def type(self):
        return self._typeList[self._idx]
    
    # to advance the iterator
    def next(self):
        self._idx += 1
    
    # parse once to remove comments, newline chars, whitespaces
    def _firstParse(self):
        for line in self._f:
            # remove the newline char '\n'
            line = line.strip()
            # check if there is parseable code in line
            if not fh.isCommentOrEmpty(line):
                line = fh.removeInlineComments(line)
                # update the clean code string
                self._code += line

    # parse second time to tokenize
    def _secParse(self):
        while self._code != "":
            # if first char is space
            if self._code[0] == " ":
                # remove it from line
                self._code = self._code[1:]
            # check for tokens and their types
            # reset the loop if self._code was edited
            if self._handleKeyword(): continue
            if self._handleSymbol(): continue                    
            if self._handleInteger(): continue
            if self._handleString(): continue
            if self._handleIdentifier(): continue                    

    # find keywords in line
    def _handleKeyword(self):
        # for each jack lang keyword
        for keyword in Tokenizer._keywords:
            # if current code string starts with it
            if self._code.startswith(keyword):
                # add it to token and type list
                self._tokenList.append(keyword)
                self._typeList.append(KEYWORD)
                # print(keyword, KEYWORD, "keyword")
                # get the substring minus found keyword
                self._code = self._code[len(keyword):]
                return True
        return False
    
    # find symbol in line
    def _handleSymbol(self):
        # if curr code char is a jack lang symbol
        if self._code[0] in Tokenizer._symbols:
            # add it to token and type list
            self._tokenList.append(self._code[0])
            self._typeList.append(SYMBOL)
            # print(self._code[0], SYMBOL, "symbol")
            # get the substring minus found symbol
            self._code = self._code[1:]
            return True
        return False

    # find integer constant in line
    def _handleInteger(self):
        # if curr code char is a digit
        if self._code[0].isdigit():
            # create a string with this char
            integer = self._code[0]
            self._code = self._code[1:]
            # while the next chars are digits
            while self._code[0].isdigit():
                # keep updating the string
                integer += self._code[0]
                self._code = self._code[1:]
            # add it to token and type list
            self._tokenList.append(integer)
            self._typeList.append(INTEGER)
            # print(integer, INTEGER, "integer")
            return True
        return False
    
    # find string contant in line
    def _handleString(self):
        # if curr char is quotation mark "
        if self._code[0] == "\"":
            # ignore the quotation
            self._code = self._code[1:]
            string = ""
            # store everything btw the quotation
            while self._code[0] != '\"':
                string += self._code[0]
                self._code = self._code[1:]
            self._code = self._code[1:]
            # add it to token and type list
            self._tokenList.append(string)
            self._typeList.append(STRING)
            # print(string, STRING, "string")
            return True
        return False
    
    # find identifier in line
    def _handleIdentifier(self):
        # check if first char is a letter or "_"
        if self._code[0].isalpha() or self._code[0] == "_":
            identifier = self._code[0]
            self._code = self._code[1:]
            # while chars are letter, "_", or digits
            while (self._code[0].isalpha() or \
                self._code[0].isdigit() or \
                    self._code[0] == "_"):
                identifier += self._code[0]
                self._code = self._code[1:]
            # add it to token and type list
            self._tokenList.append(identifier)
            self._typeList.append(IDENTIFIER)
            # print(identifier, IDENTIFIER, "identifier")
            return True
        return False
