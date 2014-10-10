#!/bin/sh

NOT_CONCATENATED=";kinetic-xia.js;"

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

        if printf ";$js_shortname;\n" | grep -q "$NOT_CONCATENATED"
        then
            # Not in xia.js but we must minify the script.
            printf "Minify $js_shortname in $theme_shortname theme\n"
            perl "$script_dir/minify_js.pl" "$js"
            rm "$js" # useless now.
        else
            # Must be include in xia.js
            cat "$js" >> "$theme/js/xia.js"
            echo "" >> "$theme/js/xia.js"
            rm "$js" # useless now.
        fi
    done

done

# Minify js in vendors/ directory.
for js in "$build_dir/share/vendors/"*.js
do
    js_shortname=${js##*/}
    printf "Minify $js_shortname in vendors/ directory\n"
    perl "$script_dir/minify_js.pl" "$js"
done




