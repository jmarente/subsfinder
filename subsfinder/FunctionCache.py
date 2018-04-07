# -*- encoding: utf-8 -*-

import pickle
import os
import time
import hashlib

from subsfinder.Config import config

class FunctionCache(object):

    def __init__(self, cache_time = 300):
        self.cache_time = cache_time

    def __call__(self, fn, *args, **kwargs):
        def new_func(*args, **kwargs):
            output = self._get_function_cache(fn, *args, **kwargs)

            if output is None:
                output = fn(*args, **kwargs)
                self._save_function_cache(output, fn, *args, **kwargs)

            return output

        return new_func

    def _get_function_cache(self, fn, *args, **kwargs):
        cache_file_name = self._get_file_name(fn, *args, **kwargs)
        file_path = os.path.join(config.cache_path, cache_file_name)

        file_content = None

        if os.path.isfile(file_path):
            file_time = os.path.getmtime(file_path)
            elapsed_time = time.time() - file_time
            if elapsed_time <= self.cache_time:
                with open(file_path) as f:
                    file_content = pickle.loads(f.read())

        return file_content

    def _save_function_cache(self, output, fn, *args, **kwargs):
        cache_file_name = self._get_file_name(fn, *args, **kwargs)
        file_path = os.path.join(config.cache_path, cache_file_name)

        with open(file_path, 'w') as f:
            file_content = f.write(pickle.dumps(output))

    def _get_file_name(self, fn, *args, **kwargs):
        key = [fn.__module__, fn.__name__, args, tuple(sorted(kwargs.items()))]

        hashed_key = hashlib.md5(pickle.dumps(key)).hexdigest()

        return '{}.{}'.format(hashed_key, 'txt')
