# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect all numpy and cv2 files
numpy_datas, numpy_binaries, numpy_hiddenimports = collect_all('numpy')
cv2_datas, cv2_binaries, cv2_hiddenimports = collect_all('cv2')

a = Analysis(['watermark.py'],
             pathex=[],
             binaries=numpy_binaries + cv2_binaries,
             datas=[('img', 'img')] + numpy_datas + cv2_datas,
             hiddenimports=['numpy', 'numpy.core._multiarray_umath',
                            'numpy.core.multiarray'] + numpy_hiddenimports + cv2_hiddenimports,
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='s42_watermark',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

if sys.platform == 'darwin':
    app = BUNDLE(exe,
                 name='s42_watermark.app',
                 icon=None,
                 bundle_identifier=None)