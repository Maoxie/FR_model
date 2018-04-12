#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from relap import run_relap, import_data


def main(argv='-i'):
    if argv=='-i':
        run_relap.run_new_model()
    elif argv=='-s':
        run_relap.run_strip()
        import_data.stripf_preprocess()
        

if __name__=="__main__":
    try:
        argv = sys.argv[1]
        print('run main with argv=="{}"'.format(argv))
        main(argv)
    except IndexError:
        print('run main with default argv')
        main()
        

