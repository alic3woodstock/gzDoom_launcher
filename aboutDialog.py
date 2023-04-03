import wx
import functions


class MyDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(MyDialog, self).__init__(parent, title=title, size=(500, wx.DefaultCoord))
        panel = wx.Panel(self)

        png = wx.Image('pentagrama.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        pentagram = wx.StaticBitmap(panel, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))

        btnClose = wx.Button(panel, wx.ID_CLOSE)
        lblNome = wx.StaticText(panel, label="GZDoom Launcher")

        font = lblNome.GetFont()
        font.MakeLarger()
        font.MakeBold
        lblNome.SetFont(font)

        lblVersao = wx.StaticText(panel, label='Version:' + functions.APPVERSION)
        lblAuthor = wx.StaticText(panel, label=functions.AUTHOR)

        self.Bind(wx.EVT_BUTTON, self.BtnCloseOnClick, btnClose)
        panel.Bind(wx.EVT_CHAR_HOOK, self.PanelOnKeyHook)

        boxV = wx.BoxSizer(wx.VERTICAL)
        boxButtons = wx.BoxSizer(wx.HORIZONTAL)
        boxV.AddSpacer(4)
        boxH = wx.BoxSizer(wx.HORIZONTAL)
        boxH.AddSpacer(8)
        boxLabel = wx.BoxSizer(wx.VERTICAL)
        boxLabel.Add(pentagram, 0, wx.ALIGN_CENTER)
        boxLabel.AddSpacer(16)
        boxLabel.Add(lblNome, 0, wx.ALIGN_CENTER)
        boxLabel.Add(lblVersao, 0, wx.ALIGN_CENTER)
        boxLabel.AddSpacer(16)
        boxLabel.Add(lblAuthor, 0, wx.ALIGN_CENTER)
        boxLabel.SetMinSize((200, 50))
        boxH.Add(boxLabel)
        boxH.AddSpacer(8)
        boxV.Add(boxH)
        boxV.AddSpacer(4)
        boxV.Add(wx.StaticLine(panel, id=wx.ID_ANY, style=wx.LI_HORIZONTAL), 0, wx.EXPAND)
        boxButtons.Add(btnClose)
        boxV.Add(boxButtons, 0, wx.ALIGN_RIGHT)

        panel.SetSizer(boxV)
        boxV.SetSizeHints(self)

    def BtnCloseOnClick(self, event):
        try:
            self.Close()
        except Exception as e:
            functions.log(event)
            functions.log(e)

    def PanelOnKeyHook(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
