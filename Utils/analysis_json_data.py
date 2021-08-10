# coding:utf-8
# @Author: wang_cong
# @File: analysis_json_data.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 9:46
from Utils.operation_log import initLogger

logger = initLogger(__file__)


# 分析json文件的数据，从中获取每个接口的名称
def get_every_path_summary(all_paths, path):
    """
    获取每个接口的名称，返回值是str类型的数据
    :param all_paths: 所有接口的地址信息
    :param path: 每个接口的请求地址
    :return: str类型的数据
    """
    for method in all_paths[path].keys():
        if 'summary' in all_paths[path][method].keys():
            summary = all_paths[path][method]['summary']
            return summary


# 分析json文件的数据，从中获取每个接口的所属模块
def get_every_path_tags(all_paths, path):
    """
    获取每个接口的所属模块，返回值是str类型的数据
    :param all_paths: 所有接口的地址信息
    :param path: 每个接口的请求地址
    :return: str类型的数据
    """
    for method in all_paths[path].keys():
        if 'tags' in all_paths[path][method].keys():
            tags = all_paths[path][method]['tags'][0]
            return tags


# 分析json文件的数据，从中获取每个接口的请求方法
def get_every_path_method(all_paths, path):
    """
    获取每个接口的请求方法，返回值是str类型的数据
    :param all_paths: 所有接口的地址信息
    :param path: 每个接口的请求地址
    :return: str类型的数据
    """
    for method in all_paths[path].keys():
        return method


# 分析json文件的数据，从中获取每个接口的请求参数类型
def get_every_path_parameter_type(all_paths, path):
    """
    获取每个接口的请求参数类型，返回值是str类型的数据
    :param all_paths: 所有接口的地址信息
    :param path: 每个接口的请求地址
    :return: str类型的数据
    """
    for method in all_paths[path].keys():
        if 'consumes' in all_paths[path][method].keys():
            parameter_type = all_paths[path][method]['consumes'][0]
            return parameter_type


# 分析json文件的数据，从中获取每个接口的废弃状态
def get_every_path_deprecated(all_paths, path):
    """
    获取每个接口的废弃状态，返回值是str类型的数据
    :param all_paths: 所有接口的地址信息
    :param path: 每个接口的请求地址
    :return: str类型的数据
    """
    for method in all_paths[path].keys():
        if 'deprecated' in all_paths[path][method].keys():
            deprecated = all_paths[path][method]['deprecated']
            return deprecated


# 分析json文件的数据，从中获取每个接口的请求参数
def get_every_path_parameters(all_paths, path, definition_list, all_definitions):
    """
    获取每个接口的请求参数，返回值是dict类型的数据
    :param all_paths: 所有接口的地址信息
    :param path: 每个接口的请求地址
    :param definition_list: 每个接口的要被替换的参数名组成的列表
    :param all_definitions: 所有接口的要被替换的参数信息
    :return: dict类型的数据
    """
    parameter_dict = {}
    all_param_name_list = []
    all_paths_list = all_paths
    for method in all_paths_list[path].keys():
        if 'parameters' in all_paths_list[path][method].keys():
            parameters = all_paths_list[path][method]['parameters']  # list类型
            for i in range(0, len(parameters)):
                name = all_paths_list[path][method]['parameters'][i]['name']
                all_param_name_list.append(name)  # 这是所有参数的名称，组成的list
                if 'schema' in all_paths_list[path][method]['parameters'][i].keys():
                    if '$ref' in all_paths_list[path][method]['parameters'][i]['schema'].keys():
                        ref = all_paths_list[path][method]['parameters'][i]['schema']['$ref'].split('/')[-1]
                        ref = ref.split('/')[-1]
                        for replace_parameter in definition_list:
                            if replace_parameter == ref:
                                all_param_name_list[all_param_name_list.index(name)] = ref
                                params = all_definitions[replace_parameter]['properties'].keys()
                                for pp in list(params):
                                    parameter_dict[pp] = pp
                                    all_param_name_list.append(pp)
                                all_param_name_list.remove(ref)
                                for pa in params:
                                    parameter_dict[pa] = all_definitions[replace_parameter]['properties'][pa]
                                    if 'type' in parameter_dict[pa].keys():
                                        if parameter_dict[pa]['type'] == 'array':
                                            if 'items' in parameter_dict[pa].keys():
                                                if '$ref' in parameter_dict[pa]['items']:
                                                    original = parameter_dict[pa]['items']['$ref'].split("/")[-1]
                                                    for origin in definition_list:
                                                        if original == origin:
                                                            original_value = all_definitions[original]['properties']
                                                            original_params = all_definitions[original]['properties'].keys()
                                                            parameter_dict[pa] = []
                                                            parameter_replace_dict = {}
                                                            for p_k in original_params:
                                                                parameter_replace_dict[p_k] = original_value[p_k]
                                                            parameter_dict[pa].append(parameter_replace_dict)
                                        else:
                                            if 'items' in parameter_dict[pa].keys():
                                                if '$ref' in parameter_dict[pa]['items']:
                                                    original = parameter_dict[pa]['items']['$ref'].split("/")[-1]
                                                    for origin in definition_list:
                                                        if original == origin:
                                                            original_value = all_definitions[original]['properties']
                                                            original_params = all_definitions[original]['properties'].keys()
                                                            parameter_dict[pa] = {}
                                                            parameter_replace_dict = {}
                                                            for p_k in original_params:
                                                                parameter_replace_dict[p_k] = original_value[p_k]
                                                            parameter_dict[pa] = parameter_replace_dict
                                    else:
                                        if 'items' in parameter_dict[pa].keys():
                                            pass
                                        else:
                                            if '$ref' in parameter_dict[pa].keys():
                                                original = parameter_dict[pa]['$ref'].split("/")[-1]
                                                for origin in definition_list:
                                                    if original == origin:
                                                        original_value = all_definitions[original]['properties']
                                                        original_params = all_definitions[original]['properties'].keys()
                                                        parameter_dict[pa] = {}
                                                        parameter_replace_dict = {}
                                                        for p_k in original_params:
                                                            parameter_replace_dict[p_k] = original_value[p_k]
                                                        parameter_dict[pa] = parameter_replace_dict
                    else:
                        if 'type' in all_paths_list[path][method]['parameters'][i]['schema'].keys():
                            parameter_dict[name] = all_paths_list[path][method]['parameters'][i]
                else:
                    parameter_dict[name] = all_paths_list[path][method]['parameters'][i]
        else:
            logger.debug("{}接口不存在parameters字段，也就是说，不需要传参")
            pass
    logger.debug("{}----未去除请求头的参数，请求参数是-----{}".format(path, parameter_dict))
    return parameter_dict


