#!/bin/sh

# Copyright: 2014 Francois Lafont <francois.lafont@ac-versailles.fr>
#
# License: GPL-3.0+
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

set -e
export PATH='/usr/bin:/bin'

# Get root directory and build directory of the project.
script_dir=$(dirname "$0")
root_dir=$(cd "$script_dir/.."; pwd)
src_dir="$root_dir/src"

# xgettext is run in a subshell in "$src_dir" directory to
# have relative paths for locations in comments in .pot and
# .po files.
(
    cd "$src_dir"

    # Extract gettext from source.
    xgettext --from-code=UTF-8 --keyword=translate \
        -o "share/i18n/messages.pot"               \
        $(find "." -type f -name "*.py")
)

for loc in "$src_dir/share/i18n/"*
do
    # Don't handle "messages.pot" file which is not a directory.
    [ ! -d "$loc" ] && continue

    loc_shortname=${loc##*/}
    printf "Merging xia-converter.po in share/i18n/$loc_shortname\n"
    mv "$loc/LC_MESSAGES/xia-converter.po" "$loc/LC_MESSAGES/xia-converter.po.old"
    msgmerge --no-fuzzy-matching                \
        "$loc/LC_MESSAGES/xia-converter.po.old" \
        "$src_dir/share/i18n/messages.pot"      \
        -o "$loc/LC_MESSAGES/xia-converter.po"
done

# Remove "xia-converter.po.old" and "messages.pot" files
# in "$src_dir/share/i18n/" directory.
find "$src_dir/share/i18n/" -type f                          \
  \( -name "xia-converter.po.old" -o -name "messages.pot" \) \
  -exec rm "{}" \+


