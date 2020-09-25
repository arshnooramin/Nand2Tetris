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
    
    # class method to get the name of the assembly file
    @staticmethod
    def getFileName(filePath):
        if '/' not in filePath:
            return filePath[:-4]
        else:
            return filePath.split('/')[-1][:-4]
    
    # write the file from provided list
    @staticmethod
    def writeHackFile(filePath, writeList):
        fileName = self.getFileName(filePath) + '.hack'
        pass
    
    @staticmethod
    def removeSpaces(line):
        return line.replace(" ", "")

    @staticmethod
    def removeInlineComments(line):
        return line.split('//')[0]

        
