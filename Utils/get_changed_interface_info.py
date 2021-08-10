# coding:utf-8
# @Author: wang_cong
# @File: get_changed_interface_info.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 13:41
from Utils.analysis_json_data import get_every_path_summary, get_every_path_method, get_every_path_parameter_type, \
    get_every_path_params, get_every_path_header
from Utils.operation_log import initLogger

logger = initLogger(__file__)


# 获取接口地址未变更的所有接口列表
def get_not_change_interface_info(old_json_data, new_json_data):
    """
    获取新版本中，接口地址未变更的所有接口列表
    :param old_json_data: 上个版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :param new_json_data: 当前版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :return: 返回接口地址未变更的所有接口列表
    """
    not_change_list = []  # 旧版本中，未变更的接口，组成的列表
    old_paths = old_json_data["paths"]
    new_paths = new_json_data["paths"]
    old_path_list = list(old_paths.keys())
    new_path_list = list(new_paths.keys())
    # 比较请求地址的数量
    if len(new_path_list) > len(old_path_list):  # 新版本数量大于旧版本
        # 比较旧版本中的每个接口地址，判断其是否在新版本中
        for i in range(len(old_path_list)):
            if old_path_list[i] in new_path_list:
                not_change_list.append(old_path_list[i])
    elif len(new_path_list) < len(old_path_list):  # 新版本数量小于旧版本
        # 比较旧版本中的每个接口地址，判断其是否在新版本中
        for i in range(len(old_path_list)):
            if old_path_list[i] in new_path_list:
                not_change_list.append(old_path_list[i])
    else:  # 新版本数量等于旧版本
        # 比较旧版本中的每个接口地址，判断其是否在新版本中
        for i in range(len(old_path_list)):
            if old_path_list[i] in new_path_list:
                not_change_list.append(old_path_list[i])
    # 此逻辑视项目而定，有些项目的此字段的值，写的不规范时，默认是false，若不改此字段的值，则影响统计
    # 从未变更的接口列表中，得到已废弃的接口，从未变更接口列表中去除
    # for i in range(len(not_change_list)):
    #     path = not_change_list[i]
    #     new_deprecated = get_every_path_deprecated(new_paths, path)
    #     if new_deprecated:
    #         delete_list.append(path)
    #         not_change_list.remove(path)
    logger.debug("新版本与旧版本相比，未变更的接口地址，组成的列表是：{}".format(not_change_list))
    return not_change_list


# 获取新版本中，接口描述发生变化的接口列表
def get_summary_changed_interface_info(old_json_data, new_json_data):
    """
    获取新版本中，接口描述发生变化的接口列表
    :param old_json_data: 上个版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :param new_json_data: 当前版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :return: 返回接口描述发生变化的接口列表
    """
    old_paths = old_json_data["paths"]
    new_paths = new_json_data["paths"]
    old_definition_list = []
    new_definition_list = []
    all_old_definitions = old_json_data['definitions']
    all_new_definitions = new_json_data['definitions']
    for definition in all_old_definitions:
        old_definition_list.append(definition)
    for definition in all_new_definitions:
        new_definition_list.append(definition)
    not_change_list = get_not_change_interface_info(old_json_data, new_json_data)
    # summary发生变化的接口，组成的列表
    summary_change_list = []
    # 接下来，获取未变更接口地址的各种变更信息
    for i in range(len(not_change_list)):
        path = not_change_list[i]
        old_summary = get_every_path_summary(old_paths, path)
        new_summary = get_every_path_summary(new_paths, path)
        change_dict = {
            path: {
                "老版本的接口请求描述": "",
                "新版本的接口请求描述": ""
            }
        }
        # 判断接口请求头是否有变化
        if old_summary != new_summary:
            change_dict[path]["老版本的接口请求描述"] = old_summary
            change_dict[path]["新版本的接口请求描述"] = new_summary
            summary_change_list.append(change_dict)
    # 接下来，再从这些接口信息变更了接口地址中，筛选出真正的，没有任何内容变更的接口信息列表
    # 合并目前这五大类列表，并去重，只要地址出现在任何一个列表中，都说明这个接口变更了
    all_list = []
    for s in summary_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    # 去重
    all_list = list(set(all_list))
    for address in all_list:
        if address in not_change_list:
            # 去除变更了的地址
            not_change_list.remove(address)
    logger.debug("新版本与旧版本相比，接口描述发生变更的接口，组成的列表是：{}".format(summary_change_list))
    return summary_change_list


