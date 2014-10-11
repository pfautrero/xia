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

# Compile .po to .mo.
for loc in "$build_dir/share/i18n/"*
do
    [ ! -d "$loc" ] && continue
    msgfmt "$loc/LC_MESSAGES/xia-converter.po" \
        -o "$loc/LC_MESSAGES/xia-converter.mo"
done

# Remove "xia-converter.po" files in "$build_dir/share/i18n/" directory.
find "$build_dir/share/i18n/" -type f -name "xia-converter.po" -exec rm "{}" \+


