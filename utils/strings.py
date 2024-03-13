import string
from secrets import SystemRandom


def generate_random_string(length: int) -> str:
    return f"-{''.join(SystemRandom().choices(
        string.ascii_letters + string.digits, k=length
    ))}"
