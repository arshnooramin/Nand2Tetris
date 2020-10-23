from ctypes import *

# class with helper functions to format the commands and write asm code
class CFormatter:
    # memory segments mapping scheme
    _segmap = {
        'local': 'LCL', 'argument': 'ARG',
        'this': 'THIS', 'that': 'THAT', 
        'temp': '5'
    }

    # arithmetic operations mapping scheme
    _opmap = {
        'add': '+', 'sub': '-', 'and': '&',
        'or': '|', 'neg': '-', 'not': '!',
        'eq': 'JNE', 'lt': 'JGE', 'gt': 'JLE'
    }

    # the common pre asm code for operators and comparators
    _preArithmeticAsm = "@SP\nAM=M-1\nD=M\nA=A-1\n"

    # the common post asm code for pop commands
    _postPopAsm = "@13\nM=D\n@SP\nAM=M-1\nD=M\n@13\nA=M\nM=D\n"

    # the common post asm code for push commands
    _postPushAsm = "D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    # writes asm code for add, sub, and, or operators
    @staticmethod
    def writeOpAsm(operator):
        return CFormatter._preArithmeticAsm + \
            "M=M{}D\n".format(CFormatter._opmap[operator])
    
    # writes asm code for eq, lt, gt comparators
    @staticmethod
    def writeCompAsm(operator, num):
        return CFormatter._preArithmeticAsm + \
            "D=M-D\n@ELSE{}\nD;{}\n".format(num, CFormatter._opmap[operator]) + \
            "@SP\nA=M-1\nM=-1\n@IF{}\n".format(num) + \
            "0;JMP\n(ELSE{})\n@SP\n".format(num) + \
            "A=M-1\nM=0\n(IF{})\n".format(num)

    # write asm code for not, neg unary operators
    @staticmethod
    def writeUnaryAsm(operator):
        return "@SP\nA=M-1\nM={}M\n".format(CFormatter._opmap[operator])

    # write asm code for push command
    @staticmethod
    def writeConstantPushPopAsm(num):
            return "@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(str(num))

    # write asm code push/pop command for this, local, argument, that, temp
    @staticmethod
    def writePushPopAsm1(ptype, seg, num):
        if seg == "temp": num += 5
        if ptype == PUSH:
            return "@{}\nD=M\n@{}\nA=D+A\n".format(CFormatter._segmap[seg], str(num)) + \
                CFormatter._postPushAsm 
        elif ptype == POP:
            return "@{}\nD=M\n@{}\nD=D+A\n".format(CFormatter._segmap[seg], str(num)) + \
                CFormatter._postPopAsm
    
    # write asm code push/pop command for static, pointer
    @staticmethod
    def writePushPopAsm2(ptype, seg, num):
        if seg == "pointer":
            if num == 0:
                segmap = CFormatter._segmap["this"]
            elif num == 1:
                segmap = CFormatter._segmap["that"]
        elif seg == "static":
            segmap = str(16 + num)
        if ptype == PUSH:
            return "@{}\n".format(segmap) + \
                CFormatter._postPushAsm
        elif ptype == POP:
            return "@{}\nD=A\n".format(segmap) + \
                CFormatter._postPopAsm
    
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
    
    # returns the type of the push/pop command that is passed in
    @staticmethod
    def pushPopType(segment):
        if segment == "this" or segment == "local" or \
        segment == "argument" or segment == "that" or \
        segment == "temp":
            return GROUP_1
        elif segment == "static" or segment == "pointer":
            return GROUP_2
        elif segment == "constant":
            return CONSTANT


