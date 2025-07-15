[app]
title = VersePad Pro
package.name = versepad
package.domain = org.example
source.dir = .
source.include_exts = py,kv,ttf
version = 1.0
requirements = python3,kivy==2.3.0,nltk,pronouncing
orientation = portrait
fullscreen = 0
osx.kivy_version = 2.3.0

[buildozer]
log_level = 2
warn_on_root = 1

[app.android]
android.api = 30
android.minapi = 21
android.ndk = 25b
android.sdk = 24
android.permissions = INTERNET
# Internet is required for downloading nltk corpora at runtime

# Optional: allow storing temporary downloaded data
# If you want access to external storage too:
# android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[app:source.exclude_patterns]
*.pyc
*.pyo
*.pyd
__pycache__/
.git*
docs/
tests/
images/
nltk_data/

[app.android.entrypoint]
main = main:VersePadApp().run()
