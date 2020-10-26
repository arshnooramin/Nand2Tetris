import os

# class with helper functions to handle and parse the .vm input file
class FileHandler:
    # checks if the user provided file path is valid
    @staticmethod
    def dirExists(dirPath):
        return os.path.isdir(dirPath)
    
    # gets file paths for all the vm files in dir path
    @staticmethod
    def getVmFiles(dirPath):
        filePaths = []
        for file in os.listdir(dirPath):
            if file.endswith(".vm"):
                filePaths.append(os.path.join(dirPath, file))
        return filePaths

    # gets the name for the output asm files
    @staticmethod
    def getFileName(dirPath):
        return dirPath.split('/')[-2]

    # gets the name for the vm file
    @staticmethod
    def getVmFileName(filePath):
        print(filePath.split('/')[-1][:-3])
        return filePath.split('/')[-1][:-3]

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
    def writeAsmFile(dirPath, writeList):
        fileName = FileHandler.getFileName(dirPath)
        asmFilePath = dirPath + fileName + '.asm'
        with open(asmFilePath, 'w') as out:
            out.writelines(writeList)



        
