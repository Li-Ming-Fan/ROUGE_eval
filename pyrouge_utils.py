# -*- coding: utf-8 -*-
"""
https://github.com/Li-Ming-Fan/ROUGE_eval

"""

import os
import shutil
import time
import re

import logging
from pyrouge import Rouge155


import argparse
def parse_args():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser('pyrouge_eval')
    parser.add_argument('--data', type=str, default = 'data_result',
                        help = 'specify directory where data are stored')
    return parser.parse_args()

#
default_rouge_score = {'rouge_1_recall': 0.0, 'rouge_1_recall_cb': 0.0, 'rouge_1_recall_ce': 0.0,
               'rouge_1_precision': 0.0, 'rouge_1_precision_cb': 0.0, 'rouge_1_precision_ce': 0.0,
               'rouge_1_f_score': 0.0, 'rouge_1_f_score_cb': 0.0, 'rouge_1_f_score_ce': 0.0,
               'rouge_2_recall': 0.0, 'rouge_2_recall_cb': 0.0, 'rouge_2_recall_ce': 0.0,
               'rouge_2_precision': 0.0, 'rouge_2_precision_cb': 0.0, 'rouge_2_precision_ce': 0.0,
               'rouge_2_f_score': 0.0, 'rouge_2_f_score_cb': 0.0, 'rouge_2_f_score_ce': 0.0,
               'rouge_3_recall': 0.0, 'rouge_3_recall_cb': 0.0, 'rouge_3_recall_ce': 0.0,
               'rouge_3_precision': 0.0, 'rouge_3_precision_cb': 0.0, 'rouge_3_precision_ce': 0.6,
               'rouge_3_f_score': 0.0, 'rouge_3_f_score_cb': 0.0, 'rouge_3_f_score_ce': 0.0,
               'rouge_4_recall': 0.0, 'rouge_4_recall_cb': 0.0, 'rouge_4_recall_ce': 0.0,
               'rouge_4_precision': 0.0, 'rouge_4_precision_cb': 0.0, 'rouge_4_precision_ce': 0.0,
               'rouge_4_f_score': 0.0, 'rouge_4_f_score_cb': 0.0, 'rouge_4_f_score_ce': 0.0,
               'rouge_l_recall': 0.0, 'rouge_l_recall_cb': 0.0, 'rouge_l_recall_ce': 0.0,
               'rouge_l_precision': 0.0, 'rouge_l_precision_cb': 0.0, 'rouge_l_precision_ce': 0.0,
               'rouge_l_f_score': 0.0, 'rouge_l_f_score_cb': 0.0, 'rouge_l_f_score_ce': 0.0,
               'rouge_w_1.2_recall': 0.0, 'rouge_w_1.2_recall_cb': 0.0, 'rouge_w_1.2_recall_ce': 0.0, 
               'rouge_w_1.2_precision': 0.0, 'rouge_w_1.2_precision_cb': 0.0, 'rouge_w_1.2_precision_ce': 0.0,
               'rouge_w_1.2_f_score': 0.0, 'rouge_w_1.2_f_score_cb': 0.0, 'rouge_w_1.2_f_score_ce': 0.0,
               'rouge_s*_recall': 0.0, 'rouge_s*_recall_cb': 0.0, 'rouge_s*_recall_ce': 0.0, 
               'rouge_s*_precision': 0.0, 'rouge_s*_precision_cb': 0.0, 'rouge_s*_precision_ce': 0.0,
               'rouge_s*_f_score': 0.0, 'rouge_s*_f_score_cb': 0.0, 'rouge_s*_f_score_ce': 0.0,
               'rouge_su*_recall': 0.0, 'rouge_su*_recall_cb': 0.0, 'rouge_su*_recall_ce': 0.0,
               'rouge_su*_precision': 0.0, 'rouge_su*_precision_cb': 0.0, 'rouge_su*_precision_ce': 0.0,
               'rouge_su*_f_score': 0.0, 'rouge_su*_f_score_cb': 0.0, 'rouge_su*_f_score_ce': 0.0}
#

