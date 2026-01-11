from collections import deque

class RateLimiter:
    def __init__(self, limit: int, window: int):
        self.limit = limit
        self.window = window
        self.requests = deque()

    def allow(self, timestamp: int) -> bool:
        while self.requests and self.requests[0] <= timestamp - self.window:
            self.requests.popleft()
        if len(self.requests) < self.limit:
            self.requests.append(timestamp)
            return True
        return False