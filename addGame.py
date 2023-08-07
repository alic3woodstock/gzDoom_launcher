import wx
import wx.lib.dialogs as wx_dialogs
import os
import wx.dataview as dataview
import gameDef
import gameDefDb
import functions

TEXT_HEIGHT = 400


# Some try...except on events was used only to stop warnings from IDE (pyCharm or pyDev)

class SmallButton(wx.Button):
    def AcceptsFocusFromKeyboard(self):
        return False


class MyDialog(wx.Dialog):
    _gameDef = None

    def __init__(self, parent, title, game=None):
        self._gameDef = game
        super(MyDialog, self).__init__(parent, title=title, size=(500, wx.DefaultCoord))
        panel = wx.Panel(self)

        gameData = gameDefDb.GameDefDb()
        # "Name", "Is Mod" "Tab Index","Executable","Group","Last run mod","iWad","file1"
        # Name
        lblName = wx.StaticText(panel, label="Name:")
        self.txtName = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))

        lblMod = wx.StaticText(panel, label="")
        self.chkMod = wx.CheckBox(panel, label="Is as Mod",)

        # Tab Index
        lblType = wx.StaticText(panel, label="Tab:")
        self.cbxType = wx.ComboBox(panel, style=wx.CB_READONLY)
        tabConfig = gameData.SelectAllGameTabConfigs()
        for t in tabConfig:
            if t.GetName().strip():
                self.cbxType.Append(t.GetName(), t)
            else:
                self.cbxType.Append("(no title)", t)
        self.cbxType.Select(0)

        # Executable
        lblExec = wx.StaticText(panel, label="Game Exec.:")
        self.txtExec = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))
        if not game:
            if os.name == 'nt':
                self.txtExec.write('gzdoom\\gzdoom.exe')
            else:
                self.txtExec.write('gzdoom/gzdoom')
        btnFindExec = SmallButton(panel, label='...', size=(36, self.txtExec.GetSize().GetHeight()))

        # Mod Group
        lblGroup = wx.StaticText(panel, label="Mod Group:")
        self.cbxGroup = wx.ComboBox(panel, style=wx.CB_READONLY)
        groups = gameData.SelectAllGroups()
        for g in groups:
            self.cbxGroup.Append(g.GetGroupName(), g)
        self.cbxGroup.Select(0)

        # iWAD
        lblWad = wx.StaticText(panel, label="Wad:")
        self.txtWad = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))
        self.btnFindWad = SmallButton(panel, label='...', size=(36, self.txtExec.GetSize().GetHeight()))

        # Command line parameters
        lblCmdPar = wx.StaticText(panel, label="Cmd. Parameters:")
        self.txtCmdPar = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))

        # Files
        lblFiles = wx.StaticText(panel, label="Files:")
        self.txtFiles = wx.TextCtrl(panel, size=(TEXT_HEIGHT, wx.DefaultCoord))
        btnFindFiles = SmallButton(panel, label='...', size=(36, self.txtExec.GetSize().GetHeight()))
        self.gridFiles = dataview.DataViewListCtrl(
            panel, id=wx.ID_ANY, style=dataview.DV_NO_HEADER | dataview.DV_ROW_LINES, size=(400, 100))
        self.gridFiles.AppendTextColumn(label="Path")
        btnAddFile = SmallButton(panel, label='Add', size=(64, self.txtExec.GetSize().GetHeight()))
        btnDeleteFile = SmallButton(panel, label='Del', size=(64, self.txtExec.GetSize().GetHeight()))
        btnClearGrid = SmallButton(panel, label='Clear', size=(64, self.txtExec.GetSize().GetHeight()))

        # Buttons
        btnCancel = wx.Button(panel, wx.ID_CANCEL)
        btnOK = wx.Button(panel, wx.ID_OK)

        if game:
            self.txtName.write(game.GetItem().GetText())
            if game.GetTab() >= 0:
                self.chkMod.SetValue(False)
                self.cbxType.Select(game.GetTab())
            else:
                self.chkMod.SetValue(True)
                self.cbxType.Enable(False)
                self.txtWad.Enable(False)
                self.btnFindWad.Enable(False)

            self.txtExec.write(game.GetExec())
            self.txtWad.write(game.GetIWad())

            for f in game.GetFiles():
                self.gridFiles.AppendItem([f])

            for i in range(self.cbxGroup.GetCount()):
                gGroup = game.GetGroup().GetGroupId()
                cGroup = self.cbxGroup.GetClientData(i).GetGroupId()
                if cGroup == gGroup:
                    self.cbxGroup.Select(i)

            self.txtCmdPar.write(game.GetCmdParams())

        # Bind Events
        self.Bind(wx.EVT_CHECKBOX, self.ChkModOnChange, self.chkMod)
        self.Bind(wx.EVT_BUTTON, self.BtnFindExecOnClick, btnFindExec)
        self.Bind(wx.EVT_BUTTON, self.BtnFindWadOnClick, self.btnFindWad)
        self.Bind(wx.EVT_BUTTON, self.BtnFindFilesOnClick, btnFindFiles)
        self.Bind(wx.EVT_BUTTON, self.BtnAddFileOnClick, btnAddFile)
        self.Bind(wx.EVT_BUTTON, self.BtnOKOnClick, btnOK)
        self.Bind(wx.EVT_CHAR_HOOK, self.TxtFilesOnKeyDown, self.txtFiles)
        self.Bind(wx.EVT_BUTTON, self.BtnDeleteFileOnClick, btnDeleteFile)
        self.Bind(wx.EVT_BUTTON, self.BtnClearGridOnClick, btnClearGrid)

        # Align componentes
        gridData = wx.FlexGridSizer(10, 0, 5, 5)
        gridData.AddGrowableCol(0)
        gridData.AddGrowableCol(1)

        lines = [[lblName, self.txtName], [lblMod, self.chkMod], [lblType, self.cbxType]]
        boxExec = wx.BoxSizer(wx.HORIZONTAL)
        boxExec.Add(self.txtExec)
        boxExec.Add(btnFindExec)
        lines.append([lblExec, boxExec])
        lines.append([lblGroup, self.cbxGroup])

        boxWad = wx.BoxSizer(wx.HORIZONTAL)
        boxWad.Add(self.txtWad)
        boxWad.Add(self.btnFindWad)
        lines.append([lblWad, boxWad])

        lines.append([lblCmdPar, self.txtCmdPar])

        boxFiles = wx.BoxSizer(wx.HORIZONTAL)
        boxFiles.Add(self.txtFiles)
        boxFiles.Add(btnFindFiles)
        lines.append([lblFiles, boxFiles])

        boxSpacer = wx.BoxSizer(wx.HORIZONTAL)
        boxSpacer.AddSpacer(4)
        boxGrid = wx.BoxSizer(wx.HORIZONTAL)
        boxGrid.Add(self.gridFiles)
        boxBtnGrid = wx.BoxSizer(wx.VERTICAL)
        boxBtnGrid.Add(btnAddFile)
        boxBtnGrid.Add(btnDeleteFile)
        boxBtnGrid.Add(btnClearGrid)
        boxGrid.Add(boxBtnGrid)
        lines.append([boxSpacer, boxGrid])

        for line in lines:
            gridData.Add(line[0], 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=4)
            gridData.Add(line[1], 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=4)

        boxV = wx.BoxSizer(wx.VERTICAL)
        boxButtons = wx.BoxSizer(wx.HORIZONTAL)
        boxV.AddSpacer(4)
        boxV.Add(gridData, 0, wx.ALIGN_CENTER)
        boxV.AddSpacer(4)
        boxV.Add(wx.StaticLine(panel, id=wx.ID_ANY, style=wx.LI_HORIZONTAL), 0, wx.EXPAND)
        boxButtons.Add(btnOK, 0, wx.ALL, border=4)
        boxButtons.Add(btnCancel, 0, wx.ALL, border=4)
        btnOK.MoveBeforeInTabOrder(btnCancel)
        boxV.Add(boxButtons, 0, wx.ALIGN_RIGHT)
        panel.SetSizer(boxV)
        boxV.SetSizeHints(self)

    def BtnOKOnClick(self, event):
        canSave = True
        try:
            if self.txtName.GetLineText(0).strip() == "":
                wx_dialogs.alertDialog(self, "Name can not be blank")
                canSave = False
            elif self.txtName.GetLineText(0).find(",") >= 0:
                wx_dialogs.alertDialog(self, 'Name can not contain ","!')
                canSave = False
            elif not os.path.isfile(self.txtExec.GetLineText(0)):
                wx_dialogs.alertDialog(self, message='Game exec. not found!', title='Alert')
                canSave = False

            if canSave:
                if self.chkMod.IsChecked():
                    self.txtWad.Clear()
                elif self.txtWad.GetLineText(0).strip():
                    if not os.path.isfile(self.txtWad.GetLineText(0)):
                        wx_dialogs.alertDialog(self, message='Invalid wad!',
                                               title='Alert')
                        canSave = False

            if canSave:
                if self.txtFiles.GetLineText(0) != '':
                    self.AppendFile(self.txtFiles.GetLineText(0))

                for i in range(self.gridFiles.GetItemCount()):
                    gameFile = self.gridFiles.GetValue(i, 0)
                    if not os.path.isfile(gameFile):
                        wx_dialogs.alertDialog(self, message='File ' + gameFile + ' not found!', title='Alert')
                        canSave = False
                        break
            if canSave:
                if not os.path.isfile('games.sqlite3'):
                    wx_dialogs.alertDialog(self, message='Database not found, press extract before add a game!')
                    canSave = False
        except Exception as e:
            functions.log(e)
            wx_dialogs.alertDialog(self, message='Unknown error!', title='Alert')
            canSave = False

        if canSave:
            if os.name == "nt":
                gameExec = self.txtExec.GetLineText(0).replace("/", "\\")
            else:
                gameExec = self.txtExec.GetLineText(0).replace("\\", "/")

            groupId = self.cbxGroup.GetClientData(self.cbxGroup.GetSelection()).GetGroupId()
            groupName = self.cbxGroup.GetStringSelection()

            if self.chkMod.IsChecked():
                tabIndex = -1
            else:
                tabIndex = self.cbxType.GetClientData(self.cbxType.GetSelection()).GetIndex()

            game = gameDef.GameDef(0,
                                   self.txtName.GetLineText(0),
                                   tabIndex,
                                   gameExec,
                                   groupId,
                                   0,
                                   self.txtWad.GetLineText(0),
                                   [],
                                   groupName,
                                   self.txtCmdPar.GetLineText(0))
            for i in range(self.gridFiles.GetItemCount()):
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
            except Exception as e:
                wx_dialogs.alertDialog(self, message='Failed to write data!')
                functions.log(e)

    def ChkModOnChange(self, event):
        self.cbxType.Enable(not event.GetEventObject().IsChecked())
        self.txtWad.Enable(not event.GetEventObject().IsChecked())
        self.btnFindWad.Enable(not event.GetEventObject().IsChecked())

    def BtnFindExecOnClick(self, event):
        exeFile = wx_dialogs.fileDialog(parent=self, title='Open', style=wx.FD_OPEN)
        try:
            exeP = exeFile.paths[0]  # if cancel rises an exception
            self.txtExec.Clear()
            self.txtExec.write(exeP)
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def BtnFindWadOnClick(self, event):
        wadFile = wx_dialogs.fileDialog(parent=self, title='Open', style=wx.FD_OPEN)
        try:
            wadP = wadFile.paths[0]  # if cancel rises an exception
            self.txtWad.Clear()
            self.txtWad.write(wadP)
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def BtnFindFilesOnClick(self, event):
        extraFiles = wx_dialogs.fileDialog(self, title='Open', style=wx.FD_OPEN | wx.FD_MULTIPLE)
        try:
            for f in extraFiles.paths:
                self.AppendFile(f)
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def BtnAddFileOnClick(self, event):
        try:
            if self.AppendFile(self.txtFiles.GetLineText(0)):
                self.txtFiles.Clear()
            else:
                self.txtFiles.SetFocus()
                self.txtFiles.SelectAll()
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def TxtFilesOnKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            if self.AppendFile(self.txtFiles.GetLineText(0)):
                self.txtFiles.Clear()
            else:
                self.txtFiles.SetFocus()
                self.txtFiles.SelectAll()
        event.Skip()

    def BtnDeleteFileOnClick(self, event):
        try:
            if self.gridFiles.HasSelection():
                self.gridFiles.DeleteItem(self.gridFiles.GetSelectedRow())
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def BtnClearGridOnClick(self, event):
        try:
            self.gridFiles.DeleteAllItems()
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def AppendFile(self, f):
        canInsert = True
        if not os.path.isfile(f):
            wx_dialogs.alertDialog(self, message='File ' + f + ' not found!', title='Alert')
            canInsert = False
        else:
            for i in range(self.gridFiles.GetItemCount()):
                if self.gridFiles.GetValue(i, 0) == f:
                    wx_dialogs.alertDialog(self, message='File ' + f + ' already inserted!', title='Alert')
                    canInsert = False
                    break
        if canInsert:
            self.gridFiles.AppendItem([f])
        return canInsert
