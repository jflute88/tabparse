import xml.etree.ElementTree as ET
import os
from .metadatarecord import MetadataRecord

class ConnectionTag(object):
    ATTRIBUTES = [
        'caption',
        'name'
    ]

    def __init__(self, xml):
        if xml is None:
            return None

        self._xml = xml
        namedconnections = self._xml.find('.//named-connections')
        if namedconnections is not None:
            for namedconnection in namedconnections.findall("named-connection"):
                self._caption = namedconnection.get('caption',None)
                self._name = namedconnection.get('name',None)

        # relation（未解析）

        # metadata-recordsの解析
        self._metadataRecords = []
        metadatarecords = self._xml.find('.//metadata-records')
        if metadatarecords is not None:
            for metadatarecord in metadatarecords.findall("metadata-record"):
                metarec = MetadataRecord(metadatarecord)
                self._metadataRecords.append(metarec)
