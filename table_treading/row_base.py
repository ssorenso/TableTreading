#!/usr/bin/env python
# Copyright 2017 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import collections
import re


class RowBase(object):
    @property
    def __dict__(self):
        return_value = dict()
        for attr in self.__attr_chain:
            return_value[attr] = self.getattr(attr)

        return return_value

    def __init__(self, kwargs):
        self.__attr_chain = list()
        is_number = re.compile('^(\d+\.\d+)|(\d+)$')
        unacceptable = re.compile('[^\w]|_+')
        for key in kwargs:
            key = unacceptable.sub('_', key)
            key = unacceptable.sub('_', key)  # __ to _
            self.__attr_chain.append(key)
            value = kwargs[key]
            num_match = is_number.search(value)
            if num_match and '.' in value:
                value = float(value)
            elif num_match:
                value = int(value)
            else:
                value = str(value)
            setattr(self, key, value)
        self.__namedtuple = namedtuple("RowBase", ', '.join(self.__attr_chain))

    def namedtuple(self):
        """Returns a namedtuple of this row's contents"""
        for
