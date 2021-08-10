# coding:utf-8
# @Author: wang_cong
# @File: get_no_change_interface_info.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 13:41
from Utils.operation_log import initLogger

logger = initLogger(__file__)


# 获取未变更接口信息，仅包括未变更的接口名称列表，包括未变更的这个接口的各项详细信息
def get_no_changes_interface_info(old_json_data, new_json_data):
    """
    获取新版本中，未变更的所有接口地址信息，返回未变更接口地址列表以及其他各项接口变更信息列表
    :param old_json_data: 上个版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :param new_json_data: 当前版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :return: 返回未变更接口地址列表以及其他各项接口变更信息列表
    """
    no_change_list = []  # 旧版本中，未变更的接口，组成的列表
    old_paths = old_json_data["paths"]
    new_paths = new_json_data["paths"]
    old_path_list = list(old_paths.keys())
    new_path_list = list(new_paths.keys())
    # 比较请求地址的数量
    if len(new_path_list) > len(old_path_list):  # 新版本数量大于旧版本
        # 比较旧版本中的每个接口地址，判断其是否在新版本中
        for i in range(len(old_path_list)):
            if old_path_list[i] in new_path_list:
                no_change_list.append(old_path_list[i])
    elif len(new_path_list) < len(old_path_list):  # 新版本数量小于旧版本
        # 比较旧版本中的每个接口地址，判断其是否在新版本中
        for i in range(len(old_path_list)):
            if old_path_list[i] in new_path_list:
                no_change_list.append(old_path_list[i])
    else:  # 新版本数量等于旧版本
        # 比较旧版本中的每个接口地址，判断其是否在新版本中
        for i in range(len(old_path_list)):
            if old_path_list[i] in new_path_list:
                no_change_list.append(old_path_list[i])
    # 此逻辑视项目而定，有些项目的此字段的值，写的不规范时，默认是false，若不改此字段的值，则影响统计
    # 从未变更的接口列表中，得到已废弃的接口，从未变更接口列表中去除
    # for i in range(len(no_change_list)):
    #     path = no_change_list[i]
    #     new_deprecated = get_every_path_deprecated(new_paths, path)
    #     if new_deprecated:
    #         delete_list.append(path)
    #         no_change_list.remove(path)
    logger.debug("新版本与旧版本相比，未变更的接口地址，组成的列表是：{}".format(no_change_list))
    return no_change_list
