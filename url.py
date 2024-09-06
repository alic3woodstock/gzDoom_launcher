from kivy.network.urlrequest import UrlRequest

from dataPath import data_path


class Url:
    _url = ""
    _filer1Name = ""

    def __init__(self, url, file_name, sha_hash=""):
        self.url = url
        self.fileName = file_name
        self.sha_hash = sha_hash
        self.redirect = False
        self.on_progress = None
        self.on_failure = None
        self.on_finish = None

    def get_file_path(self):
        return data_path().download + self.fileName

    def download(self):
        if self.url.find("moddb") >= 0:
            self.url = self.get_moddb_url()

        request = self.request()
        while self.redirect:
            if request.resp_headers.get('Location'):
                self.url = request.resp_headers['Location']
            elif request.resp_headers.get('location'):
                self.url = request.resp_headers['location']
            request = self.request()

    def request(self):

        headers = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/128.0.0.0 Safari/537.36')
        self.redirect = False
        request = UrlRequest(url=self.url, on_progress=self.on_progress, chunk_size=1024,
                             file_path=self.get_file_path(), on_failure=self.on_failure,
                             on_redirect=self.on_redirect, user_agent=headers)

        request.wait()
        while not request.is_finished:
            pass

        return request

    def on_redirect(self, _req, _resp):
        self.redirect = True

    def get_moddb_url(self):
        r1 = self.get_html()
        tmp_str = r1.result
        start = tmp_str.find('/downloads/start')
        end = tmp_str.find('"', start)
        tmp_str = 'https://moddb.com' + tmp_str[start:end].strip()
        self.url = tmp_str
        tmp_str = self.get_html(r1.resp_headers.get('set-cookie')).result
        start = tmp_str.find('/downloads/mirror/')
        end = tmp_str.find('"', start)
        tmp_str = tmp_str[start:end]
        tmp_str = 'https://moddb.com' + tmp_str
        return tmp_str

    def get_html(self, cookies=None):
        request = UrlRequest(url=self.url, on_failure=self.on_failure, on_redirect=self.on_redirect)
        request.wait()
        while self.redirect:
            self.redirect = False
            if request.resp_headers.get('Location'):
                self.url = request.resp_headers['Location']
            elif request.resp_headers.get('location'):
                self.url = request.resp_headers['location']
            request = UrlRequest(url=self.url, on_failure=self.on_failure,
                                 on_redirect=self.on_redirect, cookies=cookies)
            request.wait()
        return request
