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

NOT_CONCATENATED=";kinetic-xia.js;hooks.js;"
NOT_MINIFIED=";hooks.js;"

set -e
export PATH='/usr/bin:/bin'

# Get root directory and build directory of the project.
script_dir=$(dirname "$0")
root_dir=$(cd "$script_dir/.."; pwd)
build_dir="$root_dir/build"


for theme in "$build_dir/share/themes/"*
do
    [ ! -d "$theme" ] && continue

    # Create xia.js or minify js.
    rm -f "$theme/js/xia.js"
    for js in "$theme/js/"*.js
    do
        js_shortname=${js##*/}
        theme_shortname=${theme##*/}
        #if printf ";$js_shortname;\n" | grep -q "$NOT_CONCATENATED"
        if printf "$NOT_CONCATENATED" | grep -q ";$js_shortname;"
        then
            if ! printf "$NOT_MINIFIED" | grep -q ";$js_shortname;"
            then
                # Not in xia.js but we must minify the script.
                printf "Minify $js_shortname in $theme_shortname theme\n"
                perl "$script_dir/minify_js.pl" "$js"
                rm "$js" # useless now.
            fi
        else
            # Must be include in xia.js
            cat "$js" >> "$theme/js/xia.js"
            echo "" >> "$theme/js/xia.js"
            rm "$js" # useless now.
        fi
    done
    #perl "$script_dir/minify_js.pl" "$theme/js/xia.js"

done

# Minify js in vendors/ directory.
for js in "$build_dir/share/vendors/"*.js
do
    js_shortname=${js##*/}
    printf "Minify $js_shortname in vendors/ directory\n"
    perl "$script_dir/minify_js.pl" "$js"
    rm $js
done




