#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
from pathlib import Path



def run_new_model(root=r".\model"):
    # delete outdta for a "new" question before running
    root_path = Path(os.path.abspath(root))
    relap_bin_path = root_path.parent / 'relap_bin'
    relap_bin_exe = relap_bin_path / 'relap5.exe'      # main relap5 executatble file

    i_file = root_path / 'indta'
    o_file = root_path / 'outdta'
    r_file = root_path / 'rstplt'
    for filepath in [o_file, r_file]:
        __remove_exist_file(filepath)

    run_options = {
        '-i': '"{}"'.format(i_file),
        '-o': '"{}"'.format(o_file),
        '-r': '"{}"'.format(r_file),
    }
    options_str = ' '.join([ key +' '+ value for key,value in run_options.items()])
    call_str = '{relap} {option}'.format(relap=relap_bin_exe, option=options_str)
    print("----start run new model----")
    print("-->> {}".format(call_str))
    os.chdir(relap_bin_path)
    subprocess.call(call_str)
    print("----complete model----")


def run_strip(root=r".\model"):
    root_path = Path(os.path.abspath(root))
    relap_bin_path = root_path.parent / 'relap_bin'
    relap_bin_exe = relap_bin_path / 'relap5.exe'      # main relap5 executatble file

    i_file = root_path / 'strip'
    o_file = root_path / 'outdta'
    r_file = root_path / 'rstplt'
    sf_file = root_path / 'stripf'
    for filepath in [sf_file, o_file]:
        __remove_exist_file(filepath)
    run_options = {
        '-i': '"{}"'.format(i_file),
        '-o': '"{}"'.format(o_file),
        '-r': '"{}"'.format(r_file),
        '-s': '"{}"'.format(sf_file),
    }
    options_str = ' '.join([ key +' '+ value for key,value in run_options.items()])
    call_str = '{relap} {option}'.format(relap=relap_bin_exe.name, option=options_str)
    print("----start strip----")
    print("-->> {}".format(call_str))
    os.chdir(relap_bin_path)
    subprocess.call(call_str)
    print("----complete strip----")


def __remove_exist_file(filepath):
    filepath = Path(filepath)
    if filepath.exists():
        opt = input(u"是否删除已有的{}? y/n: ".format(filepath.name))
        if opt=="" or opt.lower()=="y":
            filepath.replace(filepath.with_name('{}.old'.format(filepath.name)))
            print("{0} has been renamed as {0}.old.".format(filepath.name))


