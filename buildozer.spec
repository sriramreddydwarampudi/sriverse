[app]
title = VersePad
package.name = versepad
package.domain = org.sriram
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.3.0,pyenchant==3.2.2,pronouncing==0.2.0,nltk==3.8.1,matplotlib==3.8.2,language-tool-python==2.7.1,setuptools
orientation = portrait
fullscreen = 1
osx.python_version = 3
osx.kivy_version = 2.3.0

# Permissions
android.permissions = INTERNET

# Icons
icon.filename = %(source.dir)s/icon.png

# Entry point
entrypoint = verse.py

# Package format for Android
android.package = org.sriram.versepad

[buildozer]
log_level = 2
warn_on_root = 1
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.arch = arm64-v8a

# GitHub Actions safe path
build_dir = .buildozer

# Force latest pip for dependencies
pip_upgrade = true

[python]
# If you use .venv in GitHub Actions or Termux
virtualenv = .venv
