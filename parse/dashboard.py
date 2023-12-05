import xml.etree.ElementTree as ET
import os

class Dashboard(object):
    ATTRIBUTES = [
        'name'
    ]
    ATTRIBUTES_DATASOURCE = [
        'caption',
        'name'
    ]

    def __init__(self, xml):
        if xml is None:
            return None

        self._xml = xml
        for attrib in Dashboard.ATTRIBUTES:
            setattr(self, '_{}'.format(attrib), self._xml.get(attrib,None))
        
        # datasourceタグの解析
        self._datasources = []
        datasources = self._xml.find('.//datasources')
        if datasources is not None:
            for datasource in datasources.findall("datasource"):
                dsdic = {}
                for attrib in Dashboard.ATTRIBUTES_DATASOURCE:
                    dsdic[attrib] = datasource.get(attrib,None)
                self._datasources.append(dsdic)

        # datasource-dependenciesタグの解析
        self._datasourceDependencies = []

        # zoneタグ（未解析）
        