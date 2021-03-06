# -*- encoding: utf-8 -*-

import argparse
import os
import sys

from subsfinder.OpenSubtitlesClient import OpenSubtitlesClient
import utils


class SubsFinder:

    def __init__(self):
        self.os_client = OpenSubtitlesClient()

    def start_cli(self):

        parser = argparse.ArgumentParser(description='Subtitles Finder.')
        subparsers = parser.add_subparsers()

        download_parser = subparsers.add_parser('download', help='Download subtitles for a giving video file')
        download_parser.add_argument('filepath', type=str, help='filepath to search subtitles')
        download_parser.add_argument('-l', '--language', dest='language', default='eng',
                            type=self.check_valid_language,
                            help='subtitles language, default "eng". Use languages command to get all languages')
        download_parser.set_defaults(func=self.download)

        language_parser = subparsers.add_parser('languages', help='Show avaible languages')
        language_parser.set_defaults(func=self.languages)

        gui_parser = subparsers.add_parser('gui', help='Start subsfinder gui')
        gui_parser.set_defaults(func=self.gui)

        # Set download as default parser
        input_args = sys.argv[1:]
        if len(input_args) and not input_args[0] in ['download', 'languages', 'gui']:
            input_args = ['download'] + input_args

        args = parser.parse_args(input_args)

        args.func(args)

    def gui(self, args):
        from subsfinder.gui.MainGui import MainGui
        main_gui = MainGui()
        main_gui.show()

    def languages(self, args):
        languages = self.os_client.get_languages()
        formated_languages = []

        max_width = 0
        columns = 3
        row_printed_columns = 0

        for lang_id, lang_name in languages.items():
            formated = '{} ({})'.format(lang_name, lang_id)
            max_width = len(formated) if len(formated) > max_width else max_width

            formated_languages.append(formated)
            row_printed_columns += 1

            if row_printed_columns % columns == 0:
                formated_languages.append(os.linesep)

        output = ''
        for language in formated_languages:
            output += language.ljust(max_width) if language != os.linesep else language

        print output

        # print "".join('{} ({}){}'.format(lang_name, lang_id, os.linesep) for lang_id, lang_name in languages.items())

    def download(self, args):

        if not os.path.isfile(args.filepath):
            print('ERROR: file not found')
            sys.exit(1)

        print('Searching subtitles for «{}» in {}'.format(args.filepath, args.language))
        subtitles_data = self.os_client.search_subtitles(args.language, args.filepath)

        if len(subtitles_data) == 0:
            print('No subtitles found')
            sys.exit(1)

        for i, sub_data in enumerate(subtitles_data):
            print('[{}] {} - {}'.format(i+1, sub_data['MovieReleaseName'].strip(), sub_data['SubLanguageID']))

        valid_input = False
        selected_option = None
        while not valid_input:
            option = raw_input('Select a option to download: ')
            if not option.isdigit():
                print('Please select a valid option')
                continue

            option = int(option) -1
            if option >= len(subtitles_data) or option < 0:
                print('Please select a valid option')
                continue

            selected_option = subtitles_data[option]
            valid_input = True

        print('Downloading subtitle...')
        data = self.os_client.download_subtitle(selected_option['IDSubtitleFile'])

        if len(data) == 0:
            print('Subtitle could not be downloaded')

        path = os.path.dirname(os.path.abspath(args.filepath))

        sub_path = utils.get_subtitle_path(args.filepath)

        utils.decompress_and_save(sub_path, data[0]['data'])

        print('Subtitle successfully saved at {}'.format(sub_path))

    def check_valid_language(self, value):
        languages = self.os_client.get_languages()
        if not value in languages:
            raise argparse.ArgumentTypeError("%s is an invalid language value, use «languages» command to list available languages" % value)
        return value
