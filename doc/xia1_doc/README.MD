# Generate .pot file from text
po4a-gettextize -f latex -m documentation.tex -M UTF8 -p en_EN.pot

# Generate translation
po4a-translate -f latex -m documentation.tex -M UTF8 -p fr/documentation-fr_FR.po -l documentation-fr.tex

# Update translations when source document changes
po4a-updatepo -f latex -m documentation.tex -M UTF8 -p fr/documentation-fr_FR.po
