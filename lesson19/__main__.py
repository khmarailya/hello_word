import argparse
import json
import os
import time
from collections import defaultdict
from glob import glob
from typing import Optional, List
from lesson19.lib import Matcher, Arguments


parser = argparse.ArgumentParser(description='Process access.log')
parser.add_argument(
    '-f', dest='file', action='store', default='')
parser.add_argument(
    '-c', dest='cnt', action='store', default='0', type=int)
parser.add_argument(
    '--top_long_cnt', dest='top_long_cnt', action='store', default='3', type=int)
parser.add_argument(
    '--top_ip_cnt', dest='top_ip_cnt', action='store', default='3', type=int)

args = parser.parse_args()
top_long_cnt = args.top_long_cnt
top_ip_cnt = args.top_ip_cnt
fn = args.file or os.path.dirname(os.path.realpath(__file__))
max_lines = args.cnt

matcher = Matcher()
log_list = glob(fn + '/**/*.log', recursive=True) if os.path.isdir(fn) else [fn] if os.path.isfile(fn) else []
for fn in log_list:
    fn = fn.replace('\\', '/')
    ip_req_cnt = defaultdict(int)
    req_cnt = defaultdict(int)
    req_top_long: List[Optional[Arguments]] = [None] * top_long_cnt
    bad_lines = []

    with open(fn) as file:
        idx = 0
        big_idx = 0
        t = time.time()
        for line in file:
            if max_lines and idx >= max_lines:
                break

            arguments = matcher.match(line)
            if not arguments:
                bad_lines.append(line)
                continue

            idx += 1
            big_idx += 1
            if big_idx >= 1000:
                print(f'\rWork in progress... {fn} - {idx}', end='')
                big_idx = 0

            if arguments.ip is not None:
                if arguments.r_type is not None:
                    ip_req_cnt[arguments.ip] += 1
                    req_cnt[arguments.r_type] += 1

                if arguments.lng is not None:
                    for i, top_arguments in enumerate(req_top_long):
                        if top_arguments is None:
                            need_re_calc = False
                        elif arguments.lng > top_arguments.lng:
                            need_re_calc = True
                        else:
                            continue

                        req_top_long[i] = arguments
                        if need_re_calc:
                            for j in range(i + 2, top_long_cnt):
                                req_top_long[j] = req_top_long[j - 1]
                        break
    res = {
        'file': fn,
        'cnt_req': req_cnt,
        'top_ip_req': {
            k: v for k, v in sorted(ip_req_cnt.items(), key=lambda x: x[1], reverse=True)[:top_ip_cnt]
        },
        'top_long_req': [
            {
                'type': args.r_type,
                'url': args.url,
                'ip': args.ip,
                'long': args.lng,
                'tm': args.tm,
            }
            for i, args in enumerate(req_top_long, start=1) if args
        ],
        'lines': idx,
        'time': round(time.time() - t, 1),
        'errors': [e.to_dict() for e in list(matcher.errors)[:3]],
        'bad_lines': bad_lines[:3],
    }
    print(f'\r{fn} - {idx}')
    res_fn = os.path.splitext(fn)[0] + '.json'
    with open(res_fn, 'w') as res_file:
        json.dump(res, res_file, indent=4)
