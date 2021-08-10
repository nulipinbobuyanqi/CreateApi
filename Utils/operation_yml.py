# coding:utf-8
# @Author: wang_cong
# @File: operation_yml.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/21 15:51
import os


def get_yaml_data(yaml_path, yaml_file_name):
    """
    读取yaml文件，返回一个dict类型的数据
    :param yaml_path: yaml文件所在路径，不含最后一个"/"符号
    :param yaml_file_name: yaml文件名称，不含".yaml"后缀名
    :return: 返回dict类型的数据
    """
    import yaml
    yaml_file = yaml_path + "/" + yaml_file_name + ".yml"
    if not os.path.exists(yaml_file):
        raise Exception("{}.yml文件，不存在！".format(yaml_file_name))
    with open(yaml_file, "r", encoding="utf-8") as f:
        str_yml_data = f.read()
    dict_yaml_data = yaml.load(str_yml_data, Loader=yaml.FullLoader)
    return dict_yaml_data


def save_ruamel_data(yaml_path, yaml_file_name, yaml_data):
    """
    将yaml字符串写入yaml文件，会按照顺序写入文件，建议采用这种方式写入yaml文件
    :param yaml_path: yaml文件所在路径，不含最后一个"/"符号
    :param yaml_file_name: yaml文件名称，不含".yaml"后缀名
    :param yaml_data: 待写入的yaml文件内容
    :return:
    """
    from ruamel import yaml
    yaml_file = yaml_path + "/" + yaml_file_name + ".yml"
    with open(yaml_file.replace("\\", "/"), "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, Dumper=yaml.RoundTripDumper, allow_unicode=True)


def save_yaml_data(yaml_path, yaml_file_name, yaml_data):
    """
    将yaml字符串写入yaml文件，不会按照顺序写入文件
    :param yaml_path: yaml文件所在路径，不含最后一个"/"符号
    :param yaml_file_name: yaml文件名称，不含".yaml"后缀名
    :param yaml_data: 待写入的yaml文件内容
    :return:
    """
    import yaml
    yaml_file = yaml_path + "/" + yaml_file_name + ".yml"
    with open(yaml_file.replace("\\", "/"), "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True)
