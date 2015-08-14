import sys
import conf
from datetime import datetime, timedelta
from collections import defaultdict

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


def p_xtime(logs):

    dicttree = lambda: defaultdict(dicttree)
    out = dicttree()
    utasks = set()
    for system, lines in logs.items():
        for line in lines:
            if line[46] == ' ':
                items = line.strip().split()
                minute = items[0][:16]
                task = ' '.join(items[1:3])
                port = items[3]
                count = out[system][minute][port].get(task, 0)
                out[system][minute][port][task] = count + 1
                utasks.add(task)

    utasks = sorted(utasks)

    for systems, s_values in out.items():
        sys.stdout.write(system)
        for minute, m_values in s_values.items():
            sys.stdout.write('{0}{1}\n'.format('{0:>16}'.format(''), ''.join(['{0:>6}'.format(task.split()[0]) for task in utasks])))
            sys.stdout.write('{0}{1}\n'.format('{0:>16}'.format(''), ''.join(['{0:>6}'.format(task.split()[1]) for task in utasks])))
            for port, p_values in m_values.items():
                sys.stdout.write('{0}{1}\n'.format('{0:>16}'.format(port), ''.join(['{0:>6}'.format(p_values.get(task, '-')) for task in utasks])))
                     

#    ukeys = [x3.keys() for x1 in out.values() for x2 in x1.values() for x3 in x2.values()]
#    print(set(sum(ukeys, [])))




def p_time(logs):

    alldts = {}
    for system, lines in logs.items():
        dts = {}

        for line in lines:
            items = line.strip().split()
            dtstr = items[0][:16]
            task = ' '.join(items[1:3])
            if not dtstr in dts:
                dts[dtstr] = {}
            if not task in dts[dtstr]:
                dts[dtstr][task] = 0
            dts[dtstr][task] += 1
        alldts[system] = dts


    ukeys = [list(x.keys()) for dts in alldts.values() for x in dts.values()]
    ukeys = sorted(set(sum(ukeys, [])))

    for system, dts in alldts.items():

#        ukeys = [list(x.keys()) for x in dts.values()]
#        ukeys = sorted(set(sum(ukeys, [])))

        sys.stdout.write('\n{0}\n'.format(system))
        sys.stdout.write('{0}{1}\n'.format(' '*16, ''.join(['{0:>6}'.format(n.split()[0]) for n in ukeys])))
        sys.stdout.write('{0}{1}\n'.format(' '*16, ''.join(['{0:>6}'.format(n.split()[1]) for n in ukeys])))
        sys.stdout.write('\n')

        dts_keys = sorted(dts.keys())
        min_dt = datetime.strptime(min(dts_keys), "%Y-%m-%dT%H:%M") 
        max_dt = datetime.strptime(max(dts_keys), "%Y-%m-%dT%H:%M")
        for m in range(int((max_dt-min_dt).seconds)/60+1):
            dt = min_dt +timedelta(minutes=m)
            dtstr = dt.isoformat()[:16]
            tasks = dts.get(dtstr, {})
            dtstr = dtstr.replace('T',' ')

            items = [tasks.get(k, '') for k in ukeys]

            sys.stdout.write('{0:<16}{1}\n'.format(dtstr, ''.join(['{0:>6}'.format(i) for i in items])))



#            dt = datetime.strptime(items[0], "%Y-%m-%dT%H:%M:%S.%f")
#            print(dt)


def p_task(logs):

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

    sys.stdout.write('')
    for keyspart in itemstoparts(keys, 12):
        
        sys.stdout.write('\n')
        sys.stdout.write('{0} {1}\n'.format(' '*12, ''.join(['{0:>6}'.format(n.split()[0]) for n in keyspart])))
        sys.stdout.write('{0} {1}\n'.format(' '*12, ''.join(['{0:>6}'.format(n.split()[1]) for n in keyspart])))

        for system in systems:
            items = []
            for key in keyspart:
                num = allnums[system].get(key, '')
                items.append(num)
            sys.stdout.write('{0:<12} {1}\n'.format(system, ''.join(['{0:>6}'.format(i) for i in items])))
        sys.stdout.write('')
    sys.stdout.write('\n')

#===============================================================================

def p_port(logs):

    allnums = {}
    for system, lines in logs.items():
        total = len(lines)
        nums = {}

        for line in lines:
            if line[46] == ' ':
                items = line.strip().split()
                key = items[3]
                if not key in nums:
                    nums[key] = 0
                nums[key] += 1

        for key, value in nums.items():
            nums[key] = int(value*100/total)

        allnums[system] = nums

    sys.stdout.write('')

    systems = list(allnums)
    systems = sortsystems(systems)
    
    for system in systems:
        nums = list(allnums[system].items())
        nums.sort(key=lambda x: x[1], reverse=True)

        sys.stdout.write('\n')
        for numspart in itemstoparts(nums, 8):
            sys.stdout.write('{0:<14} {1}\n'.format(system, '  '. join(['{0:>3}:{1:>3}'.format(p, v) for p, v in numspart])))
    sys.stdout.write('\n')

#===============================================================================


def p_stat(logs):

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

    if systems:
        sys.stdout.write("\n{0:<17}{1:<11}{2:<13}{3:<25}{4:<25}\n".format('', 'lines', 'duration', 'from', 'till'))
    for system in systems:
        items = [system] + allnums[system]
        sys.stdout.write("{0:<17}{1:<11}{2:<13}{3:<25}{4:<25}\n".format(*items))
    sys.stdout.write('\n')


