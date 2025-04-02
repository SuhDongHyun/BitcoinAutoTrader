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
