import os
import shutil
import zipfile
import tarfile
import datetime
import tkinter as tk
from tkinter import messagebox
import sys

def unzip(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def untar(tar_path, extract_path, mode='r:*'):
    with tarfile.open(tar_path, mode) as tar_ref:
        tar_ref.extractall(extract_path)

def get_folder_name_from_file_path(file_path):
    # 获取文件的基本名称，不包括文件扩展名
    return os.path.splitext(os.path.basename(file_path))[0]

def handle_single_file(file_path):
    """解压单个文件并记录日志"""
    if not os.path.exists(file_path):
        return
    # # 获取压缩文件的基本名称，用作解压后的文件夹名称
    folder_name = get_folder_name_from_file_path(file_path)
    # # extract_path = os.path.join(os.path.dirname(file_path), folder_name)
    # # 解压路径为压缩包所在路径
    # extract_path = os.path.dirname(file_path)
    extract_path = os.path.join(os.path.dirname(file_path), folder_name)

    # 如果目标文件夹已存在，跳过解压
    if os.path.exists(extract_path):
        print(f"The folder {folder_name} already exists. Skipping extraction.")
        return    
    
    if file_path.endswith('.zip'):
        unzip(file_path, extract_path)
        handle_folder(extract_path)
    elif file_path.endswith('.tar'):
        untar(file_path, extract_path)
        handle_folder(extract_path)
    elif file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
        untar(file_path, extract_path, mode='r:gz')
        handle_folder(extract_path)
    elif file_path.endswith('.gz'):
        # .gz files are usually single file archives, not directories
        # You might want to handle them differently
        print(".gz files are not typically directories and may need special handling.")
    else:
        print("Unsupported file type.")

    # write_log(log_content)

def handle_folder(folderpath):
    print(folderpath + " is a path")

    if not os.path.exists(folderpath):
        print(f"The folder {folderpath} does not exists. Skipping")
        return 
    # log_content = f'开始解压文件夹：{folderpath}\n'    
    for entry in os.listdir(folderpath):
        full_path = os.path.join(folderpath, entry)
        if os.path.isdir(full_path):
            print(f'this is a path: {full_path}')
            handle_folder(full_path)  # 递归调用处理子文件夹
        else:
            print(f'this is a file: {full_path}')
            handle_single_file(full_path)
    # log_content += f'成功解压 {folderpath}\n'
    # write_log(log_content)

# def write_log(content):
#     """将日志内容写入日志文件"""
#     log_file = os.path.join(os.getcwd(), 'unzip_log.txt')
#     with open(log_file, 'a', encoding='utf-8') as f:
#         f.write(content)

def process(filepath):
    """处理文件或文件夹"""
    if os.path.isfile(filepath):
        # 选中单个文件
        print(filepath + " is a file")
        handle_single_file(filepath)
    elif os.path.isdir(filepath):
        # 选中文件夹
        
        answer = messagebox.askquestion('解压确认', f'是否解压文件夹 {filepath}?')
        if answer == 'yes':
            handle_folder(filepath)
        else:
            # print(f'已取消解压文件夹 {filepath}')
            print(filepath + " is a danger")


if __name__ == '__main__':
    # 获取传入参数
    filepath = sys.argv[1]
    print("Received arguments:", sys.argv[1])
    # 判断文件或文件夹是否存在
    if not os.path.exists(filepath):
        print(f'文件或文件夹不存在：{filepath}')
        exit(1)
    # 处理文件或文件夹
    process(filepath)
    input("\nPress Enter to exit...")
