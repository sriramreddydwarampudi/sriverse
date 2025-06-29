[app]
title = VersePad
package.name = versepad
package.domain = org.sriram
source.dir = .
source.include_exts = py,kv,png,jpg,txt
version = 1.1
requirements = python3,kivy==2.3.0,pronouncing,nltk,setuptools,symspellpy
orientation = portrait
fullscreen = 1
entrypoint = main.py
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
pip_upgrade = true
