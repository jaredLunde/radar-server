#!/usr/bin/python3 -S
# -*- coding: utf-8 -*-
import os
import re
import sys
import glob
import inspect
import importlib.util
from os.path import dirname, basename, isfile
from vital.debug import line, bold, colorize, get_terminal_width


cd = os.path.dirname(os.path.abspath(__file__))
path = cd.split('radar_server')[0] + 'radar_server'
sys.path.insert(0, path)
rows, columns = os.popen('stty size', 'r').read().split()


defsub = re.compile('''def (.*?):\n''')


def main():
    modules = glob.glob(dirname(__file__) + "/*.py")
    benches = [
        (f, basename(f)[:-3])
        for f in modules if isfile(f) and not f.endswith('__init__.py')
    ]

    for path, name in sorted(benches):
        spec = importlib.util.spec_from_file_location(name, path)
        bench = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bench)

        for attr in dir(bench):
            if attr.startswith('bench_'):
                print()
                print(colorize(attr, 'green'), colorize(f'[{path}]', 'purple'), '\n')
                fn = getattr(bench, attr)
                print(
                    '\033[0;100m'
                    + ''.join(str(' ') for x in range(int(columns)))
                    + defsub.sub('', ''.join(inspect.getsource(fn)))
                    + '\033[1;m'
                )
                print()
                fn()
                print()
                line()


if __name__ == '__main__':
    main()