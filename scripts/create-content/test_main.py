#!/usr/bin/env python3
#
# Copyright (C) 2022 SRE France
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dogtag is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dogtag.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from unittest import mock
from io import StringIO

from main import main
from main import slugify


class TestSlugyFunction(unittest.TestCase):
    def test_happy_path(self):
        date = "2020-10-02"
        title = "This is a title"
        expected = "posts/2020-10-02-this-is-a-title.md"
        output = slugify(date, title)
        self.assertEqual(expected, output)

    def test_single_quote(self):
        date = "2020-10-02"
        title = "It's a title"
        expected = "posts/2020-10-02-its-a-title.md"
        output = slugify(date, title)
        self.assertEqual(expected, output)

    def test_single_quote_utf(self):
        date = "2020-10-02"
        title = "Under Deconstruction: The State of Shopify’s Monolith"
        expected = "posts/2020-10-02-under-deconstruction-the-state-of-shopifys-monolith.md"
        output = slugify(date, title)
        self.assertEqual(expected, output)

    def test_question_mark(self):
        date = "2020-10-02"
        title = "how they test ?"
        expected = "posts/2020-10-02-how-they-test.md"
        output = slugify(date, title)
        self.assertEqual(expected, output)

    def test_percent_sign(self):
        date = "2020-10-02"
        title = "Why is 100% reliability the wrong target?"
        expected = "posts/2020-10-02-why-is-100-reliability-the-wrong-target.md"
        output = slugify(date, title)
        self.assertEqual(expected, output)

    def test_em_dash_and_ellipsis(self):
        date = "2020-10-02"
        title = "SLO — From Nothing to… Production"
        expected = "posts/2020-10-02-slo-from-nothing-to-production.md"
        output = slugify(date, title)
        self.assertEqual(expected, output)

    def test_comma_punctuation(self):
        date = "2021-03-09"
        title = "Everything is broken, and it’s okay"
        expected = "posts/2021-03-09-everything-is-broken-and-its-okay.md"
        output = slugify(date, title)
        self.assertEqual(expected, output)

    def test_exclamation_mark(self):
        date = "2021-03-09"
        title = "Hello, SRE world!"
        expected = "posts/2021-03-09-hello-sre-world.md"
        output = slugify(date, title)
        self.assertEqual(expected, output)


class TestMain(unittest.TestCase):
    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_parse_issue(self, mock_stdout):
        json_data = r"""
            {
                "issue": {
                    "title": "First article",
                    "created_at": "2020-09-12T11:19:56Z",
                    "user": {
                        "login": "pabluk"
                    },
                    "body": "url: https://example.com\r\nhashtags: #hash1,#hash2\r\n---\r\nMarkdown content..."
                }
            }"""
        expected = """posts/2020-09-12-first-article.md
---
title: "First article"
date: 2020-09-12T11:19:56Z
github_username: pabluk
twitter_username: pabluk
link: https://example.com
hashtags: "#hash1,#hash2"
---
Markdown content...

"""
        with mock.patch("main.open", mock.mock_open(read_data=json_data)):
            main(None)
            self.assertEqual(expected, mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
