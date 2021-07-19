import psutil
import time
import numpy as np
import tracemalloc
from sys import argv
# get the number of seconds in a minute
def minsSecs(mins):
    return mins*60


def processHpyReport(report):
    return int(str(report).split('.')[1].split('=')[1].strip().split(' ')[0])


def getHeapDel(r1, r2):
    return r2 - r1


def grab_report(h):
    return processHpyReport(h.heap())

def CPU_percent(interval=.5):
    return ps.util.cpu_percent(interval=interval)

def EnergyProfile():
    print((psutil.sensors_battery().percent))
    return

def calculateRAM():
    return int(psutil.virtual_memory().total - psutil.virtual_memory().available)



def RamUsage(size='MB'):
    """
    Obtains the absolute number of RAM bytes currently in use by the system.
    :returns: System RAM usage in bytes.
    :rtype: int
    """
    rmsz = calculateRAM()

    if size=='MB':
        rmsz = int(np.around(rmsz/1000000, 0))
        print('rmz: ', rmsz)


    return rmsz


def RamTracker(mins, rate=10):

    tdiff = 0
    t0 = time.time()
    lims = minsSecs(mins)
    
    print('lims: ', lims)
    print('t0: ', t0)

    while tdiff < lims:
        vll = int(tdiff)%rate
        # print('mo: {}'.format(vll))
        if vll == 0:
            print('the Ram usage: {}'.format(RamUsage()))
            # RamUsage()
            print("sec: {}".format(tdiff))
        tdiff = time.time() - t0

def get_my_profile(exeName, start=0, end=None):
    print('taking memory snapshot for {}...'.format(exeName))
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")
    if end is None:
        end = start + len(top_stats)
    for stat in top_stats[start:end]:
        if str().split(':')[0] == exeName:
            print(stat)
    return 0


def get_profile(start=0, end=None, verbose=False):
    if verbose:
        print('taking memory snapshot for ...')
    return tracemalloc.take_snapshot()

# uses tracemalloc to start a memory 
# usage trace
def start_trace(verbose=False):
    if verbose:
        print("starting trace....")
    tracemalloc.start()
