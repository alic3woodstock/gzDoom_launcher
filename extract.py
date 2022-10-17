import os
import shutil

class zipFile():
    _format = ""
    _name = ""
    
    def __init__(self,name, format = "zip"):
        self._format = format
        self._name = name
        
    def ExtractTo(self,path):
        return(True)
        
    def CopyTo(self,path):
        fromFile = "downloads/" + self._name
        if os.path.isfile(fromFile):
            shutil.copy(fromFile,path)
            
def ExtractAll(self):
    fileNames = os.listdir("downloads")
    #print(fileNames)  
    
    if(not os.path.exists("temp")):
        os.mkdir("temp")   

    zipFiles = []
    for zip in fileNames:
        extPos = zip.rfind(".")
        format = "zip"
        if (extPos >= 0):
            format = zip[extPos + 1:].lower()
        zipFiles.append(zipFile(zip, format))
    
    for zip in zipFiles:
        zip.CopyTo("temp")