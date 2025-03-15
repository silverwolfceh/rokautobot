# -*- mode: python ; coding: utf-8 -*-

PROGNAME = "RSSTransfer_v1"
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=PROGNAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=PROGNAME,
)

import shutil
import os
def post_build():
    destfolder = os.path.join(DISTPATH, PROGNAME, "_internal")
    shutil.copyfile('config.json', '{0}/config.json'.format(destfolder))
    shutil.copyfile('devices_config.json', '{0}/devices_config.json'.format(destfolder))
    shutil.rmtree(os.path.join(destfolder, "adb"), ignore_errors=True)
    shutil.copytree('adb','{0}/adb'.format(destfolder))
    shutil.rmtree(os.path.join(destfolder, "tesseract"), ignore_errors=True)
    shutil.copytree('tesseract','{0}/tesseract'.format(destfolder))
    shutil.rmtree(os.path.join(destfolder, "save"), ignore_errors=True)
    shutil.copytree('save','{0}/save'.format(destfolder))
post_build()