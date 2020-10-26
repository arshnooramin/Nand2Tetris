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

    def __init__(self):
        # index to keep track of all the jumps
        self._jmpNum = 0
        # index to keep track of all the jumps
        self._lblNum = 0

    # writes asm code for add, sub, and, or operators
    @staticmethod
    def writeOpAsm(operator):
        return CFormatter._preArithmeticAsm + \
            "M=M{}D\n".format(CFormatter._opmap[operator])
    
    # writes asm code for eq, lt, gt comparators
    def writeCompAsm(self, operator):
        retstr = CFormatter._preArithmeticAsm + \
            "D=M-D\n@ELSE{}\nD;{}\n".format(self._jmpNum, CFormatter._opmap[operator]) + \
            "@SP\nA=M-1\nM=-1\n@IF{}\n".format(self._jmpNum) + \
            "0;JMP\n(ELSE{})\n@SP\n".format(self._jmpNum) + \
            "A=M-1\nM=0\n(IF{})\n".format(self._jmpNum) + \
            "@SP\nAM=M-1\nD=M\nA=A-1\n"
        self._jmpNum += 1
        return retstr

    # write asm code for not, neg unary operators
    @staticmethod
    def writeUnaryAsm(operator):
        return "@SP\nA=M-1\nM={}M\n".format(CFormatter._opmap[operator])

    # write asm code for push command
    @staticmethod
    def writeConstantPushPopAsm(num):
        return "@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(str(num))
    
    # write asm code for push command
    @staticmethod
    def writeStaticPushPopAsm(fname, ptype, num):
        if ptype == PUSH:
            return "@{}\n".format(fname + str(num)) + \
                CFormatter._postPushAsm
        elif ptype == POP:
            return "@{}\nD=A\n".format(fname + str(num)) + \
                CFormatter._postPopAsm

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
    def writePushPopAsm2(ptype, seg, num=None):
        if seg == "pointer":
            if num == 0:
                segmap = CFormatter._segmap["this"]
            elif num == 1:
                segmap = CFormatter._segmap["that"]
        else:
            segmap = CFormatter._segmap[seg]
        if ptype == PUSH:
            return "@{}\n".format(segmap) + \
                CFormatter._postPushAsm
        elif ptype == POP:
            return "@{}\nD=A\n".format(segmap) + \
                CFormatter._postPopAsm
    
    # write the initial bootstrap asm code
    @staticmethod
    def writeInitAsm():
        return "@256\nD=A\n@SP\nM=D\n"
    
    # write asm code for the label command
    @staticmethod
    def writeLabelAsm(lblstr):
        return "({})\n".format(lblstr)
    
    # write asm code for the goto command
    @staticmethod
    def writeGotoAsm(lblstr):
        return "@{}\n0;JMP\n".format(lblstr)

    # write asm code for the if-goto command
    @staticmethod
    def writeIfGotoAsm(lblstr):
        return CFormatter._preArithmeticAsm + \
            "@{}\nD;JNE\n".format(lblstr)
    
    # write asm code for the call command
    def writeCallAsm(self, fname, argnum):
        retlbl = "RETURN{}".format(self._lblNum)
        retstr = "@{}\n".format(retlbl) + \
            "D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" + \
            CFormatter.writePushPopAsm2(PUSH, "local") + \
            CFormatter.writePushPopAsm2(PUSH, "argument") + \
            CFormatter.writePushPopAsm2(PUSH, "pointer", 0) + \
            CFormatter.writePushPopAsm2(PUSH, "pointer", 1) + \
            "@SP\nD=M\n@5\nD=D-A\n@{}\n".format(str(argnum)) + \
            "D=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n" + \
            CFormatter.writeGotoAsm(fname) + \
            CFormatter.writeLabelAsm(retlbl)
        self._lblNum += 1
        return retstr
    
    # write asm code for the return command
    @staticmethod
    def writeReturnAsm():
        return "@LCL\nD=M\n@11\nM=D\n@5\nA=D-A\nD=M\n@12\nM=D\n" + \
            CFormatter.writePushPopAsm1(POP, "argument", 0) + \
            "@ARG\nD=M\n@SP\nM=D+1\n@11\nD=M-1\nAM=D\nD=M\n@THAT\n" + \
            "M=D\n@11\nD=M-1\nAM=D\nD=M\n@THIS\nM=D\n@11\nD=M-1\n" + \
            "AM=D\nD=M\n@ARG\nM=D\n@11\nD=M-1\nAM=D\nD=M\n@LCL\nM=D\n" + \
            "@12\nA=M\n0;JMP\n"
    
    # write asm code for the if-goto command
    @staticmethod
    def writeFunctionAsm(fname, lclnum):
        retstr = CFormatter.writeLabelAsm(fname)
        for _ in range(lclnum):
            retstr += CFormatter.writeConstantPushPopAsm(0)
        return retstr

    # returns the type of the command that is passed in
    @staticmethod
    def commandType(command):
        if command == "push":
            return PUSH
        elif command == "pop":
            return POP
        elif command in CFormatter._opmap.keys():
            return ARITHMETIC
        elif command == "label":
            return LABEL
        elif command == "goto":
            return GOTO
        elif command == "if-goto":
            return IF
        elif command == "function":
            return FUNCTION
        elif command == "return":
            return RETURN
        elif command == "call":
            return CALL
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
        elif segment == "static":
            return STATIC
        elif segment == "pointer":
            return GROUP_2
        elif segment == "constant":
            return CONSTANT


