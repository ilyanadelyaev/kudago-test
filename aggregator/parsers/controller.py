import logging

import aggregator.parsers.kudago


logger = logging.getLogger('aggregator.parsers.controller')


class Controller(object):
    """
    Store and run your parsers from here

    See logs/aggregator.log after processing to catch errors and unknowns
    """

    # add your parser here
    __active_parsers = (
        aggregator.parsers.kudago.Parser,
    )

    @classmethod
    def run(cls):
        logger.info('Parse feeds')
        #
        statuses = []
        for parser in cls.__active_parsers:
            logger.info('Run parser "%s"', parser.ID)
            st = parser.run()
            logger.info('Done for "%s"', parser.ID)
            statuses.append((parser.ID, st))
        return statuses
