import functions
import modGroup


class GameDef:
    # Id,Name,Tab Index,Exe,Group,Last run mod,iWad,files...
    def __init__(self, itemId, gameId, name, tab, gameExec = "", groupId=1, lastMod=0, wad='freedoom1.wad',
                 files=None, groupName=None, cmdParams=""):
        if not gameExec.strip():
            gameExec = functions.gzDoomExec

        if files is None:
            files = []

        self.itemId = itemId
        self.gameId = gameId
        self.name = name
        self.tab = tab
        self.exec = gameExec
        self.group = modGroup.ModGroup(groupId, groupName)
        self.lastMod = lastMod
        self.iWad = wad
        self.files = files
        self.cmdParams = cmdParams
