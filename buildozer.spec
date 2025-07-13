[app]

# (str) Title of your application
title = Sriverse

# (str) Package name
package.name = sriverse

# (str) Package domain (needed for android/ios packaging)
package.domain = org.sriverse.app

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = kivy,android,requests

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Android API to use
android.api = 34

# (int) Minimum API required
android.minapi = 23

# (str) Android NDK version to use
android.ndk = 25c

# (str) Architecture to use (e.g. arm64-v8a, armeabi-v7a)
android.arch = arm64-v8a

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Custom source folders for requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY

# (string) Presplash background color
#android.presplash_color = #FFFFFF

# (str) Adaptive icon (Android API 26+)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# End of [app] section

# -- Uncomment and configure other sections as needed --
