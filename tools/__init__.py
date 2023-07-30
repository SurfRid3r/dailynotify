import importlib
import os

# 获取tools目录下所有.py文件
files = os.listdir(os.path.dirname(__file__))
py_files = [f for f in files if f.endswith(".py")]

# 导入tools目录下的所有.py文件
for py_file in py_files:
    if py_file == "__init__.py":
        continue
    module_name = os.path.splitext(py_file)[0]
    importlib.import_module("." + module_name, __package__)