import psutil
import os
import sys

BIGV = 8000000000

pagesize = 4096
# byte conversion factors
# https://convertlive.com/u/convert/bytes/to/gigabytes
byte_conversion_dict = {
        "G":1073741824, 
        "M":1048576, 
        "K":1024, 
}


def process_cmdline(argv):
    exe, rsslim, vmlim, = '', BIGV, BIGV
    the_args = list()
    # grab all the args an look for certain ones:
    if len(argv) > 1:
        for arg in argv[1:]:
            if '-vm' in arg:
                print('found the vm ')
                vmlim = int(arg.split(':')[1].strip())
            if '-rs' in arg:
                print('found the vm ')
                rsslim = int(arg.split(':')[1].strip())
            if '.py' in arg:
                exe = arg
    print('exe: {}, rsslim: {}, vmlim: {}'.format(exe, rsslim, vmlim))

    return exe, rsslim, vmlim

def limit_checker(rsslim, vmlim, rss, vm):
    rssR = rsslim < rss
    vmR = vmlim < vm
    return rssR or vmR




def convert_GB_to_B(gb):
    return gb * byte_conversion_dict["G"]


def convert_bytes_to(bytes, conv="G"):
    return bytes/byte_conversion_dict[conv]

#print('there are {} GB  or {} MB in {} B'.format(convert_bytes_to(9666560), 
#    convert_bytes_to(9666560, conv="M"), 9666560))

#quit(9)

#myPid = os.getpid()

#print('the pid for {} is {}'.format(sys.argv[0], myPid))

def log_cpu_prct(interval=1, numsamples=4, percpu=False):
    """
        will get snap shots of % cpu used for given interval time, 
        for the given number of samples. if percpu is true then does for every cpu
    """
    for i in range(numsamples):
        print(psutil.cpu_percent(interval=interval, percpu=percpu ))

def get_ctx_swtchs():
    return psutil.cpu_stats().ctx_switches

def get_vm_stat(stat='total'):
    if stat=='total':
        return psutil.virtual_memory().total
    elif stat == 'available':
        return psutil.virtual_memory().available
    elif stat == 'used':
        return psutil.virtual_memory().used
    elif stat == 'percent':
        return psutil.virtual_memory().percent
    elif stat == 'free':
        return psutil.virtual_memory().free
    elif stat == 'buffers':
        return psutil.virtual_memory().buffers
    elif stat == 'cached':
        return psutil.virtual_memory().cached


def get_batt_stat(stat='percent'):
    #print(psutil.sensors_battery())
    if stat == 'percent':
        return psutil.sensors_battery().percent
    elif stat == 'secsleft':
        return psutil.sensors_battery().secsleft
    elif stat == 'plugged':
        return psutil.sensors_battery().power_plugged
    
def get_running_pids():
    return psutil.pids()

def search_pids():
    for pid in get_running_pids():
        print('Pid: {}'.format(pid))


def get_process_by_id(pid):
    return psutil.Process(pid)


def get_process_kidsId_by_process(process):
    kids = list()
    for kid in process.children(recursive=True):
        kids.append(kid.pid)
    print(kids)
    return kids


def get_process_kids_by_id(pid):
    process = get_process_by_id(pid)
    kidIds = get_process_kidsId_by_process(process)    
    return kidIds

def get_process_mem_info(process=None, pid=None, des_info=[]):
    if process is None and pid is None:
        print('error: need either pid or process, none given')
        quit(-74)

    if process is not None:
        memInfo = process.memory_full_info()
    elif pid is not None:
        memInfo = get_process_by_id(pid).memory_full_info()
    if len(des_info) == 0:
        rss = memInfo.rss
        print('returning rss: {}'.format(rss))
        return rss


"""
# test the percent counter
log_cpu_prct(interval=.25, percpu=True)


# check the number of cpu's available

ncp = psutil.cpu_count(logical=False)
print("There are {} cpu's available".format(ncp))

# see how many context switches have occured
print(get_ctx_swtchs())

# look at some virtual memory info:
tot = get_vm_stat(stat='total')
avl = get_vm_stat(stat='available')
usd = get_vm_stat(stat='used')
print("total: {}, available: {}, used: {}".format(tot, avl, usd))

# log some battery info
#  NOTE: the timing, metric dosent work
plgin = get_batt_stat(stat='plugged')
seslft = get_batt_stat(stat='secsleft')
bpct = get_batt_stat(stat='percent')
print('\t\t\tBattery info:')
print("Plugged in?: {}, secs left: {}, % left: {}".format(plgin, seslft, bpct))

search_pids()

get_process_kids_by_id(myPid)


get_process_mem_info(process=None, pid=myPid, des_info=[])
"""
