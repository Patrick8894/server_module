import logging

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    logger.handlers.clear()

    formatter = logging.Formatter('%(levelname)s(%(name)s):     %(message)s')

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger

startup_logger = get_logger("startup")

api_logger = get_logger("api")

middleware_logger = get_logger("middleware")

token_logger = get_logger("token")

crypto_logger = get_logger("crypto")

user_logger = get_logger("user")

post_logger = get_logger("post")