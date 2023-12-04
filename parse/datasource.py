import xml.etree.ElementTree as ET
import os
from .connectiontag import ConnectionTag
from .column import Column

class Datasource(object):
    ATTRIBUTES = [
        'caption',
        'name',
        'version'
    ]
    def __init__(self, xml):
        if xml is None:
            return None

        self._xml = xml
        for attrib in Datasource.ATTRIBUTES:
            setattr(self, '_{}'.format(attrib), self._xml.get(attrib,None))
        
        # connectionの解析
        # バージョンにより形式が異なる
        self._connections = []
        connections = self._xml.find('.//connections')
        if connections is not None:
            for conxml in connections.findall("connection"):
                connection = ConnectionTag(conxml)
                self._connections.append(connection)
        else:
            connection = self._xml.find('.//connection')
            if connection is not None:
                self._connections.append(ConnectionTag(connection))

        # columnの解析
        self._columns = []
        for colxml in self._xml.findall("column"):
            column = Column(colxml)
            self._columns.append(column)
