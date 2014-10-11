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
build_dir="$root_dir/build"

# Extract gettext from source.
xgettext --from-code=UTF-8 --keyword=translate \
    -o "$build_dir/share/i18n/messages.pot"    \
    $(find "$build_dir/xiaconverter/" -type f -name "*.py")

# In a subshell:
#   - update .po files with msgmerge;
#   - generate .mo files;
#   - remove all files except .mo in i18n.
(
    cd "$build_dir/share/i18n/"
    for loc in *
    do
        # Skip the messages.pot file. /!\
        [ ! -d "$build_dir/share/i18n/$loc" ] && continue
        msgmerge --no-fuzzy-matching                           \
            "$loc/LC_MESSAGES/xia-converter.po" "messages.pot" \
            -o "$loc/LC_MESSAGES/xia-converter.po.updated"     \
            >/dev/null 2>&1
        msgfmt "$loc/LC_MESSAGES/xia-converter.po.updated" \
            -o "$loc/LC_MESSAGES/xia-converter.mo"
    done

    find . -type f ! -name '*.mo' -exec rm "{}" \+
)


