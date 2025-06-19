from os import getenv

PROJECT_URL = getenv("PROJECT_URL")
if not PROJECT_URL:
    msg = "PROJECT_URL environment variable is not set."
    raise ValueError(msg)
