import logging

def get_logger(name):
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

crypto_logger = get_logger("crypto")