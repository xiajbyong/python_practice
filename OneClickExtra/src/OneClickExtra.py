import os
import shutil
import zipfile
import tarfile
import datetime
import tkinter as tk
from tkinter import messagebox
import sys
import gzip
from concurrent.futures import ThreadPoolExecutor, as_completed

def unzip(zip_path, extract_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except Exception as e:
        print(f"Failed to unzip {zip_path}: {e}")

def untar(tar_path, extract_path, mode='r:*'):
    try:
        with tarfile.open(tar_path, mode) as tar_ref:
            tar_ref.extractall(extract_path)
    except Exception as e:
        print(f"Failed to untar {tar_path}: {e}")

def ungz(gz_path):
    try:
        with gzip.open(gz_path, 'rb') as f_in:
            with open(gz_path[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        print(f"Failed to ungz {gz_path}: {e}")

def untar_bz2(tar_path, extract_path):
    try:
        with tarfile.open(tar_path, 'r:bz2') as tar_ref:
            tar_ref.extractall(extract_path)
    except Exception as e:
        print(f"Failed to untar_bz2 {tar_path}: {e}")

# 获取文件的基本名称，不包括文件扩展名
def get_folder_name_from_file_path(file_path):
    base_name = os.path.basename(file_path)
    
    # 检查文件扩展名是否为 '.tar.gz' 或 '.tar.bz2'
    if base_name.endswith('.tar.gz'):
        base_name = base_name[:-7]
    elif base_name.endswith('.tar.bz2'):
        base_name = base_name[:-8]
    else:
        # 如果不是，使用os.path.splitext获取文件名和扩展名
        base_name, ext = os.path.splitext(base_name)
    
    return base_name

def handle_single_file(file_path):
    if not os.path.exists(file_path):
        return
    # 获取压缩文件的基本名称，用作解压后的文件夹名称
    folder_name = get_folder_name_from_file_path(file_path)
    extract_path = os.path.join(os.path.dirname(file_path), folder_name)
    # # 解压路径为压缩包所在路径
    # extract_path = os.path.dirname(file_path)

    # 如果目标文件夹已存在，跳过解压
    if os.path.exists(extract_path):
        print(f"The folder {folder_name} already exists. Skipping extraction.")
        return    
    
    if file_path.endswith('.zip'):
        unzip(file_path, extract_path)
        handle_folder_multithreaded(extract_path)
    elif file_path.endswith('.tar'):
        untar(file_path, extract_path)
        handle_folder_multithreaded(extract_path)
    elif file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
        untar(file_path, extract_path, mode='r:gz')
        handle_folder_multithreaded(extract_path)
    elif file_path.endswith('.tar.bz2'):
        untar_bz2(file_path, extract_path)
        handle_folder_multithreaded(extract_path)    
    elif file_path.endswith('.gz'):
        # .gz files are usually single file archives, just unzip the single file to PWD
        ungz(file_path)
        # print(".gz files are not typically directories and may need special handling.")
    else:
        print("Unsupported file type.")

    # write_log(log_content)

# def handle_folder(folderpath):
#     if not os.path.exists(folderpath):
#         # print(f"The folder {folderpath} does not exists.")
#         return 
#     if not os.path.isdir(folderpath):
#         # print(f'this is not a folder: {folderpath}')
#         return
#     # log_content = f'开始解压文件夹
#     for entry in os.listdir(folderpath):
#         full_path = os.path.join(folderpath, entry)
#         if os.path.isdir(full_path):
#             # print(f'this is a path: {full_path}')
#             handle_folder(full_path)  # 递归调用处理子文件夹
#         else:
#             # print(f'this is a file: {full_path}')
#             handle_single_file(full_path)
#             print(f'extra {full_path} successful')

# def process(sellect_path):
#     if os.path.isdir(sellect_path):
#         # print(f'this is a folder: {sellect_path}')
#         # 创建一个隐藏的Tk窗口实例作为messagebox的父窗口
#         root = tk.Tk()
#         root.withdraw()  # 隐藏窗口，不显示在屏幕上        
#         answer = messagebox.askquestion('解压确认', f'是否解压文件夹 {sellect_path}?')
#         if answer == 'yes':
#             handle_folder(sellect_path)  # 递归调用处理子文件夹
#     else:
#         # print(f'this is a file: {sellect_path}')
#         handle_single_file(sellect_path)

# if __name__ == '__main__':
#     # 获取传入参数
#     # sellect_path = r'D:\01 工作\03 维护\03 巡检\20240416-科威特例行巡检\E9000H_LogCollect_20240417101028\LogCollect_20240417101028\LogCollectResult\20240417101106\10.23.14.28\Datacollect_2103050EET10M9000095_20240417101830901'
#     sellect_path = sys.argv[1]
#     # print("Received arguments:", sys.argv[1])
#     # 判断文件或文件夹是否存在
#     if not os.path.exists(sellect_path):
#         print(f'选中的文件或文件夹不存在：{sellect_path}. Skipping')
#         exit(1)
#     # 处理文件或文件夹
#     process(sellect_path)
#     input("\nPress Enter to exit...")

# 增加线程池来处理文件和文件夹
def handle_folder_multithreaded(folderpath, max_workers=4):
    if not os.path.exists(folderpath):
        return
    if not os.path.isdir(folderpath):
        return

    # 使用线程池处理子文件和子文件夹
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {}

        # 遍历文件夹内容
        for entry in os.listdir(folderpath):
            full_path = os.path.join(folderpath, entry)
            if os.path.isdir(full_path):
                # 对子文件夹递归处理
                future = executor.submit(handle_folder_multithreaded, full_path, max_workers)
                future_to_path[future] = full_path
            else:
                # 对文件调用解压处理
                future = executor.submit(handle_single_file, full_path)
                future_to_path[future] = full_path

        # 等待所有任务完成
        for future in as_completed(future_to_path):
            try:
                future.result()  # 获取任务执行结果
                print(f"Processed: {future_to_path[future]}")
            except Exception as e:
                print(f"Error processing {future_to_path[future]}: {e}")

# 主处理逻辑调用多线程版本
def process_multithreaded(sellect_path, max_workers=4):
    if os.path.isdir(sellect_path):
        root = tk.Tk()
        root.withdraw()
        answer = messagebox.askquestion('解压确认', f'是否解压文件夹 {sellect_path}?')
        if answer == 'yes':
            handle_folder_multithreaded(sellect_path, max_workers)
    else:
        handle_single_file(sellect_path)

if __name__ == '__main__':
    sellect_path = sys.argv[1]
    if not os.path.exists(sellect_path):
        print(f'选中的文件或文件夹不存在：{sellect_path}. Skipping')
        exit(1)
    process_multithreaded(sellect_path, max_workers=4)
    input("\nPress Enter to exit...")