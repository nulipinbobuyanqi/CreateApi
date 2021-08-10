# coding:utf-8
# @Author: wang_cong
# @File: get_delete_interface_info.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 13:40
from Utils.operation_log import initLogger

logger = initLogger(__file__)


# 获取已删除接口信息，仅包括已删除的接口名称列表，不包括已删除的这个接口的各项详细信息
def get_deleted_interface_info(old_json_data, new_json_data):
    """
    获取新版本中，已删除的所有接口地址信息，返回已删除接口地址列表
    :param old_json_data: 上个版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :param new_json_data: 当前版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :return: 返回已删除接口地址列表
    """
    delete_list = []  # 旧版本中，被删除的接口，组成的列表
    old_paths = old_json_data["paths"]
    new_paths = new_json_data["paths"]
    old_path_list = list(old_paths.keys())
    new_path_list = list(new_paths.keys())
    # 比较请求地址的数量
    if len(new_path_list) > len(old_path_list):  # 新版本数量大于旧版本
        # 比较旧版本中的每个接口地址，判断其是否在新版本中
        for i in range(len(old_path_list)):
            if old_path_list[i] not in new_path_list:
                delete_list.append(old_path_list[i])
    elif len(new_path_list) < len(old_path_list):  # 新版本数量小于旧版本
        # 比较旧版本中的每个接口地址，判断其是否在新版本中
        for i in range(len(old_path_list)):
            if old_path_list[i] not in new_path_list:
                delete_list.append(old_path_list[i])
    else:  # 新版本数量等于旧版本
        # 比较旧版本中的每个接口地址，判断其是否在新版本中
        for i in range(len(old_path_list)):
            if old_path_list[i] not in new_path_list:
                delete_list.append(old_path_list[i])
    logger.debug("新版本与旧版本相比，被删除的接口地址，组成的列表是：{}".format(delete_list))
    return delete_list
