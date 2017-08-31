"""
Misc. useful functions that can be used at many places in the program.
"""

import subprocess as sp
import sys
import warnings
import re
import os
from datetime import datetime
import time
#import gevent
import threading

try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

def sys_write_flush(s):
    """ Writes and flushes without delay a text in the console """
    sys.stdout.write(s)
    sys.stdout.flush()

def verbose_print(verbose, s):
    """ Only prints s (with sys_write_flush) if verbose is True."""
    if verbose:
        sys_write_flush(s)

def subprocess_call(cmd, verbose=True, errorprint=True):
    #from multiprocessing import Process
    #print("\n... subprocess_call\n")
    """ Executes the given subprocess command."""

    verbose_print(verbose, "\n[Mo7amed3aly] Running:\n>>> " + " ".join(cmd))

    popen_params = {"stdout": sp.PIPE,"stderr": sp.PIPE,"stdin": DEVNULL}

    if os.name == "nt":
        popen_params["creationflags"] = 0x08000000

    proc = sp.Popen(cmd, **popen_params)
    out, err = proc.communicate() # proc.wait()
    toStr = bytes.decode(out)
    #print("\n... command successful.\n")
    #verbose_print(verbose, "\n... command successful.\n")

    """
    out, err = proc.communicate() # proc.wait()
    proc.stderr.close()

    if proc.returncode:
        verbose_print(errorprint, "\n[Mo7amed3aly] This command returned an error !")
        raise IOError(err.decode('utf8'))
    else:
        verbose_print(verbose, "\n... command successful.\n")


    #del proc

    from tools import *
    cmd = ['ls', '-l']
    out = subprocess_call(cmd)
    """
    return toStr

import requests
def startCalculating(numberOfstream,testkey,quality):
    requests.post("http://192.168.100.6:8000/api/startcalcul",data={"number":numberOfstream,"key":testkey,"quality":quality})

def ffmpeg_resize(video, output):
    cmd = ["ffmpeg", "-i", video]
    src480 = ['-strict', '-2', "-vf", "scale=480:trunc(ow/a/2)*2", output+'_480.mp4']
    cmd+=src480
    return cmd
from uuid import uuid4
def subbprocessCommand(cmd, verbose=False, errorprint=True):
    verbose_print(verbose, "\n[Mo7amed3aly] Running:\n>>> " + " ".join(cmd))

    popen_params = {"stdout": sp.PIPE,  "stderr": sp.PIPE,  "stdin": DEVNULL}
    proc = sp.Popen(cmd, **popen_params)
    out, err = proc.communicate()  # proc.wait()
    #output = subprocess.check_output(['ls','-l'])
    bytes.decode(out)
    return out

""""
import subprocess as sp
from subprocess import DEVNULL
cmd = 'snort -c /etc/snort/etc/snort.conf >> file4.txt 2>&1'
popen_params = {"stdout": sp.PIPE,  "stderr": sp.PIPE,  "stdin": DEVNULL}
proc = sp.Popen(cmd.split(), **popen_params)
proc.terminate()






"""
import os, signal, subprocess as sp, re, time, json, datetime
import psutil

