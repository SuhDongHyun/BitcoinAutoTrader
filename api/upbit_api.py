import pyupbit


class UpbitApi:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.access_key = "zry4vxghMixsVamXLyibZxJnR3IhKQ4C0GzUCwT8"
        self.secret_key = "tZsYxNv98LIdCxqPTLBRypcEvGDV3jjkBtFM0Ifh"
        self.upbit = pyupbit.Upbit(self.access_key, self.secret_key)
        self._initialized = True

    # noinspection PyMethodMayBeStatic
    def get_current_price(self, ticker="KRW-BTC"):
        return pyupbit.get_current_price(ticker)

    # noinspection PyMethodMayBeStatic
    def get_price_trend(self, ticker="KRW-BTC", interval="day", count=200, to=None):
        return pyupbit.get_ohlcv(ticker, interval, count, to)
    