from loguru import logger
import sys
import logging

# 定义统一的日志格式字符串
log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}"

# 配置 Loguru，移除默认的日志配置
logger.remove()

# 使用统一的日志格式配置标准输出和标准错误输出，支持彩色显示
logger.add(sys.stdout, level="DEBUG", format=log_format, colorize=True)
logger.add(sys.stderr, level="ERROR", format=log_format, colorize=True)

# 同样使用统一的格式配置日志文件输出，设置文件大小为1MB自动轮换
logger.add("logs/app.log", rotation="1 MB", level="DEBUG", format=log_format)

# 创建一个默认的日志记录器实例
LOG = logger.bind(name="default")

# 定义获取logger的函数
def get_logger(name=None):
    return logger.bind(name=name)

# 将LOG变量和get_logger函数公开，允许其他模块导入使用
__all__ = ["LOG", "get_logger"]
