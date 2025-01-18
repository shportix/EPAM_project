"""
runner file
"""
import logging
from api import app  # pylint: disable=import-error


file_log = logging.FileHandler('delivery_app_logger.log', mode='w')
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out),
                    level=logging.INFO)
logging.info('Started')
if __name__ == '__main__':
    app.run()
logging.info('Finished')
