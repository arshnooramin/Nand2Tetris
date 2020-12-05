# class with helper function to handle and parse the .jack input file
class FileHandler:
    # checks if the user provided file path is valid
    @staticmethod
    def fileExists(filePath):
        try:
            with open(filePath, 'r'): pass
            return True
        except OSError:
            return False
    
    # check if the provided file is .jack format
    @staticmethod
    def isJackFile(filePath):
        return filePath[-5:] == '.jack'
    
    # write the file from provided list
    @staticmethod
    def writeXMLFile(filePath, writeList):
        hackFilePath = filePath[:-5] + '-e.xml'
        with open(hackFilePath, 'w') as out:
            out.writelines(writeList)
    
    # remove whitespaces from the code
    @staticmethod
    def removeSpaces(line):
        return line.replace(" ", "")

    # remove any inline comments
    @staticmethod
    def removeInlineComments(line):
        if '//' in line:
            return line.split('//')[0]
        elif '/*' in line:
            return line.split('/*')[0]
        else: return line
    
    # checks if line is either comments or whitespace
    @staticmethod
    def isCommentOrEmpty(line):
        return line[:2] == '//' or \
            line[:2] == '/*' or \
            line[-2:] == '*/' or \
            line[:1] == "*" or \
            line[:2] == " *" or \
            line.isspace() or len(line) == 0