# 分析json文件的数据，从中获取每个接口的请求参数，这个参数是去除了请求头的有效请求参数
def get_every_path_params(all_paths, path, definition_list, all_definitions):
    """
    获取每个接口的请求头，返回值是dict类型的数据
    :param all_paths: 所有接口的地址信息
    :param path: 每个接口的请求地址
    :param definition_list: 每个接口的要被替换的参数名组成的列表
    :param all_definitions: 所有接口的要被替换的参数信息
    :return: dict类型的数据
    """
    # 请求参数interface_parameters，注意：将请求头中需要的key从参数里去除
    interface_parameters = get_every_path_parameters(all_paths, path, definition_list, all_definitions)
    logger.debug("{}----未去除请求头的参数，请求参数是-----{}".format(path, interface_parameters))
    # 请求头interface_headers，注意：登录接口不需要token，清除headers里面的信息
    for key in list(interface_parameters.keys()):
        if key in ['token', 'cpytoken', 'Authorization']:
            interface_parameters.pop(key)
    logger.debug("{}----去除请求头的参数之后，有效的请求参数是-----{}".format(path, interface_parameters))
    logger.debug("{}----去除请求头的参数之后，有效的请求参数的key组成的列表是-----{}".format(path, list(interface_parameters.keys())))
    return interface_parameters


# 分析json文件的数据，从中获取每个接口的请求头
def get_every_path_header(all_paths, path, definition_list, all_definitions):
    """
    获取每个接口的请求头，返回值是dict类型的数据
    :param all_paths: 所有接口的地址信息
    :param path: 每个接口的请求地址
    :param definition_list: 每个接口的要被替换的参数名组成的列表
    :param all_definitions: 所有接口的要被替换的参数信息
    :return: dict类型的数据
    """
    interface_headers = {}
    # 请求参数interface_parameters，注意：将请求头中需要的key从参数里去除
    interface_parameters = get_every_path_parameters(all_paths, path, definition_list, all_definitions)
    # 请求头interface_headers，注意：登录接口不需要token，清除headers里面的信息
    for key in list(interface_parameters.keys()):
        if key in ['token', 'cpytoken', 'Authorization']:
            # interface_headers[key] = interface_parameters[key]
            interface_headers[key] = '${' + key + '}$'
            interface_parameters.pop(key)
    if path.split("/")[-1] == "login":
        interface_headers = {}
    else:
        interface_headers = interface_headers
    logger.debug("{}----请求头是-----{}".format(path, interface_headers))
    return interface_headers


