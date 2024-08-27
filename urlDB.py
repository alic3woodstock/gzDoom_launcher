from dataFunctions import connect_db


def insert_default_urls(data_con=None):
    if data_con:
        commit = False
    else:
        data_con = connect_db()
        data_con.StartTransaction()
        commit = True

    sql = """REPLACE INTO downloadlist (url, filename) VALUES (?, ?) """

    # Blasphemer
    params = ["https://github.com/Blasphemer/blasphemer/releases/download/v0.1.8/blasphem-0.1.8.zip",
              "blasphem.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://github.com/Blasphemer/blasphemer/releases/download/v0.1.8/blasphemer-texture-pack.zip",
              "blasphemer-texture-pack.zip"]
    data_con.ExecSQL(sql, params)

    # Freedoom
    params = ["https://github.com/freedoom/freedoom/releases/download/v0.13.0/freedoom-0.13.0.zip", "freedoom.zip"]
    data_con.ExecSQL(sql, params)

    # Harmony
    params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/g-i/harmonyc.zip", "harmonyc.zip"]
    data_con.ExecSQL(sql, params)

    # 150skins
    params = ["https://awxdeveloper.edu.eu.org/downloads/150skins.zip",
              "150skins.zip"]  # my personal WordPress site
    data_con.ExecSQL(sql, params)

    # Beautiful Doom
    params = ["https://github.com/jekyllgrim/Beautiful-Doom/archive/refs/heads/master.zip",
              "Beautiful_Doom.pk3"]
    data_con.ExecSQL(sql, params)

    # Brutal Doom
    params = ["https://github.com/BLOODWOLF333/Brutal-Doom-Community-Expansion/releases/"
              "download/V21.11.2/brutalv21.11.2.pk3", "brutal.pk3"]
    data_con.ExecSQL(sql, params)

    # maps
    params = ["https://youfailit.net/pub/idgames/levels/doom2/megawads/av.zip", "av.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/aaliens.zip", "aliens.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/megawads/btsx_e1.zip", "btsx_e1.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/megawads/btsx_e2.zip", "btsx_e2.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://www.dropbox.com/s/vi47z1a4e4c4980/Sunder%202407.zip?dl=1", "sunder.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/eviternity.zip", "eviternity.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://eviternity-dl-eu.dfdoom.com/Eviternity-II.zip", "Eviternity-II.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/gd.zip", "gd.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/themes/hr/hr.zip", "hr.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/themes/hr/hr2final.zip", "hr2final.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/heretic/Ports/htchest.zip", "htchest.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/themes/mm/mm_allup.zip", "mm_allup.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/themes/mm/mm2.zip", "mm2.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/megawads/pl2.zip", "pl2.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/megawads/scythe.zip", "scythe.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/scythe2.zip", "scythe2.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/s-u/scythex.zip", "scythex.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/sunlust.zip", "sunlust.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/heretic/s-u/unbeliev.zip", "unbeliev.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/valiant.zip", "valiant.zip"]
    data_con.ExecSQL(sql, params)
    params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/zof.zip", "zof.zip"]
    data_con.ExecSQL(sql, params)

    if commit:
        data_con.Commit()
        data_con.CloseConnection()


def select_default_urls():
    from url import Url
    data_con = connect_db()
    sql = """SELECT url, filename FROM downloadlist"""
    result = data_con.ExecSQL(sql)
    urls = []
    for r in result:
        urls.append(Url(r[0], r[1]))
    data_con.CloseConnection()
    return urls
