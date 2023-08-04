import wx
import gameDefDb
import gameTabConfig
import wx.lib.dialogs as wx_dialogs

TEXT_HEIGHT = 300


class MyDialog(wx.Dialog):
    _gameDef = None

    def __init__(self, parent, title, game=None):
        super(MyDialog, self).__init__(parent, title=title, size=(500, wx.DefaultCoord))
        panel = wx.Panel(self)

        gridTabs = wx.FlexGridSizer(0, 2, 4, 4)
        gridTabs.AddGrowableCol(0)
        gridTabs.AddGrowableCol(1)

        # Tab config
        lblTabTitle = wx.StaticText(panel, label="Enable/Disable Tabs:")
        self.chkTabs = []
        self.txtTabs = []

        for i in range(1, 10):
            self.chkTabs.append(wx.CheckBox(panel, label="Tab " + str(i) + ":"))
            self.txtTabs.append(wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord)))

        self.chkTabs[0].Disable()

        lines = []

        for j in range(9):
            lines.append([self.chkTabs[j], self.txtTabs[j]])

        for line in lines:
            gridTabs.Add(line[0], 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=4)
            gridTabs.Add(line[1], 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=4)

        # Boolean options
        self.chkCheckUpdates = wx.CheckBox(panel, label="Check for GZDoom updates on startup")

        # Buttons
        btnCancel = wx.Button(panel, wx.ID_CANCEL)
        btnOK = wx.Button(panel, wx.ID_OK)

        # Bind Events
        self.Bind(wx.EVT_BUTTON, self.BtnOKOnClick, btnOK)


        boxV = wx.BoxSizer(wx.VERTICAL)
        boxButtons = wx.BoxSizer(wx.HORIZONTAL)
        boxV.AddSpacer(4)
        boxV.Add(lblTabTitle)
        boxV.Add(gridTabs, 0, wx.ALIGN_CENTER)
        boxV.AddSpacer(4)
        boxV.Add(wx.StaticLine(panel, id=wx.ID_ANY, style=wx.LI_HORIZONTAL), 0, wx.EXPAND)
        boxV.AddSpacer(4)
        boxV.Add(self.chkCheckUpdates)
        boxV.Add(wx.StaticLine(panel, id=wx.ID_ANY, style=wx.LI_HORIZONTAL), 0, wx.EXPAND)
        boxButtons.Add(btnOK, 0, wx.ALL, border=4)
        boxButtons.Add(btnCancel, 0, wx.ALL, border=4)
        btnOK.MoveBeforeInTabOrder(btnCancel)
        boxV.Add(boxButtons, 0, wx.ALIGN_RIGHT)
        panel.SetSizer(boxV)
        boxV.SetSizeHints(self)

        settingsDb = gameDefDb.GameDefDb()

        checkUpdate = settingsDb.ReadConfig("checkupdate", "bool")
        self.chkCheckUpdates.SetValue(checkUpdate)
        tabConfigs = settingsDb.SelectAllGameTabConfigs()
        for t in tabConfigs:
            self.chkTabs[t.GetIndex()].SetValue(t.IsEnabled())
            self.txtTabs[t.GetIndex()].SetValue(t.GetName())


    def BtnOKOnClick(self, event):
        canSave = True

        for i in range(9):
            if (self.chkTabs[i].GetValue()) and (not self.txtTabs[i].GetValue().strip()):
                wx_dialogs.alertDialog(self, "Enabled tab title can not be blank")
                canSave = False

        if canSave:
            settingsDb = gameDefDb.GameDefDb()
            for i in range(9):
                tabConfig = gameTabConfig.GameTabConfig(i, self.txtTabs[i].GetValue().strip(),
                                                        self.chkTabs[i].GetValue())
                settingsDb.UpdateGameTabConfig(tabConfig)

            settingsDb.WriteConfig("checkupdate", self.chkCheckUpdates.GetValue(), "bool")
            self.Close()