#!/usr/bin/env python
import wx
import os
import csv
import gameDef
import download
import extract

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        self.itens = []
        frame = wx.Frame.__init__(self, parent, title=title)
        
        #Dwonload button
        panel = wx.Panel(self, wx.ID_ANY)
        font = panel.GetFont()
        font.MakeLarger()
        font.MakeLarger()
        panel.SetFont(font)
        
        menu = wx.MenuBar()
        fileMenu = wx.Menu()
        menuDownload = fileMenu.Append(101, item = "&Download")                
        menuExtract = fileMenu.Append(102, item = "&Extract All")
        menu.Append(fileMenu, "&File")
        self.SetMenuBar(menu)
        
        gameTab = wx.Notebook(panel)
        listGames = wx.ListCtrl(gameTab, id=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER)
        listMaps = wx.ListCtrl(gameTab, id=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER)
        listRun = [listGames, listMaps]
        gameTab.InsertPage(0, listRun[0], 'Games', 1)
        gameTab.InsertPage(1, listRun[1], 'Maps', 1)

        btnOk = wx.Button(panel, wx.ID_ANY, 'OK')
        btnCancel = wx.Button(panel, wx.ID_ANY, 'Cancelar')

        box = wx.BoxSizer(wx.VERTICAL)
        #box.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, border=4)
        box.Add(gameTab, 1, wx.EXPAND | wx.ALL, border=4)
        box.AddSpacer(6)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(btnOk,0, wx.RIGHT)
        box2.AddSpacer(4)
        box2.Add(btnCancel,0, wx.RIGHT, border=4)
        box.Add(box2, 0, wx.ALIGN_RIGHT | wx.ALL)
        box.AddSpacer(8)

        #Bind Events
        self.Bind(wx.EVT_BUTTON, self.btnCancelOnPress, btnCancel)
        self.Bind(wx.EVT_BUTTON, lambda event: self.btnOkOnPress(event, gameTab), btnOk)
        panel.Bind(wx.EVT_CHAR_HOOK, lambda event: self.panelOnKeyHook(event, gameTab))
        listRun[0].Bind(wx.EVT_KEY_DOWN, self.listCtrlOnKeyDown)
        listRun[1].Bind(wx.EVT_KEY_DOWN, self.listCtrlOnKeyDown)        
        self.Bind(wx.EVT_MENU, self.menuDownloadOnClick, menuDownload)
        self.Bind(wx.EVT_MENU, self.menuExtractOnClick, menuExtract)
        
        if (not(os.path.exists('games.csv'))):
            self.writeDefaultCSV()


        listRun[0].AppendColumn('Levels', width=listRun[0].GetSize().GetWidth() - 4)
        listRun[1].AppendColumn('Levels', width=listRun[0].GetSize().GetWidth() - 4)
        self.readCSV(self.itens)

        for i in range(len(self.itens)):
            listRun[self.itens[i].GetTab()].InsertItem(self.itens[i].GetItem())
                
        listRun[0].Select(0)
        gameTab.SetSelection(0)
        listRun[0].SetFocus()
        listRun[0].Focus(0)

        # if (os.name == "nt"):
            # panel.SetForegroundColour("White")
            # panel.SetBackgroundColour(wx.Colour(25,25,25))
            # btnOk.SetForegroundColour("White")
            # btnOk.SetBackgroundColour(wx.Colour(20,20,20))
            # btnCancel.SetForegroundColour("White")
            # btnCancel.SetBackgroundColour(wx.Colour(20,20,20))
            # gameTab.SetForegroundColour("White")
            # gameTab.SetBackgroundColour(wx.Colour(20,20,20))

        panel.SetSizer(box)
        box.SetSizeHints(self)
        self.Centre()
        self.Show(True)

    def btnCancelOnPress(self, event):
        self.Close()

    def btnOkOnPress(self, event, tab):
        self.lauchGame(tab.GetChildren()[tab.GetSelection()])

    def listCtrlOnKeyDown(self, event):
        if (event.GetKeyCode() == 13):
            self.lauchGame(event.GetEventObject())
        else:
            event.Skip()

    def panelOnKeyHook(self, event, tab):
        event.DoAllowNextEvent()
        changeFocus = False
        if (event.GetKeyCode() == wx.WXK_ESCAPE):
            self.Close()
        if ((event.GetKeyCode() == wx.WXK_RIGHT) and (tab.GetSelection() < tab.GetPageCount() - 1)):
            tab.SetSelection(tab.GetSelection() + 1)
            changeFocus = True
        if ((event.GetKeyCode() == wx.WXK_LEFT) and (tab.GetSelection() > 0)):
            tab.SetSelection(tab.GetSelection() - 1)
            changeFocus = True
        if (changeFocus):
            list = tab.GetChildren()[tab.GetSelection()]
            list.Select(0)
            list.SetFocus()
            list.Focus(0)
        event.Skip()
        
    def menuDownloadOnClick(self, event):
        download.StartDownload(self)
        
    def menuExtractOnClick(self, parent):
        extract.ExtractAll(self)

    def lauchGame(self, listCtrl):
        item = self.itens[listCtrl.GetItem(listCtrl.GetFirstSelected()).GetData()]
        command = item.GetExec() + " -iWad " + item.GetIWad()
        for file in item.GetFiles():
            command += " -file " + file
        os.popen(command)
        listCtrl.SetFocus()

    def writeDefaultCSV(self):
        with open ('games.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, dialect = 'unix')
            if (os.name == "nt"):
                exec = ".\\gzdoom\\gzdoom.exe"
            else:
                exec = "./gzdoom/gzdoom"
            writer.writerow(['id', 'Name','Tab Index', 'Executable', 'Group', 'Last run mod','iWad','file1','file2','...'])
            writer.writerow([0, 'Blasphemer', 0, exec, 'heretic', 0, 'wad/blasphem-0.1.7.wad', 'wad/BLSMPTXT.WAD'])
            writer.writerow([1, 'Freedoom Phase 1', 0, exec, 'doom', 0, 'wad/freedoom1.wad'])
            writer.writerow([2, 'Freedoom Phase 2', 0, exec, 'doom', 0, 'wad/freedoom2.wad'])
            writer.writerow([3, 'Alien Vendetta', 1, exec, 'doom', 0, 'wad/freedoom2.wad', 'maps/av.zip'])
            writer.writerow([4, 'Ancient Aliens', 1, exec, 'doom', 0, 'wad/freedoom2.wad', 'maps/aaliens.zip'])                    

    def readCSV(self, itens):
        with open ('games.csv', newline = '') as csvfile:
            reader = csv.reader(csvfile, dialect='unix')
            i = 0
            for row in reader:
                if (i > 0):
                    #id, name, tab, exec, group, lastMod, wad, files':
                    game = gameDef.GameDef(int(row[0]), row[1], int(row[2]), row[3], row[4], int(row[5]), row[6], [])
                    for x in range(7, len(row)):
                       game.AppendFile(row[x])
                    itens.append(game)                            
                i += 1

app = wx.App(False)
frame = MyFrame(None, 'gzDoom Laucher')
app.MainLoop()
