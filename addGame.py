import wx
import wx.lib.dialogs as wxdialogs
import os
import csv
import wx.dataview as dataview
import gameDef
import gameDefDb

TEXT_HEIGHT = 400

class SmallButton(wx.Button):
    def AcceptsFocusFromKeyboard(self):
        return False

class MyDialog(wx.Dialog):
    _gameDef = None    
    
    def __init__(self, parent, title, gameDef = None): 
        self._gameDef = gameDef
        super(MyDialog, self).__init__(parent, title = title, size = (500, wx.DefaultCoord)) 
        panel = wx.Panel(self)
        
        #"Name","Tab Index","Executable","Group","Last run mod","iWad","file1"
        
        # Name        
        lblName = wx.StaticText(panel, label = "Name:")
        self.txtName = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))        
        
        # Tab Index
        lblType = wx.StaticText(panel, label = "Type:")
        self.cbxType = wx.ComboBox(panel, style = wx.CB_READONLY, choices = ["Game", "Map", "Mod"])
        self.cbxType.Select(0)
        
        # Executable
        lblExec = wx.StaticText(panel, label = "Game Exec.:")
        self.txtExec = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))
        if not gameDef:
            if (os.name == 'nt'):
                self.txtExec.write('gzdoom\\gzdoom.exe')
            else:
                self.txtExec.write('gzdoom/gzdoom')
        btnFindExec = SmallButton(panel, label = '...', size=(24, self.txtExec.GetSize().GetHeight()))
        
        # Mod Group
        lblGroup = wx.StaticText(panel, label = "Mod Group:")
        self.cbxGroup = wx.ComboBox(panel, style = wx.CB_READONLY, choices = ["doom", "heretic", "hexen",
                                                                        "strife", "other"])
        self.cbxGroup.Select(0)
        
        # iWAD
        lblWad = wx.StaticText(panel, label = "Wad:")        
        self.txtWad = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))
        btnFindWad = SmallButton(panel, label = '...', size=(24, self.txtExec.GetSize().GetHeight()))
        
        # Files
        lblFiles = wx.StaticText(panel, label = "Files:")
        self.txtFiles = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))
        btnFindFiles = SmallButton(panel, label = '...', size=(24, self.txtExec.GetSize().GetHeight()))
        btnAddFile = SmallButton(panel, label = '+', size=(24, self.txtExec.GetSize().GetHeight()))
        self.gridFiles = dataview.DataViewListCtrl(panel, id=wx.ID_ANY, style=dataview.DV_NO_HEADER |
                                                   dataview.DV_ROW_LINES, size=(400,100))
        self.gridFiles.AppendTextColumn(label = "Path")
        btnDeleteFile = SmallButton(panel, label = '-', size=(48, self.txtExec.GetSize().GetHeight()))
        btnClearGrid = SmallButton(panel, label = 'Clear', size=(48, self.txtExec.GetSize().GetHeight()))
        
        
        # Buttons
        btnCancel = wx.Button(panel, wx.ID_CANCEL)
        btnOK = wx.Button(panel, wx.ID_OK)      
        
        if gameDef:
            self.txtName.write(gameDef.GetItem().GetText())
            self.cbxType.Select(gameDef.GetTab())
            self.txtExec.write(gameDef.GetExec())
            self.txtWad.write(gameDef.GetIWad())  
            for f in gameDef.GetFiles():
                self.gridFiles.AppendItem([f])          
        
        # Bind Events
        self.Bind(wx.EVT_COMBOBOX, self.CbxTypeOnChange, self.cbxType)
        self.Bind(wx.EVT_BUTTON, self.BtnFindExecOnClick, btnFindExec)
        self.Bind(wx.EVT_BUTTON, self.BtnFindWadOnClick, btnFindWad)
        self.Bind(wx.EVT_BUTTON, self.BtnFindFilesOnClick, btnFindFiles)
        self.Bind(wx.EVT_BUTTON, self.BtnAddFileOnClick, btnAddFile)
        self.Bind(wx.EVT_BUTTON, self.BtnOKOnClick, btnOK)
        self.Bind(wx.EVT_CHAR_HOOK, self.TxtFilesOnKeyDown, self.txtFiles)
        self.Bind(wx.EVT_BUTTON, self.BtnDeleteFileOnClick, btnDeleteFile)
        self.Bind(wx.EVT_BUTTON, self.BtnClearGridOnClick, btnClearGrid)
        
        #Align componentes
        gridData = wx.FlexGridSizer(8, 0, 4, 4)
        gridData.AddGrowableCol(0)
        gridData.AddGrowableCol(1)                

        gridData.Add(lblName, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        gridData.Add(self.txtName, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)

        gridData.Add(lblType, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        gridData.Add(self.cbxType, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)

        gridData.Add(lblExec, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        boxExec =  wx.BoxSizer(wx.HORIZONTAL)
        boxExec.Add(self.txtExec)
        boxExec.Add(btnFindExec)
        gridData.Add(boxExec, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)        
        
        gridData.Add(lblGroup, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        gridData.Add(self.cbxGroup, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)
        
        gridData.Add(lblWad, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        boxWad =  wx.BoxSizer(wx.HORIZONTAL)
        boxWad.Add(self.txtWad)
        boxWad.Add(btnFindWad)        
        gridData.Add(boxWad, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)
        
        gridData.Add(lblFiles, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        boxFiles = wx.BoxSizer(wx.HORIZONTAL)
        boxFiles.Add(self.txtFiles)
        boxFiles.Add(btnFindFiles)
        boxFiles.Add(btnAddFile)
        gridData.Add(boxFiles, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)        
        
        
        boxSpacer = wx.BoxSizer(wx.HORIZONTAL)
        boxSpacer.AddSpacer(4)        
        boxGrid = wx.BoxSizer(wx.HORIZONTAL)
        boxGrid.Add(self.gridFiles)
        boxBtnGrid = wx.BoxSizer(wx.VERTICAL)
        boxBtnGrid.Add(btnDeleteFile)
        boxBtnGrid.Add(btnClearGrid)
        boxGrid.Add(boxBtnGrid)        
        gridData.Add(boxSpacer, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)
        gridData.Add(boxGrid, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)

        boxv = wx.BoxSizer(wx.VERTICAL)
        boxButtons = wx.BoxSizer(wx.HORIZONTAL)
        boxv.AddSpacer(4)
        boxv.Add(gridData, 0, wx.ALIGN_CENTER)
        boxv.AddSpacer(4)
        boxv.Add(wx.StaticLine(panel, id=wx.ID_ANY, style = wx.LI_HORIZONTAL), 0, wx.EXPAND)
        boxButtons.Add(btnOK, 0, wx.ALL, border = 4)
        boxButtons.Add(btnCancel, 0, wx.ALL, border = 4)
        btnOK.MoveBeforeInTabOrder(btnCancel)
        boxv.Add(boxButtons, 0 , wx.ALIGN_RIGHT)
        panel.SetSizer(boxv)
        boxv.SetSizeHints(self)        
        
    def BtnOKOnClick(self, event):
        canSave = True
        try:
            if (self.txtName.GetLineText(0).find(",") >= 0):
                wxdialogs.alertDialog(self, 'Name can not contain ","!')
                canSave = False
            elif (not os.path.isfile(self.txtExec.GetLineText(0))):
                wxdialogs.alertDialog(self, message='Game exec. not found!', title='Alert')
                canSave = False
                
            if (self.cbxType.GetSelection() <= 1):
                if (not os.path.isfile(self.txtWad.GetLineText(0))):                
                    wxdialogs.alertDialog(self, message='Wad not found!', title='Alert')
                    canSave = False
            else:
                self.txtWad.Clear()          
                    
            if canSave:
                if (self.txtFiles.GetLineText(0) != ''):            
                    self.AppendFile(self.txtFiles.GetLineText(0))
                    
                for i in range (self.gridFiles.GetItemCount()):
                    gameFile = self.gridFiles.GetValue(i, 0)
                    if (not os.path.isfile(gameFile)):
                        wxdialogs.alertDialog(self, message='File ' + gameFile + ' not found!', title='Alert')
                        canSave = False
                        break
            if canSave:
                if (not os.path.isfile('games.sqlite3')):
                    wxdialogs.alertDialog(self, message='Database not found, press extract before add a game!')
                    canSave = False
        except:
            wxdialogs.alertDialog(self, message='Unknown error!', title='Alert')
            canSave = False
        
        if canSave:
            if os.name == "nt":
                gameExec = self.txtExec.GetLineText(0).replace("/","\\")
            else:
                gameExec = self.txtExec.GetLineText(0).replace("\\","/")
                
            game = gameDef.GameDef(0, 
                                   self.txtName.GetLineText(0), 
                                   self.cbxType.GetSelection(), 
                                   gameExec,
                                   self.cbxGroup.GetStringSelection(),
                                   0, 
                                   self.txtWad.GetLineText(0))
            for i in range (self.gridFiles.GetItemCount()):
                game.GetFiles().append(self.gridFiles.GetValue(i, 0))
                             

            try:
                gameData = gameDefDb.GameDefDb()
                if self._gameDef:
                    game.GetItem().SetData(self._gameDef.GetItem().GetData())
                    updateFiles = self._gameDef.GetFiles() != game.GetFiles()
                    gameData.UpdateGame(game, updateFiles)
                else:
                    gameData.InsertGame(game)
                event.Skip()
            except:
                wxdialogs.alertDialog(self, message='Failed to write data!')
                
    def CbxTypeOnChange(self, event):
        if (event.GetEventObject().GetSelection() > 1):
            self.txtWad.Enable(False)
        else:
            self.txtWad.Enable(True)
            
    def BtnFindExecOnClick(self, event):
        exeFile = wxdialogs.fileDialog(parent=self, title='Open', style=wx.FD_OPEN)
        try:
            exeP = exeFile.paths[0] # if cancel rises an exception
            self.txtExec.Clear()
            self.txtExec.write(exeP)
        except:
            pass
        
    def BtnFindWadOnClick(self, event):
        wadFile = wxdialogs.fileDialog(parent=self, title='Open', style=wx.FD_OPEN)
        try:
            wadP = wadFile.paths[0] # if cancel rises an exception
            self.txtWad.Clear()
            self.txtWad.write(wadP)
        except:
            pass    
    
    def BtnFindFilesOnClick(self, event):
        extraFiles = wxdialogs.fileDialog(self, title='Open', style = wx.FD_OPEN | wx.FD_MULTIPLE)
        try:
            for f in extraFiles.paths:
                self.AppendFile(f)
        except:
            pass      
        
    def BtnAddFileOnClick(self, event):
        if self.AppendFile(self.txtFiles.GetLineText(0)):
            self.txtFiles.Clear()
        else:
            self.txtFiles.SetFocus()
            self.txtFiles.SelectAll()
        
    def TxtFilesOnKeyDown(self, event):
        if (event.GetKeyCode() == wx.WXK_RETURN):
            if self.AppendFile(self.txtFiles.GetLineText(0)):
                self.txtFiles.Clear()
            else:
                self.txtFiles.SetFocus()
                self.txtFiles.SelectAll()
        event.Skip()     
        
    def BtnDeleteFileOnClick(self, event):
        if self.gridFiles.HasSelection():
            self.gridFiles.DeleteItem(self.gridFiles.GetSelectedRow())
            
    def BtnClearGridOnClick(self, event):
        self.gridFiles.DeleteAllItems()   
        
    def AppendFile(self, f): 
        canInsert = True        
        if (not os.path.isfile(f)):
            wxdialogs.alertDialog(self, message='File ' + f + ' not found!', title='Alert')
            canInsert = False
        else:        
            for i in range (self.gridFiles.GetItemCount()):
                if self.gridFiles.GetValue(i,0) == f:
                    wxdialogs.alertDialog(self, message='File ' + f + ' already inserted!', title='Alert')
                    canInsert = False
                    break   
        if canInsert:                     
            self.gridFiles.AppendItem([f])
        return canInsert
        
        
