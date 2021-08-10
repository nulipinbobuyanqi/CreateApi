# coding:utf-8
# @Author: wang_cong
# @File: get_deprecated_interface_info.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 16:46
from Utils.analysis_json_data import get_every_path_deprecated
from Utils.operation_log import initLogger

logger = initLogger(__file__)


# 获取所有已废弃接口列表
def get_all_deprecated_interfaces(new_json_data):
    """
    获取新版本中，所有已废弃接口列表
    :param old_json_data: 上个版本的json文件的所有内容，没有去除废弃的接口内容的json数据
    :return: 返回所有已废弃接口列表
    """
    deprecated_list = []  # 旧版本中，未变更的接口，组成的列表
    new_paths = new_json_data["paths"]
    new_path_list = list(new_paths.keys())
    for i in range(len(new_path_list)):
        new_deprecated = get_every_path_deprecated(new_paths, new_path_list[i])
        if new_deprecated:
            deprecated_list.append(new_path_list[i])
    logger.debug("新版本与旧版本相比，所有已废弃的接口，组成的列表是：{}".format(deprecated_list))
    return deprecated_list
