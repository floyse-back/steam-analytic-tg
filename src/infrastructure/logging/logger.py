import logging
from logging import getLogger,basicConfig


logger = getLogger(__name__)
logger.setLevel(logging.INFO)

basicConfig(level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
            )

