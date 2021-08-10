# coding:utf-8
# @Author: wang_cong


sql_premise_template = {
    "step_number": 1,
    "step_describe": "SQL语句描述",
    "step_type": "sql",
    "sql": {
        "database_type": "mysql or mongodb",
        "sql_type": "SQL语句类型，select 、update、delete、insert",
        "sql_content": "SQL语句",
        "sql_check": [
            {
                "extract_path": "校验字段的提取路径，格式填写规则是： $    $.X    $.X.Y  三者中的一种方式",
                "operator": "操作器的规则，取值范围是：=, >, <, <=, !=, in, not in, is None, is not None",
                "expected_value": "预期结果，填写规则是：当前这行的后面必须跟着' !!python/tuple'内容，其每个预期结果必须写在list里面，且每个list里面的值，必须是dict，且key的顺序要与查询出来的字段顺序一致"
            }
        ],
        "sql_extractor": [
            {
                "parameter_name": "参数名称，即：为从接口中获取出来的参数命的名。引用该变量的格式是：${变量名}。若三者中，都有该变量名称，则取值优先级的顺序是：testcase先于testsuite先于global",
                "extract_path": "校验字段的提取路径，格式填写规则是： $    $.X    $.X.Y  三者中的一种方式",
                "parameter_level": "参数级别的规则，取值范围是：testcase, testsuite, global"
            }
        ]
    }
}