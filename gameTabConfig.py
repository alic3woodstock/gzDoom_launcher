class GameTabConfig:
    def GetIndex(self):
        return self._index

    def SetIndex(self, index):
        self._index = index

    def GetName(self):
        return self._name

    def SetName(self, name):
        self._name = name

    def IsEnabled(self):
        return self._isEnabled

    def SetEnabled(self, isEnabled):
        self._isEnabled = isEnabled

    def __init__(self, index=0, name="", isEnabled=False):
        self._index = index
        self._name = name
        self._isEnabled = isEnabled
