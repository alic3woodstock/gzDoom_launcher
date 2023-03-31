import wx
import wx.lib.dialogs as wxdialogs
import os
import gameDefDb
import functions

TEXT_HEIGHT = 400


class SmallButton(wx.Button):
    def AcceptsFocusFromKeyboard(self):
        return False


class MyDialog(wx.Dialog):
    def __init__(self, parent, title, modgroup=1):
        super(MyDialog, self).__init__(parent, title=title, size=(500, wx.DefaultCoord))
        panel = wx.Panel(self)

        label = ""

        if modgroup == 1:
            label = "Wad (doom2.wad recommended):"
        elif modgroup == 2:
            label = "Wad (heretic.wad recommended):"

        self.modgroup = modgroup

        # Label / textbox
        lblWad = wx.StaticText(panel, label=label)
        self.txtWad = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))
        btnFindWad = SmallButton(panel, label='...', size=(36, self.txtWad.GetSize().GetHeight()))

        # Buttons
        btnCancel = wx.Button(panel, wx.ID_CANCEL)
        btnOK = wx.Button(panel, wx.ID_OK)

        # Bind events        
        self.Bind(wx.EVT_BUTTON, self.BtnFindWadOnClick, btnFindWad)
        self.Bind(wx.EVT_BUTTON, self.BtnOkClick, btnOK)
        self.Bind(wx.EVT_CHAR_HOOK, self.TxtWadOnKeyPress, self.txtWad)

        # Align componentes
        gridData = wx.FlexGridSizer(2, 2, 4, 4)
        gridData.AddGrowableCol(0)
        gridData.AddGrowableCol(1)

        gridData.Add(lblWad, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=4)
        boxWad = wx.BoxSizer(wx.HORIZONTAL)
        boxWad.Add(self.txtWad)
        boxWad.Add(btnFindWad)
        gridData.Add(boxWad, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=4)

        boxv = wx.BoxSizer(wx.VERTICAL)
        boxButtons = wx.BoxSizer(wx.HORIZONTAL)
        boxv.AddSpacer(4)
        boxv.Add(gridData, 0, wx.ALIGN_CENTER)
        boxv.AddSpacer(4)
        boxv.Add(wx.StaticLine(panel, id=wx.ID_ANY, style=wx.LI_HORIZONTAL), 0, wx.EXPAND)
        boxButtons.Add(btnOK, 0, wx.ALL, border=4)
        boxButtons.Add(btnCancel, 0, wx.ALL, border=4)
        btnOK.MoveBeforeInTabOrder(btnCancel)
        boxv.Add(boxButtons, 0, wx.ALIGN_RIGHT)
        panel.SetSizer(boxv)
        boxv.SetSizeHints(self)

    def BtnFindWadOnClick(self, event):
        wadFile = wxdialogs.fileDialog(parent=self, title='Open', style=wx.FD_OPEN)
        try:
            wadP = wadFile.paths[0]  # if cancel rises an exception
            self.txtWad.Clear()
            self.txtWad.write(wadP)
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def BtnOkClick(self, event):
        try:
            self.UpdateWad()
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def TxtWadOnKeyPress(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.UpdateWad()
        event.Skip()

    def UpdateWad(self):
        if self.modgroup == 1:
            msg = "Replace wad on all maps of \"doom\" group?"
        elif self.modgroup == 2:
            msg = "Replace wad on all maps of \"heretic\" group?"
        else:
            msg = "Raplace wad on all maps?"

        result = wxdialogs.messageDialog(self, message=msg,
                                         title='Replace wad', aStyle=wx.ICON_WARNING | wx.YES | wx.NO | wx.RIGHT)
        if result.accepted:
            canSave = True
            try:
                if not os.path.isfile(self.txtWad.GetLineText(0)):
                    wxdialogs.alertDialog(self, message='Wad not found!', title='Alert')
                    canSave = False

            except Exception as e:
                functions.log(e)
                wxdialogs.alertDialog(self, message='Unknown error!', title='Alert')
                canSave = False

            if canSave:
                try:
                    gameData = gameDefDb.GameDefDb()
                    gameData.UpdateWad(self.txtWad.GetLineText(0), self.modgroup)
                    wxdialogs.messageDialog(self, message='Wads replaced successesfully!',
                                            title='Success', aStyle=wx.ICON_INFORMATION | wx.OK | wx.RIGHT)
                    self.Close()
                except Exception as e:
                    functions.log(e)
                    wxdialogs.alertDialog(self, message='Failed to write data!')
