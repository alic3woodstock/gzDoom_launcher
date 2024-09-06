from os import path, name as os_name, remove, mkdir

from configDB import check_gzdoom_version
from dataPath import data_path
from functions import filehash, log as write_log, WINE_GZDOOM
from url import Url


class GZDoomUpdate:
    def __init__(self):
        self.gzdoom_windows = (os_name == "nt") or WINE_GZDOOM
        self.wine_gzdoom = not (os_name == "nt") and WINE_GZDOOM
        self.file = ""
        self.filename = ""
        self.local_hash = ""
        self.version = ""
        self.url = ""
        if self.gzdoom_windows:
            self.filename = "gzdoom.zip"
        else:
            self.filename = "gzdoom.tar.xz"

        self.local_file_name = data_path().gzDoomExec

    def check_gzdoom_update(self):
        if not path.exists(data_path().download):
            mkdir(data_path().download)

        if path.exists(data_path().download + self.filename):
            remove(data_path().download + self.filename)

        if path.exists(data_path().download + 'wine.tar.xz'):
            remove(data_path().download + 'wine.tar.xz')

        try:
            gzdoom_url = get_gz_doom_url(self.gzdoom_windows)
            self.url = gzdoom_url[0]
            self.version = gzdoom_url[1]
            self.file = Url(self.url, self.filename)
            self.local_hash = filehash(self.local_file_name)

            return ((not path.isfile(self.local_file_name)) or
                    (not check_gzdoom_version(self.version, self.local_hash)))
        except Exception as e:
            write_log(e)


def get_gz_doom_url(gzdoom_windows):
    # r = get("https://github.com/coelckers/gzdoom/releases/latest", stream=False)
    r = Url("https://github.com/coelckers/gzdoom/releases/latest", '').get_html()
    tmp_str = r.result
    start = tmp_str.find("https://github.com/ZDoom/gzdoom/releases/expanded_assets")
    end = tmp_str.find('"', start)
    tmp_str = tmp_str[start:end].strip()
    start = tmp_str.find("expanded_assets/g")
    version = tmp_str[start:].strip()
    version = version[version.find('g') + 1:]

    r = Url(tmp_str, '').get_html()
    tmp_str = r.result

    start = tmp_str.find("/ZDoom/gzdoom/releases/download")
    tmp_str = tmp_str[start:]
    if gzdoom_windows:
        start = tmp_str.lower().find('windows.zip')
    else:
        start = tmp_str.lower().find('linux')
    start = tmp_str.find("/ZDoom/gzdoom/releases/download", start - 200, )
    tmp_str = tmp_str[start:]
    end = tmp_str.lower().find('" rel=')

    tmp_str = "https://github.com" + tmp_str[:end].strip()
    write_log(tmp_str, False)
    return [tmp_str, version]
