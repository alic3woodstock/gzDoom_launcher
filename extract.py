import os
import shutil
import zipfile
import wx
import csv
import tarfile

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
            try:
                if (self.GetFormat() == "zip"):
                    zip = zipfile.ZipFile(fromFile)
                    zip.extractall(path)

                if (self.GetFormat() == "xz"):
                    zip = tarfile.open(fromFile, 'r:xz')
                    zip.extractall(path)
            except:
                print("Extracting " + self.GetName() + " failed")
        
    def CopyTo(self,path):
        try:  
            fromFile = "downloads/" + self._name
            
            if (self.GetFormat() == "zip") or (self.GetFormat() == "pk3"):
                zip = zipfile.ZipFile(fromFile)
                zip.testzip
        
            if(not os.path.exists(path)):
                os.mkdir(path)
                
            if os.path.isfile(fromFile):
                shutil.copy(fromFile,path)
        except:
            print("Copying " + self.GetName() + " failed")
    
    def GetName(self):
        return self._name
        
    def TestFileName(self,str):
        if (self.GetName().lower().find(str) >= 0):
            return True
        else:
            return False
            
    def GetFormat(self):
        return self._format
        
    def GetMapName(self):
        fromFile = "downloads/" + self.GetName()
        zip = zipfile.ZipFile(fromFile)
        
        # Mps with non standard txt
        if (self.GetName() == "mm2.zip"):
            return "Memento Mori 2"            
        if (self.GetName() == "av.zip"):
            return "Alien Vendetta"            
        if (self.GetName() == "hr.zip"):
            return "Hell Revealed"

        try:
            txtFile = zip.namelist()
            for t in txtFile:
                if (t.lower().find(".txt") >= 0):
                    with zip.open(t) as f:
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
                
        # txtFiles = os.listdir("temp/map")
        # print(txtFiles)
        # except:            
            # print(self.GetName())
        
        
        
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
    
    progress.SetRange(len(zipFiles) + 22) #if everthyng works number of csv in the list is 22
    i = 1;
    for zip in zipFiles:
        if (zip.TestFileName("gzdoom")):
            if (os.name == "nt"):  
                zip.ExtractTo("gzdoom")
            else:
                try:
                    zip.ExtractTo("temp")
                    dirs = os.listdir("temp")
                    for dir in dirs:
                        if (dir.lower().find("gzdoom") >= 0):
                            shutil.copytree("temp/" + dir,"gzdoom")
                except:
                    print("Copying gzdoom failed!")
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
        exec = ".\\gzdoom\\gzdoom.exe"
    else:
        exec = "./gzdoom/gzdoom"
        
    i = 0
    for zip in zipFiles:
        fullPath = zip.GetFormat() + "/" + zip.GetName() 
        if (zip.TestFileName("blasphem")): 
            blasphenWad = (fullPath) # works because wad comes first in the list
        elif (zip.TestFileName("bls")):
            lines.append([i, "Blasphem", 0, exec, "heretic", 0, blasphenWad, fullPath])
        elif (zip.TestFileName("freedoom1")):            
            lines.append([i, "Freedoom Phase 1", 0, exec, "doom", 0, fullPath])
        elif (zip.TestFileName("freedoom2")):
            lines.append([i, "Freedoom Phase 2", 0, exec, "doom", 0, fullPath])
        elif (zip.GetFormat() == "maps"):     
            if (zip.TestFileName("htchest") or zip.TestFileName("unbeliev")):
                lines.append([i, zip.GetMapName(), 1, exec, "heretic", 0, "wads/blasphem-0.1.7.wad", fullPath])
            else:
                lines.append([i, zip.GetMapName(), 1, exec, "doom", 0, "wads/freedoom2.wad", fullPath])

        i += 1
        
        progress.Update(i + 21, "Creating a new CSV...") 
        
    with open ('games.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, dialect = 'unix')
        for l in lines:
            writer.writerow(l)
            
    progress.Update(progress.GetRange(), "Done, have fun.")