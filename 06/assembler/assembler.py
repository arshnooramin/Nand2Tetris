import sys
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
        # count for number of lines of code
        self._lineCount = -1
    
    # assemble the .hack code by parsing
    def assemble(self):
        # populate the symbol table w/ loop markers
        self.parse(self._firstPass)
        # aseemble the code
        self.parse(self._secPass)
        # write assembled code to .hack file
        fh.writeHackFile(self._filePath, self._codeList)
    
    # parse through the code, remove unwanted chars
    def parse(self, asmLogicFunc):
        for line in self._f:
            # remove the newline char '\n'
            line = line.strip()
            # remove whitespaces from lines
            line = fh.removeSpaces(line)
            # check if there is parseable code in line
            if not fh.isCommentOrEmpty(line):
                # apply assembly logic to it
                asmLogicFunc(line)
        # reset the file cursor to the start of file
        self._f.seek(0)
    
    # find the loop markers and save them in symbol table
    def _firstPass(self, line):
        # if line contain a loop marker
        if fh.isLoopMarker(line):
            loopMark = line[1:-1]
            # store it in the symbol hash table
            self._ht.addSymbol(loopMark, self._lineCount+1)
        else:
            # count number of parseable code lines
            self._lineCount += 1
    
    # find a- and c-instruction and handle each
    def _secPass(self, line):
        line = fh.removeInlineComments(line)
        # check if it's a instruction
        if fh.isAInst(line):
            # handle a-instruction
            self._handleAInst(line[1:])
        # else must be a c-instruction
        elif not fh.isLoopMarker(line):
            # handle c-instruction
            self._handleCInst(line)

    # convert a inst symbol to binary code
    # update the code list    
    def _handleAInst(self, aInst):
        address = ''
        # if a-inst is an int
        try:
            address = fh.dec2bin(int(aInst), 15)
        # else must be a symbol
        except:
            # decode the asm code
            decaddr = self._ht.symbolHandler(str(aInst))
            address = fh.dec2bin(decaddr, 15)
        # store it in the code list
        self._codeList.append('0' + address + '\n')
    
    # convert c inst symbol to binary code
    # update the code list    
    def _handleCInst(self, cInst):
        cBin = ''
        # if c-inst contains '='
        if '=' in cInst:
            # must be alu operation
            cList = cInst.split('=')
            dest, comp = cList[0], cList[1]
            cBin = self._getCInst(comp, dest, 'null')
        # else if contain ';'
        elif ';' in cInst:
            # must be a jump statement
            cList = cInst.split(';')
            comp, jump = cList[0], cList[1]
            cBin = self._getCInst(comp, 'null', jump)
        # store it in the code list
        self._codeList.append(cBin + '\n')
    
    # get and create a c-instruction with provided
    # asm codes
    def _getCInst(self, comp, dest, jump):
        return '111' + self._ht.compBin(comp) +\
               self._ht.destBin(dest) +\
               self._ht.jumpBin(jump)    

# main/executable section of the code
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(".asm file path not provided")
    
    filePath = sys.argv[1]

    # check to see if valid asm was provided
    if (not fh.fileExists(filePath)) or \
       (not fh.isAsmFile(filePath)):
        sys.exit("Incorrect .asm file path")

    asm = Assembler(filePath)
    asm.assemble()



    
