[app]
title = VersePad
package.name = versepad
package.domain = org.sriram
source.dir = .
source.include_exts = py,kv,png,jpg
version = 1.0
requirements = python3,kivy==2.3.0,pronouncing,nltk,setuptools
orientation = portrait
fullscreen = 1
entrypoint = verse.py
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
pip_upgrade = true
