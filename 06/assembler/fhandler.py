# class with helper function to handle and parse the .asm input file
class FileHandler:
    # checks if the user provided file path is valid
    @staticmethod
    def fileExists(filePath):
        try:
            with open(filePath, 'r') as tempfile: pass
            return True
        except OSError:
            return False
    
    # check if the provided file is .asm format
    @staticmethod
    def isAsmFile(filePath):
        return filePath[-4:] == '.asm'
    
    # write the file from provided list
    @staticmethod
    def writeHackFile(filePath, writeList):
        hackFilePath = filePath[:-4] + '-gen.hack'
        with open(hackFilePath, 'w') as out:
            out.writelines(writeList)
    
    # remove whitespaces from the code
    @staticmethod
    def removeSpaces(line):
        return line.replace(" ", "")

    # remove any inline comments
    @staticmethod
    def removeInlineComments(line):
        return line.split('//')[0]
    
    # convert decimal to binary
    @staticmethod
    def dec2bin(dec, bits):
        return bin(dec)[2:].zfill(bits)
    
    # checks if line is either comments or whitespace
    @staticmethod
    def isCommentOrEmpty(line):
        return line[:2] == '//' or \
            line.isspace() or len(line) == 0

    # checks if the line is an a-instruction
    @staticmethod
    def isAInst(line):
        return line[0] == '@'
    
    # checks if the line is a loop marker
    @staticmethod
    def isLoopMarker(line):
        return line[0] == '('

        
