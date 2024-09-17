from abc import ABC, abstractmethod
import mojito

class Broker():
    def __init__(self, config):
        self.api_key = config['api_key']  
        self.api_secret = config['api_secret']
        self.account_no = config['account_no']

    @abstractmethod
    def set_broker(self):
        '''
        증권사 객체 생성
        '''
        pass
    
    @abstractmethod
    def set_balance(self, broker):
        ''' 
        계좌 잔고 설정
        ''' 
        pass     

    @abstractmethod
    def get_stock_ohlcv(self, stock_no):
        '''
        일봉, 주봉, 월봉 데이터 조회 
        '''
        pass 
    
    def buy_order(self, symbol, quantity, price=None):
        '''
        매수 주문  
        '''
        if price!=None:    # 지정가 매수 
            self.broker.create_limit_buy_order(
                symbol=symbol,
                price=price,
                quantity=quantity,
            )
        else:   # 시장가 매수 
            self.broker.create_market_buy_order(
                symbol=symbol,
                quantity=quantity,
            )
        
    def sell_order(self, symbol, quantity, price=None):
        '''
        매도 주문
        '''
        if price!=None:    # 지정가 매도 
            self.broker.create_limit_sell_order(
                symbol=symbol,
                price=price,
                quantity=quantity,
            )
        else:   # 시장가 매도 
            self.broker.create_market_sell_order(
                symbol=symbol,
                quantity=quantity,
            )
    
    def cancel_order(self, symbol_no, order_no, quantity, total=False):
        '''
        취소 주문, 전량 취소 (total=True)시 quantity 값이 전체 보유 수량과 일치해야 함
        '''
        self.broker.cancel_order(
            org_no=symbol_no,
            order_no=order_no,
            quantity=quantity,    
            total=total     
        )
    
    def modify_order(self, symbol_no, order_no, order_type, price, quantity, total=False):
        '''
        주문 수정, order_type으로 인해 nasdac에서도 동작하는지 확인 필요 
        '''
        self.broker.modify_order(
            org_no=symbol_no,
            order_no=symbol_no,
            order_type=order_type,
            price=price,
            quantity=quantity,
            total=total,
        )


class KosDacBroker(Broker):
    def __init__(self):
        pass 

    def set_broker(self):
        self.broker = mojito.KoreaInvestment(
            api_key=self.api_key, 
            api_secret=self.api_secret,
            acc_no=self.account_no,
        )

    def set_balance(self, broker):
        self.balance = broker.fetch_balance()

    def get_stock_code(self):
        self.symbols = broker.fetch_symbols()
    
    def get_balance_info(self, balance):
        evlu_amt = balance['output2'][0]['tot_evlu_amt']   # 총 평가 금액 
        tot_amt = balance['output2'][0]['dnca_tot_amt']   # 예수금 
    
    def get_balance_stock_info(self, balance):
        ''' 보유 종목에 대한 정보 확인 ''' 
        resp = broker.fetch_balance()
        for comp in resp['output1']:
            print(comp['pdno'])   # 종목코드 
            print(comp['prdt_name'])   # 종목명 
            print(comp['hldg_qty'])   # 보유 수량 
            print(comp['pchs_amt'])   # 매입 금액 
            print(comp['evlu_amt'])   # 평가 금액
            print("-" * 40)

    def get_stock_ohlcv(self, stock_no): 
        price = broker.fetch_price(stock_no)
        price_open = price['output']['stock_oprc']   # 시가 
        price_high = price['output']['stock_hgpr']   # 고가 
        price_low = price['output']['stock_lwpr']   # 저가 
        price_close = price['output']['stck_clpr']   # 종가


class NasDacBroker(Broker):
    def __init__(self, config):
        super().__init__(config) 

    def set_broker(self):
        self.broker = mojito.KoreaInvestment(
            api_key=self.api_key, 
            api_secret=self.api_secret,
            acc_no=self.account_no,
            exchange="나스닥",
        )

    def set_balance(self):
        self.balance = self.broker.fetch_present_balance() 

    def get_balance_info(self, balance):
        ''' 외화예수금, 출금 가능한 원화 금액, 출금 가능한 외화 금액 ''' 
        print(balance)
        dncl_amt2 = balance['output2'][0]['frcr_dncl_amt_2']   # 외화예수금 
        psbl_amt1 = balance['output2'][0]['frcr_drwg_psbl_amt_1']   # 출금 가능한 외화 금액
        evlu_amt2 = balance['output2'][0]['frcr_evlu_amt2']   # 출금 가능한 원화 금액
        return dncl_amt2, psbl_amt1, evlu_amt2

    def get_stock_info(self, stock_no):
        price = self.broker.fetch_price(stock_no)
        price_base = price['output']['base']   # 전일 종가 
        price_pvol = price['output']['pvol']   # 전일 거래량 
        price_last = price['output']['last']   # 당일 조회 시점 현재가 
        price_tvol = price['output']['tvol']   # 당일 조회 시점까지 거래량 
        price_tamt = price['output']['tamt']   # 당일 조회 시점까지 전체 거래금액
        return price_base, price_pvol, price_last, price_tvol, price_tamt

    def get_stock_ohlcv(self, stock_no):
        ohlcv = self.broker.fetch_ohlcv(
            symbol=stock_no, 
            timeframe='D', 
            adj_price=True,
        )
        ohlcv_open = ohlcv['output2'][0]['open']   # 고가 
        ohlcv_high = ohlcv['output2'][0]['low']   # 저가 
        ohlcv_low = ohlcv['output2'][0]['clos']   # 종가 
        ohlcv_close = ohlcv['output2'][0]['tvol']   # 거래량 
        ohlcv_tamt = ohlcv['output2'][0]['tamt']   # 거래대금 
