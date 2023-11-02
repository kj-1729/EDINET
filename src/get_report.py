# -*- encoding:utf-8 -*-

import sys
import os
import urllib.request
import urllib.error
import json
import re

import datetime
import time

def get_edinetCode_dict(bank_master_path):
    edinetCode_dict = {}
    with open(bank_master_path, 'r') as f:
        line = f.readline()
        for line in f:
            data = line[:-1].split('\t')
            edinetCode_dict[data[0]] = 1

    return edinetCode_dict

def main():
    if len(sys.argv) < 8:
        sys.stderr.write('Usage: python get_list.py ymd_from ymd_to bank_master_path list_dir list_fname output_dir subscription_key\n')
        sys.exit(1)

    edinet_url = 'https://api.edinet-fsa.go.jp/api/v2/documents'
    
    ymd_from = sys.argv[1]
    ymd_to = sys.argv[2]
    this_date = datetime.date(int(ymd_from[:4]), int(ymd_from[4:6]), int(ymd_from[6:]))
    date_to = datetime.date(int(ymd_to[:4]), int(ymd_to[4:6]), int(ymd_to[6:]))

    bank_master_path = sys.argv[3]
    list_dir = sys.argv[4]
    list_fname = sys.argv[5]
    output_dir = sys.argv[6]
    subscription_key = sys.argv[7]

    edinetCode_dict = get_edinetCode_dict(bank_master_path)

    print('date\tseqno\tedinetCode\tJCN\tissuerEdinetCode\tdocID\tfilerName\tdocDescription')

    while this_date <= date_to:
        this_date_str = this_date.strftime('%Y-%m-%d')
        list_path = os.path.join(list_dir, list_fname + '_' + this_date_str + '.json')

        with open(list_path, 'r') as fp_in:
            list_data = json.load(fp_in)
            results = list_data['results']
            
            loop = 0
            for doc in results:
                docID = doc['docID']
                edinetCode = doc['edinetCode']
                
                docDescription = str(doc['docDescription'])
                m1 = re.search('有価証券報告書', docDescription)
                m2 = re.search('内国信託受益証券', docDescription)

                if edinetCode in edinetCode_dict and m1 is not None and m2 is None:
                    url = f'{edinet_url}/{docID}?type=5&Subscription-Key={subscription_key}'
                    print(this_date, loop, doc['edinetCode'], doc['JCN'], doc['issuerEdinetCode'], doc['docID'], doc['filerName'], doc['docDescription'], sep='\t')

                    try:
                        with urllib.request.urlopen(url) as res:
                            content = res.read()
                        
                        output_path = os.path.join(output_dir, docID + '.zip')
                        with open(output_path, 'wb') as fp_out:
                            fp_out.write(content)
                    except urllib.error.HTTPError as e:
                        if e.code >= 400:
                            sys.stderr.write(e.reason+'\n')
                        else:
                            raise e

                    loop += 1
                    time.sleep(1)
        this_date += datetime.timedelta(days=1)
        
    sys.exit(0)

if __name__ == '__main__':
    main()
