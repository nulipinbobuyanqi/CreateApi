# coding:utf-8
# @Author: wang_cong

api_premise_template = {
    "step_number": 1,
    "step_describe": "接口描述",
    "step_type": "api",
    "api": {
        "interface_name": "接口名称",
        "belong_module": "所属模块",
        "interface_address": "接口地址",
        "interface_method": "接口方法",
        "need_cookie": True,
        "interface_headers": {

        },
        "interface_parameters_type": "接口请求参数类型，取值范围是：application/json、multipart/form-data、application/x-www-form-urlencoded、text/xml",
        "need_file": False,
        "deprecated": False,
        "interface_parameters": {

        },
        "interface_check": [
            {
                "extract_type": "提取方式的规则，取值范围是：interface_headers, cookie, response_code, response_content",
                "not_compare": "不需要进行比较的字段信息，格式填写规则是：jsonpath的写法规则。",
                "extract_path": "提取路径的规则，格式填写规则是：jsonpath的写法规则。注意：当extract_type=response_code时，extract_path=None",
                "operator": "操作器的规则，取值范围是：=, >, <, <=, !=, in, not in, is None, is not None",
                "expected_value": "预期结果"
            }
        ],
        "interface_extractor": [
            {
                "parameter_name": "参数名称，即：为从接口中获取出来的参数命的名。引用该变量的格式是：${变量名}。若三者中，都有该变量名称，则取值优先级的顺序是：testcase先于testsuite先于global",
                "extract_type": "提取方式的规则，取值范围是：interface_headers, cookie, response_code, response_content",
                "extract_path": "提取路径的规则，格式填写规则是：jsonpath的写法规则。注意：当extract_type=response_code时，extract_path=None",
                "parameter_level": "参数级别的规则，取值范围是：testcase, testsuite, global"
            }
        ],
        "sql_check": {
            "database_type": "mysql or mongodb",
            "sql_type": "SQL语句类型，select、update、delete、insert",
            "sql_content": "sql语句",
            "sql_check": [
                {
                    "extract_path": "校验字段的提取路径，格式填写规则是： $    $.X    $.X.Y  三者中的一种方式",
                    "operator": "操作器的规则，取值范围是：=, >, <, <=, !=, in, not in, is None, is not None",
                    "expected_value": "预期结果，填写规则是：当前这行的后面必须跟着' !!python/tuple'内容，其每个预期结果必须写在list里面，且每个list里面的值，必须是dict，且key的顺序要与查询出来的字段顺序一致"
                }
            ]
        },
        "sql_extractor": [
            {
                "parameter_name": "参数名称，即：为从接口中获取出来的参数命的名。引用该变量的格式是：${变量名}。若三者中，都有该变量名称，则取值优先级的顺序是：testcase先于testsuite先于global",
                "extract_path": "校验字段的提取路径，格式填写规则是： $    $.X    $.X.Y  三者中的一种方式",
                "parameter_level": "参数级别的规则，取值范围是：testcase, testsuite, global"
            }
        ]
    }
}