#!/usr/bin/python3 -S
# -*- coding: utf-8 -*-
import os
import sys


cd = os.path.dirname(os.path.abspath(__file__))
path = cd.split('radar_server')[0] + 'radar_server'
sys.path.insert(0, path)


if __name__ == '__main__':
    # Unit test
    from tests import configure
    configure.setup()
    configure.run_discovered(cd)
    configure.cleanup()
