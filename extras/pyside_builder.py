import os

file_list = [
    ['main_window.ui', 'ui_main_window.py'],
    ['com_port_dialog.ui', 'ui_com_port_dialog.py']
]

#Build PyQt UI files for PySide6 and PySide2
for f in file_list:
    print(f"Building {f[1]}...", end="")
    # os.system(f'pyside2-uic ./{f[0]} > ./PySide2_UI/{f[1]}')
    os.system(f'pyside6-uic ./UI/windows/{f[0]} > ./UI/windows/{f[1]}')
    print("Done")