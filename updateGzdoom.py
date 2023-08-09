import wx
import download
import gameDefDb

class MyDialog(wx.Dialog):
    _gameDef = None

    def __init__(self, parent, title, game=None):
        super(MyDialog, self).__init__(parent, title=title, size=(500, wx.DefaultCoord))
        panel = wx.Panel(self)

        # Buttons
        btnNo = wx.Button(panel, wx.ID_NO)
        btnYes = wx.Button(panel, wx.ID_YES)
        self.chkCheckUpdates = wx.CheckBox(panel, label="Check for GZDoom updates on startup")

        # Bind Events
        self.Bind(wx.EVT_BUTTON, self.BtnYesClick, btnYes)
        self.Bind(wx.EVT_BUTTON, self.BtnNoClick, btnNo)

        boxV = wx.BoxSizer(wx.VERTICAL)
        boxButtons = wx.BoxSizer(wx.HORIZONTAL)
        boxV.AddSpacer(4)
        boxV.Add(self.chkCheckUpdates)
        boxV.Add(wx.StaticLine(panel, id=wx.ID_ANY, style=wx.LI_HORIZONTAL), 0, wx.EXPAND)
        boxButtons.Add(btnYes, 0, wx.ALL, border=4)
        boxButtons.Add(btnNo, 0, wx.ALL, border=4)
        btnYes.MoveBeforeInTabOrder(btnNo)
        boxV.Add(boxButtons, 0, wx.ALIGN_RIGHT)
        panel.SetSizer(boxV)
        boxV.SetSizeHints(self)

        settingsDb = gameDefDb.GameDefDb()
        checkUpdate = settingsDb.ReadConfig("checkupdate", "bool")
        self.chkCheckUpdates.SetValue(checkUpdate)

    def BtnYesClick(self, event):
        settingsDb = gameDefDb.GameDefDb()
        settingsDb.WriteConfig("checkupdate", self.chkCheckUpdates.GetValue(), "bool")
        self.Close()
        download.UpdateGzDoom(self)

    def BtnNoClick(self, event):
        self.Close()