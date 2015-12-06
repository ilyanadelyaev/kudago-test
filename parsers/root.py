import urllib2
import xml.etree.ElementTree
import logging


logger = logging.getLogger('apps.parsers.root')


class ParserRoot(object):
    ID = None
    URL = None

    @staticmethod
    def get_parser():
        """
        * virtual
        special parser for xml
        """
        return None

    # virtual method, declare unused parameters
    # pylint: disable=W0613
    @classmethod
    def parse(cls, root):
        """
        * virtual
        all logic here
        """
        return None

    @classmethod
    def _process_unknown_element(cls, el):
        ret = []
        if el.text.strip():
            ret.append((el.tag, el.text))
        ch_ret = []
        for ch in el:
            ch_ret.extend(cls._process_unknown_element(ch))
        for k, v in ch_ret:
            ret.append(('{}.{}'.format(el.tag, k), v))
        return ret

    # catch and log broadcast exception
    # to process all parsers
    # pylint: disable=W0703
    @classmethod
    def run(cls):
        if cls.URL is None:
            return
        #
        logger.info('Parsing feed "%s"', cls.URL)
        try:
            try:
                f = None
                f = urllib2.urlopen(cls.URL)
                xml_data = f.read()
            finally:
                if f:
                    f.close()
                f = None
                del f
            #
            root = xml.etree.ElementTree.fromstring(
                xml_data, parser=cls.get_parser())
            ret = cls.parse(root)  # virtual
        except Exception as ex:
            logger.error('Error on feed "%s" parse', cls.URL)
            logger.exception(ex)
            return
        logger.info('Feed "%s" has parsed', cls.URL)
        return ret
