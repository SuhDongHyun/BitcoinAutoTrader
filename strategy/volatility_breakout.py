from util.singleton import singleton
from pyupbit import get_ohlcv


@singleton
class VolatilityBreakout:
    def __init__(self, k=0.5):
        self._k = k

    def set_k(self, k):
        self._k = k

    def get_target_price(self, ticker='KRW', interval='minute60'):
        df = get_ohlcv(ticker, interval)
        yesterday = df.iloc[-2]
        return yesterday['close'] + (yesterday['high'] - yesterday['low']) * self._k
