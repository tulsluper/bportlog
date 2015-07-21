#!/usr/bin/env python

import os
import sys
import argparse
import tarfile
import tempfile
from datetime import datetime

from conf import DATA_DIR
import parsers


def exarch(filepath):
    if not os.path.exists(filepath):
        sys.stderr.write('path not found\n')
        sys.exit(1)
    if os.path.isdir(filepath):
        sys.stderr.write('specify file, not directory\n')
        sys.exit(1)
    if not tarfile.is_tarfile(filepath):
        sys.stderr.write('file is not tar archive\n')
        sys.exit(1)
    with tarfile.open(filepath) as tar:
        tempdirpath = tempfile.mkdtemp()
        tar.extractall(tempdirpath)
    return tempdirpath


def getlogs(dirpath, systems=None):
    logs = {}
    logdirpath = os.path.join(dirpath, 'portlogdump')
    for filename in os.listdir(logdirpath):
        system = os.path.splitext(filename)[0]
        if systems is None or system in systems:
            filepath = os.path.join(logdirpath, filename)
            with open(filepath) as f:
                lines = f.readlines()
                logs[system] = lines   
    return logs


def main():

    parser = argparse.ArgumentParser(description='Brocade portlogdump collector and analyzer\nExplore data',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', metavar='parser',
                        choices=('stat', 'task', 'port'), default='stat',
                        help="\
execute parser function:\n\
stat - records base statistic\n\
task - records percentage for each task event\n\
port - records percentage for for each port\n\
(default: stat)")

    parser.add_argument('-s', metavar='system',
                        nargs='+',
                        help='execute for specified system(s) or all')
    parser.add_argument('-a', metavar='archive',
                        help='get data from archive file')
    args = parser.parse_args()


    dirpath = exarch(args.a) if args.a else DATA_DIR
    logs = getlogs(dirpath, args.s)
    function = getattr(parsers, args.p)
    function(logs)

    return

if __name__ == '__main__':
    main()


