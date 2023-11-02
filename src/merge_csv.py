# -*- encoding:utf-8 -*-

import sys
import zipfile
import csv

import json
import re

import datetime
import time
import os

def main():
    if len(sys.argv) < 4:
        sys.stderr.write('Usage: python get_list.py element_id_master_path report_list_path docs_dir\n')
        sys.exit(1)

    contextID_list = ['CurrentYearDuration','CurrentYearDuration_NonConsolidatedMember','CurrentYearInstant','CurrentYearInstant_NonConsolidatedMember'] 

    element_id_master_path = sys.argv[1]
    report_list_path = sys.argv[2]
    docs_dir = sys.argv[3]

    elementID_dict = {}
    with open(element_id_master_path, 'r') as f:
        line = f.readline()
        for line in f:
            data = line[:-1].split('\t')
            elementID_dict[data[1]] = 1
            
    loop = 0
    with open(report_list_path, 'r') as f_list:
        header = f_list.readline()
        for line in f_list:
            data1 = line[:-1].split('\t')
            zip_path = os.path.join(docs_dir, data1[5] + '.zip')
            sys.stderr.write('Process ' + zip_path + '\n')

            try:
                with zipfile.ZipFile(zip_path) as fz:
                    for f in fz.namelist():
                        m = re.search('asr.*\.csv', f)
                        if m is not None:
                            fz.extract(f)

                            with open(f, 'r', encoding='utf-16') as f_rep:
                                reader = csv.reader(f_rep, delimiter='\t')
                                for data2 in reader:
                                    if loop == 0:
                                        print('edinetCode', 'docID', '\t'.join(data2), sep='\t')
                                    elif data2[0] in elementID_dict and data2[3][:2] == '当期' and data2[2] in contextID_list:
                                        print(data1[2], data1[5], '\t'.join(data2), sep='\t')
                                    loop += 1
            except:
                sys.stderr.write('Error: ' + data1[5]+'\n')

if __name__ == '__main__':
    main()

