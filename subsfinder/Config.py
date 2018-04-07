# -*- encoding: utf-8 -*-

import os

class __Config:

    def __init__(self):
        self.home_path = os.getenv('HOME')
        self.config_path = os.path.join(self.home_path, '.subsfinder')
        self.cache_path = os.path.join(self.config_path, 'cache')
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(self.file_path, '..', 'data')

    def initialize(self):
        print "Initialazing..."

        if not os.path.isdir(self.config_path):
            os.makedirs(self.config_path)
            print "Config folder created"

        if not os.path.isdir(self.cache_path):
            os.makedirs(self.cache_path)
            print "Cache folder created"

    def get_glade_file(self, filename):
        return os.path.join(self.data_path, filename)

    def initilize(self):
        pass

config = __Config()
