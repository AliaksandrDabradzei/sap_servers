'''
Created on May 17, 2013

@author: Aliaksandr_Dabradzei
'''
from xlrd import open_workbook, cellname

wb = open_workbook('d:\PROGRAMMING\servers.xls')

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

sheet = wb.sheet_by_index(0)

#print sheet.name

# for row_index in range(1):
#     for col_index in range(sheet.ncols):
#         print cellname(row_index, col_index), '-',
#         print sheet.cell(row_index, col_index).value

print sheet.row_values(0,1)
#print sheet.col(1)
