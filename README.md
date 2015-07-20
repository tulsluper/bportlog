# bportlog
Brocade portlogdump collector and analyzer
<br><br><br>

Clone the repo or download the latest release and unpack to bportlog.

Install python-dev and python-pip on system.

Install requirements `sudo pip install -r requirements.txt`.

    
### Configure bportlog

Add switches to CONNECTIONS in conf.py

```python
CONNECTIONS = [
    ['dcx1', '192.168.56.101', 'user', 'password'],   
    ['dcx2', '192.168.56.102', 'user', 'password'],
]
```

### Collect logs

`./collect.py`

run with -h for help

### Explore logs

`./explore.py`

run with -h for help

### Examples

`./collect.py -h`
```
usage: collect.py [-h] [-r R] [-i I]

Brocade portlogdump analysis
Collect data

optional arguments:
  -h, --help  show this help message and exit
  -r R        repeat R times (default: 1)
  -i I        set I seconds interval between repeats (default:300)
```

`./collect.py -r 3 -i 300`
```
Data collection finished: 2/2                          
Data save finished: 2/2                          
Duration: 14
Timeout: 286       
Data collection finished: 2/2                          
Data save finished: 2/2                          
Duration: 20
Timeout: 280       
Data collection finished: 2/2                          
Data save finished: 2/2                          
Duration: 16
```

`./explore.py -h`
```
usage: explore.py [-h] [-p parser] [-s system [system ...]]

Brocade portlogdump analysis
Explore data

optional arguments:
  -h, --help            show this help message and exit
  -p parser             execute parser function:
                        stat - records base statistic
                        task - records percentage for each task event
                        port - records percentage for for each port
                        (default: stat)
  -s system [system ...]
                        execute for specified system(s) or all
```

`./explore.py -p stat`
```
                 lines      duration     from                     till
dcx1             12568      0:15:00      2015-07-17 11:18:00      2015-07-17 11:33:00
dcx2             12264      0:14:53      2015-07-17 11:18:07      2015-07-17 11:33:00
```

`./explore.py -p task`
```
               0.we  0.we  FCPH  FCPH  FCPH  PORT  PORT  PORT  PORT  PORT  cald  cald
               ctin ctout  read   seq write    Rx   Rx3    Tx   Tx3 debug  ctin ctout
dcx1              0     0    11    23    12    14     5    14     5     1     0     0
dcx2              0     0    11    23    12    14     5    14     5     1     0     0

                msd   msd   nsd   nsd   nsd
               ctin ctout  ctin ctout  rscn
dcx1              2     2     2     2     0
dcx2              2     2     2     2     0
```
`./explore.py -p port`
```
dcx1             1: 31   65: 14    0: 12   68:  4   93:  4   32:  3   33:  3   77:  2
dcx1            76:  2   74:  2   85:  2   72:  2   73:  2  289:  2   87:  2   75:  2
dcx1            86:  2   79:  1   78:  1  305:  0  316:  0  293:  0  290:  0  312:  0
dcx1           299:  0  298:  0  318:  0  309:  0  315:  0  303:  0  314:  0  319:  0
dcx1           308:  0  291:  0  310:  0  300:  0   92:  0  313:  0  306:  0  292:  0
dcx1           297:  0  288:  0  296:  0  311:  0  302:  0  317:  0  307:  0  304:  0
dcx1           295:  0  294:  0  301:  0

dcx2             1: 31   64: 14    0: 11   32:  4   33:  4   93:  4   68:  3   75:  3
dcx2            77:  2   79:  2   76:  2   78:  2   85:  2  289:  2   86:  2   74:  1
dcx2            72:  1   73:  1   87:  1  305:  0  316:  0  293:  0  290:  0  312:  0
dcx2           299:  0  298:  0  318:  0  309:  0  315:  0  303:  0  314:  0  319:  0
dcx2           308:  0  291:  0  310:  0  300:  0   92:  0  313:  0  306:  0  292:  0
dcx2           297:  0  288:  0  296:  0  311:  0  302:  0  317:  0  307:  0  304:  0
dcx2           295:  0  294:  0  301:  0
```
    


