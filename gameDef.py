from dataPath import data_path
from gameTabDB import select_game_tab_by_id
from groupDB import select_group_by_id


class GameDef:
    @property
    def tab(self):
        return select_game_tab_by_id(self.tabId)

    @property
    def group(self):
        return select_group_by_id(self.groupId)

    def __init__(self, game_id, name, tab_id, game_exec="", group_id=1, last_mod=0, wad='freedoom1.wad',
                 files=None, cmd_params=""):
        if not game_exec.strip() and data_path():
            game_exec = data_path().gzDoomExec

        if files is None:
            files = []
        self.id = game_id
        self.name = name
        self.tabId = tab_id
        self.exec = game_exec
        self.groupId = group_id
        self.lastMod = last_mod
        self.iWad = wad
        self.files = files
        self.cmdParams = cmd_params
