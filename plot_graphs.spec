# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['plot_graphs.py'],
             pathex=['C:\\Users\\boot\\projects\\graphs-boinc'],
             binaries=[],
             datas=[("C:\\Users\\boot\\projects\\graphs-boinc\\venv\\lib\\site-packages\\kaleido\\","kaleido"),
		     ("C:\\Users\\boot\\projects\\graphs-boinc\\venv\\lib\\site-packages\\plotly\\","plotly")],
             hiddenimports=[],
             hookspath=['hooks'],
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
          name='plot_graphs',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
