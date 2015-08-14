"""
config file for bportlog scripts
"""

import os


PROCESSES = 4 # number of processes for multiprocessing

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
TEMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp'))
ARCHIVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'archive'))

CONNECTIONS = [
   #['switch name', 'switch address', 'username', 'password'],
    ['dcx1', 'dcx1.sdab.sn', 'user', 'D1az0l1n.'],
    ['dcx2', 'dcx2.sdab.sn', 'user', 'D1az0l1n.'],
    ['dcx3', 'dcx3.sdab.sn', 'user', 'D1az0l1n.'],
    ['dcx4', 'dcx4.sdab.sn', 'user', 'D1az0l1n.'],

]

COMMANDS = [
    ['portlogdump', 'portlogdump'],
]

ARGUMENTS = []
for connection in CONNECTIONS:
    ARGUMENTS.append(connection + [COMMANDS])
