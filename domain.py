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

DATASTORE_DEFAULT_LAST_WORD = u'シリトリ'

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
        user = infra.load_user(userId, DATASTORE_DEFAULT_LAST_WORD)
        infra.reset_datastore(user)
    elif startMode == PARAM_START_MODE_CONTINUE:
        logging.info(PARAM_START_MODE_CONTINUE)
    else:
        Exception(u"Unknown startMode: " + startMode)

    return {
        u'followupEventInput': {
            u'name': ASK_WORD_EVENT,
            u'languageCode': queryResult[u'languageCode'],
        }
    }


def response_word(obj):
    originalDetectIntentRequest = obj['originalDetectIntentRequest']
    queryResult = obj[u'queryResult']
    userId = originalDetectIntentRequest[u'payload'][u'user'][u'userId']
    queryText = queryResult[u'queryText']

    user = infra.load_user(userId, DATASTORE_DEFAULT_LAST_WORD)

    if queryText == ASK_WORD_EVENT:
        return {
            u'fulfillmentText': user.last_word + u'、の、' + user.last_word[-1],
            # FIXME: #414, #427                             ^^^^^^^^^^^^^^^^^^
        }
    else:
        logging.info(queryText)
        reading = infra.search_reading_from_dic(queryText)
        if reading:
            logging.info(reading)
            reading_end = reading[-1]
            if infra.check_last_word_datastore(user, reading):
                if reading_end == u'ン':
                    infra.reset_datastore(user)
                    return {
                        u'followupEventInput': {
                            u'name': DECLARE_USER_LOSE_EVENT,
                            u'languageCode': queryResult[u'languageCode'],
                        }
                    }
                elif infra.check_word_datastore(user, reading):
                    infra.save_word_datastore(user, reading)
                    if infra.is_need_google_home_lose(user):
                        return {
                            u'followupEventInput': {
                                u'name': DECLARE_GOOGLE_HOME_LOSE_EVENT,
                                u'languageCode': queryResult[u'languageCode'],
                            }
                        }
                    else:
                        word_record = infra.search_word_record_from_dic(
                            user, reading_end)
                        logging.info(word_record)
                        word = word_record[u'org'][0]
                        infra.save_word_datastore(user, word_record[u'key'])
                        fulfillmentText = word + u'、の、' + word_record[u'end']
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

    user = infra.load_user(userId, DATASTORE_DEFAULT_LAST_WORD)
    reading_end = user.last_word[-1]
    # FIXME: #414, #427 ^^^^^^^^^^^^

    word_record = infra.search_lose_word_record_from_dic(
        user, reading_end)
    logging.info(word_record)
    fulfillmentText = u''
    if word_record:
        word = word_record[u'org'][0]
        infra.save_word_datastore(user, word_record[u'key'])
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