#
def run_pyrouge_eval(dir_data=None, model_dir=None, system_dir=None, 
                     model_filename_pattern = "example.[A-Z].#ID#.txt",
                     system_filename_pattern = "example.(\d+).txt"):
    """
    """
    if model_dir is None:
        model_dir = os.path.join(dir_data, "model")
    if system_dir is None:
        system_dir = os.path.join(dir_data, "reference")
    #
    rg = Rouge155()
    rg.model_dir = model_dir
    rg.system_dir = system_dir
    #
    rg.model_filename_pattern = model_filename_pattern
    rg.system_filename_pattern = system_filename_pattern
    #
    # rg.model_filename_pattern = "#ID#_result.txt"
    # rg.system_filename_pattern = "(\d+)_reference.txt" 
    #
    # rg.model_filename_pattern = "example.[A-Z].#ID#.txt"
    # rg.system_filename_pattern = "example.(\d+).txt"
    #
    logging.getLogger('global').setLevel(logging.WARNING) # silence pyrouge logging
    output = rg.convert_and_evaluate()
    output_dict = rg.output_to_dict(output)
    #
    return output_dict, output

#
def write_rouge_results(results_dict, file_path):
    """
    """
    results_filtered = {}
    results_filtered["rouge_1_recall"] = results_dict["rouge_1_recall"]
    results_filtered["rouge_1_precision"] = results_dict["rouge_1_precision"]
    results_filtered["rouge_1_f_score"] = results_dict["rouge_1_f_score"]
    #
    results_filtered["rouge_2_recall"] = results_dict["rouge_2_recall"]
    results_filtered["rouge_2_precision"] = results_dict["rouge_2_precision"]
    results_filtered["rouge_2_f_score"] = results_dict["rouge_2_f_score"]
    #
    results_filtered["rouge_4_recall"] = results_dict["rouge_4_recall"]
    results_filtered["rouge_4_precision"] = results_dict["rouge_4_precision"]
    results_filtered["rouge_4_f_score"] = results_dict["rouge_4_f_score"]
    #
    results_filtered["rouge_l_recall"] = results_dict["rouge_l_recall"]
    results_filtered["rouge_l_precision"] = results_dict["rouge_l_precision"]
    results_filtered["rouge_l_f_score"] = results_dict["rouge_l_f_score"]
    #
    with open(file_path, "w") as fp:
        json.dump(results_filtered, fp)

#
def make_html_safe(s):
    """ Replace any angled brackets in string s to avoid interfering with HTML attention visualizer.
    
        pyrouge calls a perl script that puts the data into HTML files.
        Therefore we need to make our output HTML safe.
    """
    s.replace("<", "&lt;")
    s.replace(">", "&gt;")
    return s

#
def write_data_for_eval(data_dict, dir_data=None,
                        model_dir = None, system_dir = None,
                        model_filename_format = "example.A.%d.txt",
                        system_filename_format = "example.%d.txt",
                        flag_make_html_safe = True):
    """ data_dict: a map from example_id to (result, reference) 
    """
    if model_dir is None:
        model_dir = os.path.join(dir_data, "model")
    if system_dir is None:
        system_dir = os.path.join(dir_data, "reference")
    
    # remove the existing dir
    if os.path.exists(model_dir):
        shutil.rmtree(model_dir)

    if os.path.exists(system_dir):
        shutil.rmtree(system_dir)
    
    time.sleep(3)
    
    # make new dir
    if dir_data is not None and not os.path.exists(dir_data):
        os.mkdir(dir_data)
    #
    os.mkdir(model_dir)
    os.mkdir(system_dir)
    #

    for key in data_dict.keys():
        #
        result, ref = data_dict[key]   # (result, reference)
        #
        if flag_make_html_safe:
            result = make_html_safe(result)
            ref = make_html_safe(ref)
        #
        # file_result = os.path.join(model_dir, "example.A.%d.txt" % key)
        # file_ref = os.path.join(system_dir, "example.%d.txt" % key)
        #
        file_result = os.path.join(model_dir, model_filename_format % key)
        file_ref = os.path.join(system_dir, system_filename_format % key)
        #
        with open(file_ref, 'w', encoding = 'utf-8') as fp:
            fp.write(ref)
        #
        with open(file_result, 'w', encoding = 'utf-8') as fp:
            fp.write(result)
        #
    #

#
def get_files_with_ext(path, str_ext):
    """
    """
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)  
        if file_path.endswith(str_ext):  
            file_list.append(file_path)
            #print(file_path)
    return file_list
    #
    
if __name__ == '__main__':
    
    args = parse_args()
    dir_data = args.data

    # dir_data = os.path.abspath("./data_result")
    # print(dir_data)

    try:
        output_dict, output = run_pyrouge_eval(dir_data=dir_data)
        print(output)
    except BaseException:
        print()
        print('rouge score cannot be calculated, data NOT HTML-safe.')
    #
    