# 获取新版本中，接口方法发生变化的接口列表
def get_method_changed_interface_info(old_json_data, new_json_data):
    """
    获取新版本中，接口方法发生变化的接口列表
    :param old_json_data: 上个版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :param new_json_data: 当前版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :return: 返回接口方法发生变化的接口列表
    """
    old_paths = old_json_data["paths"]
    new_paths = new_json_data["paths"]
    old_definition_list = []
    new_definition_list = []
    all_old_definitions = old_json_data['definitions']
    all_new_definitions = new_json_data['definitions']
    for definition in all_old_definitions:
        old_definition_list.append(definition)
    for definition in all_new_definitions:
        new_definition_list.append(definition)
    not_change_list = get_not_change_interface_info(old_json_data, new_json_data)
    # method发生变化的接口，组成的列表
    method_change_list = []
    # 接下来，获取未变更接口地址的各种变更信息
    for i in range(len(not_change_list)):
        path = not_change_list[i]
        old_method = get_every_path_method(old_paths, path)
        new_method = get_every_path_method(new_paths, path)
        change_dict = {
            path: {
                "老版本的接口请求方法": "",
                "新版本的接口请求方法": ""
            }
        }
        # 判断接口请求头是否有变化
        if old_method != new_method:
            change_dict[path]["老版本的接口请求方法"] = old_method
            change_dict[path]["新版本的接口请求方法"] = new_method
            method_change_list.append(change_dict)
    # 接下来，再从这些接口信息变更了接口地址中，筛选出真正的，没有任何内容变更的接口信息列表
    # 合并目前这五大类列表，并去重，只要地址出现在任何一个列表中，都说明这个接口变更了
    all_list = []
    for s in method_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    # 去重
    all_list = list(set(all_list))
    for address in all_list:
        if address in not_change_list:
            # 去除变更了的地址
            not_change_list.remove(address)
    logger.debug("新版本与旧版本相比，接口方法发生变更的接口，组成的列表是：{}".format(method_change_list))
    return method_change_list


# 获取新版本中，接口参数类型发生变化的接口列表
def get_parameter_type_changed_interface_info(old_json_data, new_json_data):
    """
    获取新版本中，接口参数类型发生变化的接口列表
    :param old_json_data: 上个版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :param new_json_data: 当前版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :return: 返回接口参数类型发生变化的接口列表
    """
    old_paths = old_json_data["paths"]
    new_paths = new_json_data["paths"]
    old_definition_list = []
    new_definition_list = []
    all_old_definitions = old_json_data['definitions']
    all_new_definitions = new_json_data['definitions']
    for definition in all_old_definitions:
        old_definition_list.append(definition)
    for definition in all_new_definitions:
        new_definition_list.append(definition)
    not_change_list = get_not_change_interface_info(old_json_data, new_json_data)
    # parameter_type发生变化的接口，组成的列表
    parameter_type_change_list = []
    # 接下来，获取未变更接口地址的各种变更信息
    for i in range(len(not_change_list)):
        path = not_change_list[i]
        old_parameter_type = get_every_path_parameter_type(old_paths, path)
        new_parameter_type = get_every_path_parameter_type(new_paths, path)
        change_dict = {
            path: {
                "老版本的接口请求参数类型": "",
                "新版本的接口请求参数类型": ""
            }
        }
        # 判断接口请求头是否有变化
        if old_parameter_type != new_parameter_type:
            change_dict[path]["老版本的接口请求参数类型"] = old_parameter_type
            change_dict[path]["新版本的接口请求参数类型"] = new_parameter_type
            parameter_type_change_list.append(change_dict)
    # 接下来，再从这些接口信息变更了接口地址中，筛选出真正的，没有任何内容变更的接口信息列表
    # 合并目前这五大类列表，并去重，只要地址出现在任何一个列表中，都说明这个接口变更了
    all_list = []
    for s in parameter_type_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    # 去重
    all_list = list(set(all_list))
    for address in all_list:
        if address in not_change_list:
            # 去除变更了的地址
            not_change_list.remove(address)
    logger.debug("新版本与旧版本相比，接口参数类型发生变更的接口，组成的列表是：{}".format(parameter_type_change_list))
    return parameter_type_change_list


