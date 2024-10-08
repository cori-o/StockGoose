from dotenv import load_dotenv
from src import NasDacBroker
import argparse
import logging
import mojito
import json 
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,  # 로그 레벨 설정 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),# mode='w'),  # 로그를 파일에 기록
        # logging.StreamHandler()  # 콘솔에도 출력
    ]
)

logging.basicConfig(filename='warnings.log', level=logging.WARNING)
logging.captureWarnings(True)

def main(args):
    load_dotenv() 
    stock_config = dict()
    stock_config['api_key'] = os.getenv('api_key')
    stock_config['api_secret'] = os.getenv('api_secret')
    stock_config['account_no'] = os.getenv('account_no')
    
    nabroker = NasDacBroker(stock_config)
    nabroker.set_broker()
    nabroker.set_balance()
    balance = nabroker.balance
    print(nabroker.get_balance_info(balance))
    print(nabroker.get_stock_info("TSLA"))


if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("--config_path", type=str, default="./config/")
    cli_args = cli_parser.parse_args()
    main(cli_args)