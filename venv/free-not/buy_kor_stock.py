from dotenv import load_dotenv
import argparse
import logging
import json 
import mojito
import pprint
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
    api_key = os.getenv('api_key')
    api_secret = os.getenv('api_secret')
    acc_no = os.getenv('account_no')
    broker = mojito.KoreaInvestment(
        api_key=api_key, 
        api_secret=api_secret,
        acc_no=acc_no,
        # exchange="나스닥",
    )
    balance = broker.fetch_balance() 
    print(balance)
    # print(balance['output2'])
    deposit = int(balance['output2'][0]['dnca_tot_amt'])
    print(deposit)
    # 삼성전자 현재가 획득 
    SYMBOL = "005930"
    price = broker.fetch_price(symbol=SYMBOL)
    curr_price = int(price['output']['stck_prpr'])
    print(curr_price)
    QUANTITY = 1
    if curr_price < deposit: 
        broker.create_market_buy_order(symbol=SYMBOL, quantity=QUANTITY)

if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('--config_path', type=str, default='config/')
    cli_args = cli_parser.parse_args()
    main(cli_args)