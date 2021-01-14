# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\crh\\Desktop\\PROJECTS\\abylsen\\sources'],
             binaries=[],
             datas=[('./views/mainWindow.ui','./views/'),
                 ('./views/add_BU_Diag.ui','./views/'),
                 ('./views/add_IA_Diag.ui','./views/'),
                 ('./views/add_ING_Diag.ui','./views/'),
                 ('./views/deleteING_IA.ui','./views/'),
                 ('./views/ing_start_mission.ui','./views/'),
                 ('./views/ing_stop_mission.ui','./views/')],
             hiddenimports=[],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
