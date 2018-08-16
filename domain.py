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


def ask_continue(obj):
    queryResult = obj[u'queryResult']
    return {
        u'followupEventInput': {
            u'name': ASK_CONTINUE_EVENT,
            u'languageCode': queryResult[u'languageCode'],
        }
    }


def set_continue(obj):
    queryResult = obj[u'queryResult']
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
    if queryText == ASK_WORD_EVENT:
        return {
            u'fulfillmentText': u'しりとり、の、リ',
        }
    else:
        logging.info(queryText)
        reading = infra.search_reading_from_dic(queryText)
        if reading:
            logging.info(reading)
            reading_end = reading[-1]
            if infra.check_last_word_datastore(userId, reading):
                if reading_end == u'ン':
                    infra.reset_datastore(userId)
                    return {
                        u'followupEventInput': {
                            u'name': DECLARE_USER_LOSE_EVENT,
                            u'languageCode': queryResult[u'languageCode'],
                        }
                    }
                elif infra.check_word_datastore(userId, reading):
                    infra.save_word_datastore(userId, reading)
                    word_record = infra.search_word_record_from_dic(
                        userId, reading_end)
                    logging.info(word_record)
                    word = word_record[u'org'][0]
                    infra.save_word_datastore(userId, word_record[u'key'])
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
                    u'fulfillmentText': infra.get_last_word_datastore(userId) + u'で始まる言葉を使ってください',
                }
        else:
            return {
                u'fulfillmentText': u'それは知らない言葉です',
            }
