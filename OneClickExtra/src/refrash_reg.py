import os
import re

def add_backslash(path):
    new_path = ""
    for char in path:
        if char == "\\":
            new_path += "\\\\"
        else:
            new_path += char
    return new_path
# 获取当前工作目录
current_path = os.getcwd()

# 构造OneClickExtra.exe的绝对路径
exe_filename = 'OneClickExtra.exe'
Icon_filename = 'point-up.ico'
exe_path = os.path.join(current_path, exe_filename)
Icon_path = os.path.join(current_path, Icon_filename)
new_exe_path = add_backslash(exe_path)
new_Icon_path = add_backslash(Icon_path)
pattern_command = re.compile(r'OneClickExtra.exe')
pattern_Icon = re.compile(r'Icon')
# 读取add_mouse_right_func.reg文件的内容，尝试使用UTF-8编码和忽略BOM
try:
    with open('add_mouse_right_func.reg', 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
except FileNotFoundError:
    print("文件 'add_mouse_right_func.reg' 不存在。")
    exit()

new_lines = []
for i, line in enumerate(lines):
    if pattern_command.search(line):
        print(f"替换OneClickExtra.exe路径为 {exe_path}")
        new_line = '@="\\"' + new_exe_path + '\\" \\"%1\\""' + '\n'
    elif pattern_Icon.search(line):
        print(f"替换Icon路径为 {Icon_path}")
        new_line = '"Icon"="' + new_Icon_path + '"' + '\n'
    else:
        new_line = line
    new_lines.append(new_line)

# 将修改后的内容写回add_mouse_right_func.reg文件，使用UTF-8编码
try:
    with open('add_mouse_right_func.reg', 'w', encoding='utf-8') as file:
        file.writelines(new_lines)
    print("文件 'add_mouse_right_func.reg' 已更新。")
except Exception as e:
    print(f"写入文件时出错: {e}")

