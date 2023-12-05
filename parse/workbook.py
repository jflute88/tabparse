import xml.etree.ElementTree as ET
import os
import shutil
import tempfile
import zipfile
from .dashboard import Dashboard
from .datasource import Datasource

def find_file_in_zip(zip_file):
    candidate_files = filter(lambda x: x.split('.')[-1] in ('twb'),
                            zip_file.namelist())

    for filename in candidate_files:
        with zip_file.open(filename) as xml_candidate:
            try:
                ET.parse(xml_candidate)
                return filename
            except ET.ParseError:
                pass

class Workbook(object):
    ATTRIBUTES = [
        'version'
    ]
    def __init__(self, filename):
        self._filename = filename

        if zipfile.is_zipfile(filename):
            with zipfile.ZipFile(filename, allowZip64=True) as zf:
                with zf.open(find_file_in_zip(zf)) as xml_file:
                    #print(xml_file)
                    self._workbookTree = ET.parse(xml_file)
        else:
            self._workbookTree = ET.parse(filename)

        if not self._workbookTree:
            return None

        self._workbookRoot = self._workbookTree.getroot()
        for attrib in Workbook.ATTRIBUTES:
            setattr(self, '_{}'.format(attrib), self._workbookRoot.get(attrib,None))

        self._dashboards = self._prepare_dashboards(self._workbookRoot)
        self._datasources = self._prepare_datasources(self._workbookRoot)
        self._worksheets = self._prepare_worksheets(self._workbookRoot)

        # fomula内のnameをcaptionに変換
        self._prepare_formula(self)

    @property
    def dashboards(self):
        return self._dashboards

    @property
    def datasources(self):
        return self._datasources

    @property
    def worksheets(self):
        return self._worksheets

    @property
    def filename(self):
        return self._filename

    @staticmethod
    def _prepare_datasources(xml_root):
        datasources = []
        datasource_elements = xml_root.find('datasources')
        if datasource_elements is None:
            return []
        for dsxml in datasource_elements:
            ds = Datasource(dsxml)
            datasources.append(ds)
        return datasources

    @staticmethod
    def _prepare_dashboards(xml_root):
        dashboards = []

        dashboard_elements = xml_root.find('.//dashboards')
        if dashboard_elements is None:
            return []
        for dash_element in dashboard_elements.findall("dashboard"):
            dashelm = Dashboard(dash_element)
            #dash_name = dash_element.attrib['name']
            dashboards.append(dashelm)

        return dashboards

    @staticmethod
    def _prepare_worksheets(xml_root):
        worksheets = []
        worksheets_element = xml_root.find('.//worksheets')
        if worksheets_element is None:
            return worksheets

        # for worksheet_element in worksheets_element:
        #     worksheet_name = worksheet_element.attrib['name']
        #     worksheets.append(worksheet_name)

        #     dependencies = worksheet_element.findall('.//datasource-dependencies')

        #     for dependency in dependencies:
        #         datasource_name = dependency.attrib['datasource']
        #         datasource = ds_index[datasource_name]
        #         for column in dependency.findall('.//column'):
        #             column_name = column.attrib['name']
        #             if column_name in datasource.fields:
        #                 datasource.fields[column_name].add_used_in(worksheet_name)

        return worksheets

    @staticmethod
    def _prepare_formula(self):
        # columnについて、nameとcaptionのdictionaryを作成する
        coldic = {}
        for ds in self._datasources:
            for col in ds._columns:
                if hasattr(col,"_name") and hasattr(col,"_caption") :
                    coldic[col._name] = col._caption
        
        # columnのfomulaがあれば、計算式の各nameをcaptionに置換し、新たな属性として保存する
        for ds in self._datasources:
            for col in ds._columns:
                if hasattr(col,"_formula"):
                    coldic[col._name] = col._formula

        return True
