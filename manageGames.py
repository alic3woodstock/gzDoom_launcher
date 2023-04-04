import wx
import wx.dataview as dataview
import gameDefDb
import addGame
import wx.lib.dialogs as wxdialogs
import os
import functions


class MyDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(MyDialog, self).__init__(parent, title=title, size=(500, wx.DefaultCoord))
        panel = wx.Panel(self)

        btnAdd = wx.Button(panel, wx.ID_ANY, "Add...")
        btnEdit = wx.Button(panel, wx.ID_ANY, "Edit...")
        btnDelete = wx.Button(panel, wx.ID_ANY, "Delete...")
        btnClose = wx.Button(panel, wx.ID_CLOSE)
        if os.name == "nt":
            self.dataGrid = dataview.DataViewListCtrl(panel, id=wx.ID_ANY, size=(400, 300))
        else:
            self.dataGrid = dataview.DataViewListCtrl(panel, id=wx.ID_ANY, size=(640, 480))

        self.dataGrid.AppendTextColumn("Name")
        self.dataGrid.AppendTextColumn("Type")
        self.dataGrid.AppendTextColumn("Game Exec")
        self.dataGrid.AppendTextColumn("Mod Group")
        self.dataGrid.AppendTextColumn("iWad")

        self.ReadDB()

        # Bind eventes
        self.Bind(wx.EVT_BUTTON, self.BtnAddOnClick, btnAdd)
        self.Bind(wx.EVT_BUTTON, self.BtnDeleteOnClick, btnDelete)
        self.Bind(wx.EVT_BUTTON, self.BtnEditOnClick, btnEdit)
        self.Bind(dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.DataGridOnDbClick, self.dataGrid)
        self.Bind(wx.EVT_CHAR_HOOK, self.DataGridOnKeyPress, self.dataGrid)
        self.Bind(wx.EVT_BUTTON, self.BtnCloseOnClick, btnClose)
        panel.Bind(wx.EVT_CHAR_HOOK, self.PanelOnKeyHook)

        boxv = wx.BoxSizer(wx.VERTICAL)
        boxButtons = wx.BoxSizer(wx.HORIZONTAL)
        boxv.AddSpacer(4)
        boxv.Add(self.dataGrid, 0, wx.EXPAND | wx.ALL)
        boxv.AddSpacer(4)
        boxv.Add(wx.StaticLine(panel, id=wx.ID_ANY, style=wx.LI_HORIZONTAL), 0, wx.EXPAND)
        boxButtons.Add(btnAdd, 0, wx.ALL, border=4)
        boxButtons.Add(btnEdit, 0, wx.ALL, border=4)
        boxButtons.Add(btnDelete, 0, wx.ALL, border=4)
        boxButtons.Add(btnClose, 0, wx.ALL, border=4)
        btnAdd.MoveBeforeInTabOrder(btnEdit)
        btnEdit.MoveBeforeInTabOrder(btnDelete)
        btnDelete.MoveBeforeInTabOrder(btnClose)
        boxv.Add(boxButtons, 0, wx.ALIGN_RIGHT)
        panel.SetSizer(boxv)
        boxv.SetSizeHints(self)

    def BtnAddOnClick(self, event):
        try:
            addGameDiag = addGame.MyDialog(self, "Add game, map or mod")
            addGameDiag.ShowModal()
            self.ReadDB()
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def BtnEditOnClick(self, event):
        try:
            self.EditGame()
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def BtnDeleteOnClick(self, event):
        try:
            if self.dataGrid.HasSelection():
                game = self.dataGrid.RowToItem(self.dataGrid.GetSelectedRow())
                gameId = self.dataGrid.GetItemData(game)
                gameName = self.dataGrid.GetValue(self.dataGrid.GetSelectedRow(), 0)
                result = wxdialogs.messageDialog(self, message="Delete game: " + gameName + "?",
                                                 title='Delete Game',
                                                 aStyle=wx.ICON_WARNING | wx.YES | wx.NO | wx.RIGHT)
                if result.accepted:
                    gamedata = gameDefDb.GameDefDb()
                    gamedata.DeleteGameById(gameId)
                    self.ReadDB()
            else:
                wxdialogs.alertDialog(self, message='Select an item first!', title='Alert')
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def DataGridOnDbClick(self, event):
        try:
            self.EditGame()
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def DataGridOnKeyPress(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.EditGame()
        event.Skip()

    def BtnCloseOnClick(self, event):
        try:
            self.Close()
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def ReadDB(self):
        sItem = 0
        if self.dataGrid.HasSelection():
            sItem = self.dataGrid.GetSelectedRow()
        self.dataGrid.DeleteAllItems()
        gameData = gameDefDb.GameDefDb()
        games = gameData.SelectAllGames()
        for game in games:
            if game.GetTab() == 0:
                strType = "Game"
            elif game.GetTab() == 1:
                strType = "Map"
            else:
                strType = "Mod"

            self.dataGrid.AppendItem([game.GetItem().GetText(), strType, game.GetExec(),
                                      game.GetGroupName(), game.GetIWad()], game.GetItem().GetData())

        for i in range(self.dataGrid.GetColumnCount()):
            self.dataGrid.GetColumn(i).SetWidth(wx.COL_WIDTH_AUTOSIZE)
        self.dataGrid.SetFocus()
        if self.dataGrid.GetItemCount() > sItem:
            self.dataGrid.SelectRow(sItem)
        elif self.dataGrid.GetItemCount() > 0:
            self.dataGrid.SelectRow(self.dataGrid.GetItemCount() - 1)

    def EditGame(self):
        if self.dataGrid.HasSelection():
            game = self.dataGrid.RowToItem(self.dataGrid.GetSelectedRow())
            gameId = self.dataGrid.GetItemData(game)
            gameData = gameDefDb.GameDefDb()
            gameDef = gameData.SelectGameById(gameId)
            addGameDiag = addGame.MyDialog(self, "Edit game, map or mod", gameDef)
            addGameDiag.ShowModal()
            self.ReadDB()
        else:
            wxdialogs.alertDialog(self, message='Select an item first!', title='Alert')

    def PanelOnKeyHook(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
