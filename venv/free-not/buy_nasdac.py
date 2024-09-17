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
        exchange="나스닥",
        # mock=True   # 모의투자 활성화
    )
    balance = broker.fetch_present_balance()    # fetch_balance() -> fetch_present_balance()
    print(balance)
    price = broker.fetch_price("TQQQ")
    print(f"전일 종가: {price['output']['base']}달러")
    print(f"전일 거래량: {price['output']['pvol']}주")
    print(f"당일 조회 시점 현재가: {price['output']['last']}달러")
    print(f"당일 조회 시점까지 거래량: {price['output']['tvol']}")
    print(f"당일 조회 시점까지 전체 거래금액: {price['output']['tamt']}달러")
    # 지정가 매수 
    resp = broker.create_limit_buy_order(
        symbol="TQQQ",
        price=30, 
        quantity=5
    )
    print(resp)
    # 지정가 매도 
    resp = broker.create_limit_sell_order(
        symbol="TQQQ",
        price=30, 
        quantity=5
    )
    print(resp) 
    symbols = broker.fetch_symbols()
    print(symbols)
    # 일봉 조회 
    ohlcv = broker.fetch_ohlcv(
        symbol="TSLA",
        timeframe="D",
        adj_price=True, 
    )
    print(f"시가: {ohlcv['output2'][0]['open']}")
    print(f"고가: {ohlcv['output2'][0]['high']}")
    print(f"저가: {ohlcv['output2'][0]['low']}")
    print(f"종가: {ohlcv['output2'][0]['clos']}")
    print(f"거래량: {ohlcv['output2'][0]['tvol']}")
    print(f"거래대금: {ohlcv['output2'][0]['tamt']}")
    # print(f"시가: {ohlcv.open}")



if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('--config_path', type=str, default='config/')
    cli_args = cli_parser.parse_args()
    main(cli_args)