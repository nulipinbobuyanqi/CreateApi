# coding:utf-8
# @Author: wang_cong
# @File: operation_json.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/21 15:51
import json
import os
from Utils.operation_log import initLogger

logger = initLogger(__file__)


def get_json_data(json_path, json_file_name):
    """
    读取json文件，返回一个dict类型的数据
    :param json_path: json文件所在路径，不含最后一个"/"符号
    :param json_file_name: json文件名称，不含".json"后缀名
    :return: 返回dict类型的数据
    """
    json_file = json_path + "/" + json_file_name + ".json"
    if not os.path.exists(json_file):
        logger.error("{}.json文件，不存在！".format(json_file_name))
    with open(json_file, "r", encoding="utf-8") as f:
        dict_json_data = json.load(f)
    return dict_json_data


def save_json_data(json_path, json_file_name, dict_json_data):
    """
    将json字符串写入json文件
    :param json_path: json文件所在路径，不含最后一个"/"符号
    :param json_file_name: json文件名称，不含".json"后缀名
    :param dict_json_data: dict类型的json文件内容
    :return:
    """
    json_file = json_path + "/" + json_file_name + ".json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(dict_json_data, f, indent=4, ensure_ascii=False)


