from util.singleton import singleton
import pyupbit


@singleton
class UpbitApi:
    def __init__(self):
        self.access_key = "zry4vxghMixsVamXLyibZxJnR3IhKQ4C0GzUCwT8"
        self.secret_key = "tZsYxNv98LIdCxqPTLBRypcEvGDV3jjkBtFM0Ifh"
        self.upbit = pyupbit.Upbit(self.access_key, self.secret_key)

    # noinspection PyMethodMayBeStatic
    def get_current_price(self, ticker="KRW-BTC"):
        return pyupbit.get_current_price(ticker)

    # noinspection PyMethodMayBeStatic
    def get_price_trend(self, ticker="KRW-BTC", interval="day", count=200, to=None):
        return pyupbit.get_ohlcv(ticker, interval, count, to)

    def get_balance(self, ticker="KRW"):
        return self.upbit.get_balance(ticker)

    def get_balances(self):
        return self.upbit.get_balances()

    def buy(self, ticker="KRW-BTC", price=1000):
        return self.upbit.buy_market_order(ticker, price)

    def sell(self, ticker="KRW-BTC", volume=0.001):
        return self.upbit.sell_market_order(ticker, volume)
