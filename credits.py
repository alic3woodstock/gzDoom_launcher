# Credits for all resources I've utilized

class Credits:

    def __init__(self, short_name):
        self.name = ""
        self.author = ""
        self.url = ""

        short_name = short_name.lower()
        match short_name:
            case 'blasphemer':
                self.name = 'Blasphemer'
                self.author = 'Credits at Github page'
                self.url = 'https://github.com/Blasphemer/blasphemer'
            case "freedoom":
                self.name = 'Freedoom 1 and 2'
                self.author = 'Credits at Github page'
                self.url = 'https://freedoom.github.io/'
            case "harmony":
                self.name = 'Harmony Compatible'
                self.author = 'Thomas van der Velden'
                self.url = 'https://www.doomworld.com/forum/topic/141216-harmony-compatible-now-available'
            case "spacecats":
                self.name = 'Space Cat Saga'
                self.author = 'DerTimmy'
                self.url = 'https://forum.zdoom.org/viewtopic.php?t=72996'
            case "av":
                self.name = 'Alien Vendetta'
                self.author = 'Martin Aalen Hunsager'
                self.url = 'https://doom2.net/av/index.html'
            case "aaliens":
                self.name = 'Ancient Aliens'
                self.author = 'Paul "skillsaw" DeBruyne'
                self.url = 'https://www.doomworld.com/vb/thread/87784'
            case "btsx_e1":
                self.name = 'Back to Saturn X E1: Get Out Of My Stations'
                self.author = 'Sarah "Esselfortium" Mancuso and the Back to Saturn X team'
                self.url = 'https://www.doomworld.com/vb/thread/62529'
            case "btsx_e2":
                self.name = 'Back to Saturn X E2: Tower in the Fountain of Sparks'
                self.author = 'Sarah "Esselfortium" Mancuso and the Back to Saturn X team'
                self.url = 'https://www.doomworld.com/vb/thread/69960'
            case "eviternity":
                self.name = 'Eviternity'
                self.author = 'Joshua "Dragonfly" O\'Sullivan'
                self.url = 'https://www.doomworld.com/vb/thread/103425'
            case "eviternity2":
                self.name = 'Eviternity II'
                self.author = 'Joshua "Dragonfly" O\'Sullivan'
                self.url = 'https://eviternity.dfdoom.com/'
            case "gd":
                self.name = 'Going Down'
                self.author = 'Mouldy'
                self.url = 'https://www.doomworld.com/vb/thread/65955'
            case "hr":
                self.name = 'Hell Revealed'
                self.author = 'Yonatan Donner and Haggay Niv'
                self.url = 'https://web.archive.org/web/20091014023340/http://www.geocities.com/hollywood/4704/hr.html'
            case "hr2":
                self.name = 'Hell Revealed II'
                self.author = 'Mattias Berggren, Ola Bjorlin, Pedro A. Gomez Blanco and Jonas Feragen'
                self.url = 'https://www.doomworld.com/hr2/'
            case "htchest":
                self.name = 'Heretic Treasure Chest'
                self.author = 'Heretic Treasure Chest team'
                self.url = 'https://www.doomworld.com/vb/thread/48444'
            case "mm":
                self.name = 'Memento Mori'
                self.author = 'The Memento Mori Crew'
                self.url = 'https://www.doomworld.com/idgames/themes/mm/mm_allup'
            case "mm2":
                self.name = 'Memento Mori II'
                self.author = 'various'
                self.url = 'https://www.doomworld.com/idgames/themes/mm/mm2'
            case "pl2":
                self.name = 'Plutonia 2'
                self.author = 'Plutonia 2 team'
                self.url = 'https://web.archive.org/web/20180308074708/http://www.rabotik.nl/pluto2.html'
            case "scythe":
                self.name = 'Scythe'
                self.author = 'Erik Alm and Kim "Torn" Bach'
                self.url = 'https://www.doom2.net/erik/'
            case "scythe2":
                self.name = 'Scythe 2 and Scythe X'
                self.author = 'Erik Alm'
                self.url = 'https://www.doom2.net/erik/'
            case "sigil2":
                self.name = 'Sigil II'
                self.author = 'John Romero'
                self.url = 'https://romero.com/'
            case "sunder":
                self.name = 'Sunder'
                self.author = 'Insane_Gazebo'
                self.url = 'https://www.doomworld.com/vb/thread/46002'
            case "sunlust":
                self.name = 'Sunlust'
                self.author = '	Ribbiks & Dannebubinga'
                self.url = 'https://www.doomworld.com/vb/thread/68089'
            case "unbeliev":
                self.name = 'UnBeliever'
                self.author = 'Ryath/scwiba'
                self.url = 'https://www.doomworld.com/vb/thread/105690'
            case "valiant":
                self.name = 'Valiant'
                self.author = 'Paul "skillsaw" DeBruyne'
                self.url = 'https://www.doomworld.com/vb/thread/71704'
            case "zof":
                self.name = 'Zones of Fear'
                self.author = 'Damned, Des_arthes, enkeli/Matthias, Jaeden, Klofkac and Pipicz'
                self.url = 'https://liquiddoom.net/projects/zof/'
            case "150skins":
                self.name = '150 Doomguy Skins'
                self.author = 'Doomkid'
                self.url = 'https://www.doomworld.com/forum/topic/102669-150-doomguy-skins-new-download/'
            case "beaultiful":
                self.name = 'Beaultiful Doom'
                self.author = 'Jekyll Grim Payne'
                self.url = 'https://forum.zdoom.org/viewtopic.php?t=50004'
            case "brutal":
                self.name = 'Brutal Doom Community Expansion'
                self.author = 'Bloodwolf'
                self.url = 'https://github.com/BLOODWOLF333/Brutal-Doom-Community-Expansion'
            case 'sndinfo':
                self.name = "SNDINFOs for the DOOM + DOOM II rerelease's remix tracks v2"
                self.author = 'Fishytza'
                self.url = 'https://forum.zdoom.org/viewtopic.php?p=1253862'
            case 'gzdoom':
                self.name = 'GZDoom'
                self.author = 'ZDoom + GZDoom teams, and contributors'
                self.url = 'https://zdoom.org/index'
