import os

print("Compiling d75_cat_control")
os.system("pyinstaller --clean -y d75_cat_control.spec")
print("Done")