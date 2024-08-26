import functions
from gameTabDB import select_game_tab_by_id
from groupDB import select_group_by_id


class GameDef:
    @property
    def tab(self):
        return select_game_tab_by_id(self.tabId)

    @property
    def group(self):
        return select_group_by_id(self.groupId)

    # Id,Name,Tab Index,Exe,Group,Last run mod,iWad,files...
    def __init__(self, id, name, tabId, gameExec="", groupId=1, lastMod=0, wad='freedoom1.wad',
                 files=None, cmdParams=""):
        if not gameExec.strip():
            gameExec = functions.gzDoomExec

        if files is None:
            files = []
        self.id = id
        self.name = name
        self.tabId = tabId
        self.exec = gameExec
        self.groupId = groupId
        self.lastMod = lastMod
        self.iWad = wad
        self.files = files
        self.cmdParams = cmdParams
