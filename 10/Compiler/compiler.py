import sys
from fhandler import FileHandler as fh
from tokenizer import Tokenizer

# the main compiler class that converts jack tokens to xml
class Compiler:
    # constructor takes file path as argument
    def __init__(self, filePath):
        # instantiate tokenizer class
        self._tk = Tokenizer(filePath)
        # path to the jack file
        self._filePath = filePath
        # list of xml code w/ line as elem
        self._codeList = []
    
    # compile the jack code by parsing
    def compile(self):
        # write assembled code to xml file
        fh.writeXMLFile(self._filePath, self._codeList)

# main/executable section of the code
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(".jack file path not provided")
    
    filePath = sys.argv[1]

    # check to see if valid jack file was provided
    if (not fh.fileExists(filePath)) or \
       (not fh.isJackFile(filePath)):
        sys.exit("Incorrect .jack file path")

    cp = Compiler(filePath)
    cp.compile()