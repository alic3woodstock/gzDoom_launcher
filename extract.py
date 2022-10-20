import os
import shutil
import zipfile
import wx
import csv
import tarfile

class zipFile():
    _format = ""
    _name = ""
    
    def __init__(self,name, fileFormat = "zipFile"):
        self._format = fileFormat
        self._name = name
        
    def ExtractTo(self,path):
        fromFile = "downloads/" + self._name
        if(not os.path.exists(path)):
            os.mkdir(path)
        if os.path.isfile(fromFile):
            try:
                if (self.GetFormat() == "zipFile"):
                    zipFile = zipfile.ZipFile(fromFile)
                    zipFile.extractall(path)

                if (self.GetFormat() == "xz"):
                    zipFile = tarfile.open(fromFile, 'r:xz')
                    zipFile.extractall(path)
            except:
                print("Extracting " + self.GetName() + " failed")
        
    def CopyTo(self,path):
        try:  
            fromFile = "downloads/" + self._name
            
            if (self.GetFormat() == "zipFile") or (self.GetFormat() == "pk3"):
                zipFile = zipfile.ZipFile(fromFile)
                zipFile.testzip
        
            if(not os.path.exists(path)):
                os.mkdir(path)
                
            if os.path.isfile(fromFile):
                shutil.copy(fromFile,path)
        except:
            print("Copying " + self.GetName() + " failed")
    
    def GetName(self):
        return self._name
        
    def TestFileName(self,name):
        if (self.GetName().lower().find(name) >= 0):
            return True
        else:
            return False
            
    def GetFormat(self):
        return self._format
        
    def GetMapName(self):
        fromFile = "downloads/" + self.GetName()
        zipFile = zipfile.ZipFile(fromFile)
        
        # Mps with non standard txt
        if (self.GetName() == "mm2.zipFile"):
            return "Memento Mori 2"            
        if (self.GetName() == "av.zipFile"):
            return "Alien Vendetta"            
        if (self.GetName() == "hr.zipFile"):
            return "Hell Revealed"

        try:
            txtFile = zipFile.namelist()
            for t in txtFile:
                if (t.lower().find(".txt") >= 0):
                    with zipFile.open(t) as f:
                        names = f.readlines()
                        for name in names:
                            s = str(name)
                            if (s.find("Title ") == 2) and (s.find(":") >= 0) and (s.find("Screen") < 0):
                                start = s.find(":") + 1
                                s = s.replace("\\n","")
                                s = s.replace("\\r","")
                                s = s.replace("'","")
                                s = s.replace(".wad","")
                                return (s[start:].strip())
        except:
            return self.GetName()
        return self.GetName()
                
def ExtractAll(parent):
    progress = wx.ProgressDialog("Extract and Create CSV", "Extracting/Copying files...", maximum=100, parent=parent,
            style=wx.PD_APP_MODAL | wx.STAY_ON_TOP)

    fileNames = os.listdir("downloads")

    zipFiles = []
    for zipFile in fileNames:
        extPos = zipFile.rfind(".")
        fileFormat = "zipFile"        
        if (extPos >= 0):
            fileFormat = zipFile[extPos + 1:].lower()
        zipFiles.append(zipFile(zipFile, fileFormat))
    
    progress.SetRange(len(zipFiles) + 22) #if everthyng works number of csv in the list is 22
    i = 1;
    for zipFile in zipFiles:
        if (zipFile.TestFileName("gzdoom")):
            if (os.name == "nt"):  
                zipFile.ExtractTo("gzdoom")
            else:
                try:
                    zipFile.ExtractTo("temp")
                    dirs = os.listdir("temp")
                    for filePath in dirs:
                        if (filePath.lower().find("gzdoom") >= 0):
                            shutil.copytree("temp/" + filePath,"gzdoom")
                except:
                    print("Copying gzdoom failed!")
        elif (zipFile.TestFileName("blasphem")):
            zipFile.ExtractTo("wads")
        elif (zipFile.TestFileName("freedoom")):
            zipFile.ExtractTo("temp")            
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
        elif (zipFile.TestFileName("pk3") or zipFile.TestFileName( "150skins")):
            zipFile.CopyTo("mods")            
        else:
            zipFile.CopyTo("maps")
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
        zipFiles.append(zipFile(w,"wads")) # store path in fileFormat string since I don't need to use Extract
        
    maps = os.listdir("maps")
    for a in maps:
        zipFiles.append(zipFile(a,"maps"))
        
    mods = os.listdir("mods")
    for m in mods:
        zipFiles.append(zipFile(m,"mods"))    
        
    lines = []
    lines.append(['id', 'Name','Tab Index', 'Executable', 'Group', 'Last run mod','iWad','file1','file2','...'])
    blasphenWad = ""
        
    if (os.name == "nt"):
        gameExec = ".\\gzdoom\\gzdoom.exe"
    else:
        gameExec = "./gzdoom/gzdoom"
        
    i = 0
    for zipFile in zipFiles:
        fullPath = zipFile.GetFormat() + "/" + zipFile.GetName() 
        if (zipFile.TestFileName("blasphem")): 
            blasphenWad = (fullPath) # works because wad comes first in the list            
        elif (zipFile.TestFileName("bls")):
            lines.append([i, "Blasphem", 0, gameExec, "heretic", 0, blasphenWad, fullPath])
        elif (zipFile.TestFileName("freedoom1")):            
            lines.append([i, "Freedoom Phase 1", 0, gameExec, "doom", 0, fullPath])
        elif (zipFile.TestFileName("freedoom2")):
            lines.append([i, "Freedoom Phase 2", 0, gameExec, "doom", 0, fullPath])
        elif (zipFile.GetFormat() == "maps"):     
            if (zipFile.TestFileName("htchest") or zipFile.TestFileName("unbeliev")):
                lines.append([i, zipFile.GetMapName(), 1, gameExec, "heretic", 0, "wads/blasphem-0.1.7.wad", fullPath])
            else:
                lines.append([i, zipFile.GetMapName(), 1, gameExec, "doom", 0, "wads/freedoom2.wad", fullPath])
        elif (zipFile.GetFormat() == "mods"):
            if (zipFile.TestFileName("150skins")):
                i -= 1
            elif (zipFile.TestFileName("beaultiful")):
                lines.append([i, "Beaultiful Doom", 2, gameExec, "doom", 0, "", "mods/150skins.zipFile", "mods/Beaultiful_Doom.pk3"])
            elif (zipFile.TestFileName("brutal")):
                lines.append([i, "Brutal Doom", 2, gameExec, "doom", 0, "", "mods/brutal.pk3"])
            
        i += 1
        
        progress.Update(i + 21, "Creating a new CSV...") 
        
    with open ('games.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, dialect = 'unix')
        for l in lines:
            writer.writerow(l)
            
    progress.Update(progress.GetRange(), "Done, have fun!")