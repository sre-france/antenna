#!/usr/bin/env python3
#
# Parse Github issues created using this template:
# https://github.com/sre-france/antenna/blob/main/.github/ISSUE_TEMPLATE/new-content.md
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
import http.client


def slugify(date, title):
    """Very naive slugify function."""
    slug = title.lower()
    # Remove stranger chars
    slug = slug.replace("'", "")
    slug = slug.replace(":", "")
    slug = slug.replace("’", "")
    slug = slug.replace("?", "")
    slug = slug.replace("%", "")
    slug = slug.replace("—", "")
    slug = slug.replace("…", "")
    slug = slug.replace(",", "")
    slug = slug.replace("!", "")

    # Remove leading, trailing and duplicated whitespaces
    slug = " ".join(slug.split())
    # Replace spaces with "-"'s for cleaner URLs
    slug = slug.replace(" ", "-")

    date = date[:10]
    return f"posts/{date}-{slug}.md"


def get_twitter_username(username):
    """Get Twitter username from Github profile information."""
    conn = http.client.HTTPSConnection("api.github.com")
    headers = {
        "Content-type": "application/json",
        "User-Agent": "sre-paris",
    }
    conn.request("GET", "/users/%s" % username, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode())
    return data["twitter_username"]


def main(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    content = "---\n"

    title = data["issue"]["title"]
    content += 'title: "%s"\n' % title

    created_at = data["issue"]["created_at"]
    content += "date: %s\n" % created_at

    github_username = data["issue"]["user"]["login"]
    content += "github_username: %s\n" % github_username

    twitter_username = get_twitter_username(github_username)
    if twitter_username:
        content += "twitter_username: %s\n" % twitter_username

    body = data["issue"]["body"]

    url = body.splitlines()[0].replace("url: ", "")
    content += "link: %s\n" % url

    if "hashtags:" not in body.splitlines()[1]:
        description = "\n".join(body.splitlines()[2:])
        content += "---\n%s\n" % description
    else:
        hashtags = body.splitlines()[1].replace("hashtags: ", "")
        content += 'hashtags: "%s"\n' % hashtags
        description = "\n".join(body.splitlines()[3:])
        content += "---\n%s\n" % description

    post_filename = slugify(created_at, title)
    print(post_filename)
    print(content)

    with open(post_filename, "w+") as f:
        print(content, file=f)


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
