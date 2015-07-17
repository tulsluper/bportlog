import sys
import conf
from datetime import datetime

#===============================================================================

def sortsystems(systems, records=conf.CONNECTIONS):
    sortdict = {}
    for index, record in enumerate(reversed(records)):
        name = record[0]
        sortdict[name] = index 
    systems.sort(key=lambda x: sortdict.get(x, -1), reverse=True)
    return systems

#===============================================================================

def itemstoparts(items, length):
    return [items[i:i+length] for i in range(0, len(items), length)]

#===============================================================================

def task(logs):

    allnums = {}
    for system, lines in logs.items():
        total = len(lines)
        nums = {}

        for line in lines:
            items = line.strip().split()
            key = ' '.join(items[1:3])
            if not key in nums:
                nums[key] = 0
            nums[key] += 1

        for key, value in nums.items():
            nums[key] = int(value*100/total)

        allnums[system] = nums

    keys = [list(x.keys()) for x in allnums.values()]
    keys = sorted(set(sum(keys, [])))
    systems = list(allnums.keys())
    systems = sortsystems(systems)

    sys.stderr.write('')
    for keyspart in itemstoparts(keys, 12):
        
        sys.stderr.write('\n')
        sys.stderr.write('{} {}\n'.format(' '*12, ''.join(['{:>6}'.format(n.split()[0]) for n in keyspart])))
        sys.stderr.write('{} {}\n'.format(' '*12, ''.join(['{:>6}'.format(n.split()[1]) for n in keyspart])))

        for system in systems:
            items = []
            for key in keyspart:
                num = allnums[system].get(key, '')
                items.append(num)
            sys.stderr.write('{:<12} {}\n'.format(system, ''.join(['{:>6}'.format(i) for i in items])))
        sys.stderr.write('')
    sys.stderr.write('\n')

#===============================================================================

def port(logs):

    allnums = {}
    for system, lines in logs.items():
        total = len(lines)
        nums = {}

        for line in lines:
            if line[42] == ' ':
                items = line.strip().split()
                key = items[3]
                if not key in nums:
                    nums[key] = 0
                nums[key] += 1

        for key, value in nums.items():
            nums[key] = int(value*100/total)

        allnums[system] = nums

    sys.stderr.write('')

    systems = list(allnums)
    systems = sortsystems(systems)
    
    for system in systems:
        nums = list(allnums[system].items())
        nums.sort(key=lambda x: x[1], reverse=True)

        sys.stderr.write('\n')
        for numspart in itemstoparts(nums, 8):
            sys.stderr.write('{:<14} {}\n'.format(system, '  '. join(['{:>3}:{:>3}'.format(p, v) for p, v in numspart])))
    sys.stderr.write('\n')

#===============================================================================


def stat(logs):

    allnums = {}
    for system, lines in logs.items():
        total = len(lines)
        nums = {}

        if lines:
            fdt = datetime.strptime(lines[0][:19], '%Y-%m-%dT%H:%M:%S')
            ldt = datetime.strptime(lines[-1][:19], '%Y-%m-%dT%H:%M:%S')
            duration = ldt - fdt
        else:
            duration, fdt, ldt = '-', '-', '-'

        allnums[system] = [len(lines), str(duration), str(fdt), str(ldt)]

    systems = list(allnums)
    systems = sortsystems(systems)

    sys.stderr.write("\n{:<17}{:<11}{:<13}{:<25}{:<25}\n".format('', 'lines', 'duration', 'from', 'till'))
    for system in systems:
        items = [system] + allnums[system]
        sys.stderr.write("{:<17}{:<11}{:<13}{:<25}{:<25}\n".format(*items))
    sys.stderr.write('\n')

