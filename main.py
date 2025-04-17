import time
from datetime import datetime

from api.upbit_api import UpbitApi
from strategy.news_sentiment import NewsSentiment
from strategy.volatility_breakout import VolatilityBreakout
from model.lstm import LSTM
from util.discord import send_message

upbit = UpbitApi()
news = NewsSentiment()
vb = VolatilityBreakout()
model = LSTM(input_size=7, hidden_size=64, num_layers=2, output_size=3)

send_message("🤖 비트코인 자동매매 시작")

while True:
    try:
        model.train_model()

        now = datetime.now()
        current_price = upbit.get_current_price()
        target_price = vb.get_target_price(interval="day")
        predicted_price = model.predict_price()[0]
        score = news.analyze_sentiment()

        breakout = current_price > target_price
        prediction = predicted_price > current_price
        sentiment = score > 0
        total_condition = sum([breakout + prediction + sentiment])

        text = f'''
        📌 현재가: {current_price:,.0f}원
        🚀 목표가: {target_price:,.0f}원 ({breakout})
        📈 예측값: {predicted_price:,.0f}원 ({prediction})
        📰 감정값: {score:,.05f}점 ({sentiment})
        '''

        if total_condition == 3:
            krw = upbit.get_balance()

            if krw > 10000:
                upbit.buy(price=krw * 0.9995)
                send_message(f'\t✅ 매수 실행!\n{text}')
        elif total_condition <= 1:
            btc = upbit.get_balance(ticker="KRW-BTC")

            if btc and btc * current_price > 10000:
                upbit.sell(volume=btc)
                send_message(f'\t🔻 매도 실행!\n{text}')

        time.sleep(60 * 60)
    except Exception as e:
        send_message(str(e))
        break
