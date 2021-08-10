# coding:utf-8
# @Author: wang_cong
# @File: StartRun.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 19:12


import os
import re
import time
import requests
from Utils.create_api_yml_file import create_api_yml_file
from Utils.get_changed_interface_info import get_summary_changed_interface_info, \
    get_method_changed_interface_info, get_parameter_type_changed_interface_info, get_parameter_changed_interface_info, \
    get_header_changed_interface_info
from Utils.get_delete_interface_info import get_deleted_interface_info
from Utils.get_deprecated_interface_info import get_all_deprecated_interfaces
from Utils.get_new_interface_info import get_new_interface_info
from Utils.get_no_change_interface_info import get_no_changes_interface_info
from Utils.get_project_config import get_project_config_info
from Utils.operation_dir import create_every_path_dirs
from Utils.operation_json import save_json_data, get_json_data
from Utils.operation_yml import get_yaml_data, save_ruamel_data


# 获取当前日期，作为接口版本号
new = time.strftime("%Y-%m-%d", time.localtime())
# new = "2021-06-01"
# 获取项目配置信息的存放根路径
project_yaml_path = "."
project_yaml_file_name = "project_path"
gen_path = get_yaml_data(project_yaml_path, project_yaml_file_name)["project_path"]
project_path = gen_path + "/ProjectManage/"
project_config_path = project_path + "01.ProjectConfig"
if not os.path.exists(project_config_path):
    os.makedirs(project_config_path)
# 获取项目配置信息
project, protocol, swagger_url = get_project_config_info(project_path)
# 创建接口信息json文件的存放根目录
interfaces_gen_path = project_path + "02.InterfaceData" + "/" + project
if not os.path.exists(interfaces_gen_path):
    os.makedirs(interfaces_gen_path)
# 创建接口信息模板yml文件存放根目录
api_template_gen_path = project_path + "03.InterfaceTemplate" + "/" + project
if not os.path.exists(api_template_gen_path):
    os.makedirs(api_template_gen_path)
# 创建不同版本之间的区别报告根目录
api_change_report_gen_path = project_path + "04.InterfaceChangeReport" + "/" + project
if not os.path.exists(api_change_report_gen_path):
    os.makedirs(api_change_report_gen_path)
# 爬取swagger地址，获取接口信息
swagger_dict_res = requests.request(method="GET", url=swagger_url).json()
# 无论是否为首次测试该项目的接口，当前日期都在爬取swagger的地址的情况下，都需要创建各自的日期文件夹
new_interface_path = interfaces_gen_path + "/" + new
if not os.path.exists(new_interface_path):
    os.mkdir(new_interface_path)
new_api_path = api_template_gen_path + "/" + new
if not os.path.exists(new_api_path):
    os.mkdir(new_api_path)
new_report_path = api_change_report_gen_path + "/" + new
if not os.path.exists(new_report_path):
    os.mkdir(new_report_path)

# 设置爬取swagger地址后的json文件名称，通用的，所以，也是直接先设置好
api_file_name = project + ".json"
# 无论是否首次测试该项目的接口，json文件都要生成并保存
save_json_data(new_interface_path, project, swagger_dict_res)
# 无论是否首次测试该项目的接口，每个接口的yml文件的存放目录和case的yml文件存放目录，都需要创建好
new_json_data = get_json_data(new_interface_path, project)
# 获取所有已废弃的接口列表
all_deprecated_list = get_all_deprecated_interfaces(new_json_data)
if len(all_deprecated_list) != 0:
    save_json_data(new_report_path, "deprecated_interface_info", all_deprecated_list)
# 没过滤掉废弃接口前的所有接口信息
new_paths = new_json_data["paths"]
"""
已被废弃的接口，即使接口的其他信息有所变化，也不去遍历，直接过滤掉
想要获取部分变更的接口，前提是：
1. 接口地址没有变化
2. 接口没有被废弃
"""
# 去除已废弃接口的所有接口信息
for depre in all_deprecated_list:
    new_paths.pop(depre)
new_path_list = list(new_paths.keys())
new_definition_list = []
all_new_definitions = new_json_data['definitions']
for definition in all_new_definitions:
    new_definition_list.append(definition)
for new_path in new_path_list:
    new_path = re.sub(r"{.*}", "", new_path, count=0, flags=0)
    create_every_path_dirs(new_api_path, new_path)

