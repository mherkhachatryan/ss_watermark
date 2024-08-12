# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['watermark.py'],
             pathex=[],
             binaries=[],
             datas=[('img', 'img')],
             hiddenimports=['pkg_resources.py2_warn', 'binascii'],
             hookspath=[],
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
          console=True )


app = BUNDLE(exe,
             name='s42_watermark.app',
             icon=None,
             bundle_identifier=None)