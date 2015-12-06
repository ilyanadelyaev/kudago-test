import logging

import parsers.kudago


logger = logging.getLogger('apps.parsers.controller')


class Controller(object):
    # add your parser here
    __active_parsers = (
        parsers.kudago.Parser,
    )

    @classmethod
    def run(cls):
        logger.info('Parse feeds')
        #
        ret = {}
        for parser in cls.__active_parsers:
            logger.info('Run parser "{}"'.format(parser.NAME))
            ret[parser.NAME] = parser.run()
            logger.info('Done for "{}"'.format(parser.NAME))

        return ret
