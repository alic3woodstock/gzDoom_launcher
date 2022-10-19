#!/usr/bin/env python
import wx
import os
import csv
import gameDef
import download
import extract
import wx.lib.mixins.listctrl as listmix

class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        self.itens = []
        frame = wx.Frame.__init__(self, parent, title=title)
        
        #Dwonload button
        panel = wx.Panel(self, wx.ID_ANY)
        font = panel.GetFont()
        font.MakeLarger()
        # font.MakeLarger()
        panel.SetFont(font)
        
        menu = wx.MenuBar()
        fileMenu = wx.Menu()
        menuDownload = fileMenu.Append(101, item = "&Download")                
        menuExtract = fileMenu.Append(102, item = "&Extract All")
        menu.Append(fileMenu, "&File")
        self.SetMenuBar(menu)
        
        gameTab = wx.Notebook(panel)
        listGames =  MyListCtrl(gameTab, ID=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER)
        listMaps = MyListCtrl(gameTab, ID=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER)
        listMods = wx.ComboBox(panel, style = wx.CB_READONLY)
        listRun = [listGames, listMaps, listMods]        
        self.listRun = listRun
        gameTab.InsertPage(0, listRun[0], 'Games', 1)
        gameTab.InsertPage(1, listRun[1], 'Maps', 1)

        btnOk = wx.Button(panel, wx.ID_ANY, 'OK')
        btnCancel = wx.Button(panel, wx.ID_ANY, 'Cancelar')

        box = wx.BoxSizer(wx.VERTICAL)
        #box.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, border=4)
        box.Add(gameTab, 1, wx.EXPAND | wx.ALL, border=4)
        # box.AddSpacer(6)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.AddSpacer(4)
        box2.Add(wx.StaticText(panel, label = "Run with mod:"), 0, wx.CENTER, border = 4)
        box2.AddSpacer(4)
        box2.Add(listRun[2], 0, wx.EXPAND | wx.ALL, border = 4)
        
        box3 = wx.BoxSizer(wx.HORIZONTAL)
        box3.Add(btnOk,0, wx.RIGHT)
        box3.Add(btnCancel,0, wx.RIGHT, border=4)
        box.Add(box2, 0, wx.ALIGN_LEFT | wx.ALL)
        box.Add(box3, 0, wx.ALIGN_RIGHT | wx.ALL)
        box.AddSpacer(8)

        #Bind Events
        self.Bind(wx.EVT_BUTTON, self.btnCancelOnPress, btnCancel)
        self.Bind(wx.EVT_BUTTON, lambda event: self.btnOkOnPress(event, gameTab), btnOk)
        panel.Bind(wx.EVT_CHAR_HOOK, lambda event: self.panelOnKeyHook(event, gameTab))
        for i in range(2):
            listRun[i].Bind(wx.EVT_KEY_DOWN, self.listCtrlOnKeyDown)
            listRun[i].Bind(wx.EVT_LEFT_DCLICK, self.listCtrlOnDClick)
            listRun[i].Bind(wx.EVT_LIST_ITEM_SELECTED, self.listCtrlOnSelect)
        self.Bind(wx.EVT_MENU, self.menuDownloadOnClick, menuDownload)
        self.Bind(wx.EVT_MENU, self.menuExtractOnClick, menuExtract)
        
        listRun[0].AppendColumn('Levels')
        listRun[1].AppendColumn('Levels')
        self.readCSV()        
        if listRun[1].GetColumnWidth(0) >= listRun[0].GetColumnWidth(0): 
            listRun[0].resizeColumn(listRun[1].GetColumnWidth(0))       
        else:
            listRun[1].resizeColumn(listRun[0].GetColumnWidth(0))       
            
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
            
    def listCtrlOnDClick(self, event):
        self.lauchGame(event.GetEventObject())
        event.Skip()
        
    def listCtrlOnSelect(self, event):
        self.listRun[2].Clear()
        self.listRun[2].Insert("None                    ", 0, gameDef.GameDef(-1,"None",2))                
        self.listRun[2].SetSelection(0)
        
        item = ""
        tempItem = event.GetEventObject().GetItem(event.GetEventObject().GetFirstSelected())
        
        for i in self.itens:
            if (i.GetItem().GetData() == tempItem.GetData()):
                item = i
        
        for i in self.itens:
            if (i.GetTab() == 2) and (i.GetGroup() == item.GetGroup()):
                self.listRun[2].Insert(i.GetItem().GetText(), self.listRun[2].GetCount(), i)
                if (item.GetLastMod() == i.GetItem().GetData()):
                    self.listRun[2].SetSelection(self.listRun[2].GetCount() - 1)
    
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
        if (event.GetKeyCode() == wx.WXK_SPACE):
            if (self.listRun[2].GetSelection() < (self.listRun[2].GetCount() - 1)):
                self.listRun[2].SetSelection(self.listRun[2].GetSelection() + 1)
            else:
                self.listRun[2].SetSelection(0)
        event.Skip()
        
    def menuDownloadOnClick(self, event):
        download.StartDownload(self)
        
    def menuExtractOnClick(self, parent):
        extract.ExtractAll(self)
        self.readCSV()

    def lauchGame(self, listCtrl):
        item = ""
        tempItem = listCtrl.GetItem(listCtrl.GetFirstSelected())
        
        for i in self.itens:
            if (i.GetItem().GetData() == tempItem.GetData()):
                item = i
                
        command = item.GetExec() + " -iWad " + item.GetIWad()
        for file in item.GetFiles():
            command += " -file " + file

        mod = self.listRun[2].GetClientData(self.listRun[2].GetSelection())
        if (mod.GetItem().GetData() >= 0):
            for file in mod.GetFiles():
                command += " -file " + file
        
        os.popen(command)
        
        with open ('games.csv', 'r+') as csvfile:
            fileText = csvfile.readlines()

        for i in range(len(fileText)):
            fLine = fileText[i]
            x = fLine.find(',')
            if (fLine[1:x - 1] == str(item.GetItem().GetData())):
                csvLine = fLine.split(',')
                csvLine[5] = '"' + str(mod.GetItem().GetData()) + '"'
                fileText[i] = ','.join(csvLine)
                break           
        
        with open ('games.csv', 'w+') as csvfile:
            csvfile.writelines(fileText)
                        
        listCtrl.SetFocus()

    # def writeDefaultCSV(self):
        # with open ('games.csv', 'w', newline = '') as csvfile:
            # writer = csv.writer(csvfile, dialect = 'unix')
            # if (os.name == "nt"):
                # exec = ".\\gzdoom\\gzdoom.exe"
            # else:
                # exec = "./gzdoom/gzdoom"
            # writer.writerow(['id', 'Name','Tab Index', 'Executable', 'Group', 'Last run mod','iWad','file1','file2','...'])
            # writer.writerow([0, 'Blasphemer', 0, exec, 'heretic', 0, 'wad/blasphem-0.1.7.wad', 'wad/BLSMPTXT.WAD'])
            # writer.writerow([1, 'Freedoom Phase 1', 0, exec, 'doom', 0, 'wad/freedoom1.wad'])
            # writer.writerow([2, 'Freedoom Phase 2', 0, exec, 'doom', 0, 'wad/freedoom2.wad'])
            # writer.writerow([3, 'Alien Vendetta', 1, exec, 'doom', 0, 'wad/freedoom2.wad', 'maps/av.zip'])
            # writer.writerow([4, 'Ancient Aliens', 1, exec, 'doom', 0, 'wad/freedoom2.wad', 'maps/aaliens.zip'])                    

    def readCSV(self):
        self.listRun[0].DeleteAllItems()
        self.listRun[1].DeleteAllItems()
        self.itens = []
        tempItens = []
        with open ('games.csv', newline = '') as csvfile:
            reader = csv.reader(csvfile, dialect='unix')
            i = 0
            for row in reader:
                if (i > 0):
                    #id, name, tab, exec, group, lastMod, wad, files':
                    game = gameDef.GameDef(int(row[0]), row[1], int(row[2]), row[3], row[4], int(row[5]), row[6], [])
                    for x in range(7, len(row)):
                       game.AppendFile(row[x])
                    tempItens.append(game) 
                i += 1
               
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
frame = MyFrame(None, 'gzDoom Laucher')
app.MainLoop()
