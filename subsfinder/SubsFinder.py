# -*- encoding: utf-8 -*-

import argparse
import os
import sys
import StringIO
import gzip
import base64

from subsfinder.OpenSubtitlesClient import OpenSubtitlesClient


class SubsFinder:

    def __init__(self):
        self.osClient = OpenSubtitlesClient()

    def start_cli(self):

        parser = argparse.ArgumentParser(description='Subtitles Finder.')
        parser.add_argument('filepath', type=str, help='filepath to search subtitles')
        parser.add_argument('-l', '--language', dest='language', type=str, default='eng',
                            help='subtitles language, default "eng". Use languages command to get all languages')

        args = parser.parse_args()

        if not os.path.isfile(args.filepath):
            print('ERROR: file not found')
            sys.exit(1)

        print('Searching subtitles for «{}» in {}'.format(args.filepath, args.language))
        subtitles_data = self.osClient.search_subtitles(args.language, args.filepath)

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
        data = self.osClient.download_subtitle(selected_option['IDSubtitleFile'])

        if len(data) == 0:
            print('Subtitle could not be downloaded')

        path = os.path.dirname(os.path.abspath(args.filepath))

        sub_path = self.get_subtitle_path(args.filepath)

        self.decompress_and_save(sub_path, data[0]['data'])

        print('Subtitle successfully saved at {}'.format(sub_path))

    def get_subtitle_path(self, filepath):
        abspath = os.path.abspath(filepath)
        filename, file_extension = os.path.splitext(abspath)
        path = os.path.dirname(filename)

        sufix = 0
        tmp_sub_path = filename + '.srt'
        sub_path = None
        while not sub_path:
            if not os.path.isfile(tmp_sub_path):
                sub_path = tmp_sub_path
            else:
                sufix += 1
                tmp_sub_path = '{}-{}.srt'.format(filename, sufix)

        return sub_path

    def decompress_and_save(self, sub_path, data):

        gzip_file_content = base64.b64decode(data)

        compressedFile = StringIO.StringIO()
        compressedFile.write(gzip_file_content)
        compressedFile.seek(0)

        decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')

        with open(sub_path, 'w') as outfile:
            outfile.write(decompressedFile.read())

