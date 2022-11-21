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

class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        self.itens = []
        wx.Frame.__init__(self, parent, title=title)
        
        panel = wx.Panel(self, wx.ID_ANY)
        font = panel.GetFont()
        font.MakeLarger()
        panel.SetFont(font)
        
        menu = wx.MenuBar()
        fileMenu = wx.Menu()
        # menuAddGame = fileMenu.Append(104, item = "&Add game...")
        menuManageGames = fileMenu.Append(105, item = "&Manage games...")
        fileMenu.Append(id=wx.ID_SEPARATOR, item="")
        menuDownload = fileMenu.Append(101, item = "&Download")                
        menuExtract = fileMenu.Append(102, item = "&Extract All")
        fileMenu.Append(id=wx.ID_SEPARATOR, item="")
        menuClose = fileMenu.Append(103, item = "&Close")
        menu.Append(fileMenu, "&File")
        
        utilMenu = wx.Menu()
        menuReplaceDoom = utilMenu.Append(106, item = "Replace &Doom maps wad...")
        menuReplaceHeretic = utilMenu.Append(107, item = "Replace &Heretic maps wad...")
        menu.Append(utilMenu, "&Utilities")
        
        self.SetMenuBar(menu)
        
        
        gameTab = wx.Notebook(panel)
        listGames =  MyListCtrl(gameTab, ID=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER)
        listMaps = MyListCtrl(gameTab, ID=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER)
        listMods = wx.ComboBox(panel, style = wx.CB_READONLY)
        listRun = [listGames, listMaps, listMods]        
        self.listRun = listRun
        gameTab.InsertPage(0, listRun[0], 'Games', 1)
        gameTab.InsertPage(1, listRun[1], 'Maps', 1)

        btnOk = wx.Button(panel, wx.ID_ANY, 'Run Game')
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(gameTab, 1, wx.EXPAND | wx.ALL, border=4)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.AddSpacer(4)
        box2.Add(wx.StaticText(panel, label = "Run with mod:"), 0, wx.CENTER, border = 4)
        box2.AddSpacer(4)
        box2.Add(listRun[2], 0, wx.EXPAND | wx.ALL, border = 4)
        box3 = wx.BoxSizer(wx.HORIZONTAL)
        box3.Add(btnOk,0, wx.ALL, border = 4)
        box.Add(box2, 0, wx.ALIGN_LEFT | wx.ALL)
        box.AddSpacer(4)
        box.Add(wx.StaticLine(panel, id=wx.ID_ANY, style = wx.LI_HORIZONTAL), 0, wx.EXPAND)
        box.Add(box3, 0, wx.ALIGN_RIGHT | wx.ALL)

        #Bind Events
        self.Bind(wx.EVT_BUTTON, lambda event: self.BtnOkOnPress(event, gameTab), btnOk)
        panel.Bind(wx.EVT_CHAR_HOOK, lambda event: self.PanelOnKeyHook(event, gameTab))
        for i in range(2):
            listRun[i].Bind(wx.EVT_LEFT_DCLICK, self.ListCtrlOnDClick)
            listRun[i].Bind(wx.EVT_LIST_ITEM_SELECTED, self.ListCtrlOnSelect)
            
        #Bind events for menu itens
        self.Bind(wx.EVT_MENU, self.MenuDownloadOnClick, menuDownload)
        self.Bind(wx.EVT_MENU, lambda event: self.MenuExtractOnClick(event, gameTab), menuExtract)
        self.Bind(wx.EVT_MENU, self.MenuCloseOnClick, menuClose)
        self.Bind(wx.EVT_MENU, lambda event: self.MenuManageGamesOnClick(event, gameTab), menuManageGames)
        self.Bind(wx.EVT_MENU, self.MenuReplaceDoomOnClick, menuReplaceDoom)
        self.Bind(wx.EVT_MENU, self.MenuReplaceHereticOnClick, menuReplaceHeretic)
        
        listRun[0].AppendColumn('Levels')
        listRun[1].AppendColumn('Levels')
        
        if (not os.path.exists('games.sqlite3')):
            gameData = gameDefDb.GameDefDb()
            gameData.CreateGameTable()
        
        self.ReadDB()       
        if listRun[1].GetColumnWidth(0) >= listRun[0].GetColumnWidth(0): 
            columnWidth = listRun[1].GetColumnWidth(0)
        else:
            columnWidth = listRun[0].GetColumnWidth(0)            
            
        listRun[0].resizeColumn(columnWidth)       
        listRun[1].resizeColumn(columnWidth)
        
        if listRun[0].GetItemCount() <= 0:
            tempItem = wx.ListItem()
            tempItem.SetId(0)
            tempItem.SetText("Click in Download, wait, click extract...")
            listRun[0].InsertItem(tempItem)
            
        listRun[0].Select(0)
        gameTab.SetSelection(0)
        listRun[0].SetFocus()
        listRun[0].Focus(0)

        panel.SetSizer(box)
        box.SetSizeHints(self)
        self.Centre()
        self.Show(True)

    def MenuCloseOnClick(self, event):
        self.Close()
        
    def MenuAddGameOnClick(self, event, tab):
        addGameDiag = addGame.MyDialog(self, "Add game, map or mod")
        addGameDiag.ShowModal()
        self.ReadDB()
        gameList = tab.GetChildren()[tab.GetSelection()]
        gameList.Select(0)
        
    def MenuManageGamesOnClick(self, event, tab):
        manageGamesDialog = manageGames.MyDialog(self, "Manage Game/Mod List")
        manageGamesDialog.ShowModal() 
        self.ReadDB()
        gameList = tab.GetChildren()[tab.GetSelection()]
        gameList.Select(0)

    def BtnOkOnPress(self, event, tab):
        self.LauchGame(tab.GetChildren()[tab.GetSelection()])

    def ListCtrlOnDClick(self, event):
        self.LauchGame(event.GetEventObject())
        event.Skip()
        
    def ListCtrlOnSelect(self, event):
        self.listRun[2].Clear()
        self.listRun[2].Insert("None                    ", 0, gameDef.GameDef(-1,"None",2))                
        self.listRun[2].SetSelection(0)
        
        item = ""
        tempItem = event.GetEventObject().GetItem(event.GetEventObject().GetFirstSelected())
        
        for i in self.itens:
            if (i.GetItem().GetData() == tempItem.GetData()):
                item = i
        
        for i in self.itens:
            if (i.GetTab() == 2) and (i.GetGroup().GetGroupId() == item.GetGroup().GetGroupId()):
                self.listRun[2].Insert(i.GetItem().GetText(), self.listRun[2].GetCount(), i)
                if (item.GetLastMod() == i.GetItem().GetData()):
                    self.listRun[2].SetSelection(self.listRun[2].GetCount() - 1)
    
    def PanelOnKeyHook(self, event, tab):
        event.DoAllowNextEvent()
        changeFocus = False
        if (event.GetKeyCode() == wx.WXK_RETURN):
            self.LauchGame(tab.GetChildren()[tab.GetSelection()])
        if (event.GetKeyCode() == wx.WXK_ESCAPE):
            self.Close()
        if ((event.GetKeyCode() == wx.WXK_RIGHT) and (tab.GetSelection() < tab.GetPageCount() - 1)):
            tab.SetSelection(tab.GetSelection() + 1)
            changeFocus = True
        if ((event.GetKeyCode() == wx.WXK_LEFT) and (tab.GetSelection() > 0)):
            tab.SetSelection(tab.GetSelection() - 1)
            changeFocus = True
        if (changeFocus):
            gameList = tab.GetChildren()[tab.GetSelection()]
            gameList.Select(0)
            gameList.SetFocus()
            gameList.Focus(0)
        if (event.GetKeyCode() == wx.WXK_SPACE) or (event.GetKeyCode() == wx.WXK_TAB):
            if (self.listRun[2].GetSelection() < (self.listRun[2].GetCount() - 1)):
                self.listRun[2].SetSelection(self.listRun[2].GetSelection() + 1)
            else:
                self.listRun[2].SetSelection(0)
        event.Skip()
        
    def MenuDownloadOnClick(self, event):
        download.StartDownload(self)
        
    def MenuExtractOnClick(self, event, tab):
        result = wxdialogs.messageDialog(self, message="This will reset game database to the default values. \n" +
            "Do you want to continue?", 
                           title='Extract files', aStyle= wx.ICON_WARNING | wx.YES | wx.NO | wx.RIGHT )
        if result.accepted:        
            extract.ExtractAll(self)
            self.ReadDB()
            gameList = tab.GetChildren()[tab.GetSelection()]
            gameList.Select(0)
        
    def MenuReplaceDoomOnClick(self, event):
        menuReplaceDialog = replaceWad.MyDialog(self, "Replace Doom maps wad")
        menuReplaceDialog.ShowModal()
        
    def MenuReplaceHereticOnClick(self, event):
        menuReplaceDialog = replaceWad.MyDialog(self, "Replace Heretic maps wad", "Wad (heretic.wad recommended):")
        menuReplaceDialog.ShowModal()                        

    def LauchGame(self, listCtrl):
        if (listCtrl.GetFirstSelected() < 0):
            listCtrl.Select(0)
            
        item = ""
        tempItem = listCtrl.GetItem(listCtrl.GetFirstSelected())
        
        mod = self.listRun[2].GetClientData(self.listRun[2].GetSelection())
        
        for i in self.itens:
            if (i.GetItem().GetData() == tempItem.GetData()):
                item = i
                i.SetLastMod(mod.GetItem().GetData())
                
        command = item.GetExec() + " -iWad " + item.GetIWad()
        for file in item.GetFiles():
            command += " -file " + file

        if (mod.GetItem().GetData() >= 0):
            for file in mod.GetFiles():
                command += " -file " + file
        
        os.popen(command)
        gameData = gameDefDb.GameDefDb()
        gameData.UpdateLastRunMod(item,mod)
        listCtrl.SetFocus()

    def ReadDB(self):
        gameData = gameDefDb.GameDefDb()
        tempItens = gameData.SelectAllGames()
        self.listRun[0].DeleteAllItems()
        self.listRun[1].DeleteAllItems()
        self.itens = []
               
        # Show itens in alphabetical order.
        order = []                
        for i in tempItens:
            order.append([i.GetItem().GetText(),i.GetItem().GetData()])
        order.sort()
        i = 0
        
        for o in order:
            for j in tempItens:
                if (j.GetItem().GetData() == o[1]):
                    j.GetItem().SetId(i)
                    self.itens.append(j)                    
                    i += 1
                    

        self.listRun[2].Clear()
        self.listRun[2].Insert("None                    ", 0, gameDef.GameDef(-1,"None",2))                
        self.listRun[2].SetSelection(0)

        for i in range(len(self.itens)):
            if (self.itens[i].GetTab() <= 1):
                self.listRun[self.itens[i].GetTab()].InsertItem(self.itens[i].GetItem())

app = wx.App(False)
frame = MyFrame(None, 'gzDoom Launcher')
app.MainLoop()
