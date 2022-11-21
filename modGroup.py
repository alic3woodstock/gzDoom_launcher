class ModGroup():
    def __init__(self, groupId, groupName):
        self._groupId = groupId
        self._groupName = groupName
        
        
    def GetGroupId(self):
        return self._groupId
    
    def GetGroupName(self):
        return self._groupName