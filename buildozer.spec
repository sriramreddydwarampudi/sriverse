[app]
title = VersePad
package.name = versepad
package.domain = org.versepad.app
version = 1.0.0

source.dir = .
source.include_exts = py,kv,txt,pyx
source.exclude_dirs = tests, test, bin, lib, include, .buildozer

requirements = python3,kivy==2.2.1,nltk,pronouncing,regex,setuptools,cython==0.29.36

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_MEDIA_IMAGES,READ_MEDIA_AUDIO,READ_MEDIA_VIDEO

android.api = 33
android.minapi = 33
android.ndk = 25b
android.ndk_api = 33
android.archs = armeabi-v7a,arm64-v8a

p4a.bootstrap = sdl2
p4a.branch = master

android.allow_backup = True
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
# Set Cython to use Python 3 syntax
cython.compiler_directives = language_level=3
