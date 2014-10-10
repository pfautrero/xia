#!/bin/sh

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
    for lco in *
    do
        # Skip the messages.pot file. /!\
        [ ! -d "$lco" ] && continue
        msgmerge "$lco/LC_MESSAGES/xia-converter.po" "messages.pot" \
            -o "$lco/LC_MESSAGES/xia-converter.po.updated"
        msgfmt "$lco/LC_MESSAGES/xia-converter.po.updated" \
            -o "$lco/LC_MESSAGES/xia-converter.mo"
    done

    find . -type f ! -name '*.mo' -exec rm "{}" \+
)


