class GameTabConfig:
    def GetIndex(self):
        return self.index

    def SetIndex(self, index):
        self.index = index

    def GetName(self):
        return self.name

    def SetName(self, name):
        self.name = name

    def IsEnabled(self):
        return self.is_enabled

    def SetEnabled(self, isEnabled):
        self.is_enabled = isEnabled

    def __init__(self, index=0, name="", isEnabled=False):
        self.index = index
        self.name = name
        self.is_enabled = isEnabled
