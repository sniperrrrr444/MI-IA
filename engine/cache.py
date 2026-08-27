class KVCache:
    def __init__(self):
        self.past_key_values = None

    def set(self, value):
        self.past_key_values = value

    def clear(self):
        self.past_key_values = None