# 获取新版本中，接口参数发生变化的接口列表
def get_parameter_changed_interface_info(old_json_data, new_json_data):
    """
    获取新版本中，接口参数发生变化的接口列表
    :param old_json_data: 上个版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :param new_json_data: 当前版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :return: 返回接口参数发生变化的接口列表
    """
    old_paths = old_json_data["paths"]
    new_paths = new_json_data["paths"]
    old_definition_list = []
    new_definition_list = []
    all_old_definitions = old_json_data['definitions']
    all_new_definitions = new_json_data['definitions']
    for definition in all_old_definitions:
        old_definition_list.append(definition)
    for definition in all_new_definitions:
        new_definition_list.append(definition)
    not_change_list = get_not_change_interface_info(old_json_data, new_json_data)
    # params发生变化的接口，组成的列表
    params_change_list = []
    # 接下来，获取未变更接口地址的各种变更信息
    for i in range(len(not_change_list)):
        path = not_change_list[i]
        old_parameter = get_every_path_params(old_paths, path, old_definition_list, all_old_definitions)
        new_parameter = get_every_path_params(new_paths, path, new_definition_list, all_new_definitions)
        change_dict = {
            path: {
                "老版本的接口请求参数": "",
                "新版本的接口请求参数": ""
            }
        }
        # 判断接口参数是否有变化
        if old_parameter != new_parameter:
            change_dict[path]["老版本的接口请求参数"] = old_parameter
            change_dict[path]["新版本的接口请求参数"] = new_parameter
            params_change_list.append(change_dict)
    # 接下来，再从这些接口信息变更了接口地址中，筛选出真正的，没有任何内容变更的接口信息列表
    # 合并目前这五大类列表，并去重，只要地址出现在任何一个列表中，都说明这个接口变更了
    all_list = []
    for s in params_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    # 去重
    all_list = list(set(all_list))
    for address in all_list:
        if address in not_change_list:
            # 去除变更了的地址
            not_change_list.remove(address)
    logger.debug("新版本与旧版本相比，接口参数发生变更的接口，组成的列表是：{}".format(params_change_list))
    return params_change_list


# 获取新版本中，接口请求头发生变化的接口列表
def get_header_changed_interface_info(old_json_data, new_json_data):
    """
    获取新版本中，接口请求头发生变化的接口列表
    :param old_json_data: 上个版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :param new_json_data: 当前版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :return: 返回接口请求头发生变化的接口列表
    """
    old_paths = old_json_data["paths"]
    new_paths = new_json_data["paths"]
    old_definition_list = []
    new_definition_list = []
    all_old_definitions = old_json_data['definitions']
    all_new_definitions = new_json_data['definitions']
    for definition in all_old_definitions:
        old_definition_list.append(definition)
    for definition in all_new_definitions:
        new_definition_list.append(definition)
    not_change_list = get_not_change_interface_info(old_json_data, new_json_data)
    # header发生变化的接口，组成的列表
    header_change_list = []
    # 接下来，获取未变更接口地址的各种变更信息
    for i in range(len(not_change_list)):
        path = not_change_list[i]
        old_header = get_every_path_header(old_paths, path, old_definition_list, all_old_definitions)
        new_header = get_every_path_header(new_paths, path, new_definition_list, all_new_definitions)
        change_dict = {
            path: {
                "老版本的接口请求头": "",
                "新版本的接口请求头": ""
            }
        }
        # 判断接口请求头是否有变化
        if old_header != new_header:
            change_dict[path]["老版本的接口请求头"] = old_header
            change_dict[path]["新版本的接口请求头"] = new_header
            header_change_list.append(change_dict)
    # 接下来，再从这些接口信息变更了接口地址中，筛选出真正的，没有任何内容变更的接口信息列表
    # 合并目前这五大类列表，并去重，只要地址出现在任何一个列表中，都说明这个接口变更了
    all_list = []
    for s in header_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    # 去重
    all_list = list(set(all_list))
    for address in all_list:
        if address in not_change_list:
            # 去除变更了的地址
            not_change_list.remove(address)
    logger.debug("新版本与旧版本相比，接口请求头发生变更的接口，组成的列表是：{}".format(header_change_list))
    return header_change_list
