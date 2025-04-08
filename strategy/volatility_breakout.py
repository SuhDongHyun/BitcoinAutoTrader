from util.singleton import singleton


@singleton
class VolatilityBreakout:
    def __init__(self, k=0.5):
        self._k = k

    def set_k(self, k):
        self._k = k
