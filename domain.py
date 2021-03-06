# -*- coding: UTF-8 -*-

# Copyright 2019 Hayato Kubo / Takanori Kondo / Satoki Mizoguchi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

import infra

ASK_CONTINUE_EVENT = u'ASK_CONTINUE_EVENT'
ASK_DIC_EVENT = u'ASK_DIC_EVENT'
ASK_WORD_EVENT = u'ASK_WORD_EVENT'
DECLARE_USER_LOSE_EVENT = u'DECLARE_USER_LOSE_EVENT'
DECLARE_GOOGLE_HOME_LOSE_EVENT = u'DECLARE_GOOGLE_HOME_LOSE_EVENT'

PARAM_START_MODE_NEW_GAME = u'NEW_GAME'
PARAM_START_MODE_CONTINUE = u'CONTINUE'


def ask_continue(obj):
    originalDetectIntentRequest = obj['originalDetectIntentRequest']
    userId = originalDetectIntentRequest[u'payload'][u'user'][u'userId']
    queryResult = obj[u'queryResult']

    user = infra.load_user(userId)
    if user.last_word_end == u'ン' or user.words == u'シリトリ':
        infra.reset_datastore(user)

    if infra.contains_user(userId):
        return {
            u'followupEventInput': {
                u'name': ASK_CONTINUE_EVENT,
                u'languageCode': queryResult[u'languageCode'],
            }
        }
    else:
        return {
            u'followupEventInput': {
                u'name': ASK_DIC_EVENT,
                u'languageCode': queryResult[u'languageCode'],
            }
        }


def set_continue(obj):
    queryResult = obj[u'queryResult']
    startMode = queryResult[u'parameters'][u'startMode']
    if startMode == PARAM_START_MODE_NEW_GAME:
        logging.info(PARAM_START_MODE_NEW_GAME)
        originalDetectIntentRequest = obj['originalDetectIntentRequest']
        userId = originalDetectIntentRequest[u'payload'][u'user'][u'userId']
        user = infra.load_user(userId)
        infra.reset_datastore(user)
        return {
            u'followupEventInput': {
                u'name': ASK_DIC_EVENT,
                u'languageCode': queryResult[u'languageCode'],
            }
        }
    elif startMode == PARAM_START_MODE_CONTINUE:
        logging.info(PARAM_START_MODE_CONTINUE)
        return {
            u'followupEventInput': {
                u'name': ASK_WORD_EVENT,
                u'languageCode': queryResult[u'languageCode'],
            }
        }
    else:
        raise RuntimeError(u"Unknown startMode: " + startMode)


def set_dic(obj):
    queryResult = obj[u'queryResult']

    try:
        # float 型から int 型へ変換する
        dicNum = int(queryResult[u'parameters'][u'dicNum'])
    except ValueError:
        dicNum = 0

    logging.info(u'set_dic dicNum: ' + str(dicNum))

    originalDetectIntentRequest = obj['originalDetectIntentRequest']
    userId = originalDetectIntentRequest[u'payload'][u'user'][u'userId']
    user = infra.load_user(userId)

    if dicNum == 1:
        # 1番、普通の辞書
        infra.save_json_file_path(user, u'data/dict.json')
    elif dicNum == 2:
        # 2番、ポケモン辞書
        infra.save_json_file_path(user, u'data/pokemon.json')
    else:
        return {
            u'fulfillmentText': u'辞書を番号で選んでください。1番、普通の辞書。2番、ポケモン辞書。',
        }

    logging.info(u'set_dic user.json_file_path: ' + user.json_file_path)

    return {
        u'followupEventInput': {
            u'name': ASK_WORD_EVENT,
            u'languageCode': queryResult[u'languageCode'],
        }
    }


def response_word(obj):
    originalDetectIntentRequest = obj['originalDetectIntentRequest']
    userId = originalDetectIntentRequest[u'payload'][u'user'][u'userId']
    user = infra.load_user(userId)
    queryResult = obj[u'queryResult']
    queryText = queryResult[u'queryText']

    if queryText == ASK_WORD_EVENT:
        return {
            u'fulfillmentText': user.last_word + u'、の、' + user.last_word_end,
        }
    else:
        yahoo_appid = infra.load_yahoo_appid()
        queryText = queryResult[u'queryText']
        queryKanaText = infra.furigana(yahoo_appid, queryText)
        languageCode = queryResult[u'languageCode']
        return response_searched_word(queryText, queryKanaText, languageCode, user)


def response_searched_word(queryText, queryKanaText, languageCode, user):
    logging.info(queryText)

    json_dic = infra.load_dic(user.json_file_path)
    req_word_record = infra.search_reading_from_dic(
        queryText, queryKanaText, json_dic)
    if req_word_record:
        req_word_reading = req_word_record[u'key']
        logging.info(req_word_reading)
        req_word_reading_end = req_word_record[u'end']
        if infra.check_last_word_datastore(user, req_word_record):
            if infra.check_word_datastore(user, req_word_reading):
                infra.save_word_datastore(user, req_word_record)
                if req_word_reading_end == u'ン':
                    return {
                        u'followupEventInput': {
                            u'name': DECLARE_USER_LOSE_EVENT,
                            u'languageCode': languageCode,
                        }
                    }
                elif infra.is_need_google_home_lose(user):
                    return {
                        u'followupEventInput': {
                            u'name': DECLARE_GOOGLE_HOME_LOSE_EVENT,
                            u'languageCode': languageCode,
                        }
                    }
                else:
                    resp_word_record = infra.search_word_record_from_dic(
                        user, req_word_reading_end, json_dic)
                    logging.info(resp_word_record)
                    word = resp_word_record[u'org'][0]
                    infra.save_word_datastore(user, resp_word_record)
                    fulfillmentText = word + u'、の、' + \
                        resp_word_record[u'end']
                    logging.info(fulfillmentText)
                    return {
                        u'fulfillmentText': fulfillmentText,
                    }
            else:
                return {
                    u'fulfillmentText': u'それは使用済みの言葉です',
                }
        else:
            return {
                u'fulfillmentText': infra.get_last_word_datastore(user) + u'で始まる言葉を使ってください',
            }
    else:
        return {
            u'fulfillmentText': u'それは知らない言葉です',
        }


def response_lose_word(obj):
    originalDetectIntentRequest = obj['originalDetectIntentRequest']
    userId = originalDetectIntentRequest[u'payload'][u'user'][u'userId']

    user = infra.load_user(userId)
    json_dic = infra.load_dic(user.json_file_path)
    reading_end = user.last_word_end

    word_record = infra.search_lose_word_record_from_dic(
        user, reading_end, json_dic)
    logging.info(word_record)
    fulfillmentText = u''
    if word_record:
        word = word_record[u'org'][0]
        infra.save_word_datastore(user, word_record)
        fulfillmentText += word + u'。'
        fulfillmentText += u'あら、「ん」で終わってしまいました。'
    else:
        fulfillmentText += u'うーん、「' + reading_end + u'」で始まる言葉が思いつきません。'
    fulfillmentText += u'私の負けです。'
    logging.info(fulfillmentText)
    return {
        u'fulfillmentText': fulfillmentText,
    }
