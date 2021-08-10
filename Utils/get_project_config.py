# coding:utf-8
# @Author: wang_cong
# @File: get_project_config.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/28 16:05
from Utils.operation_yml import get_yaml_data


def get_project_config_info(project_path):
    config_yaml_path = project_path + "01.ProjectConfig"
    config_yaml_file_name = "ProjectConfig"
    config_yaml_data = get_yaml_data(config_yaml_path, config_yaml_file_name)
    project = config_yaml_data["project_name"]
    protocol = config_yaml_data["protocal"]
    swagger_host = config_yaml_data["swagger_info"]["swagger_host"]
    swagger_basePath = config_yaml_data["swagger_info"]["swagger_basePath"]
    swagger_path = config_yaml_data["swagger_info"]["swagger_path"]
    if swagger_basePath == "/":
        swagger_url = protocol + "://" + swagger_host + swagger_path
    else:
        swagger_url = protocol + "://" + swagger_host + swagger_basePath + swagger_path
    return project, protocol, swagger_url
