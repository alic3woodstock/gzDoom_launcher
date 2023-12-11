import functions

class Url:
    _url = ""
    _fileName = ""

    def __init__(self, url, fileName):
        self.url = url
        self.fileName = fileName

    def GetFilePath(self):
        return functions.downloadPath + self.fileName
