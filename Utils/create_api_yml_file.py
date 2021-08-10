# coding:utf-8
# @Author: wang_cong
# @File: create_api_yml_file.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 9:49
import re
from Template.interface_template import interface_template
from Utils.analysis_json_data import get_every_path_summary, get_every_path_method, get_every_path_parameter_type, \
    get_every_path_params, get_every_path_header, get_every_path_deprecated, get_every_path_tags
from Utils.operation_yml import save_ruamel_data
from Utils.operation_log import initLogger

logger = initLogger(__file__)


# 生成yml文件，填入接口信息
def create_api_yml_file(all_paths, interface_base_path, definition_list, all_definitions):
    all_yml_file_path_list = []
    for path in all_paths:
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
        interface_template['interface_parameters'] = get_every_path_params(all_paths, path, definition_list, all_definitions)
        # 请求头interface_headers
        interface_template['interface_headers'] = get_every_path_header(all_paths, path, definition_list, all_definitions)
        # 接口是否已弃用
        interface_template['deprecated'] = get_every_path_deprecated(all_paths, path)
        # 最后，生成每个接口模板信息yml文件
        path = re.sub(r"{.*}", "", path, count=0, flags=0)
        interface_yml_path = interface_base_path + path
        all_yml_file_path_list.append(interface_yml_path.replace("\\", "/"))
        if path.split("/")[-1] != "":
            yaml_file_name = path.split("/")[-1]
        else:
            yaml_file_name = path.split("/")[-2]
        yaml_data = interface_template
        save_ruamel_data(interface_yml_path, yaml_file_name, yaml_data)
    # logger.debug(all_yml_file_path_list)
    return all_yml_file_path_list
