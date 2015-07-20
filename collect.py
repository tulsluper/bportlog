#!/usr/bin/env python

import os
import sys
import json
import shutil
import argparse
from time import time, sleep
from datetime import datetime, timedelta
from multiprocessing import Pool
from paramiko import SSHClient, AutoAddPolicy
from conf import ARGUMENTS, COMMANDS, CONNECTIONS, PROCESSES, DATA_DIR, TEMP_DIR


def ssh_run(system, address, username, password, commands):
    address, port = address.split(':') if ':' in address else address, 22
    outs, errs, exception = {}, {}, None
    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(address, port=port, username=username, password=password)
        for name, command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            outs[name] = stdout.read().decode("utf-8")
            errs[name] = stderr.read().decode("utf-8")
    except Exception as e:
        exception = e
    finally:
        client.close()
    return system, outs, errs, exception

def ssh_run_wrap(args):
    return ssh_run(*args)


def multiwalk(function, arguments, processes):
    argsnum = len(arguments)
    acc = 0
    pool = Pool(processes=processes)
    results = []
    for result in pool.imap_unordered(function, arguments):
        acc +=1
        system = result[0]
        sys.stdout.write('Data collection progress: {}/{} {:<20}\r'.format(acc, argsnum, system))
        sys.stdout.flush()
        results.append(result)
    sys.stdout.write('Data collection finished: {}/{} {:<25}\n'.format(acc, argsnum, ''))
    return results


def preparedirs(COMMANDS):
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    for name, command in COMMANDS:
        dirpath = os.path.join(DATA_DIR, name)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
    return


def prepare(lines, lastline, dtnow):
    newlines = []
    dtmin = dtnow - timedelta(minutes=5)
    for line in lines[2:-1]:
        if line[3] == ' ':
           date = datetime.strptime(line, '%c').date()
        else:
           time = datetime.strptime(line[:12], '%H:%M:%S.%f').time()
           dt = datetime.combine(date, time)
           if lastline or dtmin < dt < dtnow:
               newline = '{} {}'.format(dt.isoformat()[:19], line[13:])
               newlines.append(newline)
    try:
        if lastline != newlines[-1]:
            index = newlines.index(lastline)
            newlines = newlines[index:]
    except:
        pass

    return newlines


def saveouts(records, dirpath, lastlines, dtnow):
    argsnum = len(records)
    acc = 0
    for system, outs, errs, exception in records:
        lastline = lastlines.get(system, None)
        lines = outs['portlogdump'].split('\n')
        lines = prepare(lines, lastline, dtnow)
        filepath = os.path.join(dirpath, 'portlogdump/%s.txt' %system)
        if lines:
            with open(filepath, 'a') as f:
                f.write('\n'.join(lines)+'\n')
        if lines:
            lastlines[system] = lines[-1]

        acc +=1
        sys.stdout.write('Data save progress: {}/{} {:<20}\r'.format(acc, argsnum, system))
        sys.stdout.flush()

    sys.stdout.write('Data save finished: {}/{} {:<25}\n'.format(acc, argsnum, ''))
    return lastlines


def run_timer(seconds):
   timeout = seconds
   while seconds:
       sys.stdout.write('Timeout: {:<10}\r'.format(seconds))
       sys.stdout.flush()
       sleep(1)
       seconds -= 1
   sys.stdout.write('Timeout: {}\n'.format(timeout))


def run():
    starttime = time()
    dtnow = datetime.now()

    filepath = os.path.join(TEMP_DIR, 'portlogdump.json')
    if os.path.isfile(filepath):
        with open(filepath) as f:
            lastlines = json.load(f)
    else:
        lastlines = {}

    records = multiwalk(ssh_run_wrap, ARGUMENTS, PROCESSES)
    lastlines = saveouts(records, DATA_DIR, lastlines, dtnow)

    filepath = os.path.join(TEMP_DIR, 'portlogdump.json')
    with open(filepath, 'w') as f:
        json.dump(lastlines, f)

    duration = int(time() - starttime)
    sys.stdout.write('Duration: {}\n'.format(duration))
    return duration


def main():

    preparedirs(COMMANDS)

    parser = argparse.ArgumentParser(description='Brocade portlogdump collector and analyzer\nCollect data',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-r', type=int, default=1, help='repeat R times (default: 1)')
    parser.add_argument('-i', type=int, default=300, help='set I seconds interval between repeats (default:300)')
    args = parser.parse_args()

    interval = args.i
    repeat = args.r
    while repeat:
        duration = run()
        timeout = interval - duration if interval > duration else 10
        repeat -= 1
        if repeat:
            run_timer(timeout)


if __name__ == '__main__':
    main()


