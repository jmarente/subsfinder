# -*- encoding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk

from subsfinder.Config import config
from subsfinder.OpenSubtitlesClient import OpenSubtitlesClient

class MainGui:

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file(config.get_glade_file('main.glade'))
        builder.connect_signals(self)

        self.window = builder.get_object('main_window')
        self.languages_combobox = builder.get_object('languages_combobox')
        self.languages_list = builder.get_object('languages_list')

        self.os_client = OpenSubtitlesClient()

        # Initialize languages combobox
        cell = Gtk.CellRendererText()
        self.languages_combobox.pack_start(cell, True)
        self.languages_combobox.add_attribute(cell, "text", 1)

        english_index = 0
        count = 0
        for lang_id, lang_name in self.os_client.get_languages().items():
            if lang_id == 'eng':
                english_index = count
            self.languages_list.append([lang_id, lang_name])
            count += 1

        self.languages_combobox.set_active(english_index)

    def show(self):
        self.window.show_all()
        Gtk.main()

    def on_destroy(self, *args):
        Gtk.main_quit()

