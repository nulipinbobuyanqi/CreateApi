# coding:utf-8
# @Author: wang_cong
# @File: interface_template.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 13:43

interface_template = {
    # 接口协议
    "interface_protocol": "interface_protocol",
    # 接口名称
    "interface_name": "interface_name",
    # 所属模块
    "belong_module": "所属模块",
    # 接口地址
    "interface_address": "interface_address",
    # 接口方法
    "interface_method": "interface_method",
    # 是否需要请求头
    "need_cookie": True,
    # 接口请求头
    "interface_headers": {

    },
    # 接口请求参数类型，取值范围是：application/json、multipart/form-data、application/x-www-form-urlencoded、text/xml。
    "interface_parameters_type": "interface_parameters_type",
    # 接口请求参数
    "interface_parameters": "interface_parameters",
    # 是否为上传文件类型的接口，默认是：False，表示：不需要上传文件
    "need_file": False,
    # 接口是否已废弃，默认是：False，表示：未废弃
    "deprecated": False
}