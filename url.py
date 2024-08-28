import functions


class Url:
    _url = ""
    _fileName = ""

    def __init__(self, url, file_name, sha_hash=""):
        self.url = url
        self.fileName = file_name
        self.sha_hash = sha_hash

    def GetFilePath(self):
        return functions.downloadPath + self.fileName
