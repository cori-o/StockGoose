from dotenv import load_dotenv
import argparse
import logging
import json 
import mojito
import pprint
import os

load_dotenv() 
ip_addr = os.getenv('ip_addr')
cohere_api = os.getenv('COHERE_API_KEY')

key = os.getenv('api_key')
secret = os.getenv('api_secret')
acc_no = os.getenv('account_no')

'''
KoreaInvestment 클래스의 객체를 생성하면 생성자에서 토근을 자동으로 발급하고 발급 받은 토큰에 대한 데이터를 파이썬의 피클 모듈을 사용하여 'token.dat'라는 이름의 파일로 저장
'''
broker = mojito.KoreaInvestment(
    api_key=key,
    api_secret=secret,
    acc_no=acc_no
)
'''
resp = broker.fetch_price("066570")
print(f"Open(시가): {resp['output']['stck_oprc']}원")
print(f"High(고가): {resp['output']['stck_oprc']}원")
print(f"Low(저가): {resp['output']['stck_oprc']}원")
print(f"Close(종가): {resp['output']['stck_oprc']}원")

symbols = broker.fetch_symbols()
print(symbols)
print(symbols[symbols['한글명'] == 'LG전자'])

kospi_symbols = broker.fetch_kospi_symbols()     # 코스피
kosdaq_symbols = broker.fetch_kosdaq_symbols()        # 코스닥
kospi_symbols.head()
'''
# pprint.pprint(broker.fetch_balance())
balance = broker.fetch_balance()
print(f"총 평가 금액: {balance['output2'][0]['tot_evlu_amt']}")
print(f"예수금: {balance['output2'][0]['dnca_tot_amt']}")

resp = broker.fetch_balance()
for comp in resp['output1']:
    print(comp['pdno'])
    print(comp['prdt_name'])
    print(comp['hldg_qty'])
    print(comp['pchs_amt'])
    print(comp['evlu_amt'])
    print("-" * 40)


# 지정가 매수 
resp = broker.create_limit_buy_order(
    symbol="005930",
    price=65000,
    quantity=1
)
pprint.pprint(resp)

# 지정가 매도 
resp = broker.create_limit_sell_order(
    symbol="005930",
    price=67000,
    quantity=1
)
pprint.pprint(resp)

# 시장가 매수
resp = broker.create_market_buy_order(
    symbol="005930",
    quantity=10
)

# 시장가 매도 
resp = broker.create_market_sell_order(
    symbol="005930",
    quantity=1
)
pprint.pprint(resp)

# 주문 취소 (전체)
resp = broker.cancel_order(
    org_no="91252",   # 전송주문 조직번호
    order_no="0000119206",   # 원주문번호  (buy, sell order 명령 실행 시 확인할 수 있음)
    quantity=4,  # 잔량전부 취소시 원주문 수량과 일치해야함
    total=True   # 잔량전부를 의미
)
pprint.pprint(resp)

# 주문 취소 (일부)
resp = broker.cancel_order(
    org_no="91252",
    order_no="0000120154",
    quantity=2,     # 취소하고자하는 수량
    total=False     # 잔량일부
)


# 주문 정정 (전량)
resp = broker.modify_order(
    org_no="91252",
    order_no="0000138450",
    order_type="00",
    price=60000,
    quantity=4,
    total=True
)

# 주문 정정 (일부)
resp = broker.modify_order(
    org_no="91252",
    order_no="0000143877",
    order_type="00",
    price=60000,
    quantity=2,
    total=False
)

