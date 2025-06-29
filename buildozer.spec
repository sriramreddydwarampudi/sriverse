[app]

title = sriverse
package.name = sriverse
package.domain = org.sriverse

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 1.0.0

requirements = python3,kivy==2.1.0,nltk,pronouncing,regex,setuptools

orientation = portrait
fullscreen = 0

# ✅ Add modern media permissions (Android 13+)
android.permissions = INTERNET,READ_MEDIA_IMAGES,READ_MEDIA_AUDIO,READ_MEDIA_VIDEO

# ✅ Update target API to 33 for compatibility
android.api = 33
android.minapi = 21
android.ndk_api = 33

# ✅ Build for modern architecture
android.archs = armeabi-v7a,arm64-v8a

# ✅ Required for Kivy-based apps (sdl2 is modern bootstrap)
p4a.bootstrap = sdl2

# Optional: enable wake lock if needed (to keep screen on)
# android.wakelock = True

# Optional: enable backup
android.allow_backup = True

# Optional: turn on debug logs
android.logcat_filters = *:S python:D

# Optional: if you have .jar files (Java dependencies)
# android.add_jars = libs/*.jar

[buildozer]

# Show detailed logs
log_level = 2
