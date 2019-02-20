# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 01:19:25 2018

@author: limingfan
"""

"""
https://github.com/Li-Ming-Fan/ROUGE_eval

"""

import os
import shutil
import time
import re

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
def run_pyrouge_eval(dir_data):
    """
    """
    system_dir = os.path.join(dir_data, "reference")
    model_dir = os.path.join(dir_data, "model")
    
    rg = Rouge155()
    rg.system_dir = system_dir
    rg.model_dir = model_dir
    rg.system_filename_pattern = 'example.(\d+).txt'
    rg.model_filename_pattern = 'example.[A-Z].#ID#.txt'
    
    output = rg.convert_and_evaluate()
    # print(output)
    output_dict = rg.output_to_dict(output)
    # print(output_dict)
    return output_dict, output

def write_data_for_eval(data_dict, dir_data):
    """ data_dict: a map from example_id to (result, reference) 
    """    
    system_dir = os.path.join(dir_data, "reference")
    model_dir = os.path.join(dir_data, "model")
    
    # remove the existing dir
    if os.path.exists(dir_data):
        shutil.rmtree(dir_data)
        time.sleep(3)
    
    # make new dir
    os.mkdir(dir_data)
    os.mkdir(system_dir)
    os.mkdir(model_dir)
    
    for key in data_dict.keys():
        #
        result, ref = data_dict[key]   # (result, reference) 
        #
        file_result = os.path.join(model_dir, "example.A.%d.txt" % key)
        file_ref = os.path.join(system_dir, "example.%d.txt" % key)
        #
        with open(file_ref, 'w', encoding = 'utf-8') as fp:
            fp.write(ref)
        #
        with open(file_result, 'w', encoding = 'utf-8') as fp:
            fp.write(result)
        #
    #

#
def check_conformity(text):
    #
    pattern = re.compile('<')
    match = pattern.findall(text)
    if match:  # containing character: '<'
        return False
    #
    pattern = re.compile('[0-9a-zA-Z]+')
    match = pattern.findall(text)
    if match:
        return True
    else: # not containing alphabet or numerics
        return False

def check_data_for_eval(data_dict):
    """ data_dict: a map from example_id to (result, reference) 
    """
    inconformity_list = []
    for key in data_dict.keys():
        #
        result, ref = data_dict[key]   # (result, reference) 
        #
        if check_conformity(result):
            continue
        else:
            inconformity_list.append(key)
        #
        
    return inconformity_list

#
def get_files_with_ext(path, str_ext):
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)  
        if file_path.endswith(str_ext):  
            file_list.append(file_path)
            #print(file_path)
    return file_list
    #
    
def check_data_for_eval_with_dir(data_dir):
    """ data_dir: 
    """
    model_dir = os.path.join(dir_data, "model")
    list_files = get_files_with_ext(model_dir, 'txt')
    #
    inconformity_list = []
    for item in list_files:
        #
        with open(item, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
        #
        result = lines[0].strip()
        #
        if check_conformity(result):
            continue
        else:
            inconformity_list.append( (item, result) )
        #
        
    return inconformity_list
    #
      
    
if __name__ == '__main__':
    
    args = parse_args()
    dir_data = args.data
    
    #
    inconformity_list = check_data_for_eval_with_dir(dir_data)
    #
    print(inconformity_list)
    len_inconformity_list = len(inconformity_list)
    print("inconformity_list: %d" % len_inconformity_list)
    #
    assert len_inconformity_list == 0, "inconformity_list: %d" % len_inconformity_list
    #
    try:
        output_dict, output = run_pyrouge_eval(dir_data)
        print(output)
    except BaseException:
        print()
        print('rouge score CANNOT be calculated, there are something wrong in the results.')
    #
    