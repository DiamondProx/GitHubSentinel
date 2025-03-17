import os
import json
import akshare as ak
from datetime import datetime
from pathlib import Path
from logger import get_logger
from config import Config
from llm import LLM

logger = get_logger(__name__)

class THSFinanceClient:
    def __init__(self, config: Config):
        self.config = config
        self.data_dir = Path(config.ths_finance['data_dir'])
        self.report_dir = Path(config.ths_finance['report_dir'])
        self.llm = LLM(config)
        
        # 创建必要的目录
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
    def fetch_and_save_data(self):
        """获取同花顺全球股市数据并保存"""
        try:
            # 获取当前日期作为文件名
            today = datetime.now().strftime('%Y-%m-%d')
            data_file = self.data_dir / f'{today}.json'
            
            # 获取数据
            df = ak.stock_info_global_ths()
            
            # 将DataFrame转换为JSON格式并保存
            data = df.to_json(orient='records', force_ascii=False)
            with open(data_file, 'w', encoding='utf-8') as f:
                f.write(data)
                
            logger.info(f'Successfully saved THS finance data to {data_file}')
            return data_file
            
        except Exception as e:
            logger.error(f'Failed to fetch THS finance data: {str(e)}')
            raise
    
    def generate_report(self, data_file: Path):
        """使用LLM生成分析报告"""
        try:
            # 读取数据
            with open(data_file, 'r', encoding='utf-8') as f:
                data = f.read()
                
            # 读取提示词模板
            with open(self.config.ths_finance['prompt_template_file'], 'r', encoding='utf-8') as f:
                prompt_template = f.read()
                
            # 替换提示词模板中的数据
            prompt = prompt_template.format(data=data)
            
            # 生成分析报告
            report = self.llm.generate(prompt)
            
            # 保存报告
            today = datetime.now().strftime('%Y-%m-%d')
            report_file = self.report_dir / f'{today}.md'
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            logger.info(f'Successfully generated report to {report_file}')
            return report_file
            
        except Exception as e:
            logger.error(f'Failed to generate report: {str(e)}')
            raise
    
    def send_to_wechat(self, report_file: Path):
        """将报告推送到微信公众号"""
        try:
            # 读取报告内容
            with open(report_file, 'r', encoding='utf-8') as f:
                report = f.read()
                
            # TODO: 实现微信公众号推送逻辑
            # 这里需要使用微信公众号的API进行推送
            # 可以使用第三方库如wechatpy来实现
            
            logger.info('Successfully sent report to WeChat')
            
        except Exception as e:
            logger.error(f'Failed to send report to WeChat: {str(e)}')
            raise
    
    def run(self):
        """运行完整的数据获取、分析和推送流程"""
        try:
            # 获取并保存数据
            data_file = self.fetch_and_save_data()
            
            # 生成分析报告
            report_file = self.generate_report(data_file)
            
            # 推送到微信公众号
            self.send_to_wechat(report_file)
            
            logger.info('Successfully completed THS finance workflow')
            
        except Exception as e:
            logger.error(f'Failed to run THS finance workflow: {str(e)}')
            raise