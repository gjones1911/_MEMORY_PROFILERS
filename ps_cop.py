import psutil
import sys, os
from time import time, sleep
from psutilPlay import process_cmdline, limit_checker, convert_bytes_to
from bytes_conversions import bytes2human
import argparse
from  process_file import process_file #, show_result
import numpy as np

parser = argparse.ArgumentParser(description='Watches for and logs memory usage for a given program')
parser.add_argument('--suspect', help='the program to watch for', type=str)
parser.add_argument('--vmlim', help='Optional virtual memory limit in Bytes', type=int)
parser.add_argument('--rslim', help='Optional resident set size  limit in Bytes', type=int)
parser.add_argument('--logfile', help='the file the results will be stored in', type=str)
parser.add_argument('--sample_rate', help='the file the results will be stored in', type=float)

args = parser.parse_args()



exe = 'mem_cop_tester.py'
exe = args.suspect
if args.logfile:
    logfile = args.logfile
else:
    logfile = 'log_file2.txt'




# exf, rslim, vmlim = process_cmdline(sys.argv) 

# if exf != '':
#    print('given the file: {}'.format(exe))
#    exe = exf


interval = .8
if args.sample_rate:
    interval = args.sample_rate



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
# now set some limits on the thing
# limit virtual memory 

#pyproc.rlimit(psutil.RLIMIT_AS, (1000000, 1000000))
print('vmlim: ', pyproc.rlimit(psutil.RLIMIT_AS,))
print('rss lim: ', pyproc.rlimit(psutil.RLIMIT_RSS, ))
#pyproc.rlimit(psutil.RLIMIT_RSS, (100, 100))
print('rss lim: ', pyproc.rlimit(psutil.RLIMIT_RSS,))

print('pid: {}'.format(pyid))
print("trying: ")
# use the pid and ps to take a snap shot of the memory usage and store it into the logfile
thecmd = "ps -p {} -o pid,rss,vsz,time >> {}".format(pyid, logfile)
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
ret_df = process_file(logfile) 
#show_result(ret_df, title='{} memory profile'.format(exe))


rssmxO = np.max(ret_df['RSS'])
rssmx = bytes2human(rssmxO)

vmmxO = np.max(ret_df['VSZ'])
vmmx = bytes2human(vmmxO)


print("Max virtual memory size: {}/{}".format(vmmx, vmmxO))
print("Max Resident Set size: {}/{}".format(rssmx, rssmxO))


os.system("rmv {}".format(logfile))
quit(-90)







#pyproc.cpu_affinity([1,2])
print('cpu affinity', pyproc.cpu_affinity())
#pyproc.cpu_affinity([1,2])
#pyproc.cpu_affinity([1])
print('cpu affinity', pyproc.cpu_affinity())


# pyproc.resume()
rssmx, vmmx, dsizemx = 0, 0, 0
verbose=True
v2 = False
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
    dsizemx = max(dsizemx, dsize)
    batt_pct = "Nope"    
    batt_secsleft = "Nope"    
    try:
        batt_pct = psutil.sensors_battery().percent
        batt_secsleft = psutil.sensors_battery().secsleft
    except Exception as err:
        batt_pct = "Nope"
        batt_secsleft = "Nope"
        if verbose and v2:
            print('Exception: {}'.format(err))
        if err == "NoneType":
            if verbose and v2:
                print("________________________------------------>>>>Yep")
    
    try:
        if psutil.pid_exists(pyid):
            sts = pyproc.info['status']
        if psutil.pid_exists(pyid):
            cpupct = pyproc.cpu_percent(interval=1)
        if psutil.pid_exists(pyid):
            vctxs, ivctxs = pyproc.num_ctx_switches().voluntary,  pyproc.num_ctx_switches().involuntary
            ctxs = vctxs + ivctxs
    except Exception as err:
        if verbose:
            print('Exception: {}'.format(err))

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
        print('ContextSwitchs:               {:,}'.format(ctxs))
        print('Voluntary ContextSwitchs:     {:,}'.format(vctxs))
        print('Involuntary ContextSwitchs:   {:,}'.format(ivctxs))
        print('cpu %:                        {:.3f}'.format(cpupct))
        print('-------------------------------------------\n')
    #if rss > mlimit or not psutil.pid_exists(pyid):
    if limit_checker(rslim, vmlim, rss, vmm)  or not psutil.pid_exists(pyid):
        if rss > rslim:
            print('rss limit reached, killing process: {}'.format(pyid))
            print('limit: {:>30}'.format(rslim))
            print('rss:   {: >30}'.format(rss))
            pyproc.kill()
        elif vmm > vmlim:
            print('vm limit reached, killing process: {}'.format(pyid))
            print('limit: {:>30}'.format(vmlim))
            print('vm: {:>30}'.format(vmm))
            pyproc.kill()
        else:
            print('Process Finished:')
            print('limit: {:>30}'.format(mlimit))
            print('rss: {:>30}'.format(rss))
        break
    #pyproc.resume()                                                        # now keep going
    sleep(interval)


# convert the values to more readable ones
rssmx = bytes2human(rssmx)
rss = bytes2human(rss)
rslim= bytes2human(rslim)

vmmx = bytes2human(vmmx)
vmm = bytes2human(vmm)
vmlim = bytes2human(vmlim)

dsizemx = bytes2human(float(dsizemx))
dsize = bytes2human(float(dsize))

print('pid: {}'.format(pyid))
print('----------------------------   Process Finished:  --------------------------------')
print('                    Max     Final                            -')
print('rss:                {:6}    {:}          bytes'.format(rssmx, rss,))
print('virual_memory:      {:4}     {:}          bytes'.format(vmmx, vmm,))
print('data size:          {:5}     {:}          bytes'.format(dsizemx, dsize,))

