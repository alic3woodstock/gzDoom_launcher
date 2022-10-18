import os
import shutil
import zipfile
import wx
import csv

class zipFile():
    _format = ""
    _name = ""
    
    def __init__(self,name, format = "zip"):
        self._format = format
        self._name = name
        
    def ExtractTo(self,path):
        fromFile = "downloads/" + self._name
        if(not os.path.exists(path)):
            os.mkdir(path)
        if os.path.isfile(fromFile):
            zip = zipfile.ZipFile(fromFile)
            zip.extractall(path)
        
    def CopyTo(self,path):
        fromFile = "downloads/" + self._name
        
        if(not os.path.exists(path)):
            os.mkdir(path)
            
        if os.path.isfile(fromFile):
            shutil.copy(fromFile,path)
    
    def GetName(self):
        return self._name
        
    def TestFileName(self,str):
        if (self.GetName().lower().find(str) >= 0):
            return True
        else:
            return False
            
    def GetFormat(self):
        return self._format
        
        
def ExtractAll(parent):
    progress = wx.ProgressDialog("Extract and Create CSV", "Extracting/Copying files...", maximum=100, parent=parent,
            style=wx.PD_APP_MODAL | wx.STAY_ON_TOP)

    fileNames = os.listdir("downloads")
    #print(fileNames)      

    zipFiles = []
    for zip in fileNames:
        extPos = zip.rfind(".")
        format = "zip"
        if (extPos >= 0):
            format = zip[extPos + 1:].lower()
        zipFiles.append(zipFile(zip, format))
    
    progress.SetRange(len(zipFiles)*2)
    i = 1;
    for zip in zipFiles:
        if (zip.TestFileName("gzdoom")):
            zip.ExtractTo("gzdoom")
        elif (zip.TestFileName("blasphem")):
            zip.ExtractTo("wads")
        elif (zip.TestFileName("freedoom")):
            zip.ExtractTo("temp")            
            tempNames = os.listdir("temp")
            for f in tempNames:
                if (f.lower().find("freedoom") >= 0):
                    tempNames2 = os.listdir("temp/" + f)
                    for g in tempNames2:
                        if (g.lower().find("wad") >= 0):
                            h = "temp/" + f + "/" + g
                            if(not os.path.exists("wads")):
                                os.mkdir("wads")
                            shutil.copy(h, "wads")
        elif (zip.TestFileName("pk3") or zip.TestFileName( "150skins")):
            zip.CopyTo("mods")            
        else:
            zip.CopyTo("maps")
        progress.Update(i)
        i += 1
    
    # Remove temp directory if exists
    if (os.path.exists("temp")):
        shutil.rmtree("temp")
        
    CreateCSV(progress)    
        
def CreateCSV(progress):
    zipFiles = []
    
    wads = os.listdir("wads")  
    for w in wads:
        zipFiles.append(zipFile(w,"wads")) # store path in format string since I don't need to use Extract
        
    mods = os.listdir("mods")
    for m in mods:
        zipFiles.append(zipFile(m,"mods"))
    
    maps = os.listdir("maps")
    for a in maps:
        zipFiles.append(zipFile(a,"maps"))
        
    lines = []
    lines.append(['id', 'Name','Tab Index', 'Executable', 'Group', 'Last run mod','iWad','file1','file2','...'])
    blasphenWad = ""
        
    if (os.name == "nt"):
        exec = ".\\gzdoom\\gzdoom.exe"
    else:
        exec = "./gzdoom/gzdoom"

    for zip in zipFiles:
        fullPath = zip.GetFormat() + "/" + zip.GetName() 
        if (zip.TestFileName("blasphem")): 
            blasphenWad = (fullPath) # works because wad comes first in the list
        elif (zip.TestFileName("bls")):
            lines.append([0, "Blasphem", 0, exec, "heretic", 0, blasphenWad, fullPath])
        elif (zip.TestFileName("freedoom1")):            
            lines.append([1, "Freedoom Phase 1", 0, exec, "doom", 0, fullPath])
        elif (zip.TestFileName("freedoom2")):
            lines.append([2, "Freedoom Phase 2", 0, exec, "doom", 0, fullPath])
        
    with open ('games.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, dialect = 'unix')
        for l in lines:
            writer.writerow(l)
            
    progress.Update(progress.GetRange())