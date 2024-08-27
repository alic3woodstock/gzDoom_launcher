# Credits for all resources I've utilized

class Credits:

    def __init__(self, short_name):
        self.name = ""
        self.author = ""

        short_name = short_name.lower()
        match short_name:
            case 'blasphemer':
                self.name = 'Blasphemer'
                self.author = 'https://github.com/Blasphemer/blasphemer/blob/master/CREDITS.md'
            case "freedoom":
                self.name = 'Freedoom 1 and 2'
                self.author = 'https://github.com/freedoom/freedoom/blob/master/CREDITS'
            case "harmony":
                self.name = 'Harmony Compatible'
                self.author = 'Thomas van der Velden'
            case "spacecats":
                self.name = 'Space Cat Saga'
                self.author = 'DerTimmy'
            case "av":
                self.name = 'Alien Vendetta'
                self.author = 'Martin Aalen Hunsager'
            case "aaliens":
                self.name = 'Ancient Aliens'
                self.author = 'Paul "skillsaw" DeBruyne'
            case "btsx_e1":
                self.name = 'Back to Saturn X E1: Get Out Of My Stations'
                self.author = 'Sarah "Esselfortium" Mancuso and the Back to Saturn X team'
            case "btsx_e2":
                self.name = 'Back to Saturn X E2: Tower in the Fountain of Sparks'
                self.author = 'Sarah "Esselfortium" Mancuso and the Back to Saturn X team'
            case "eviternity":
                self.name = 'Eviternity and Eviternity II'
                self.author = 'Joshua "Dragonfly" O\'Sullivan'
            case "gd":
                self.name = 'Going Down'
                self.author = 'Mouldy'
            case "hr":
                self.name = 'Hell Revealed'
                self.author = 'Yonatan Donner and Haggay Niv'
            case "hr2":
                self.name = 'Hell Revealed II'
                self.author = 'Mattias Berggren, Ola Bjorlin, Pedro A. Gomez Blanco and Jonas Feragen'
            case "htchest":
                self.name = 'Heretic Treasure Chest'
                self.author = 'Heretic Treasure Chest team'
            case "mm":
                self.name = 'Memento Mori'
                self.author = 'The Memento Mori Crew'
            case "mm2":
                self.name = 'Memento Mori II'
                self.author = 'various'
            case "pl2":
                self.name = 'Plutonia 2'
                self.author = 'Plutonia 2 team'
            case "scythe":
                self.name = 'Scythe'
                self.author = 'Erik Alm and Kim "Torn" Bach'
            case "scythe2":
                self.name = 'Scythe 2 and Scythe X'
                self.author = 'Erik Alm'
            case "sunder":
                self.name = 'Sunder'
                self.author = 'Insane_Gazebo'
            case "sunlust":
                self.name = 'Sunlust'
                self.author = '	Ribbiks & Dannebubinga'
            case "unbeliev":
                self.name = 'UnBeliever'
                self.author = 'Ryath/scwiba'
            case "valiant":
                self.name = 'Valiant'
                self.author = 'Paul "skillsaw" DeBruyne'
            case "zof":
                self.name = 'Zones of Fear'
                self.author = 'Damned, Des_arthes, enkeli/Matthias, Jaeden and Klofkac pipicz'
