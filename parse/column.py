import xml.etree.ElementTree as ET
import os

class Column(object):
    ATTRIBUTES = [
        'caption',
        'datatype',
        'role',
        'type',
        'name',
        'formura'
    ]

    def __init__(self, xml):
        if xml is None:
            return None

        # columnタグの属性をオブジェクトの属性として設定
        self._xml = xml
        for attrib in Column.ATTRIBUTES:
            setattr(self, '_{}'.format(attrib), self._xml.get(attrib,None))

        # 計算式があれば情報追加する        
        calc = self._xml.find('.//calculation')
        if calc is not None:
            self._formura = calc.get("formula",None)


