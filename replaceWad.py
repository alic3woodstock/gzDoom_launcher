import wx
import wx.lib.dialogs as wxdialogs

TEXT_HEIGHT = 400

# Most frontend code was copyed from addGame.py consider put in a separate class.        

class SmallButton(wx.Button):
    def AcceptsFocusFromKeyboard(self):
        return False

class MyDialog(wx.Dialog): 
    def __init__(self, parent, title, label = "Wad (doom2.wad recommended):"): 
        super(MyDialog, self).__init__(parent, title = title, size = (500, wx.DefaultCoord)) 
        panel = wx.Panel(self)

        # Label / textbox
        lblWad = wx.StaticText(panel, label = label)        
        self.txtWad = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))
        btnFindWad = SmallButton(panel, label = '...', size=(24, self.txtWad.GetSize().GetHeight()))                           

        # Buttons
        btnCancel = wx.Button(panel, wx.ID_CANCEL)
        btnOK = wx.Button(panel, wx.ID_OK)
        
        # Bind events        
        self.Bind(wx.EVT_BUTTON, self.BtnFindWadOnClick, btnFindWad)
        
        
        #Align componentes
        gridData = wx.FlexGridSizer(2, 2, 4, 4)
        gridData.AddGrowableCol(0)
        gridData.AddGrowableCol(1)
        
        gridData.Add(lblWad, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border = 4)
        boxWad =  wx.BoxSizer(wx.HORIZONTAL)
        boxWad.Add(self.txtWad)
        boxWad.Add(btnFindWad)        
        gridData.Add(boxWad, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border = 4)

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


    def BtnFindWadOnClick(self, event):
        wadFile = wxdialogs.fileDialog(parent=self, title='Open', style=wx.FD_OPEN)
        try:
            wadP = wadFile.paths[0] # if cancel rises an exception
            self.txtWad.Clear()
            self.txtWad.write(wadP)
        except:
            pass    
