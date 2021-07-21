import psutil
import sys, os
from time import time, sleep
from psutilPlay import process_cmdline, limit_checker, convert_bytes_to
from bytes_conversions import bytes2human
import argparse
from  process_file import process_file, show_result
import numpy as np
try:
    import pandas as pd
except Exception as ex:
    print("lldkl")
# exe = 'mem_cop_tester.py'


#exf, rslim, vmlim = process_cmdline(sys.argv)

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


interval = .8
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

print('Memory Cop Activated......')
print('sample interval: {}'.format(interval))
print('memory boundary: {}'.format(mlimit))
print('Waiting on program {} to show it self'.format(exe))
print('')


tstart=0
while holdtight:
    # look through the current prosesses and find the one with the name you were given
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        if proc.info['name'] == 'python3' and exe in proc.cmdline() and proc.info['status'] == 'running' and sys.argv[0] not in proc.cmdline():
            print( proc.cmdline())
        if proc.info['name'] == 'python3' and exe in proc.cmdline() and proc.info['status'] == 'running' and sys.argv[0] not in proc.cmdline():
            tstart = time()
            print('Found subject: {} with PID: {}'.format(exe, proc.info['pid']))
            pyproc = proc
            #pyproc.suspend()
            holdtight = False
            pyid = proc.pid
            
# https://unix.stackexchange.com/questions/35129/need-explanation-on-resident-set-size-virtual-size
# now set some limits on the thing
# limit virtual memory 

#pyproc.rlimit(psutil.RLIMIT_AS, (1000000, 1000000))
#print('vmlim: ', pyproc.rlimit(psutil.RLIMIT_AS,))
#print('rss lim: ', pyproc.rlimit(psutil.RLIMIT_RSS, ))
#pyproc.rlimit(psutil.RLIMIT_RSS, (100, 100))
#print('rss lim: ', pyproc.rlimit(psutil.RLIMIT_RSS,))

print('logging pid: {}/{}'.format(pyid, exe))

#pyproc.cpu_affinity([1,2])
#print('cpu affinity', pyproc.cpu_affinity())
#pyproc.cpu_affinity([1,2])
#pyproc.cpu_affinity([1])
#print('cpu affinity', pyproc.cpu_affinity())


#pyproc.resume()
rssmx, vmmx, dsizemx = 0, 0, 0
verbose=False
v2 = False

data_dict = {
    "PID":[],
    "RSS":[],
    "VSZ":[],
    "%CPU":[],
    "ELAPSED":[],
    "STAT":[],
}


# now start watching its rss and make sure it doesn't get to big
while psutil.pid_exists(pyid):
    #pyproc.suspend()                              # hold on there fella
    minfo = pyproc.memory_full_info()
    rss = int(minfo.rss)
    uss = int(minfo.uss)
    vmm = int(minfo.vms)   
    textsz = minfo.text
    dsize  = minfo.data
    swped = minfo.swap
    rssmx = max(rss, rssmx)
    vmmx = max(vmm, vmmx)
    try:
        if psutil.pid_exists(pyid):
            sts = pyproc.info['status']
        if psutil.pid_exists(pyid):
            cpupct = pyproc.cpu_percent(interval=1)
    except Exception as err:
        if verbose:
            print('Exception: {}'.format(err))
        sts = np.nan
        cpupct = np.nan

    data_dict["PID"].append(pyid)
    data_dict["RSS"].append(rss)
    data_dict["VSZ"].append(vmm)
    data_dict["%CPU"].append(cpupct)
    data_dict["ELAPSED"].append(time()-tstart)
    data_dict["STAT"].append(sts)
    #dsizemx = max(dsizemx, dsize)

    # try:
    #     #batt_pct = psutil.sensors_battery().percent
    #     #batt_secsleft = psutil.sensors_battery().secsleft
    # except Exception as err:
    #     #batt_pct = "Nope"
    #     #batt_secsleft = "Nope"
    #     if verbose and v2:
    #         print('Exception: {}'.format(err))
    #     if err == "NoneType":
    #         if verbose and v2:
    #             print("________________________------------------>>>>Yep")

    if verbose:
        print('-------------------------------------------')
        print('Limit:                        {:,}'.format(mlimit))
        print('rss:                          {:,}'.format(rss))
        print('uss:                          {:,}'.format(uss))
        print('virual_memory alloted:        {:,}'.format(vmm))
        print('swap:                         {:,}'.format(swped))
        print('data size:                    {:,}'.format(dsize))
        print('code size:                    {:,}'.format(textsz))
        print('status:                       {:}'.format(sts))
        #print('%bat:                         {}'.format(batt_pct))
        #print('bat secs left:                {:}'.format(batt_secsleft))
        #print('ContextSwitchs:               {:,}'.format(ctxs))
        #print('Voluntary ContextSwitchs:     {:,}'.format(vctxs))
        #print('Involuntary ContextSwitchs:   {:,}'.format(ivctxs))
        #print('cpu %:                        {:.3f}'.format(cpupct))
        print('-------------------------------------------\n')                                            # now keep going
    sleep(interval)
if os.path.isfile("Log.csv"):
    try:
        old_df = pd.read_csv("Log.csv")
        new_df = pd.concat([old_df, pd.DataFrame(data_dict)])
        new_df.to_csv("Log.csv", index=False)
    except Exception as ex:
        print("ex: ", ex)




# convert the values to more readable ones
rssmx = bytes2human(rssmx)

vmmx = bytes2human(vmmx)

print('pid: {}'.format(pyid))
print('----------------------------   Process Finished:  --------------------------------')
print('                    Max')
print('virual_memory:      {:4}'.format(vmmx,))
print('rss:                {:6}'.format(rssmx,))

