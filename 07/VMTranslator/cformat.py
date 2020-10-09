from ctypes import *

class CFormatter:
    # memory mapping scheme
    _segmap = {
        'local': '@LCL', 'argument': '@ARG',
        'this': '@THIS', 'that': '@THAT'
    }

    # arithmetic operations mapping scheme
    _opmap = {
        'add': '+', 'sub': '-', 'and': '&',
        'or': '|', 'neg': '-', 'not': '!',
        'eq': 'JNE', 'lt': 'JGE', 'gt': 'JLE'
    }

    _preAsm = "@SP\nAM=M-1\nD=M\nA=A-1\n"

    # writes asm code for add, sub, and, or operators
    @staticmethod
    def writeOpAsm(operator):
        return CFormatter._preAsm + \
            "M=M{}D".format(CFormatter._opmap[operator])
    
    # writes asm code for eq, lt, gt comparators
    @staticmethod
    def writeCompAsm(operator, num):
        return CFormatter._preAsm + \
            "D=M-D\n@ELSE{}\nD;{}\n".format(num, CFormatter._opmap[operator]) + \
            "@SP\nA=M-1\nM=-1\n@IF{}\n".format(num) + \
            "0;JMP\n(ELSE{})\n@SP\n".format(num) + \
            "A=M-1\nM=0\n(IF{})\n".format(num)

    # write asm code for not, neg unary operators
    @staticmethod
    def writeUnaryAsm(operator):
        return "@SP\nA=M-1\nM={}M".format(CFormatter._opmap[operator])

    # write asm code for push command
    @staticmethod
    def writePushAsm(cmd, seg, num):
        if seg == "constant":
            return "@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(num)

    # write asm code for pop command
    @staticmethod
    def writePopAsm(cmd, seg, num):
        if seg == "constant":
            return "@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(num)
    
    # returns the type of the command that is passed in
    @staticmethod
    def commandType(command):
        if command == "push":
            return PUSH
        elif command == "pop":
            return POP
        elif command in CFormatter._opmap.keys():
            return ARITHMETIC
        # unknown command
        return -1
    
    # returns the type of the arithmetic command that is passed in
    @staticmethod
    def arithmeticType(command):
        if command == "add" or command == "sub" or \
        command == "and" or command == "or":
           return BI_OP
        elif command == "eq" or command == "lt" or \
        command == "gt":
            return COMP
        elif command == "not" or command == "neg":
            return UN_OP

