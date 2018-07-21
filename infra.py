#!/usr/local/bin/python3

import json

with open('data/dict.json') as json_file:
    json_dic = json.load(json_file)


def search_reading_from_dic(search_word):
    """
    json形式の辞書ファイルを全探索し、引数の文字列の読みをカタカナで返す
    引数 : 検索する文字列
    戻り値 : 検索した文字列のカタカナ読み(辞書にない場合は'')
    """
    for dict_record in json_dic:
        for word in dict_record['org']:
            if(word == search_word):
                return dict_record['key']
    return ''


if __name__ == '__main__':
    print(search_reading_from_dic(u'リンゴ'))
    print(search_reading_from_dic(u'林檎'))
    print(search_reading_from_dic(u'りんご'))
