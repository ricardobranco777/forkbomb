#!/usr/bin/env python
"""
See how many processes we can create
"""

import os
import signal


def fork_bomb():
    """
    Fork bomb
    """
    pids = 0
    # Reset signal handler for SIGTERM
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    # Fork and create as many children as we can
    while True:
        try:
            pid = os.fork()
        except OSError:
            break
        if pid == 0:
            signal.pause()
        pids += 1
    # Create our own process group so we can kill 'em all at once
    os.setpgid(0, 0)
    # Kill 'em all without killing ourselves
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    os.killpg(os.getpgid(0), signal.SIGTERM)
    return pids


print(fork_bomb())
