class StoreLogger:
    def __init__(self):
        self.messages = []

    def log(self, *messages):
        self.messages.extend(messages)
