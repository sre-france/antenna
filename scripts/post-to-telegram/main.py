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

import sys
import json
import os
from html import unescape

import telegram
from feedparser.sanitizer import _HTMLSanitizer


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
DRY_RUN = os.environ.get("TELEGRAM_DRY_RUN", "false").lower() in ["true", "yes", "1"]

TEMPLATE = """
<em>From</em> {link}

{content}

<em>Shared by {user} via reliability.re</em>
"""


def clean_html(content):
    p = _HTMLSanitizer(None, "text/html")
    p.acceptable_elements = {
        "b",
        "strong",
        "i",
        "em",
        "underline",
        "ins",
        "s",
        "strike",
        "del",
        "a",
        "code",
        "pre",
    }
    p.acceptable_attributes = {"href"}
    p.feed(content)
    cleaned = p.output()
    cleaned = cleaned.strip()
    cleaned = unescape(cleaned)
    return cleaned


def format_message(payload):
    """
    Format HTML content on a subset of HTML tags supported by the Telegram Bot API.
    See https://core.telegram.org/bots/api#html-style
    """

    user = '<a href="https://github.com/{username}">@{username}</a>'.format(
        username=payload["github_username"]
    )
    content = clean_html(payload["content"])
    message = TEMPLATE.format(
        link=payload["link"],
        content=content,
        user=user,
    )
    return message.strip()


def send_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    chat_id = TELEGRAM_CHAT_ID
    bot.sendMessage(
        chat_id=chat_id,
        text=message,
        disable_web_page_preview=False,
        parse_mode=telegram.ParseMode.HTML,
    )


def main(filename):
    with open(filename, "r") as f:
        payload = json.load(f)
    message = format_message(payload)
    print(f"Message: {message}")
    if not DRY_RUN:
        send_message(message)


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
