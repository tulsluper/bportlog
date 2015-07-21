#!/usr/bin/env python

import os
import tarfile
from datetime import datetime
from conf import DATA_DIR, ARCHIVE_DIR


def main():
    datadirpath = os.path.join(DATA_DIR, 'portlogdump')
    archivedirpath = os.path.join(ARCHIVE_DIR, 'portlogdump')
    if not os.path.exists(archivedirpath):
        os.makedirs(archivedirpath)

    filenames = os.listdir(datadirpath)
    if filenames:
        filepath = os.path.join(datadirpath, filenames[0])
        dt = os.path.getmtime(filepath)
        dt = datetime.fromtimestamp(dt).strftime('%Y-%m-%d.%H-%M-%S')
        archivefilepath = os.path.join(archivedirpath, '{0}.tar.gz'.format(dt))
    
        with tarfile.open(archivefilepath, "w:gz") as tar:
            tar.add(datadirpath, arcname=os.path.basename(datadirpath))

if __name__ == '__main__':
    main()
