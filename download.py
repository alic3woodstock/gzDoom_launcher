import wx
import requests
import os

class MyDialog(wx.Dialog): 
   def __init__(self, parent, title): 
      super(MyDialog, self).__init__(parent, title = title, size = (250,150)) 
      panel = wx.Panel(self) 
      self.btn = wx.Button(panel, wx.ID_OK, label = "ok", size = (50,20), pos = (75,50))

def StartDownload(parent):
    progress = wx.ProgressDialog("Download Files", "Starting Download...", maximum=100, parent=parent,
            style=wx.PD_APP_MODAL | wx.STAY_ON_TOP)
    if(not os.path.exists("downloads")):
        os.mkdir("downloads")
    
    GetFile("https://github.com/coelckers/gzdoom/releases/download/g4.8.2/gzdoom-4-8-2-Windows-64bit.zip","gzdoom.zip", progress, 1, 2)
    GetFile("https://github.com/Blasphemer/blasphemer/releases/download/v0.1.7/blasphem-0.1.7.zip","blasphem-0.1.7.zip", progress, 2, 2)    
    
    
def GetFile(url,name, progress, current, total):               
    url = url
    r = requests.get(url, stream = True)
    with open("downloads/" + name, "wb") as downloadF:
        total_length = int(r.headers.get('content-length'))
        #progress.SetRange(total_length)        
        i = 1024
        
        #updates dialog based on percentage since I don't know the total size of all files before download each file.
        totalParc = (100 // total)
        percentDone = (current - 1) * totalParc
        for chunk in r.iter_content(chunk_size = 1024):
            if chunk:            
                downloadF.write(chunk)                    
                #Adding 1 prevents dialog freezes even with download completed
                y = i * totalParc // total_length + 1 + percentDone  
                
                if (y > 100): #prevent Update function error.
                    y = 100
                progress.Update(y, "Geting file " +  str(current) + "/" + str(total) + "...")
                i += 1024
                
        if (i < total_length):
            #the line below showd never occur in normal situations, but sometimes we have to expect odd results.        
            progress.Update(100, "Failed...") #close the dialog even if download fails.
            return False
        else:
            return True        
