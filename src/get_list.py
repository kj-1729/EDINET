import sys
import os
import urllib.request
import urllib.error

import datetime
import time

def main():
    if len(sys.argv) < 6:
        sys.stderr.write('Usage: python get_list.py ymd_from ymd_to output_dir output_fname subscription_key\n')
        sys.exit(1)

    edinet_url = 'https://api.edinet-fsa.go.jp/api/v2/documents.json'
    
    ymd_from = sys.argv[1]
    ymd_to = sys.argv[2]
    this_date = datetime.date(int(ymd_from[:4]), int(ymd_from[4:6]), int(ymd_from[6:]))
    date_to = datetime.date(int(ymd_to[:4]), int(ymd_to[4:6]), int(ymd_to[6:]))

    output_dir = sys.argv[3]
    output_fname = sys.argv[4]
    subscription_key = sys.argv[5]
    
    while this_date <= date_to:
        url = f'{edinet_url}?date={this_date}&type=2&Subscription-Key={subscription_key}'
        print(this_date, url)

        try:
            with urllib.request.urlopen(url) as res:
                content = res.read().decode('utf-8')
            this_date_str = this_date.strftime('%Y-%m-%d')

            output_path = os.path.join(output_dir, output_fname + '_' + this_date_str + '.json')
            with open(output_path, 'w') as fp:
                fp.write(content)
        except urllib.error.HTTPError as e:
            if e.code >= 400:
                print(e.reason)
            else:
                raise e

        time.sleep(1)

        this_date += datetime.timedelta(days=1)

if __name__ == '__main__':
    main()
    
