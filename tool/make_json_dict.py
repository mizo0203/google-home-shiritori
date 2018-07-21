#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

"""
ipadicをjsonの辞書ファイルに変換するスクリプト
第一引数:読込ファイル
第二引数:出力ファイル
"""

import json
import sys

with open(sys.argv[1]) as f:
    inputData = {}
    for line in f:
        line = line.replace('(', '').replace(')', '').rstrip().split(' ')
        org = line[4]
        keys = line[7].replace('{', '').replace('}', '').split('/')
        for key in keys:
            if key in inputData:
                inputData[key].append(org)
            else:
                inputData[key] = [org]

outputData = []
for key in sorted(inputData.keys()):
    data = {}
    if key == '':
        sys.stderr.write('key is null\n')
        continue
    data['key'] = key
    data['org'] = inputData[key]
    data['first'] = key[0]
    data['end'] = key[-1]
    outputData.append(data)

with open(sys.argv[2], 'w') as wf:
    json.dump(outputData, wf, indent=2)
