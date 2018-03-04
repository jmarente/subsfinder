# -*- encoding: utf-8 -*-

from subsfinder.OpenSubtitlesClient import OpenSubtitlesClient

import argparse

class SubsFinder:

    def __init__(self):
        self.osClient = OpenSubtitlesClient()

    def start_cli(self):

        print(self.osClient.login())
        print(self.osClient.get_languages())
