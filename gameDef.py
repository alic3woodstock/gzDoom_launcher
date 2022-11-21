import wx
import modGroup

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
        
    def SetExec(self, gameExec):
        self._exec = gameExec
        
    def GetGroup(self):
        return self._group
        
    def SetGroup(self, group):
        self._group = group
        
    def GetGroupName(self):         
        return self.GetGroup().GetGroupName()
    
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
    def __init__ (self, listId, name, tab, gameExec = './gzdoom/gzdoom', groupId = 1, lastMod = 0, wad = 'freedoom1.wad', 
                  files = [], groupName = None):
        self._item = wx.ListItem()
        self._item.SetId(listId) 
        self._item.SetData(listId) #listctrl may change item id
        self._item.SetText(name)
        self._tab = tab
        self._exec = gameExec
        self._group = modGroup.ModGroup(groupId, groupName)
        self._lastMod = lastMod
        self._iWad = wad
        self._files = files

