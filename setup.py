from setuptools import setup

APP = ['VOLSBB.py']
APP_NAME = 'VOLSBB'
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': APP_NAME + " info",
        'CFBundleIdentifier': "com.akigugale.osx.VOLSBB",
        'CFBundleVersion': "1.0",
        'CFBundleShortVersionString': "1.0",
        'NSHumanReadableCopyright': u"Copyright \u00a9, 2018, Akshay Gugale"
    },
    'packages': ['rumps','requests'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    url='https://github.com/akigugale/volsbb',
    author='Akshay Gugale',
    author_email='gugaleaki@gmail.com',
    license='MIT',
)