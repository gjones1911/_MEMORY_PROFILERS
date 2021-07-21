import psutil
import sys, os
from time import time, sleep
from psutilPlay import process_cmdline, limit_checker, convert_bytes_to
from bytes_conversions import bytes2human
import argparse
from  process_file import process_file, show_result
import numpy as np

parser = argparse.ArgumentParser(description='Watches for and logs memory usage for a given program')
parser.add_argument('--suspect', help='the program to watch for', type=str)
parser.add_argument('--vmlim', help='Optional virtual memory limit in Bytes', type=int)
parser.add_argument('--rslim', help='Optional resident set size  limit in Bytes', type=int)
parser.add_argument('--logfile', help='the file the results will be stored in', type=str)
parser.add_argument('--sample_rate', help='the file the results will be stored in', type=float)

args = parser.parse_args()



# exe = 'mem_cop_tester.py'
exe = args.suspect
if args.logfile:
    logfile = args.logfile
else:
    logfile = 'log_file2.txt'
#if args.suspect is None:
#    exe = "train_sample.py"
if args.suspect is None:
    exe = input("Give me the name of the program to monitor:> ")


# Sampleing interval
interval = .8
if args.sample_rate:
    interval = args.sample_rate


# used to wait for the suspect program to show up
holdtight = True
pypoc = None
pyid = None

mlimit = 1000000000


'''
# if given get the program to watch from the command line
if len(sys.argv) > 1:
    exe = sys.argv[1]

# if given get the program to watch from the command line
if len(sys.argv) > 2:
    intverval = float(sys.argv[2])

# if given get the program to watch from the command line
if len(sys.argv) > 3:
    mlimit  = int(sys.argv[3])
'''

print('Memory Monitor Activated......')
print('sample interval: {}'.format(interval))
print('memory boundary: {}'.format(mlimit))
print('Logging results in {}'.format(logfile))
print('Waiting on program {} to show it self'.format(exe))
print('')


# hold tight until we see the program show up
while holdtight:
    # look through the current prosesses and find the one with the name you were given
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        if proc.info['name'] == 'python3' and exe in proc.cmdline() and proc.info['status'] == 'running' and sys.argv[0] not in proc.cmdline():
            print( proc.cmdline())
        if proc.info['name'] == 'python3' and exe in proc.cmdline() and proc.info['status'] == 'running' and sys.argv[0] not in proc.cmdline():
            print('Found subject: {} with PID: {}'.format(exe, proc.info['pid']))
            pyproc = proc
            # pyproc.suspend()
            holdtight = False
            pyid = proc.pid
            
# https://unix.stackexchange.com/questions/35129/need-explanation-on-resident-set-size-virtual-size
# use the pid and ps to take a snap shot of the memory usage and store it into the logfile
thecmd = "ps -p {} -o pid,rss,vsz,%cpu,etime,stat >> {}".format(pyid, logfile)
print(thecmd)
# pyproc.resume()
while psutil.pid_exists(pyid):
    os.system(thecmd)
    tsample = time()
    #while time() - tsample < interval:
    #    print('sampled')
    #    continue
print("process ended") 

# call method to process the log file
# into a data frame
# columns are:
#
#
#
ret_df = process_file(logfile)

try:
    show_result(ret_df, title='{} memory profile'.format(exe))
except Exception as ex:
    print("We tried to show results but got an exception")
    print("EXC: {}".format(ex))

rssmxO = np.max(ret_df['RSS'])
rssmx = bytes2human(rssmxO)

vmmxO = np.max(ret_df['VSZ'])
vmmx = bytes2human(vmmxO)

# Display the virtual memory and resident set size maximums
print("Max virtual memory size: {}/{}".format(vmmx, vmmxO))
print("Max Resident Set size: {}/{}".format(rssmx, rssmxO))

# remove the logfile if desired
os.system("rm {}".format(logfile))
quit(-90)

