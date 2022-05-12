#!/bin/bash
#
# This script search for files added on $commit
# and checkout the file on the current workspace

set -xe

commit="$1"
branch="origin/hugo-site"
pattern="posts/*/index.json"

# core.quotepath defaults to 'true' which quotes and escapes "unusual" characters in the pathname (accents included)
git config --local core.quotepath false
json_post=$(git diff-tree --no-commit-id --name-only --diff-filter=A -r "$commit" -- "$pattern")
git checkout "$branch" -- "$json_post"
echo "$json_post"
