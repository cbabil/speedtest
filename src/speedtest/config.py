# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger(__name__)


def setup_logging(loglevel):
    """
    Defines the logging
    """
    loglevel = 'INFO' if not loglevel else loglevel
    logging.basicConfig(
        level=loglevel,
        format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    )
    logger.info('log level: {}'.format(loglevel))
