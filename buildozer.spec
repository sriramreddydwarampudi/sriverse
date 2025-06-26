[buildozer]
log_level = 2
warn_on_root = 1

[app]
title = LyricPad
package.name = lyricpad
package.domain = org.lyricpad
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 1.1

requirements = 
    kivy==2.3.0,
    pyenchant==3.2.2,
    pronouncing==0.2.0,
    nltk==3.8.1

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE
android.api = 33
android.ndk = 25b
p4a.branch = master
orientation = portrait
