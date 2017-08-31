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


def subbprocessCommand(cmd, verbose=True, errorprint=True):
    verbose_print(verbose, "\n[Mo7amed3aly] Running:\n>>> " + " ".join(cmd))
    print('\n end of command')

    popen_params = {"stdout": sp.PIPE,  "stderr": sp.PIPE,  "stdin": DEVNULL}
    proc = sp.Popen(cmd, **popen_params)
    out, err = proc.communicate()  # proc.wait()
    #output = subprocess.check_output(['ls','-l'])
    bytes.decode(out)
    return out


