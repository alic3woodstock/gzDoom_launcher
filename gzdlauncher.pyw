#!/usr/bin/env python
import wx
import os
import gameDef
import download
import extract
import wx.lib.mixins.listctrl as listmix
import addGame
import gameDefDb
import manageGames
import replaceWad
import wx.lib.dialogs as wxdialogs
import functions
import aboutDialog
import settings
import gameTabConfig
import updateGzdoom

class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, index = 0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)
        self._index = index

    def GetIndex(self):
        return self._index


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        self.itens = []
        functions.setDataPath()
        wx.Frame.__init__(self, parent, title=title)

        panel = wx.Panel(self, wx.ID_ANY)
        font = panel.GetFont()
        font.MakeLarger()
        panel.SetFont(font)

        menu = wx.MenuBar()
        fileMenu = wx.Menu()
        menuManageGames = fileMenu.Append(105, item="&Manage games...")
        fileMenu.Append(id=wx.ID_SEPARATOR, item="")
        menuExtract = fileMenu.Append(102, item="&Reset to default games")
        fileMenu.Append(id=wx.ID_SEPARATOR, item="")
        menuSettings = fileMenu.Append(104, item="&Settings...")
        menuAbout = fileMenu.Append(109, item="&About...")
        fileMenu.Append(id=wx.ID_SEPARATOR, item="")
        menuClose = fileMenu.Append(103, item="&Exit")
        menu.Append(fileMenu, "&File")

        utilMenu = wx.Menu()
        menuReplaceDoom = utilMenu.Append(106, item="Replace &Doom maps wad...")
        menuReplaceHeretic = utilMenu.Append(107, item="Replace &Heretic maps wad...")
        menuUpdateGzDoom = utilMenu.Append(108, item='&Update gzDoom')
        menu.Append(utilMenu, "&Utilities")

        self.SetMenuBar(menu)

        gameTab = wx.Notebook(panel)
        tabConfigs = []

        if not os.path.exists(functions.dbPath):
            gameData = gameDefDb.GameDefDb()
            gameData.CreateGameTable()

        try:
            gameDefDb.GameDefDb().UpdateDatabase()
        except Exception as e:
            functions.log(e)
            wxdialogs.alertDialog(self, "Erro ao atualizar o banco de dados!")

        self.listMods = wx.ComboBox(panel, style=wx.CB_READONLY)
        self.listRun = self.ConfigGameList(gameTab)

        # gameTab.InsertPage(1, listRun[1], 'Maps', 1)

        btnOk = wx.Button(panel, wx.ID_ANY, 'Run Game')
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(gameTab, 1, wx.EXPAND | wx.ALL, border=4)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.AddSpacer(4)
        box2.Add(wx.StaticText(panel, label="Run with mod:"), 0, wx.CENTER, border=4)
        box2.AddSpacer(4)
        box2.Add(self.listMods, 0, wx.EXPAND | wx.ALL, border=4)
        box3 = wx.BoxSizer(wx.HORIZONTAL)
        box3.Add(btnOk, 0, wx.ALL, border=4)
        box.Add(box2, 0, wx.ALIGN_LEFT | wx.ALL)
        box.AddSpacer(4)
        box.Add(wx.StaticLine(panel, id=wx.ID_ANY, style=wx.LI_HORIZONTAL), 0, wx.EXPAND)
        box.Add(box3, 0, wx.ALIGN_RIGHT | wx.ALL)

        # Bind Events
        self.Bind(wx.EVT_BUTTON, lambda event: self.BtnOkOnPress(event, gameTab), btnOk)
        panel.Bind(wx.EVT_CHAR_HOOK, lambda event: self.PanelOnKeyHook(event, gameTab))

        # Bind events for menu itens
        # self.Bind(wx.EVT_MENU, self.MenuDownloadOnClick, menuDownload)
        self.Bind(wx.EVT_MENU, lambda event: self.MenuExtractOnClick(event, gameTab), menuExtract)
        self.Bind(wx.EVT_MENU, self.MenuCloseOnClick, menuClose)
        self.Bind(wx.EVT_MENU, lambda event: self.MenuManageGamesOnClick(event, gameTab),
                  menuManageGames)
        self.Bind(wx.EVT_MENU, lambda event: self.MenuReplaceDoomOnClick(event, gameTab),
                  menuReplaceDoom)
        self.Bind(wx.EVT_MENU, lambda event: self.MenuReplaceHereticOnClick(event, gameTab),
                  menuReplaceHeretic)
        self.Bind(wx.EVT_MENU, self.MenuUpdageGzDoomOnClick, menuUpdateGzDoom)
        self.Bind(wx.EVT_MENU, lambda event: self.SettingsMenuOnClick(event, gameTab), menuSettings)
        self.Bind(wx.EVT_MENU, self.AboutMenuOnClick, menuAbout)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.GameTabOnPageChange, gameTab)

        self.ReadDB()

        panel.SetSizer(box)
        box.SetSizeHints(self)
        self.Centre()
        self.Show(True)

        settingsDb = gameDefDb.GameDefDb()
        if settingsDb.ReadConfig("checkupdate", "bool"):
            updateDialog = updateGzdoom.MyDialog(self, "Update GzDoom")
            if not download.CheckGzDoomVersion():
                updateDialog.ShowModal()

        self.listRun[0].Select(0)
        gameTab.SetSelection(0)
        self.listRun[0].SetFocus()
        self.listRun[0].Focus(0)

    def MenuCloseOnClick(self, event):
        try:
            self.Close()
        except Exception as e:
            functions.log('MenuCloseOnClick')
            functions.log(e)

    def MenuAddGameOnClick(self, event, tab):
        try:
            addGameDiag = addGame.MyDialog(self, "Add game, map or mod")
            addGameDiag.ShowModal()
            self.ReadDB()
            gameList = tab.GetChildren()[tab.GetSelection()]
            gameList.Select(0)
        except Exception as e:
            functions.log('MenuAddGameOnClick')
            functions.log(e)

    def MenuManageGamesOnClick(self, event, tab):
        try:
            manageGamesDialog = manageGames.MyDialog(self, "Manage Game/Mod List")
            manageGamesDialog.ShowModal()
            self.ReadDB()
            gameList = tab.GetChildren()[tab.GetSelection()]
            gameList.Select(0)
        except Exception as e:
            functions.log('MenuManageGamesOnClick')
            functions.log(e)

    def BtnOkOnPress(self, event, tab):
        try:
            self.LaunchGame(tab.GetChildren()[tab.GetSelection()])
        except Exception as e:
            functions.log('BtnOkOnPressent')
            functions.log(e)

    def ListCtrlOnDClick(self, event):
        self.LaunchGame(event.GetEventObject())
        event.Skip()

    def ListCtrlOnSelect(self, event):
        self.RefreshhModList(event.GetEventObject())

    def PanelOnKeyHook(self, event, tab):
        event.DoAllowNextEvent()
        changeFocus = False
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.LaunchGame(tab.GetChildren()[tab.GetSelection()])
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        if (event.GetKeyCode() == wx.WXK_RIGHT) and (tab.GetSelection() < tab.GetPageCount() - 1):
            tab.SetSelection(tab.GetSelection() + 1)
            changeFocus = True
        if (event.GetKeyCode() == wx.WXK_LEFT) and (tab.GetSelection() > 0):
            tab.SetSelection(tab.GetSelection() - 1)
            changeFocus = True
        if changeFocus:
            gameList = tab.GetChildren()[tab.GetSelection()]
            gameList.Select(0)
            gameList.SetFocus()
            gameList.Focus(0)
        if (event.GetKeyCode() == wx.WXK_SPACE) or (event.GetKeyCode() == wx.WXK_TAB):
            if self.listMods.GetSelection() < (self.listMods.GetCount() - 1):
                self.listMods.SetSelection(self.listMods.GetSelection() + 1)
            else:
                self.listMods.SetSelection(0)
        event.Skip()

    def MenuExtractOnClick(self, event, tab):
        try:
            result = wxdialogs.messageDialog(self, message="This will reset game database to the default values. \n" +
                                                           "Do you want to continue?",
                                             title='Reset to default games',
                                             aStyle=wx.ICON_WARNING | wx.YES | wx.NO | wx.RIGHT)
            if result.accepted:
                extract.ExtractAll(self)
                self.listRun = self.ConfigGameList(tab)
                self.ReadDB()
                gameList = tab.GetChildren()[tab.GetSelection()]
                gameList.Select(0)
        except Exception as e:
            functions.log('MenuExtractOnClick')
            functions.log(e)

    def MenuReplaceDoomOnClick(self, event, tab):
        try:
            menuReplaceDialog = replaceWad.MyDialog(self, "Replace Doom maps wad")
            menuReplaceDialog.ShowModal()
            self.ReadDB()
            gameList = tab.GetChildren()[tab.GetSelection()]
            gameList.Select(0)
        except Exception as e:
            functions.log('MenuReplaceDoomOnClick')
            functions.log(e)

    def MenuReplaceHereticOnClick(self, event, tab):
        try:
            menuReplaceDialog = replaceWad.MyDialog(self, "Replace Heretic maps wad", 2)
            menuReplaceDialog.ShowModal()
            self.ReadDB()
            gameList = tab.GetChildren()[tab.GetSelection()]
            gameList.Select(0)
        except Exception as e:
            functions.log('MenuReplaceHereticOnClick')
            functions.log(e)

    def LaunchGame(self, listCtrl):
        if listCtrl.GetFirstSelected() < 0:
            listCtrl.Select(0)

        item = ""
        tempItem = listCtrl.GetItem(listCtrl.GetFirstSelected())

        mod = self.listMods.GetClientData(self.listMods.GetSelection())

        for i in self.itens:
            if i.GetItem().GetData() == tempItem.GetData():
                item = i
                i.SetLastMod(mod.GetItem().GetData())

        if isinstance(item, gameDef.GameDef):
            if item.GetIWad().strip() == "":
                command = item.GetExec() + " "
            else:
                command = item.GetExec() + " -iWad " + item.GetIWad()

            for file in item.GetFiles():
                command += " -file " + file

            if mod.GetItem().GetData() >= 0:
                for file in mod.GetFiles():
                    command += " -file " + file

            if item.GetCmdParams().strip() != "":
                command += item.GetCmdParams().strip()

            functions.log(command, False)
            os.popen(command)
            gameData = gameDefDb.GameDefDb()
            gameData.UpdateLastRunMod(item, mod)
            listCtrl.SetFocus()

    def MenuUpdageGzDoomOnClick(self, event):
        try:
            download.UpdateGzDoom(self)
        except Exception as e:
            functions.log('MenuUpdageGzDoomOnClick')
            functions.log(e)

    def AboutMenuOnClick(self, event):
        try:
            aboutMenuDialog = aboutDialog.MyDialog(self, "About")
            aboutMenuDialog.ShowModal()
        except Exception as e:
            functions.log('AboutMenuOnClick')
            functions.log(e)

    def SettingsMenuOnClick(self, event, tab):
        try:
            settingsMenuDialog = settings.MyDialog(self, "Settings")
            settingsMenuDialog.ShowModal()
            self.listRun = self.ConfigGameList(tab)
            tab.SetSelection(0)
            self.ReadDB()

            if self.listRun[0].GetFirstSelected() < 0:
                self.listRun[0].Select(0)
        except Exception as e:
            functions.log('SettingsMenuOnClick')
            functions.log(e)

    def GameTabOnPageChange(self, event):
        try:
            tab = event.GetEventObject()
            gameList = tab.GetChildren()[tab.GetSelection()]
            if gameList.GetItemCount() > 0:
                gameList.Select(0)
                self.RefreshhModList(gameList)
        except Exception as e:
            functions.log('GameTabOnPageChange')
            functions.log(e)

    def ReadDB(self):
        gameData = gameDefDb.GameDefDb()
        tempItens = gameData.SelectAllGames()
        for l in self.listRun:
            l.DeleteAllItems()

        self.itens = []

        # Show itens in alphabetical order.
        order = []
        for i in tempItens:
            order.append([i.GetItem().GetText(), i.GetItem().GetData()])
        order.sort()
        i = 0

        for o in order:
            for j in tempItens:
                if j.GetItem().GetData() == o[1]:
                    j.GetItem().SetId(i)
                    self.itens.append(j)
                    i += 1

        self.listMods.Clear()
        self.listMods.Insert("None                    ", 0, gameDef.GameDef(-1, "None", 2))
        self.listMods.SetSelection(0)

        for i in range(len(self.itens)):
            if self.itens[i].GetTab() >= 0:
                for l in self.listRun:
                    if l.GetIndex() == self.itens[i].GetTab():
                        l.InsertItem(self.itens[i].GetItem())
                # self.listRun[self.itens[i].GetTab()].InsertItem(self.itens[i].GetItem())
            else:
                self.listMods.Append(self.itens[i].GetItem().GetText(), self.itens[i])

        i = 0
        for l in self.listRun:
            if l.GetItemCount() <= 0:
                tempItem = wx.ListItem()
                tempItem.SetId(0)
                if i == 0:
                    tempItem.SetText('No games found, click "Reset to default games"...')
                else:
                    tempItem.SetText('Empty tab')
                l.InsertItem(tempItem)
            i += 1

        columnWidth = self.listRun[0].GetColumnWidth(0)
        for i in range(1, len(self.listRun)):
            if self.listRun[i].GetItemCount() > 0:
                if self.listRun[i].GetColumnWidth(0) >= self.listRun[i-1].GetColumnWidth(0):
                    columnWidth = self.listRun[i].GetColumnWidth(0)

        for l in self.listRun:
            l.resizeColumn(columnWidth)

    def ConfigGameList(self, gameTab):

        tabData = gameDefDb.GameDefDb()

        tabConfig = tabData.SelctGameTabConfigByIndex(0)
        if not tabConfig.GetName().strip():
            tabConfig = gameTabConfig.GameTabConfig(0, "Games", True)
            tabData.UpdateGameTabConfig([tabConfig])

        tabConfigs = tabData.SelectAllGameTabConfigs()

        gameTab.DeleteAllPages()
        listRun = []
        for t in tabConfigs:
            if t.IsEnabled():
                listRun.append(
                    MyListCtrl(gameTab, ID=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER,
                               index = t.GetIndex()
                               ))
                gameTab.AddPage(listRun[-1], t.GetName(), 1)
                listRun[-1].Bind(wx.EVT_LEFT_DCLICK, self.ListCtrlOnDClick)
                listRun[-1].Bind(wx.EVT_LIST_ITEM_SELECTED, self.ListCtrlOnSelect)
                listRun[-1].AppendColumn('Levels')

        return listRun

    def RefreshhModList(self, listRun):
        self.listMods.Clear()
        self.listMods.Insert("None                    ", 0, gameDef.GameDef(-1, "None", 2))
        self.listMods.SetSelection(0)

        item = ""
        tempItem = listRun.GetItem(listRun.GetFirstSelected())

        for i in self.itens:
            if i.GetItem().GetData() == tempItem.GetData():
                item = i

        for i in self.itens:
            if isinstance(item, gameDef.GameDef):
                if (i.GetTab() < 0) and (i.GetGroup().GetGroupId() == item.GetGroup().GetGroupId()):
                    self.listMods.Append(i.GetItem().GetText(), i)
                    if item.GetLastMod() == i.GetItem().GetData():
                        self.listMods.SetSelection(self.listMods.GetCount() - 1)




app = wx.App(False)
frame = MyFrame(None, 'GZDoom Launcher')
app.MainLoop()

