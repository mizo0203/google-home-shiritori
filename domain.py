# -*- coding: UTF-8 -*-

# Copyright 2018 [name of copyright owner]
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
ASK_WORD_EVENT = u'ASK_WORD_EVENT'
DECLARE_USER_LOSE_EVENT = u'DECLARE_USER_LOSE_EVENT'
DECLARE_GOOGLE_HOME_LOSE_EVENT = u'DECLARE_GOOGLE_HOME_LOSE_EVENT'

PARAM_START_MODE_NEW_GAME = u'NEW_GAME'
PARAM_START_MODE_CONTINUE = u'CONTINUE'


def ask_continue(obj):
    originalDetectIntentRequest = obj['originalDetectIntentRequest']
    userId = originalDetectIntentRequest[u'payload'][u'user'][u'userId']
    queryResult = obj[u'queryResult']

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
                u'name': ASK_WORD_EVENT,
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
    elif startMode == PARAM_START_MODE_CONTINUE:
        logging.info(PARAM_START_MODE_CONTINUE)
    else:
        raise RuntimeError(u"Unknown startMode: " + startMode)

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
    return response_word_inner(obj, user)


def response_word_inner(obj, user):
    queryResult = obj[u'queryResult']
    queryText = queryResult[u'queryText']

    if queryText == ASK_WORD_EVENT:
        return {
            u'fulfillmentText': user.last_word + u'、の、' + user.last_word_end,
        }
    else:
        logging.info(queryText)
        req_word_record = infra.search_reading_from_dic(queryText)
        if req_word_record:
            req_word_reading = req_word_record[u'key']
            logging.info(req_word_reading)
            req_word_reading_end = req_word_record[u'end']
            if infra.check_last_word_datastore(user, req_word_record):
                if req_word_reading_end == u'ン':
                    infra.reset_datastore(user)
                    return {
                        u'followupEventInput': {
                            u'name': DECLARE_USER_LOSE_EVENT,
                            u'languageCode': queryResult[u'languageCode'],
                        }
                    }
                elif infra.check_word_datastore(user, req_word_reading):
                    infra.save_word_datastore(user, req_word_record)
                    if infra.is_need_google_home_lose(user):
                        return {
                            u'followupEventInput': {
                                u'name': DECLARE_GOOGLE_HOME_LOSE_EVENT,
                                u'languageCode': queryResult[u'languageCode'],
                            }
                        }
                    else:
                        resp_word_record = infra.search_word_record_from_dic(
                            user, req_word_reading_end)
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
    reading_end = user.last_word_end

    word_record = infra.search_lose_word_record_from_dic(
        user, reading_end)
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
    infra.reset_datastore(user)
    return {
        u'fulfillmentText': fulfillmentText,
    }
