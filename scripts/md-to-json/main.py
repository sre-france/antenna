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

from datetime import datetime
import frontmatter
import json
import sys


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat().replace("+00:00", "Z")
        return super().default(obj)


def md_to_json(markdown):
    post = frontmatter.loads(markdown).to_dict()

    post["id"] = post["link"]
    post["plain"] = post["content"]

    json_data = json.dumps(post, indent=2, sort_keys=True, cls=CustomJSONEncoder)
    return json_data


def main(filename):
    with open(filename) as f:
        markdown = f.read()
    json_data = md_to_json(markdown)
    print(json_data)


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)