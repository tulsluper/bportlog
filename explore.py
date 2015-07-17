#!/usr/bin/env python

import os
import argparse
from datetime import datetime
import conf
import parsers


def getlogs(systems=None, dirpath=conf.DATA_DIR):
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

    parser = argparse.ArgumentParser(description='Brocade portlogdump analysis\nExplore data',
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
    args = parser.parse_args()

    logs = getlogs(args.s)
    function = getattr(parsers, args.p)
    result = function(logs)
    pass

if __name__ == '__main__':
    main()


