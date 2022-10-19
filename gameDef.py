import wx

class GameDef():

    def GetItem(self):
        return self._item

    def SetItem(self, item):
        self._item = item
    
    def GetTab(self):
        return self._tab
    
    def SetTab(self, tab):
        self._tab = tab

    def GetExec(self):
        return self._exec
        
    def SetExec(self, exec):
        self._exec = exec
        
    def GetGroup(self):
        return self._group
        
    def SetGroup(self, group):
        self._group = group
        
    def GetLastMod(self):
        return self._lastMod
        
    def SetLastMod(self, lastMod):
        self._lastMod = lastMod
        
    def GetIWad(self):
        return self._iWad
        
    def SetIWad(self, wad):
        self._iWad = wad
        
    def GetFiles(self):
        return self._files
        
    def SetFiles(self,files):
        self._files = files
        
    def AppendFile(self,file):
        self._files.append(file)
    
    #Id,Name,Tab Index,Exe,Group,Last run mod,iWad,files...
    def __init__ (self, id, name, tab, exec = './gzdoom/gzdoom', group = 'doom', lastMod = 0, wad = 'freedoom1.wad', files = []):
        self._item = wx.ListItem()
        self._item.SetId(id) 
        self._item.SetData(id) #listctrl may change item id
        self._item.SetText(name)
        self._tab = tab
        self._exec = exec
        self._group = group
        self._lastMod = lastMod
        self._iWad = wad
        self._files = files

    # def __init__(self):
        # self._item = wx.ListItem()
        # self._item.SetId(0)
        # self._item.SetText('')
        # self._tab = 0 #integer
        # self._exec = '' #string
        # self._group = '' #string
        # self_lastMod = 0 #integer
        # self._iWad = '' #string
        # self._files = [] #array
