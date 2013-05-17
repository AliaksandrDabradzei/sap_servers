'''
Created on May 17, 2013

@author: Aliaksandr_Dabradzei
'''
from xlrd import open_workbook, cellname  # @UnusedImport
from sap_servers.models import OS, Database
import re

sheet = open_workbook('d:\PROGRAMMING\servers.xls').sheet_by_index(0)

#===================================================
# OS loading
#===================================================

print 'OS loading'
oses = list(set(sheet.col_values(5, 1))) # list of uniqe OSes
OS.objects.all().delete() 
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

#===================================================
# Database loading
#===================================================

print 'Database loading'
dbs = list(set(sheet.col_values(9, 1))) # list of uniqe OSes
Database.objects.all().delete() 
for db in dbs:
    db = db.strip()
    x = re.search("\d", db)
    if x:
        name = db[:x.start()-1]
        version = db[x.start():]
    else:
        name = db
        version = None
    db = Database(name=name,
                  version=version)
    db.save()
   
for row in Database.objects.all():
    if Database.objects.filter(name=row.name, version=row.version).count() > 1:
        row.delete()
print 'Database loading finished'

