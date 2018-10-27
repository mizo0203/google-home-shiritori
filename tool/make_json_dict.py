#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

"""
ipadicをjsonの辞書ファイルに変換するスクリプト
第一引数:読込ファイル
第二引数:出力ファイル
"""

import argparse
import json
import sys
import csv

LOWER_CASE = {u'ァ': u'ア', u'ィ': u'イ', u'ゥ': u'ウ', u'ェ': u'エ', u'ォ': u'オ',
              u'ャ': u'ヤ', u'ュ': u'ユ', u'ョ': u'ヨ', u'ヮ': u'ワ',
              u'ッ': u'ツ',
              }

CONVERSION_TABLE = {u'ヂ': u'ジ', u'ヅ': u'ズ', }

VOICED_SOUND_MARK = {u'ヴ': u'ウ',
                     u'ガ': u'カ', u'ギ': u'キ', u'グ': u'ク', u'ゲ': u'ケ', u'ゴ': u'コ',
                     u'ザ': u'サ', u'ジ': u'シ', u'ズ': u'ス', u'ゼ': u'セ', u'ゾ': u'ソ',
                     u'ダ': u'タ', u'ヂ': u'チ', u'ヅ': u'ツ', u'デ': u'テ', u'ド': u'ト',
                     u'バ': u'ハ', u'ビ': u'ヒ', u'ブ': u'フ', u'ベ': u'ヘ', u'ボ': u'ホ',
                     u'パ': u'ハ', u'ピ': u'ヒ', u'プ': u'フ', u'ペ': u'ヘ', u'ポ': u'ホ',
                     }

POKEMON_TABLE = {u'X': u'エックス', u'Y': u'ワイ', u'Z': u'ゼット',
                 u'2': u'ツー',
                 u'♂': u'オス', u'♀': u'メス',
                 }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=u'JSON辞書作成スクリプト')
    parser.add_argument('-n', '--naistdic', action='store_true', help=u'NAIST Japanese Dictionaryの読み込み時に使用')
    parser.add_argument('-p', '--pokemon', action='store_true', help=u'kotofurumiya/pokemon_dataの読み込み時に使用')
    parser.add_argument('-s', '--station', action='store_true', help=u'geonlp_japan_stationの読み込み時に使用')
    parser.add_argument('inputfile', type=argparse.FileType('r'))
    parser.add_argument('outputfile', type=argparse.FileType('w'))
    args = parser.parse_args()

    with args.inputfile as f:
        inputData = {}
        if args.naistdic:
            for line in f:
                line = line.replace('(', '').replace(')', '').rstrip().split(' ')
                org = line[4]
                keys = line[7].replace('{', '').replace('}', '').split('/')
                for key in keys:
                    if key in inputData:
                        inputData[key].append(org)
                    else:
                        inputData[key] = [org]
        elif args.pokemon:
            obj = json.load(f)
            for record in obj:
                name = record['name']
                yomi = u''
                for v in name:
                    if v in POKEMON_TABLE:
                        yomi += POKEMON_TABLE[v]
                    else:
                        yomi += v
                inputData[yomi] = [name]
        elif args.station:
            obj = csv.reader(f)
            for line in obj:
                org = line[2]
                key = line[3]
                if key in inputData:
                    if org not in inputData[key]:
                        inputData[key].append(org)
                else:
                    inputData[key] = [org]
        else:
            sys.exit(u'オプションが指定されていません')

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
        if args.pokemon:
            if data['first'] in VOICED_SOUND_MARK:
                data['first'] = VOICED_SOUND_MARK[data['first']]
            if data['end'] in VOICED_SOUND_MARK:
                data['end'] = VOICED_SOUND_MARK[data['end']]
        outputData.append(data)

    with args.outputfile as wf:
        json.dump(outputData, wf, indent=2)
