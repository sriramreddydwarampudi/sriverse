[buildozer]
log_level = 2
warn_on_root = 1

[app]
title = LyricVerse
package.name = lyricverse
package.domain = org.lyricverse
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 1.2

requirements = 
    python3==3.9.13,  # Changed from 3.8.5 to 3.9.13
    kivy==2.3.0,
    pyenchant==3.2.2,
    pronouncing==0.2.0,
    nltk==3.8.1,
    android

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE
android.api = 33
android.ndk = 25b
android.ndk_version = 23b
p4a.branch = master
android.enable_androidx = True
orientation = portrait

# Add these new sections
[buildozer]
default.fabric = 1

[requirements]
hostpython3 = 3.9.13  # Match the Python version
