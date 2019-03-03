#!/usr/bin/python3 -S
# -*- coding: utf-8 -*-
import os
import sys


cd = os.path.dirname(os.path.abspath(__file__))
path = cd.split('radar_server_legacy')[0] + 'radar_server_legacy'
sys.path.insert(0, path)
