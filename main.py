from src.server import run_server
import logging


if __name__ == '__main__':
    FORMAT = "[%(asctime)s][%(filename)s][%(lineno)s][%(funcName)5s()] %(message)s"
    formatter = logging.Formatter(FORMAT)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[console_handler])
    logging.info('Start Serving...')
    try:
        run_server('0.0.0.0')
    except Exception as e:
        logging.info('Exception detected，Server will exit', exc_info=True)
