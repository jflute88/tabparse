from parse import Workbook
from parse import Dashboard
from parse import Datasource
from parse import ConnectionTag
from parse import Column
from parse import MetadataRecord

# sourceTWBX = Workbook('Tableau.xml')
workbook = Workbook('Which Sport is the Toughest_.twbx')

print('----------------------------------------------------------')

print('--WORKBOOK--')
print('---- filename:\t{0}'.format(workbook.filename))
for attr in workbook.ATTRIBUTES:
    if hasattr(workbook,"_" + attr) :
        print('---- '  + attr + ':' + workbook.__dict__[ "_" + attr] )

print('--dashboards:\t{0}'.format(len(workbook.dashboards)))
for dash in workbook.dashboards:
    print('----dashboard')
    for attr in dash.ATTRIBUTES:
        if hasattr(dash,"_" + attr) :
            print( '------'  + attr + ':' + dash.__dict__[ "_" + attr] )
    for ds in dash._datasources:
        print("------datasource:{}".format(ds))

print('--datasources:\t{0}'.format(len(workbook.datasources)))
for ds in workbook.datasources:
    print('----datasource')
    for attr in ds.ATTRIBUTES:
        if hasattr(ds,"_" + attr) :
            print( '------'  + attr + ':' + ds.__dict__["_" + attr] )

    print( '------connections')
    for con in ds._connections:
        print( '--------connection')
        for attr in ConnectionTag.ATTRIBUTES:
            if hasattr(con,"_" + attr) :
                print("----------{} {}".format(attr , con.__dict__["_" + attr]))
        print( '----------Metadata Records')
        for metarec in con._metadataRecords:
            print('------------Metadata Record')
            for attr in MetadataRecord.ATTRIBUTES:
                if hasattr(metarec,"_" + attr) :
                    print("--------------{} {}".format(attr , metarec.__dict__["_" + attr]))

    print( '------columns')
    for col in ds._columns:
        print( '--------column')
        for attr in Column.ATTRIBUTES:
            if hasattr(col,"_" + attr) :
                print("----------{} {}".format(attr , col.__dict__["_" + attr]))

print('--worksheets:\t{0}'.format(len(workbook.worksheets)))
for data in workbook.worksheets:
    print("--      {}".format(data))

print('----------------------------------------------------------')

worksheets = workbook.worksheets
for worksheet in worksheets:
    print("worksheet: {}".format(worksheet))
    for datasource in workbook.datasources:
        print("-- datasource: {}".format(datasource.name))
        for count, field in enumerate(datasource.fields.values()):
            if worksheet in field.worksheets:
                print(field)
