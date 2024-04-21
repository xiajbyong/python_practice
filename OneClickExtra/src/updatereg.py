import os
import re
import sys

def add_backslash(path):
    new_path = ""
    for char in path:
        if char == "\\":
            new_path += "\\\\"
        else:
            new_path += char
    return new_path
# 获取当前工作目录
setup_path = os.getcwd()
source_path = os.path.join(setup_path, 'source')
# source_path = r'D:\test\0421\source'
print(f"当前路径{setup_path}")

exe_filename = 'OneClickExtra.exe'
Icon_filename = 'OneClickExtra.ico'
reg_filename = 'add_mouse_right_func.reg'
# 构造OneClickExtra.exe的绝对路径
exe_path = os.path.join(source_path, exe_filename)
Icon_path = os.path.join(source_path, Icon_filename)
reg_path = os.path.join(source_path, reg_filename)
if not os.path.exists(exe_path):
    print(f"{source_path}下找不到文件{exe_filename}")
    sys.exit(1)
if not os.path.exists(Icon_path):
    print(f"{source_path}下找不到文件{Icon_filename}")
    sys.exit(1)
if not os.path.exists(reg_path):
    print(f"{source_path}下找不到注册表文件{reg_filename}")
    sys.exit(1)
new_exe_path = add_backslash(exe_path)
new_Icon_path = add_backslash(Icon_path)
pattern_command = re.compile(r'OneClickExtra.exe')
pattern_Icon = re.compile(r'Icon')
# 读取add_mouse_right_func.reg文件的内容，尝试使用UTF-8编码和忽略BOM
try:
    with open(reg_path, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"读取注册表文件{reg_filename}失败")
    sys.exit(1)

new_lines = []
update_exe_mark = 0
update_icon_mark = 0
for i, line in enumerate(lines):
    if pattern_command.search(line):
        if not update_exe_mark :
            print(f"更新{exe_filename}路径为:{exe_path}")
            update_exe_mark = 1
        new_line = '@="\\"' + new_exe_path + '\\" \\"%1\\""' + '\n'
    elif pattern_Icon.search(line):
        if not update_icon_mark:
            print(f"更新{Icon_filename}路径为:{Icon_path}")
            update_icon_mark = 1
        new_line = '"Icon"="' + new_Icon_path + '"' + '\n'
    else:
        new_line = line
    new_lines.append(new_line)

# 将修改后的内容写回add_mouse_right_func.reg文件，使用UTF-8编码
try:
    with open(reg_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)
    print(f"注册表文件{reg_filename}已更新。")
except Exception as e:
    print(f"写入注册表文件{reg_filename}时出错: {e}")
    sys.exit(1)

