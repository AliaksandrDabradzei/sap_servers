'''
Created on May 17, 2013

@author: Aliaksandr_Dabradzei
'''
from xlrd import open_workbook, cellname
# from models import *
from sap_servers.models import OS


sheet = open_workbook('d:\PROGRAMMING\servers.xls').sheet_by_index(0)

print 'OS loading'
oses = list(set(sheet.col_values(5, 1))) # list of uniqe OSes

for os in oses:
    os = os.strip() # clear information
    x = os.find('x') #position of bit number
    if x != -1: #if bits mentioned
        bit = int(os[x + 1:x + 3])
        if x == 0: #at the beggining
            os_name = os[x + 3:]
        else:
            os_name = os[:x - 3]    #at the end    
    else:
        os_name, bit = os, None

    os = OS(name=str(os_name),
           bit=bit)
    os.save()
    
for row in OS.objects.all():
    if OS.objects.filter(name=row.name, bit=row.bit).count() > 1:
        row.delete()
print 'OS loading finished'



# for s in wb.sheets():
#     print 'Sheet:', s.name
# #     for row in range(s.nrows):
# #         values = []
# #         for col in range(s.ncols):
# #             values.append(str(s.cell(row,col).value)) 
# #         print ','.join(values)
# #         print values
# #     print
#     values = []
#     for row in range(s.nrows):
#         values.append(str(s.cell(row,10).value)) 
#         
#     print values

# sheet = wb.sheet_by_index(0)

# print sheet.name

# for row_index in range(1):
#     for col_index in range(sheet.ncols):
#         print cellname(row_index, col_index), '-',
#         print sheet.cell(row_index, col_index).value

# print sheet.row_values(0,1)
# print sheet.col(1)
