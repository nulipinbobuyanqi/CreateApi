# coding:utf-8
# @Author: wang_cong
# @File: get_new_interface_info.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 13:40
from Utils.analysis_json_data import get_every_path_summary, get_every_path_method, get_every_path_parameter_type, \
    get_every_path_params, get_every_path_header, get_every_path_deprecated, get_every_path_tags


# 获取新增接口信息，仅包括新增的接口名称列表，不包括新增的这个接口的各项详细信息
def get_new_interface_info(old_json_data, new_json_data):
    """
    获取新版本中，新增的所有接口地址信息，返回新增接口地址列表
    :param old_json_data: 上个版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :param new_json_data: 当前版本的json文件的所有内容，已去除废弃的接口内容的json数据
    :return: 返回新增接口地址列表
    """
    new_interface_info = [

    ]
    new_list = []  # 新版本中，新增的接口，组成的列表
    old_paths = old_json_data["paths"]
    new_paths = new_json_data["paths"]
    old_path_list = list(old_paths.keys())
    new_path_list = list(new_paths.keys())
    new_definition_list = []
    all_new_definitions = new_json_data['definitions']
    for definition in all_new_definitions:
        new_definition_list.append(definition)
    definition_list = new_definition_list
    all_paths = new_paths
    all_definitions = all_new_definitions
    # 比较请求地址的数量
    if len(new_path_list) > len(old_path_list):  # 新版本数量大于旧版本
        # 比较新版本中的每个接口地址，判断其是否在旧版本中
        for i in range(len(new_path_list)):
            if new_path_list[i] not in old_path_list:
                new_list.append(new_path_list[i])
    elif len(new_path_list) < len(old_path_list):  # 新版本数量小于旧版本
        # 比较新版本中的每个接口地址，判断其是否在旧版本中
        for i in range(len(new_path_list)):
            if new_path_list[i] not in old_path_list:
                new_list.append(new_path_list[i])
    else:  # 新版本数量等于旧版本
        # 比较新版本中的每个接口地址，判断其是否在旧版本中
        for i in range(len(new_path_list)):
            if new_path_list[i] not in old_path_list:
                new_list.append(new_path_list[i])
    # 此逻辑视项目而定，有些项目的此字段的值，写的不规范时，默认是false，若不改此字段的值，则影响统计
    # 从新增的接口列表中，得到已废弃的接口，从新增接口列表中去除
    # for i in range(len(new_list)):
    #     path = new_list[i]
    #     new_deprecated = get_every_path_deprecated(new_paths, path)
    #     if new_deprecated:
    #         delete_list.append(path)
    #         new_list.remove(path)
    for i in range(len(new_list)):
        if new_path_list[i] not in old_path_list:
            path = new_path_list[i]
            interface_template = {}
            # 接口协议interface_protocol
            interface_template['interface_protocol'] = "interface_protocol"
            # 接口名称interface_name
            interface_template['interface_name'] = get_every_path_summary(all_paths, path)
            # 所属模块belong_module
            interface_template['belong_module'] = get_every_path_tags(all_paths, path)
            # 接口地址interface_address
            interface_template['interface_address'] = path
            # 请求方法interface_method
            interface_template['interface_method'] = get_every_path_method(all_paths, path)
            # 请求参数类型interface_parameters_type
            interface_template['interface_parameters_type'] = get_every_path_parameter_type(all_paths, path)
            # 请求参数interface_parameters
            interface_template['interface_parameters'] = get_every_path_params(all_paths, path, definition_list,
                                                                               all_definitions)
            # 请求头interface_headers
            interface_template['interface_headers'] = get_every_path_header(all_paths, path, definition_list,
                                                                            all_definitions)
            # 接口是否已弃用
            interface_template['deprecated'] = get_every_path_deprecated(all_paths, path)
            new_interface_info.append(interface_template)
    return new_list, new_interface_info

