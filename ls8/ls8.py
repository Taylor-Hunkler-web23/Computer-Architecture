#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

filename=sys.argv[1]

if len(sys.argv) != 2:
    print("usage: simple.py filename")
    sys.exit(1)


cpu.load(filename)
cpu.run()