def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output:
           mb= 300002347.946
    """

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return(r)


try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

def handler(signum, frame):
    print('Signal handler called with signal', signum)
    #raise OSError("Couldn't open device!")
def getBandWidth():

    start = datetime.datetime.now()
    startSnetio = psutil.net_io_counters()
    time.sleep(5)
    endSnetio = psutil.net_io_counters()
    end = datetime.datetime.now()

    bytes_sent = endSnetio.bytes_sent -startSnetio.bytes_sent
    bytes_recv = endSnetio.bytes_recv -startSnetio.bytes_recv
    packets_sent = endSnetio.packets_sent - startSnetio.packets_sent
    packets_recv = endSnetio.packets_recv - startSnetio.packets_recv
    testTiming = (end -start).total_seconds()
    bandwidthSent = bytes_sent/testTiming
    bandwidthRecv = bytes_recv/testTiming
    """print('start: '+start.strftime("%Y-%m-%d %H:%M:%S"))
    print('end: '+end.strftime("%Y-%m-%d %H:%M:%S"))
    print('bytes_sent: '+str(bytesto(bytes_sent, 'g'))+'Gb/s')
    print('bytes_recv: '+str(bytesto(bytes_recv, 'g'))+'Gb/s')
    print('packets_sent: '+str(packets_sent))
    print('packets_recv: '+str(packets_recv))
    print('bandwidthSent: '+str(bytesto(bandwidthSent, 'g'))+'Gb/s')
    print('bandwidthRecv: '+str(bytesto(bandwidthRecv, 'g'))+'Gb/s')
    """


def generateTestFile(bandWidth):
    fname = bandWidth + '_' + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.json'
    try:
        f = open(fname, 'w')
        f.writelines('{"test": []}')

        # f.writelines('http://aljazeera-eng-apple-live.adaptive.level3.net/apple/aljazeera/arabic/800.m3u8\n')
        f.close()
    except Exception as e:
        print('IOFile Exception:' + str(e))

    return fname

def snort(bandWidth):
    packetsPerSeconds =0
    popen_params = {"stdout": sp.PIPE, "stderr": sp.PIPE, "stdin": DEVNULL}
    cmd = 'snort -c /etc/snort/etc/snort.conf'
    proc = sp.Popen(cmd.split(), shell = True, **popen_params)
    time.sleep(5)
    #pid = sp.check_output(["pidof", "-s", 'snort'])
    pid = sp.check_output(["pidof",  'snort']).split()
    for p in pid:
        print('pid: '+str(p))
        #os.kill(int(p), signal.SIGKILL)
        signal.signal(signal.SIGALRM, handler)
        os.kill(int(p), signal.SIGKILL)
    out = proc.stderr.read()
    try:
        matchObj = re.search(r'(.*)kts(.*?) .*', bytes.decode(out))
        split = matchObj.group()
        packetsPerSeconds = int(split.split()[1])
    except Exception as e:
        print('Exception wile matchObj data: ' + str(e))

    try:
                        if packetsPerSeconds>0:
                            fname = generateTestFile(bandWidth)
                            f = open(fname, 'r')
                            data = json.load(f)
                            f.close()
                            f = open(fname, 'w')
                            data.append({
                                "bandWidth": bandWidth,
                                "packetsPerSeconds": packetsPerSeconds
                            })
                            json.dump(data, f)
                            f.close()
    except Exception as e:
                        print('Exception wile writing data: ' + str(e))


def fullTest(range=1):
    packetsPerSeconds =0
    popen_params = {"stdout": sp.PIPE, "stderr": sp.PIPE, "stdin": DEVNULL}
    cmd = 'snort -c /etc/snort/etc/snort.conf'
    proc = sp.Popen(cmd.split(), shell = True, **popen_params)

    start = datetime.datetime.now()
    startSnetio = psutil.net_io_counters()
    time.sleep(10)

    pid = sp.check_output(["pidof",  'snort']).split()
    for p in pid:
        print('pid: '+str(p))
        #os.kill(int(p), signal.SIGKILL)
        os.kill(int(p), signal.SIGTERM)


    endSnetio = psutil.net_io_counters()
    end = datetime.datetime.now()

    out = proc.stdout.read()
    err = proc.stderr.read()
    try:
            # print('Exception wile matchObj data: ' + str(e))
            matchObj = re.search(r'(.*)kts(.*?) .*', bytes.decode(err))
            split = matchObj.group()
            packetsPerSecondserr = int(split.split()[1])
            print('packetsPerSeconds err: ' + str(packetsPerSecondserr))
    except Exception as e:
            print('Exception2 wile matchObj data: ' + str(e))

    try:
        matchObj = re.search(r'(.*)kts(.*?) .*', bytes.decode(out))
        split = matchObj.group()
        packetsPerSeconds = int(split.split()[1])
        print('packetsPerSeconds: ' + str(packetsPerSeconds))
    except Exception as e:
        try:
            # print('Exception wile matchObj data: ' + str(e))
            matchObj = re.search(r'(.*)kts(.*?) .*', bytes.decode(err))
            split = matchObj.group()
            packetsPerSeconds = int(split.split()[1])
            #print('packetsPerSeconds err: ' + str(packetsPerSeconds))
        except Exception as e:
            print('Exception2 wile matchObj data: ' + str(e))

    bytes_sent = endSnetio.bytes_sent - startSnetio.bytes_sent
    bytes_recv = endSnetio.bytes_recv - startSnetio.bytes_recv
    packets_sent = endSnetio.packets_sent - startSnetio.packets_sent
    packets_recv = endSnetio.packets_recv - startSnetio.packets_recv
    testTiming = (end - start).total_seconds()
    bandwidthSent = bytes_sent / testTiming
    bandwidthRecv = bytes_recv / testTiming


    try:
                        if packetsPerSeconds>0:
                            fname = generateTestFile(int(bandwidthRecv))
                            f = open(fname, 'r')
                            data = json.load(f)
                            f.close()
                            f = open(fname, 'w')
                            data.append({
                                "bandWidth": bandwidthRecv,
                                "bandwidthRecv": bandwidthRecv,
                                "bandwidthSent": bandwidthSent,
                                "testTiming": testTiming,
                                "packets_recv": packets_recv,
                                "packets_sent": packets_sent,
                                "packetsPerSeconds": packetsPerSeconds
                            })
                            json.dump(data, f)
                            f.close()
    except Exception as e:
                        print('Exception wile writing data: ' + str(e))

    print('Snort Test Num: '+str(range))
    print('====================================================================== ')

    print('     start: ' + start.strftime("%Y-%m-%d %H:%M:%S"))
    print('     end: ' + end.strftime("%Y-%m-%d %H:%M:%S"))
    print('     bytes_sent: ' + str(bytesto(bytes_sent, 'g')) + 'Gb/s')
    print('     bytes_recv: ' + str(bytesto(bytes_recv, 'g')) + 'Gb/s')
    print('     packets_sent: ' + str(packets_sent))
    print('     packets_recv: ' + str(packets_recv))
    print('     bandwidthSent: ' + str(bytesto(bandwidthSent, 'g')) + 'Gb/s')
    print('     bandwidthRecv: ' + str(bytesto(bandwidthRecv, 'g')) + 'Gb/s')
    print('     packetsPerSeconds: ' + str(packetsPerSeconds))

def floatToString(f):
    s = s = str(f).split('.')
    ss = s[0] + ',' + s[1]

def testSnort(bandWidth):
    print('Snort Test By Mohamed Aly')
    fname = generateTestFile(int(bandWidth))
    for i in range(5):
        snort(i)


if __name__ == '__main__':
    testSnort(3)