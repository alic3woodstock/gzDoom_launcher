import wx
import wx.lib.dialogs as wxdialogs
import os
import csv

class MyDialog(wx.Dialog): 
    def __init__(self, parent, title): 
        super(MyDialog, self).__init__(parent, title = title, size = (500, wx.DefaultCoord)) 
        panel = wx.Panel(self)
        
        boxv = wx.BoxSizer(wx.VERTICAL)
        boxButtons = wx.BoxSizer(wx.HORIZONTAL) 
        
        #"Name","Tab Index","Executable","Group","Last run mod","iWad","file1"
        
        # Name        
        lblName = wx.StaticText(panel, label = "Name:")
        self.txtName = wx.TextCtrl(panel, size=(300, wx.DefaultCoord))        
        
        # Tab Index
        lblType = wx.StaticText(panel, label = "Type:")
        self.cbxType = wx.ComboBox(panel, style = wx.CB_READONLY, choices = ["Game", "Map", "Mod"])
        self.cbxType.Select(0)
        
        # Executable
        lblExec = wx.StaticText(panel, label = "Game Exec.:")
        self.txtExec = wx.TextCtrl(panel, size=(300, wx.DefaultCoord))
        if (os.name == 'nt'):
            self.txtExec.write('gzdoom\\gzdoom.exe')
        else:
            self.txtExec.write('gzdoom/gzdoom')
             
        
        # Mod Group
        lblGroup = wx.StaticText(panel, label = "Mod Group:")
        self.cbxGroup = wx.ComboBox(panel, style = wx.CB_READONLY, choices = ["doom", "heretic", "hexen",
                                                                        "strife", "other"])
        self.cbxGroup.Select(0)
        
        # iWAD
        lblWad = wx.StaticText(panel, label = "Wad:")        
        self.txtWad = wx.TextCtrl(panel, size=(300, wx.DefaultCoord))
        
        # Files
        lblFiles = wx.StaticText(panel, label = "Files (file1, file2, ...):")
        self.txtFiles = wx.TextCtrl(panel, size=(300, wx.DefaultCoord))
        
        # Buttons
        btnCancel = wx.Button(panel, wx.ID_CANCEL)
        btnOK = wx.Button(panel, wx.ID_OK)      

        #Align componentes
        gridData = wx.FlexGridSizer(6, 0, 4, 4)
        gridData.AddGrowableCol(0)
        gridData.AddGrowableCol(1)                

        gridData.Add(lblName, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        gridData.Add(self.txtName, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)

        gridData.Add(lblType, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        gridData.Add(self.cbxType, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)

        gridData.Add(lblExec, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        gridData.Add(self.txtExec, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)
        
        gridData.Add(lblGroup, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        gridData.Add(self.cbxGroup, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)
        
        gridData.Add(lblWad, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        gridData.Add(self.txtWad, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)
        
        gridData.Add(lblFiles, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        gridData.Add(self.txtFiles, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)

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
        
        self.Bind(wx.EVT_BUTTON, self.btnOkClick, btnOK)
        
    def btnOkClick(self, event):
        canSave = True
        try:
            if (self.txtName.GetLineText(0).find(",") >= 0):
                wxdialogs.alertDialog(self, 'Name can not contain ","!')
                canSave = False
            elif (not os.path.isfile(self.txtExec.GetLineText(0))):
                wxdialogs.alertDialog(self, message='Game exec. not found!', title='Alert')
                canSave = False
            elif (not os.path.isfile(self.txtWad.GetLineText(0))):
                wxdialogs.alertDialog(self, message='Wad not found!', title='Alert')
                canSave = False
                
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