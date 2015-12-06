import logging

import parsers.kudago


logger = logging.getLogger('apps.parsers.controller')


class Controller(object):
    """
    Store and run your parsers from here

    See logs/apps.log after processing to catch errors and unknowns
    """

    # add your parser here
    __active_parsers = (
        parsers.kudago.Parser,
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
