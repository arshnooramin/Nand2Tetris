# class to store and manage all the asm code/symbols hash tables
class HTable:
    # All class variables are protected (encapsulation)
    # undef symbol counter
    symbCount = 0
    # last pre-defined symbol address
    LAST_ADDRESS = 15
    # symbol codes
    _symbol = {
        'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
        'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 
        'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 
        'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 
        'SCREEN': 16384, 'KBD': 24576
    }
    # destination codes
    _dest = {
        "null": "000", "M": "001", "D": "010",
        "A": "100", "MD": "011", "AM": "101",
        "AD": "110", "AMD": "111"
    }
    # jump codes
    _jump = {
        "null": "000", "JGT": "001", "JEQ": "010",
        "JGE": "011", "JLT": "100", "JNE": "101",
        "JLE": "110", "JMP": "111"
    }
    # computation/ALU codes
    _comp = {
        '0': '0101010', '1': '0111111', '-1': '0111010',
        'D': '0001100', 'A': '0110000', '!D': '0001101',
        '!A': '0110001', '-D': '0001111', '-A': '0110011',
        'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
        'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
        'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
        'M': '1110000', '!M': '1110001', '-M': '1110011',
        'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010',
        'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000',
        'D|M': '1010101',
    }

    # constructor doesn't take arguments
    def __init__(self):
        pass
    
    # gets the destination binary code for inputted dCode
    def destBin(self, dCode):
        try:
            return self._dest[dCode]
        # error handling to check if valid code
        except KeyError:
            print("Invalid destination code!")
    
    # gets the jump binary code for inputted jCode
    def jumpBin(self, jCode):
        try:
            return self._jump[jCode]
        # error handling to check if valid code
        except KeyError:
            print("Invalid jump code!")
    
    # gets the computation binary code for inputted cCode
    def compBin(self, cCode):
        try:
            return self._dest[dCode]
        # error handling to check if valid code
        except KeyError:
            print("Invalid computation code!")
    
    # gets the binary address or updates the tables for the 
    # inputted inSymb
    def symbolHandler(self, symbIn):
        if symbIn not in self._symbol:
            self.symbCount += 1
            self._symbol[symbIn] = self.LAST_ADDRESS + self.symbCount
        return self._symbol[symbIn]

    