# 无论是否首次测试该项目的接口，每个接口的yml文件和case的yml文件，都需要创建好，
all_api_file_list = create_api_yml_file(new_paths, new_api_path, new_definition_list, all_new_definitions)
for every_api_file in all_api_file_list:
    if every_api_file.split("/")[-1] != "":
        file_name = every_api_file.split("/")[-1]
    else:
        file_name = every_api_file.split("/")[-2]
    data = get_yaml_data(every_api_file, file_name)
    data["interface_protocol"] = protocol
    save_ruamel_data(every_api_file, file_name, data)

# 准备进行对比，拿json文件进行对比，得到版本的差异
if os.listdir(interfaces_gen_path)[0] == new:
    # print("首次进行该项目的接口测试，直接以当前日期为版本号，依次执行创建json文件、创建接口yml文件、创建用例yml文件")
    # print("无需进行比较")
    pass
else:
    # print("非首次测试该项目的接口")
    # print("需要进行比较")
    # 在interfacedata目录下，列举出所有的版本日期，组成一个list，然后寻找到上个版本号日期，即:用来和当前日期版本进行比较
    all_version_list = list(os.listdir(interfaces_gen_path))
    # 最新版本日期为列表的最后一个值
    # 上个版本日期为列表的倒数第二个值
    old_version = all_version_list[-2]
    new_version = all_version_list[-1]
    new_interface_path = interfaces_gen_path + "/" + old_version
    old_json_data = get_json_data(new_interface_path, project)
    # 获取所有已废弃的接口列表
    all_old_deprecated_list = get_all_deprecated_interfaces(old_json_data)
    # 没过滤掉废弃接口前的所有接口信息
    old_paths = old_json_data["paths"]
    # 去除已废弃接口的所有接口信息
    for depre in all_old_deprecated_list:
        old_paths.pop(depre)
    # 将新增的接口，写入json文件中
    new_list, new_interface_info = get_new_interface_info(old_json_data, new_json_data)
    for every_interface in new_interface_info:
        every_interface["interface_protocol"] = protocol
    if len(new_list) != 0:
        save_json_data(new_report_path, "new_interface_info", new_interface_info)
    # 将删除的接口，写入json文件中
    delete_list = get_deleted_interface_info(old_json_data, new_json_data)
    if len(delete_list) != 0:
        save_json_data(new_report_path, "delete_interface_info", delete_list)
    # delete的接口，本就不会被创建目录和生成接口yml文件、用例yml文件，所以，无需处理删除
    # 将变化的接口，写入json文件中
    summary_change_list = get_summary_changed_interface_info(old_json_data, new_json_data)
    if len(summary_change_list) != 0:
        save_json_data(new_report_path, "summary_interface_info", summary_change_list)
    method_change_list = get_method_changed_interface_info(old_json_data, new_json_data)
    if len(method_change_list) != 0:
        save_json_data(new_report_path, "method_interface_info", method_change_list)
    parameter_type_change_list = get_parameter_type_changed_interface_info(old_json_data, new_json_data)
    if len(parameter_type_change_list) != 0:
        save_json_data(new_report_path, "parameter_type_interface_info", parameter_type_change_list)
    parameter_change_list = get_parameter_changed_interface_info(old_json_data, new_json_data)
    if len(parameter_change_list) != 0:
        save_json_data(new_report_path, "parameter_interface_info", parameter_change_list)
    header_change_list = get_header_changed_interface_info(old_json_data, new_json_data)
    if len(header_change_list) != 0:
        save_json_data(new_report_path, "header_interface_info", header_change_list)
    # 获取没有变化的接口列表，没有去除部分信息变化的接口地址
    no_change_list = get_no_changes_interface_info(old_json_data, new_json_data)
    # 合并目前这五大类列表，并去重，只要地址出现在任何一个列表中，都说明这个接口变更了
    all_list = []
    for s in summary_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    for s in method_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    for s in parameter_type_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    for s in parameter_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    for s in header_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    # 去重
    all_list = list(set(all_list))
    if len(all_list) != 0:
        save_json_data(new_report_path, "part_change_interface_info", all_list)
    for address in all_list:
        if address in no_change_list:
            # 去除变更了的地址
            no_change_list.remove(address)
    if len(no_change_list) != 0:
        save_json_data(new_report_path, "no_change_interface_info", no_change_list)
