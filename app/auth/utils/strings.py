import random
import string


def generate_oauth2_state(length: int = 32) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))
