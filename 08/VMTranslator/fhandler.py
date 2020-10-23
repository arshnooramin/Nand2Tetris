# class with helper functions to handle and parse the .vm input file
class FileHandler:
    # checks if the user provided file path is valid
    @staticmethod
    def fileExists(filePath):
        try:
            with open(filePath, 'r'): pass
            return True
        except OSError:
            print("error1")
            return False
    
    # check if the provided file is .vm format
    @staticmethod
    def isVmFile(filePath):
        return filePath[-3:] == '.vm'
    
    # checks if line is either comments or whitespace
    @staticmethod
    def isCommentOrEmpty(line):
        return line[:2] == '//' or \
            line.isspace() or len(line) == 0
    
    # remove any inline comments
    @staticmethod
    def removeInlineComments(line):
        return line.split('//')[0]
    
    # write the file from provided list
    @staticmethod
    def writeAsmFile(filePath, writeList):
        hackFilePath = filePath[:-3] + '.asm'
        with open(hackFilePath, 'w') as out:
            out.writelines(writeList)



        
