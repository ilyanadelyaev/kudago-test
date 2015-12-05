import urllib2
import xml.etree.ElementTree


class ParserRoot(object):
    @staticmethod
    def get_url():
        """
        * virtual
        url to read
        """
        return None

    @staticmethod
    def get_parser():
        """
        * virtual
        special parser for xml
        """
        return None

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

    @classmethod
    def run(cls):
        url = cls.get_url()
        if url is None:
            return
        #
        try:
            f = urllib2.urlopen(url)
            xml_data = f.read()
        finally:
            f.close()
            f = None
        #
        root = xml.etree.ElementTree.fromstring(xml_data, parser=cls.get_parser())
        return cls.parse(root)  # virtual
