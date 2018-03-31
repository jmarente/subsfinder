# -*- encoding: utf-8 -*-

import struct, os
import StringIO
import gzip
import base64

def hash_file(filepath):
    try:

        longlongformat = '<q'  # little-endian long long
        bytesize = struct.calcsize(longlongformat)

        f = open(filepath, "rb")

        filesize = os.path.getsize(filepath)
        hash = filesize

        if filesize < 65536 * 2:
            return "SizeError"

        for x in range(65536/bytesize):
            buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number


        f.seek(max(0,filesize-65536),0)
        for x in range(65536/bytesize):
            buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash =  "%016x" % hash
        return returnedhash

    except(IOError):
        return "IOError"

def get_subtitle_path(filepath):
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

def decompress_and_save(sub_path, data):

    gzip_file_content = base64.b64decode(data)

    compressedFile = StringIO.StringIO()
    compressedFile.write(gzip_file_content)
    compressedFile.seek(0)

    decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')

    with open(sub_path, 'w') as outfile:
        outfile.write(decompressedFile.read())
