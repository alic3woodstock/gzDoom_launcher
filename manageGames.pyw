import wx
import wx.dataview as dataview
import gameDefDb
import wx.lib.mixins.listctrl as listmix

class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)

class MyDialog(wx.Dialog): 
    def __init__(self, parent, title): 
        super(MyDialog, self).__init__(parent, title = title, size = (500, wx.DefaultCoord)) 
        panel = wx.Panel(self)
        
        btnAdd = wx.Button(panel, wx.ID_ANY, "Add...")
        btnEdit = wx.Button(panel, wx.ID_ANY, "Exit...")
        btnDelete = wx.Button(panel, wx.ID_ANY, "Delete...")
        dataGrid = dataview.DataViewListCtrl(panel, id=wx.ID_ANY, size=(400,300))
        
        dataGrid.AppendTextColumn("Name")
        dataGrid.AppendTextColumn("Type")
        dataGrid.AppendTextColumn("Game Exec")
        dataGrid.AppendTextColumn("Mod Group")
        dataGrid.AppendTextColumn("iWad")
        
        gameData = gameDefDb.GameDefDb()
        games = gameData.selectAllGames()
        for game in games:            
            if game.GetTab() == 0:
                strType = "Game"
            elif game.GetTab() == 1:
                strType = "Map"
            else:
                strType = "Mod"
                        
            dataGrid.AppendItem([game.GetItem().GetText(), strType, game.GetExec(),
                                 game.GetGroup(), game.GetIWad()], game.GetItem().GetData())
            
        for i in range(dataGrid.GetColumnCount()):
            dataGrid.GetColumn(i).SetWidth(wx.COL_WIDTH_AUTOSIZE)            
        
        
        boxv = wx.BoxSizer(wx.VERTICAL)
        boxButtons = wx.BoxSizer(wx.HORIZONTAL)
        boxv.AddSpacer(4)
        boxv.Add(dataGrid, 0, wx.EXPAND | wx.ALL)
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