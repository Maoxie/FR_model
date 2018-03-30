#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
from pathlib import Path



def run_new_model(root=r".\relap_bin"):
    # delete outdta for a "new" question before running
    root_path = Path(os.path.abspath(root))
    relap_bin_exe = root_path / 'relap5.exe'      # main relap5 executatble file

    i_file = root_path / 'indta'
    o_file = root_path / 'outdta'
    r_file = root_path / 'rstplt'
    for filepath in [o_file, r_file]:
        if filepath.exists():
            opt = input(u"是否删除已有的{}? y/n: ".format(filepath.name))
            if opt=="" or opt.lower()=="y":
                filepath.replace(o_file.with_name('{}.old'.format(filepath.name)))
                print("{0} has been renamed as {0}.old.".format(filepath.name))

    run_options = {
        '-i': '"{}"'.format(i_file),
        '-o': '"{}"'.format(o_file),
        '-r': '"{}"'.format(r_file),
    }
    options_str = ' '.join([ key +' '+ value for key,value in run_options.items()])
    call_str = '{relap} {option}'.format(relap=relap_bin_exe, option=options_str)
    print("----start run new model----")
    print("-->> {}".format(call_str))
    os.chdir(root_path)
    subprocess.call(call_str)
    print("----complete model----")

def run_strip(root=r".\relap_bin"):
    root_path = Path(root)
    relap_bin_exe = root_path / 'relap5.exe'      # main relap5 executatble file

    i_file = root_path / 'strip'
    o_file = root_path / 'outdta'
    r_file = root_path / 'rstplt'
    run_options = {
        'i': "'{}'".format(i_file),
        'o': "'{}'".format(o_file),
        'r': "'{}'".format(r_file),
    }
    options_str = '-i {i} -o {o} -r {r}'.format(
        i=run_options['i'], 
        o=run_options['o'], 
        r=run_options['r'],
    )

    print("----start strip----")
    subprocess.call('{relap} {option}'.format(relap=relap_bin_exe, option=options_str))
    print("----complete strip----")

