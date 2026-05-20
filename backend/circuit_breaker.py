import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_time=10):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def can_request(self):

        if self.state == "OPEN":

            elapsed = time.time() - self.last_failure_time

            if elapsed > self.recovery_time:
                self.state = "HALF_OPEN"
                return True

            return False

        return True

    def success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"