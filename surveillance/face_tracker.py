# surveillance/face_tracker.py

import time

class FaceTracker:
    def __init__(self, timeout=60):
        self.last_seen = {}  # dict {identity: timestamp}
        self.timeout = timeout

    def is_duplicate(self, name):
        now = time.time()
        if name not in self.last_seen:
            self.last_seen[name] = now
            return False
        elif now - self.last_seen[name] > self.timeout:
            self.last_seen[name] = now
            return False
        else:
            return True
