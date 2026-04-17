import time
from collections import defaultdict

# simple in-memory rate limiter
# not production-ready but works fine for this scope
# TODO: swap this out with Redis if we need multi-instance support

RATE_LIMIT = 10  # requests per minute
WINDOW = 60  # seconds

# structure: { api_key: [(timestamp, count), ...] }
request_log: dict = defaultdict(list)


def is_rate_limited(api_key: str) -> bool:
    now = time.time()
    window_start = now - WINDOW

    # clean up old entries outside the window
    request_log[api_key] = [
        ts for ts in request_log[api_key] if ts > window_start
    ]

    if len(request_log[api_key]) >= RATE_LIMIT:
        print(f"[rate limiter] key {api_key[:8]}... hit limit")
        return True

    request_log[api_key].append(now)
    return False
