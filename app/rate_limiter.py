import time
from collections import defaultdict

# storing timestamps per key, check if too many in last 60s
# not using redis here, just a dict - works fine for single server

MAX_REQUESTS = 10
TIME_WINDOW = 60  # seconds

# key_id -> list of timestamps
_tracker: dict = defaultdict(list)


def check_rate_limit(key_id: str) -> bool:
    """returns True if the key has exceeded the limit"""
    now = time.time()
    cutoff = now - TIME_WINDOW

    # drop old timestamps
    _tracker[key_id] = [t for t in _tracker[key_id] if t > cutoff]

    if len(_tracker[key_id]) >= MAX_REQUESTS:
        print(f"rate limit hit for key: {key_id[:10]}")
        return True

    _tracker[key_id].append(now)
    return False
