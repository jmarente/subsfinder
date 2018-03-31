# -*- encoding: utf-8 -*-

import sys
import collections

from subsfinder import utils

# FIXME: move somewhere else
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    from xmlrpclib import ServerProxy, Transport
else:
    from xmlrpc.client import ServerProxy, Transport


DEFAULT_USER_AGENT = 'TemporaryUserAgent'
API_URL = 'https://api.opensubtitles.org/xml-rpc'

class OpenSubtitlesClient:

    def __init__(self, user_agent=DEFAULT_USER_AGENT, username=None, password=None):

        self.user_agent = user_agent
        self.username = username
        self.password = password

        transport = Transport()
        transport.user_agent = self.user_agent

        self.xmlrpc = ServerProxy(API_URL, allow_none=True, transport=transport)

        self._token = None

    def login(self):

        response = self.xmlrpc.LogIn(self.username, self.password, None, self.user_agent)

        self._token = response.get('token', None)

    @property
    def token(self):
        if self._token is None:
            self.login()
        return self._token

    def get_languages(self):

        response = self.xmlrpc.GetSubLanguages()

        data = response.get('data')
        languages = {lang.get('SubLanguageID'): lang.get('LanguageName') for lang in data}
        od = collections.OrderedDict(sorted(languages.items()))

        return od

    def search_subtitles(self, language, filepath):

        moviehash = utils.hash_file(filepath)

        request_data = [{ 'moviehash': moviehash, 'sublanguageid': language}]

        response = self.xmlrpc.SearchSubtitles(self.token, request_data, {'limit': 10})

        return response.get('data', [])

    def download_subtitle(self, id_subtitle_file):

        response = self.xmlrpc.DownloadSubtitles(self.token, [id_subtitle_file])

        return response.get('data', [])
