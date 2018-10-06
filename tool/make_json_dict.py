#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

"""
ipadicをjsonの辞書ファイルに変換するスクリプト
第一引数:読込ファイル
第二引数:出力ファイル
"""

import json
import sys

LOWER_CASE = {u'ァ': u'ア', u'ィ': u'イ', u'ゥ': u'ウ', u'ェ': u'エ', u'ォ': u'オ',
              u'ャ': u'ヤ', u'ュ': u'ユ', u'ョ': u'ヨ', u'ヮ': u'ワ',
              u'ッ': u'ツ',
              }

CONVERSION_TABLE = {u'ヂ': u'ジ', u'ヅ': u'ズ', }

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
    if key[-1] == u'ー':
        data['end'] = key[-2]
    else:
        data['end'] = key[-1]
    if data['end'] in LOWER_CASE:
        data['end'] = LOWER_CASE[data['end']]
    if data['first'] in CONVERSION_TABLE:
        data['first'] = CONVERSION_TABLE[data['first']]
    if data['end'] in CONVERSION_TABLE:
        data['end'] = CONVERSION_TABLE[data['end']]
    outputData.append(data)

with open(sys.argv[2], 'w') as wf:
    json.dump(outputData, wf, indent=2)
