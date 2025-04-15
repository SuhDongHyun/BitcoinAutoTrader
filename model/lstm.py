import numpy as np
import pandas
import torch
import torch.nn as nn
import torch.optim as optim
from pyupbit import get_ohlcv
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, output_size)
        self.criterion = nn.L1Loss()
        self.optimizer = optim.Adam(self.lstm.parameters(), lr=0.001)
        self.scaler = MinMaxScaler()
        self.window = 24
        self.horizon = 3

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        linear_out = self.linear(lstm_out[:, -1, :])
        return linear_out

    # noinspection PyMethodMayBeStatic
    def load_data(self):
        df = get_ohlcv(ticker="KRW-BTC", interval="minute60")
        df = df.assign(
            pct=lambda x: x.close.pct_change(),
            ma5=lambda x: x.close.rolling(window=5).mean(),
            ma10=lambda x: x.close.rolling(window=10).mean(),
            upper=lambda x: x.close.rolling(window=20).mean() + 2 * x.close.rolling(window=20).std(),
            lower=lambda x: x.close.rolling(window=20).mean() - 2 * x.close.rolling(window=20).std()
        )
        return df[['close', 'volume', 'pct', 'ma5', 'ma10', 'upper', 'lower']].dropna()

    def preprocess(self, dataset: pandas.DataFrame):
        feature = dataset.values
        target = self.scaler.fit_transform(dataset[['close']].values)
        seq_len = len(dataset) - self.window - self.horizon + 1
        feature_seq = [feature[i:i+self.window] for i in range(seq_len)]
        target_seq = [target[i+self.window:i+self.window+self.horizon].flatten() for i in range(seq_len)]
        return np.array(feature_seq), np.array(target_seq)

    def train_model(self):
        dataset = self.load_data()
        x, y = self.preprocess(dataset)
        x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, shuffle=False)

        for epoch in range(30):
            self.lstm.train()
            self.optimizer.zero_grad()
            x_train_torch = torch.tensor(x_train, dtype=torch.float32)
            y_train_torch = torch.tensor(y_train, dtype=torch.float32)
            output = self.forward(x_train_torch)
            loss = self.criterion(output, y_train_torch)
            loss.backward()
            self.optimizer.step()

            self.lstm.eval()
            with torch.no_grad():
                x_val_torch = torch.tensor(x_val, dtype=torch.float32)
                y_val_torch = torch.tensor(y_val, dtype=torch.float32)
                val_output = self.forward(x_val_torch)
                val_loss = self.criterion(val_output, y_val_torch)

            print(f"[Epoch {epoch+1}] Train Loss: {loss.item():.6f} | Val Loss: {val_loss.item():.6f}")

    def predict_price(self):
        dataset = self.load_data()
        x_input = torch.tensor(dataset.values[-self.window:], dtype=torch.float32).unsqueeze(0)

        self.lstm.eval()
        with torch.no_grad():
            predicted_scaled = self.forward(x_input).numpy()
            predicted = self.scaler.inverse_transform(predicted_scaled)

        return predicted.flatten()
