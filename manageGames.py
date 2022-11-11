import wx
import wx.dataview as dataview
import gameDefDb
import addGame

class MyDialog(wx.Dialog): 
    def __init__(self, parent, title): 
        super(MyDialog, self).__init__(parent, title = title, size = (500, wx.DefaultCoord)) 
        panel = wx.Panel(self)
        
        btnAdd = wx.Button(panel, wx.ID_ANY, "Add...")
        btnEdit = wx.Button(panel, wx.ID_ANY, "Exit...")
        btnDelete = wx.Button(panel, wx.ID_ANY, "Delete...")
        self.dataGrid = dataview.DataViewListCtrl(panel, id=wx.ID_ANY, size=(400,300))
        
        self.dataGrid.AppendTextColumn("Name")
        self.dataGrid.AppendTextColumn("Type")
        self.dataGrid.AppendTextColumn("Game Exec")
        self.dataGrid.AppendTextColumn("Mod Group")
        self.dataGrid.AppendTextColumn("iWad")
        
        self.ReadDB()
        
        #Bind eventes
        self.bind(wx.EVT_BUTTON, self.BtnAddOnClick, btnAdd)
        
        boxv = wx.BoxSizer(wx.VERTICAL)
        boxButtons = wx.BoxSizer(wx.HORIZONTAL)
        boxv.AddSpacer(4)
        boxv.Add(self.dataGrid, 0, wx.EXPAND | wx.ALL)
        boxv.AddSpacer(4)
        boxv.Add(wx.StaticLine(panel, id=wx.ID_ANY, style = wx.LI_HORIZONTAL), 0, wx.EXPAND)
        boxButtons.Add(btnAdd, 0, wx.ALL, border = 4)
        boxButtons.Add(btnEdit, 0, wx.ALL, border = 4)
        boxButtons.Add(btnDelete, 0, wx.ALL, border = 4)
        btnAdd.MoveBeforeInTabOrder(btnEdit)
        btnEdit.MoveBeforeInTabOrder(btnDelete)
        boxv.Add(boxButtons, 0 , wx.ALIGN_RIGHT)
        panel.SetSizer(boxv)
        boxv.SetSizeHints(self)            
        
    def BtnAddOnClick(self, event):
        addGameDiag = addGame.MyDialog(self, "Add game, map or mod")
        addGameDiag.ShowModal()
        self.ReadDB()
        
    def ReadDB(self):
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
                                 game.GetGroup(), game.GetIWad()], game.GetItem().GetData())
            
        for i in range(self.dataGrid.GetColumnCount()):
            self.dataGrid.GetColumn(i).SetWidth(wx.COL_WIDTH_AUTOSIZE)

