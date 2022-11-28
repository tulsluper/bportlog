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
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, tempdirpath)
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
                        choices=('stat', 'task', 'port', 'time', 'xtime'), default='stat',
                        help="\
execute parser function:\n\
stat - records base statistic\n\
task - records percentage for each task event\n\
port - records percentage for each port\n\
time - records percentage for each minute\n\
(default: stat)")

    parser.add_argument('-s', metavar='system',
                        nargs='+',
                        help='execute for specified system(s) or all')
    parser.add_argument('-a', metavar='archive',
                        help='get data from archive file')
    args = parser.parse_args()


    dirpath = exarch(args.a) if args.a else DATA_DIR
    logs = getlogs(dirpath, args.s)
    function = getattr(parsers, 'p_%s' %args.p)
    function(logs)

    return

if __name__ == '__main__':
    main()


