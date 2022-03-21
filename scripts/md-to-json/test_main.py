#!/usr/bin/env python3
#
# Copyright (C) 2022 SRE France
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import unittest

from main import md_to_json


class TestMDtoJSON(unittest.TestCase):
    def test_basic(self):
        """A basic test for the Happy Path."""
        with open("test_data/01-content.md", "r") as f:
            markdown = f.read()
        with open("test_data/01-content.expected.json", "r") as f:
            expected = f.read().strip()
        json_data = md_to_json(markdown)
        self.assertEqual(json_data, expected)

    def test_non_supported_html(self):
        """Test conversion of non-supported HTML"""
        with open("test_data/02-non-supported-html.md", "r") as f:
            markdown = f.read()
        with open("test_data/02-non-supported-html.expected.json", "r") as f:
            expected = f.read().strip()
        json_data = md_to_json(markdown)
        self.assertEqual(json_data, expected)


if __name__ == "__main__":
    unittest.main()
