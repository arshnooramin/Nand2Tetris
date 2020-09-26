import sys
import re
from htable import HTable
from fhandler import FileHandler as fh

# the main assembler script that converts asm to hack
class Assembler:
    # constructor takes file path as argument
    def __init__(self, filePath):
        # path to the asm file
        self._filePath = filePath
        # file read object
        self._f = open(filePath, 'r')
        # initialize a new htable object
        self._ht = HTable()
        # list of hack code w/ line as elem
        self._codeList = []
    
    def parse(self):
        for line in self._f:
            # remove the newline char '\n'
            line = line.strip()
            # remove whitespaces from lines
            line = fh.removeSpaces(line)
            # check if there is parseable code in line
            if not self._isCommentOrEmpty(line):
                line = fh.removeInlineComments(line)
                # check if it's a instruction
                if self._isAInst(line):
                    # handle a instruction
                    self._handleAInst(line[1:])
                # check if it's a loop marker
                elif self._isLoopMarker(line):
                    # don't do anything
                    continue
                # else must be a c-instruction
                else:
                    self._handleCInst(line)

        print(self._codeList)

    # convert a inst symbol to binary code
    # update the code list    
    def _handleAInst(self, aInst):
        address = ''
        try:
            address = self._dec2bin(int(aInst), 15)
        except:
            decaddr = self._ht.symbolHandler(str(aInst))
            address = self._dec2bin(decaddr, 15)
        print(aInst + " " + address)
        self._codeList.append('0' + address)
    
    # convert c inst symbol to binary code
    # update the code list    
    def _handleCInst(self, cInst):
        cBin = ''
        if '=' in cInst:
            cList = cInst.split('=')
            dest, comp = cList[0], cList[1]
            cBin = self._getCInst(comp, dest, 'null')
        elif ';' in cInst:
            cList = cInst.split(';')
            comp, jump = cList[0], cList[1]
            cBin = self._getCInst(comp, 'null', jump)
        print(cInst + " " + cBin)
        self._codeList.append(cBin)
    
    def _getCInst(self, comp, dest, jump):
        return '111' + self._ht.compBin(comp) +\
               self._ht.destBin(dest) +\
               self._ht.jumpBin(jump)    

    # convert decimal to binary
    @staticmethod
    def _dec2bin(dec, bits):
        return bin(dec)[2:].zfill(bits)
    
    # checks if line is either comments or whitespace
    @staticmethod
    def _isCommentOrEmpty(line):
        return line[:2] == '//' or \
            line.isspace() or len(line) == 0

    # checks if the line is an a-instruction
    @staticmethod
    def _isAInst(line):
        return line[0] == '@'
    
    # checks if the line is a loop marker
    @staticmethod
    def _isLoopMarker(line):
        return line[0] == '('

# main/executable section of the code
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(".asm file path not provided")
    
    filePath = sys.argv[1]

    if (not fh.fileExists(filePath)) or \
       (not fh.isAsmFile(filePath)):
        sys.exit("Incorrect .asm file path")

    asm = Assembler(filePath)
    asm.parse()



    
