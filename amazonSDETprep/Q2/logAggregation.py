from typing import List
from collections import deque

class LogAggregator:
    def __init__(self):
        self.logs = deque()
 
    def add_log(self, timestamp: int, error_code: str) -> None:
        self.logs.append([timestam
                          p] = error_code
        pass

    def get_top_k(self, timestamp: int, window: int, k: int) -> List[str]:
        left = timestamp-window
        right = timestamp

        pass


# -------------------------
# Local test runner
# -------------------------
if __name__ == "__main__":
    la = LogAggregator()

    # Add logs
    la.add_log(1, "404")
    la.add_log(2, "500")
    la.add_log(3, "404")
    la.add_log(10, "404")

    # Query
    result = la.get_top_k(timestamp=10, window=5, k=1)
    print("Top K errors:", result)