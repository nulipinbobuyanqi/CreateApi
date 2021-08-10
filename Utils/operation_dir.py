# coding:utf-8
# @Author: wang_cong
# @File: operation_dir.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/26 17:19
import os


def create_every_path_dirs(base_path, path):
    """
    使用"/"对传入的每个目录结构，进行切片，然后创建各个层级的目录名称
    :param base_path: 待创建的所有目录，其根目录
    :param path: 具体的每个含有层级关系的目录结构，例如：
    1. 只有一层目录结构时，写法为：目录A
    2. 不止一层目录结构时，写法为：目录A/目录B/目录C
    :return:
    """
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    os.chdir(base_path)
    every_path_list = [every_path for every_path in path.split('/') if every_path != '']
    if len(every_path_list) == 1:
        if not os.path.exists(every_path_list[0]):
            os.mkdir(every_path_list[0])
        os.chdir(every_path_list[0])
    elif len(every_path_list) >= 2:
        for every_path in every_path_list:
            if not os.path.exists(every_path):
                os.mkdir(every_path)
            os.chdir(every_path)
