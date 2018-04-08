# -*- encoding: utf-8 -*-

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk

from subsfinder.Config import config
from subsfinder.OpenSubtitlesClient import OpenSubtitlesClient
from subsfinder import utils

class MainGui:

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file(config.get_glade_file('main.glade'))
        builder.connect_signals(self)

        self.window = builder.get_object('main_window')
        self.file_selector = builder.get_object('file_selector')
        self.languages_combobox = builder.get_object('languages_combobox')
        self.languages_list = builder.get_object('languages_list')

        self.search_btn = builder.get_object('search_btn')
        self.download_btn = builder.get_object('download_btn')
        self.cancel_btn = builder.get_object('cancel_btn')

        self.results_treeview = builder.get_object('results_treeview')
        self.subtitles_result_list = builder.get_object('subtitles_result_list')

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Subtitles", renderer, text=0)
        self.results_treeview.append_column(column)
        self.results_treeview.set_headers_visible(False)

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

        self._handle_elements_status()

    def show(self):
        self.window.show_all()
        Gtk.main()

    def on_destroy(self, *args):
        Gtk.main_quit()

    def on_file_set(self, *args):
        self._handle_elements_status()

    def get_selected_language(self):
        active_item = self.languages_combobox.get_active()

        model = self.languages_combobox.get_model()
        lang_id, lang_name = model[active_item][:2]

        return lang_id

    def get_selected_subtitle(self):
        select = self.results_treeview.get_selection()
        model, tree_iter = select.get_selected()
        if tree_iter is not None:
            return model[tree_iter]
        else:
            return None

    def _handle_elements_status(self):
        filename = self.file_selector.get_filename()

        self.cancel_btn.set_sensitive(False)

        if filename is None:
            self.search_btn.set_sensitive(False)
            self.download_btn.set_sensitive(False)
        else:
            self.search_btn.set_sensitive(True)

        selected_subtitle = self.get_selected_subtitle()
        if selected_subtitle is not None:
            self.download_btn.set_sensitive(True)
        else:
            self.download_btn.set_sensitive(False)

    def on_search_btn_clicked(self, *args):

        language = self.get_selected_language()
        filename = self.file_selector.get_filename()

        subtitles = self.os_client.search_subtitles(language, filename)

        if len(subtitles) == 0:
            # TODO: set label
            pass
        else:
            for sub_data in subtitles:
                self.subtitles_result_list.append([sub_data['MovieReleaseName'], sub_data['IDSubtitleFile']])

    def on_results_treeview_select_cursor_row(self, *args):
        self._handle_elements_status()

    def on_download_btn_clicked(self, *args):
        selected_subtitle = self.get_selected_subtitle()
        filename = self.file_selector.get_filename()

        data = self.os_client.download_subtitle(selected_subtitle[1])

        sub_path = utils.get_subtitle_path(filename)

        utils.decompress_and_save(sub_path, data[0]['data'])
