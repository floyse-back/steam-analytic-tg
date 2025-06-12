import logging
from logging import getLogger,basicConfig


logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)

basicConfig(level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
            )

