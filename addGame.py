import wx
import wx.lib.dialogs as wxdialogs
import os
import csv

TEXT_HEIGHT = 400

class SmallButton(wx.Button):
    def AcceptsFocusFromKeyboard(self):
        return False

class MyDialog(wx.Dialog): 
    def __init__(self, parent, title): 
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
        lblFiles = wx.StaticText(panel, label = "Files (file1, file2, ...):")
        self.txtFiles = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))
        btnFindFiles = SmallButton(panel, label = '...', size=(24, self.txtExec.GetSize().GetHeight()))
        
        # Buttons
        btnCancel = wx.Button(panel, wx.ID_CANCEL)
        btnOK = wx.Button(panel, wx.ID_OK)      
        
        # Bind Events
        self.Bind(wx.EVT_COMBOBOX, self.cbxTypeOnChange, self.cbxType)
        self.Bind(wx.EVT_BUTTON, self.btnFindExecOnClick, btnFindExec)
        self.Bind(wx.EVT_BUTTON, self.btnFindWadOnClick, btnFindWad)
        self.Bind(wx.EVT_BUTTON, self.btnFindFilesOnClick, btnFindFiles)
        self.Bind(wx.EVT_BUTTON, self.btnOKOnClick, btnOK)

        #Align componentes
        gridData = wx.FlexGridSizer(6, 0, 4, 4)
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
        gridData.Add(boxFiles, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)

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
        
    def btnOKOnClick(self, event):
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
                gameFiles =[]
                if (self.txtFiles.GetLineText(0) != ''):            
                    gameFiles = self.txtFiles.GetLineText(0).split(',')
                    
                    for gameFile in gameFiles:
                        if (not os.path.isfile(gameFile)):
                            wxdialogs.alertDialog(self, message='File ' + gameFile + ' not found!', title='Alert')
                            canSave = False
                            break
            if canSave:
                if (not os.path.isfile('games.csv')):
                    wxdialogs.alertDialog(self, message='File games.csv not found, press extract before add a game!')
                    canSave = False
                
        except:
            wxdialogs.alertDialog(self, message='Unknown error!', title='Alert')
            canSave = False
        
        if canSave:
            with open ('games.csv', newline = '') as csvfile:
                reader = csv.reader(csvfile, dialect='unix')
                gameId = 0
                firstRow = True
                for row in reader:
                    if (not firstRow):
                        gameId = int(row[0])
                    firstRow = False
                
                gameId += 1
                
            try:
                with open ('games.csv', 'a', newline = '') as csvfile:
                    writer = csv.writer(csvfile, dialect='unix')                    
                    
                    csvLine = [gameId, self.txtName.GetLineText(0), self.cbxType.GetSelection(),
                               self.txtExec.GetLineText(0).replace("/","\\"), self.cbxGroup.GetStringSelection(),
                               0, self.txtWad.GetLineText(0)]
                    
                    if len(gameFiles) > 0:
                        for gameFile in gameFiles:
                            csvLine.append(gameFile)                    
                    writer.writerow(csvLine)
                    event.Skip()
            except:
                wxdialogs.alertDialog(self, message='Failed to save games.csv!')
                
    def cbxTypeOnChange(self, event):
        if (event.GetEventObject().GetSelection() > 1):
            self.txtWad.Enable(False)
        else:
            self.txtWad.Enable(True)
            
    def btnFindExecOnClick(self, event):
        exeFile = wxdialogs.fileDialog(parent=self, title='Open', style=wx.FD_OPEN)
        try:
            exeP = exeFile.paths[0] # if cancel rises an exception
            self.txtExec.Clear()
            self.txtExec.write(exeP)
        except:
            pass
        
    def btnFindWadOnClick(self, event):
        wadFile = wxdialogs.fileDialog(parent=self, title='Open', style=wx.FD_OPEN)
        try:
            wadP = wadFile.paths[0] # if cancel rises an exception
            self.txtWad.Clear()
            self.txtWad.write(wadP)
        except:
            pass    
    
    def btnFindFilesOnClick(self, event):
        extraFiles = wxdialogs.fileDialog(self, title='Open', style = wx.FD_OPEN | wx.FD_MULTIPLE)
        try:
            extraF = ','.join(extraFiles.paths)
            self.txtFiles.Clear()
            self.txtFiles.write(extraF)
        except:
            pass       
