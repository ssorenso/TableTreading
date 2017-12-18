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
import csv
import re

import row_base.RowBase

"""table_base.py

A library hosting an organizational tool for non-specific table types that
assume only that:
  1. Each table will be given a name
  2. Each table will have a headers row (first row)
  3. That the first element of the headers row makes that row unique
"""


class TableBase(object):
    """Creates a table's base object

    This object can be inherited by other table objects as needed, but can act
    as a standalone.  Currently, there are no ABC methods implemented.
    """
    empty_whitespace = '[\s\W]*'
    skip_line_re = re.compile(
        '^=+{}$|^{}$'.format(empty_whitespace, empty_whitespace))

    def __init__(self, datetime=None, table_name=''):
        self.__table_name = table_name
        self.__datetime = datetime
        self.__original_content = str()
        self.__table = None

    def add_line(self, line):
        """A reading method that excludes what the csv lib can't take

        This is a simple method that ignores empty lines or header lines for an
        expected sub-section.
        """
        if self.skip_line_re.search(line):
            return
        line += "\n" if not line.endswith("\n") else line
        self.__original_content += line

    def done_parsing_table(self):
        """Performs final changes to the Table that constructs the table"""
        lines = self.__original_content.split("\n")
        reader = csv.DictReader(lines, delimiter=',')
        contents = list()
        for row in reader:
            rows_contents = collections.OrderedDict()
            for key, value in row:
                rows_contents[key] = str(value)
            contents.append(row_base.RowBase(rows_contents))
        self.__table = contents

    def set_unique_name(self):
        """By default, this method will grab the [0,0] position of the table

        This method assumes that each row should be named after [0,0]'s value.
        """
        lines = self.__original_content.split("\n")
        my_unique_column = lines[0].split(',')[0]
        self.__unique_column = my_unique_column

    @property
    def table(self):
        """Returns the constructed, python-interpreted table"""
        return tuple(self.__table)

    @property
    def table_name(self):
        """Returns the table's name as given upon creation"""
        return self.__table_name

    @property
    def main_attr(self):
        """Returns the uniquely-driven table header"""
        return self.__unique_column
