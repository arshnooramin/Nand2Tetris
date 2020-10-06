from ctypes import *

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
    
    # check if the provided file is .vm format
    @staticmethod
    def isVmFile(filePath):
        return filePath[-4:] == '.vm'
    
    # returns the type of the command that is passed in
    @staticmethod
    def commandType(line):
        pass

    # gets the first arg from each line of code
    @staticmethod
    def getFirstArg(line):
        pass

    # gets the second arg from each line of code
    @staticmethod
    def getSecArg(line):
        pass
    
    # write the file from provided list
    @staticmethod
    def writeAsmFile(filePath, writeList):
        hackFilePath = filePath[:-4] + '-gen.asm'
        with open(hackFilePath, 'w') as out:
            out.writelines(writeList)



        
