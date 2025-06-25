[app]
title = sriverse
package.name = sriverse
package.domain = org.sriverse
source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0
requirements = 
    kivy==2.3.0,
    pyenchant==3.2.2,
    pronouncing==0.2.0,
    nltk==3.8.1,
    matplotlib==3.8.2,
    language-tool-python==2.7.1,
    pycairo

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE
android.api = 33
android.ndk = 25b
p4a.branch = master
orientation = portrait
