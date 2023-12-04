import xml.etree.ElementTree as ET
import os

class MetadataRecord(object):
    ATTRIBUTES = [
        'remote-name',
        'remote-type',
        'local-name',
        'parent-name',
        'remote-alias>',
        'ordinal',
        'local-type',
        'precision',
        'aggregation',
        'contains-null',
        'collation'
    ]

    def __init__(self, xml):
        if xml is None:
            return None

        # MetadataRecordタグの内部のタグの値をオブジェクトの属性として設定
        self._xml = xml
        for attrib in MetadataRecord.ATTRIBUTES:
            tag = self._xml.find('.//' + attrib)
            if tag is not None:
                setattr(self, '_{}'.format(attrib), tag.text)

