[app]

title = sriverse
package.name = sriverse
package.domain = org.sriverse

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 1.0.0

requirements = python3,kivy==2.1.0,nltk,pronouncing,regex,setuptools,pillow

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_MEDIA_IMAGES,READ_MEDIA_AUDIO,READ_MEDIA_VIDEO

android.api = 33
android.minapi = 21
android.ndk_api = 33
android.ndk = 25b

android.archs = armeabi-v7a,arm64-v8a
p4a.bootstrap = sdl2
p4a.branch = master

android.allow_backup = True
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
