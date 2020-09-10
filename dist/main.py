from logging import LOGGER
from app import app


HOST = '0.0.0.0'
PORT = 80


try:
    LOGGER.info('Running server at {}:{}'.format(HOST, PORT))
    app.run(
        host=HOST,
        port=PORT,
    )
except KeyboardInterrupt:
    LOGGER.info('Shutting down server')
    app.shutdown()
