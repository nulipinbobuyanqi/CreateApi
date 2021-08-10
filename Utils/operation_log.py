# coding:utf-8
import logging
import os
import sys
import time
import colorlog
import logbook
from logbook.more import ColorizedStderrHandler
from Utils.get_project_config import get_project_config_info
from Utils.operation_yml import get_yaml_data


# 获取当前日期，作为接口版本号
new = time.strftime("%Y-%m-%d", time.localtime())
# 获取项目配置信息的存放根路径
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_yaml_file_name = "project_path"
gen_path = get_yaml_data(project_path, project_yaml_file_name)["project_path"]
project_path = gen_path + "/ProjectManage/"
# 获取项目配置信息
project, protocol, swagger_url = get_project_config_info(project_path)
# 单元测试用例的日志存放根目录
log_gen_path = project_path + "06.UnitTest/06.UnitTestLog" + "/" + project
if not os.path.exists(log_gen_path):
    os.makedirs(log_gen_path)
# 当前版本的单元测试日志目录
log_path = log_gen_path + "/" + new
if not os.path.exists(log_path):
    os.makedirs(log_path)
# 单元测试用例的运行配置文件存放根目录
# run_config_gen_path = project_path + "06.UnitTest/03.UnitTestRunConfig" + "/" + project
# 当前版本的单元测试的运行配置文件目录
# run_config_path = run_config_gen_path + "/" + new
# 当前版本的单元测试日志配置信息
# log_config = get_yaml_data(run_config_path, "RunConfig")["log_config"]
log_config = {
    "backup" : 5,
    "console_level": "INFO",
    "file_level": "INFO",
    "console_pattern": '[%(log_color)s%(asctime)s]  [%(filename)s]  [%(funcName)s]  [line:%(lineno)2d]  [%(levelname)s]: %(message)s',
    "file_pattern": '[%(asctime)s]  [%(filename)s]  [%(funcName)s]  [line:%(lineno)2d]  [%(levelname)s]: %(message)s'
}

# # 设置日志输出格式
# def console_pattern(record, handler):
#     log_formatter = "[{date}] [{level}] [{file_name}] [{func_name}] [{line}] {msg}".format(
#         date=record.time,
#         level=record.level_name,
#         file_name=os.path.split(record.filename)[-1],
#         func_name=record.func_name,
#         line=record.lineno,
#         msg=record.message
#     )
#     return log_formatter


def initLogger(file_name):
    # 设置控制台输出的日志，其颜色规则
    log_colors_config = {
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }
    # 设置日志文件的名称格式
    # log_file_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    all_log_file_name = log_path + "/" + "all.log"
    error_log_file_name = log_path + "/" + "error.log"
    # 初始化logger
    logger = logging.getLogger()
    # 设置默认的日志级别
    logger.setLevel(logging.DEBUG)
    # 设置
    logger.handlers = []
    # 创建一个FileHandler，用于写入全部日志
    all_file_handler = logging.FileHandler(all_log_file_name, mode='a+', encoding='utf-8')
    # 设置FileHandler日志级别
    all_file_handler.setLevel(log_config['file_level'])
    # 创建一个FileHandler，用于写入错误日志
    error_file_handler = logging.FileHandler(error_log_file_name, mode='a+', encoding='utf-8')
    # 设置FileHandler日志级别
    error_file_handler.setLevel(logging.ERROR)
    # 创建一个StreamHandler，用于输出日志到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    # 设置StreamHandler日志级别
    console_handler.setLevel(log_config['console_level'])
    # 定义StreamHandler和FileHandler的输出格式
    handler_formatter = colorlog.ColoredFormatter(log_config['console_pattern'], log_colors=log_colors_config)
    file_formatter = logging.Formatter(log_config['file_pattern'])
    all_file_handler.setFormatter(file_formatter)
    error_file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(handler_formatter)
    # 将logger添加到handler里面
    logger.addHandler(all_file_handler)
    logger.addHandler(error_file_handler)
    logger.addHandler(console_handler)
    return logger
    # logbook.set_datetime_format('local')
    # logger = logbook.Logger(file_name)
    # logger.handlers = []
    # # 将日志打印到屏幕
    # log_std = ColorizedStderrHandler(bubble=True)
    # log_std.formatter = console_pattern
    # logger.handlers.append(log_std)
    # # 将日志写进文件
    # log_file = logbook.TimedRotatingFileHandler(os.path.join(log_path, '%s.log' % 'log'), date_format='%Y-%m-%d', bubble=True, encoding='utf-8')
    # log_file.formatter = console_pattern
    # logger.handlers.append(log_file)
    # return logger
