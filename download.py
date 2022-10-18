import wx
import requests
import os
import dropbox

# class MyDialog(wx.Dialog): 
   # def __init__(self, parent, title): 
      # super(MyDialog, self).__init__(parent, title = title, size = (250,150)) 
      # panel = wx.Panel(self) 
      # self.btn = wx.Button(panel, wx.ID_OK, label = "ok", size = (50,20), pos = (75,50))

MAX_RANGE = 1000
totalFiles = 0
current = 0

class Url():
    _url = ""
    _fileName = ""

    def __init__(self, url, fileName):
        self._url = url
        self._fileName = fileName
    
    def GetUrl(self):
        return self._url
        
    def GetFileName(self):
        return self._fileName
        
    def GetFilePath(self):
        return ("downloads/" + self._fileName)
    

def StartDownload(parent):
    global progress
    progress = wx.ProgressDialog("Download Files", "Starting Download...", maximum=100, parent=parent,
            style=wx.PD_APP_MODAL | wx.STAY_ON_TOP)
    progress.SetRange(MAX_RANGE)
            
    if(not os.path.exists("downloads")):
        os.mkdir("downloads")
        
    files = []        
    
    #GzDoom
    if (os.name == "nt"): 
        files.append(Url("https://github.com/coelckers/gzdoom/releases/download/g4.8.2/gzdoom-4-8-2-Windows-64bit.zip","gzdoom.zip"))
    else:
        files.append(Url("https://github.com/ZDoom/gzdoom/releases/download/g4.8.2/GZDoom.v4.8.2.Linux.tar.xz","gzdoom.tar.xz"))
    
    #Blasphemer
    files.append(Url("https://github.com/Blasphemer/blasphemer/releases/download/v0.1.7/blasphem-0.1.7.zip","blasphem.zip"))
    files.append(Url("https://github.com/Blasphemer/blasphemer/releases/download/v0.1.7/blasphemer-texture-pack.zip","blasphemer-texture-pack.zip"))
    
    #Freedoom
    files.append(Url("https://github.com/freedoom/freedoom/releases/download/v0.12.1/freedoom-0.12.1.zip","freedoom.zip"))
    
    #150skins 
    files.append(Url("https://doomshack.org/wads/150skins.zip","150skins.zip"))
    
    #Beaultiful Doom
    files.append(Url("https://github.com/jekyllgrim/Beautiful-Doom/releases/download/7.1.6/Beautiful_Doom_716.pk3","Beaultiful_Doom.pk3"))
    
    #Brutal Doom
    files.append(Url("https://github.com/BLOODWOLF333/Brutal-Doom-Community-Expansion/releases/download/V21.11.2/brutalv21.11.2.pk3","brutal.pk3"))
    
    #maps
    files.append(Url("https://uca33b27708475e12d125e97f419.dl.dropboxusercontent.com/cd/0/get/BvEKSo2HAmEsPFPw5zleo0AviWI0jLE8Tezy_jf8b16dU4Gr8o4-4V8FauiFG75gLIjl-S1la5Pa-16dESkZY5hhIRNnQxIFH4wrDlb0gUy9lz1jrAW55mhhsNqYZXgRdT24-vKqX5Qk4P5iqIoL8xCUvsRg4yzSug4x3U2e86YVa4HmhBy7eG14m1nAiGa1hkY/file?_download_id=9815169858843142338449664975160590021971407357996857694533512262&_notify_domain=www.dropbox.com&dl=1","Sunder_2407.zip")) #it's easier not deal with spaces at file names
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/megawads/av.zip","av.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/aaliens.zip","aliens.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/megawads/btsx_e1.zip","btsx_e1.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/megawads/btsx_e2.zip","btsx_e2.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/eviternity.zip","eviternity.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/themes/hr/hr.zip","hr.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/themes/hr/hr2final.zip","hr2final.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/heretic/Ports/htchest.zip","htchest.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/themes/mm/mm_allup.zip","mm_allup.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/themes/mm/mm2.zip","mm2.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/megawads/pl2.zip","pl2.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/megawads/scythe.zip","scythe.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/scythe2.zip","scythe2.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/s-u/scythex.zip","scythex.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/sunlust.zip","sunlust.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/heretic/s-u/unbeliev.zip","unbeliev.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/valiant.zip","valiant.zip"))
    files.append(Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/zof.zip","zof.zip"))
    
    global totalFiles
    totalFiles = len(files)
    
    for f in files:
        GetFile(f)        
    
def GetFile(f):  
    global current
    global progress
    if (current < totalFiles):
        current  += 1

        #updates dialog based on a fixed max range since I don't know the total size of all files before download each file.
        totalParc = (MAX_RANGE / totalFiles)
        percentDone = (current - 1) * totalParc
        
        if (not os.path.isfile(f.GetFilePath())):
            r = requests.get(f.GetUrl(), stream = True)        
            with open(f.GetFilePath(), "wb") as downloadF:
                total_length = r.headers.get('content-length')
                if (total_length == None):
                    total_length = 0
                else:
                    total_length = int(total_length)
                i = 1024               
                
                for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:           
                        intProgress = int(round(percentDone))
                        if (total_length > 0):
                            #Adding 1 prevents dialog freezes even with download completed
                            intProgress = int(round(i * totalParc / total_length + 1 + percentDone))
                            strTotal = str(total_length // 1024)
                        else:
                            strTotal = "..."
                        downloadF.write(chunk)
                    i += 1024
                    
                    if (intProgress >= MAX_RANGE):
                        intProgress = MAX_RANGE - 1
                        
                    progress.Update(intProgress, "Downloading file " +  str(current) + "/" + str(totalFiles) + ": " +
                            str(i // 1024) + "k of " + strTotal + "k")            
        else:
            intProgress = int(round(percentDone + totalParc))
            
            if (intProgress >= MAX_RANGE):
                intProgress = MAX_RANGE - 1
            
            progress.Update(intProgress, "File exists, skiping...")            
                       
        if (current == totalFiles):
            progress.Update(MAX_RANGE, "Download Complete!")