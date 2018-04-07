#/usr/bin/python
# -*- encoding: utf-8 -*-

from subsfinder.SubsFinder import SubsFinder
from subsfinder.Config import config

def main():
    config.initialize()
    subsFinder = SubsFinder()
    subsFinder.start_cli()

if __name__ == '__main__':
    main();
