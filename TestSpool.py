from threadBLD import *
import sys
mem = ''

if len(sys.argv) > 1:
    mem = sys.argv[1]


mem_sp = MonitorSpooler()


exe = 'vec_test.py {}'.format(mem)

mem_sp.Spool(exe)
