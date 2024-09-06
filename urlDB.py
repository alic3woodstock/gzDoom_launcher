from dataFunctions import connect_db


def insert_default_urls(data_con=None):
    if data_con:
        commit = False
    else:
        data_con = connect_db()
        data_con.start_transaction()
        commit = True

    sql = """REPLACE INTO downloadlist (url, filename, sha_hash) VALUES (?, ?, ?) """

    # Blasphemer
    params = ["https://github.com/Blasphemer/blasphemer/releases/download/v0.1.8/blasphem-0.1.8.zip",
              "blasphem.zip", "5838d211add81e1696a621485c1e40771035daf6609d08bad7018f52acfa5e54"]
    data_con.exec_sql(sql, params)
    params = ["https://github.com/Blasphemer/blasphemer/releases/download/v0.1.8/blasphemer-texture-pack.zip",
              "blasphemer-texture-pack.zip", "ec5a485d2722913f75ed29a5cfc25f0f2069a66a6ad40864ffc050a6a3f7c63d"]
    data_con.exec_sql(sql, params)

    # Freedoom
    params = ["https://github.com/freedoom/freedoom/releases/download/v0.13.0/freedoom-0.13.0.zip",
              "freedoom.zip", "3f9b264f3e3ce503b4fb7f6bdcb1f419d93c7b546f4df3e874dd878db9688f59"]
    data_con.exec_sql(sql, params)

    # Harmony
    params = ["https://youfailit.net/pub/idgames/levels/doom2/Ports/g-i/harmonyc.zip",
              "harmonyc.zip", "bf161162e5177a3a3f6f9c99a3922a13eff098a8b08b9d00d5095c247903e114"]
    data_con.exec_sql(sql, params)

    # Space Cats Saga
    params = ['https://www.moddb.com/mods/space-cats-saga-chapter-2-macrocosm/downloads/space-cats-saga',
              "space_cats.7z", "b8d475467a0ddcffb3d9865299f16401bca5fb38292debbbb4a905278536c0ba"]
    data_con.exec_sql(sql, params)

    # 150skins
    params = ["https://awxdeveloper.edu.eu.org/downloads/150skins.zip",  # my personal server
              "150skins.zip", "0d19636653d2b3135351ae5da2614a5bc32b4fdfb0caa214205c9fa2bd4db648"]
    data_con.exec_sql(sql, params)

    # Beautiful Doom
    params = ["https://github.com/jekyllgrim/Beautiful-Doom/archive/refs/heads/master.zip",
              "Beautiful_Doom.pk3", "3e85bb9bdb4eedfc69cd3fbb37ed53412f98314d59358ced54f52151bad3d105"]
    data_con.exec_sql(sql, params)

    # Brutal Doom
    params = ["https://github.com/BLOODWOLF333/Brutal-Doom-Community-Expansion/releases/download/"
              "v21.15.0/brutalv21.15.0.pk3",
              "brutal.pk3", "50c8f4dd27a5c2284b1c6458591b1b20fa3701169ccda45f0ab6db3e8f9d8fcf"]
    data_con.exec_sql(sql, params)

    # maps
    idg_mirror = "https://youfailit.net/pub/idgames"
    params = ["https://doom2.net/av/av.zip", "av.zip",
              "5c5382cc50b565946b6725b3058cc1fdefe7367ee3067808068900117aabf8fc"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/doom2/Ports/megawads/aaliens.zip", "aaliens.zip",
              "1c9d1e256a44bab531c8017e5a590cdcc51ac4411f154446c694589054ec2884"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/doom2/megawads/btsx_e1.zip", "btsx_e1.zip",
              "9f6d2fba63e20e2fddd5a1012813da1087b751f9311d3d8bf4757f69373c2c9a"]
    data_con.exec_sql(sql, params)
    params = ["https://esselfortium.net/wasd/btsx_e2.zip", "btsx_e2.zip",
              "1bc72e790aa5438ae3e7b51c3578cde4a2007b14b69337da75848996c686c7ab"]
    data_con.exec_sql(sql, params)
    params = ["https://www.dropbox.com/s/vi47z1a4e4c4980/Sunder%202407.zip?dl=1", "sunder.zip",
              "c11bb7bb6f601b0badbed58f23d04e8b8f352795ebee66074645329d3f17fd2e"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/doom2/Ports/megawads/eviternity.zip", "eviternity.zip",
              "ad2f8b73108df7e4d3843d46a9e903238ac7e321ae9281f8c61f67fb92983656"]
    data_con.exec_sql(sql, params)
    params = ["https://eviternity-dl-eu.dfdoom.com/Eviternity-II.zip", "Eviternity-II.zip",
              "b7dc107ad633a637a9e89473596faf8d973294c9e069f89c6c89f6fb66cf8f86"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/doom2/Ports/megawads/gd.zip", "gd.zip",
              "48accac85af296534565e4c6cbc4cb7312e70756012c327b3d7c1c14c9872dc9"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/themes/hr/hr.zip", "hr.zip",
              "0b353a4ba6f5fb5bb06d1484e737fbf7422bbc5894d8a648921844c4042583b3"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/themes/hr/hr2final.zip", "hr2final.zip",
              "df1ae9f86f339403c6b472b767e02610312727632c02de273cf722e2e62022d2"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/heretic/Ports/htchest.zip", "htchest.zip",
              "fee8b94cb0606568e7c369b97b6466d6be7e465828d615c25ccf44f9079235ea"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/themes/mm/mm_allup.zip", "mm_allup.zip",
              "c8607a7a32d4f6547d492e0f734324320b955e2b11691b02b107de09ac2e7bfb"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/themes/mm/mm2.zip", "mm2.zip",
              "f4e7a10b035b123647f631348d63fc46392d8d8e21fab8a5158cd9ef35027451"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/doom2/megawads/pl2.zip", "pl2.zip",
              "bb925d13119e6d5dfea69a5ffe17d8954cdc3f2da0a6128a58f6ff6a366a0c66"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/doom2/megawads/scythe.zip", "scythe.zip",
              "a38246e005b4675d1f91474cd8dd93f4da016c4a22b1169dcede2608d72f6e99"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/doom2/Ports/megawads/scythe2.zip", "scythe2.zip",
              "0d5c1ab9d0152f5f1cf7a0d4ca2f41f5a6ac2986fa6ee850504d1d49e020cd8d"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/doom2/Ports/s-u/scythex.zip", "scythex.zip",
              "f214b580fd30855c02db0fe509b5939052a6c52eae03044f9b216bdf5598b5b4"]
    data_con.exec_sql(sql, params)
    params = ["https://romero.com/s/SIGIL_II_V1_0.zip", "sigil2.zip",
              "41741ce797e6faf9ebd0e3d577b5eaf9a648b64d850fbd741c1b9c28d8461017"]
    data_con.exec_sql(sql, params)

    params = [idg_mirror + "/levels/doom2/Ports/megawads/sunlust.zip", "sunlust.zip",
              "46bc1fe72abec5ad06739b91657f3ed2fed1fda967cd38e6faa4a1701999d64a"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/heretic/s-u/unbeliev.zip", "unbeliev.zip",
              "55dd8be5e20047c20be0de8be1611996f4340461113dc6a51e5fa05b8c1dce47"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/doom2/Ports/megawads/valiant.zip", "valiant.zip",
              "067d649f2a845386ea20ad20b458125143ead3e6f1dbfb4e161ca0eb8f159121"]
    data_con.exec_sql(sql, params)
    params = [idg_mirror + "/levels/doom2/Ports/megawads/zof.zip", "zof.zip",
              "d5726956472edf8e0140e5cc8a4755ea6deff5672af6b9f8d23abc5d01171374"]
    data_con.exec_sql(sql, params)

    if commit:
        data_con.commit()
        data_con.close_connection()


def select_default_urls():
    from url import Url
    data_con = connect_db()
    sql = """SELECT url, filename, sha_hash FROM downloadlist"""
    result = data_con.exec_sql(sql)
    urls = []
    for r in result:
        urls.append(Url(r[0], r[1], r[2]))
    data_con.close_connection()
    return urls
