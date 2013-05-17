'''
Created on May 17, 2013

@author: Aliaksandr_Dabradzei
'''
from xlrd import open_workbook  
from sap_servers.models import OS, Database, Location, Host
import re

sheet = open_workbook('d:\PROGRAMMING\servers.xls').sheet_by_index(0)

def load_oses():  # load OSes to database    
    print 'OS loading'
    oses = list(set(sheet.col_values(5, 1)))  # list of uniqe OSes
    OS.objects.all().delete()  
    
    for os in oses:
        os = os.strip()
        x = os.find('x')  # position of bit number
        if x != -1:  # if bits mentioned
            bit = int(os[x + 1:x + 3])  # select bits
            if x == 0:  # at the beggining
                os_name = os[x + 3:]  # select OS name
            else:  # at the end
                os_name = os[:x - 3]        
        else:
            os_name, bit = os, None  # if bits are unknown
        
        os = OS(name=str(os_name),
               bit=bit)
        os.save()  # load OS to database
              
    for row in OS.objects.all():
        if OS.objects.filter(name=row.name, bit=row.bit).count() > 1: row.delete()  # delete dublicates
        
    print 'OS loading finished' 
         
def load_dbs():
    print 'Database loading'
    dbs = list(set(sheet.col_values(9, 1)))  # list of uniqe OSes
    Database.objects.all().delete()  # clear Databases
    
    for db in dbs:
        db = db.strip()
        x = re.search("\d", db)  # find DB version symbols
        if x:  # if version exist
            name = db[:x.start() - 1]
            version = db[x.start():]
        else:
            name = db
            version = None
            
        db = Database(name=name,
                      version=version)
        db.save()
            
    for row in Database.objects.all():
        if Database.objects.filter(name=row.name, version=row.version).count() > 1: row.delete()  # delete dublicates
    print 'Database loading finished' 

def load_locs():     
    print 'Locations loading'
    locs = list(set(sheet.col_values(3, 1)))  # list of uniqe Locations
    Location.objects.all().delete() 
    
    for loc in locs:
        loc = loc.strip()
        loc = Location(location=str(loc))
        loc.save()
            
    for row in Location.objects.all():
        if Location.objects.filter(location=row.location).count() > 1: row.delete()
    print 'Locations loading finished'

def load_hosts():
    print 'Hosts loading'
    Host.objects.all().delete() 
    
    for row in range(1, sheet.nrows):
        host = {}
        host['name'] = sheet.cell(row, 10).value  # Server name
        host['vn'] = sheet.cell(row, 2).value  # V/H
        host['sbea'] = sheet.cell(row, 4).value  # SBEA
        host['ram'] = sheet.cell(row, 6).value  # Mem
        host['hdd'] = sheet.cell(row, 7).value  # Disk space full
        host['hdd_occ'] = sheet.cell(row, 8).value  # Occupied disk space        
        host['loc'] = sheet.cell(row, 3).value.strip() # Location
        host['os'] = sheet.cell(row, 5).value.strip() # OS
        host['db'] = sheet.cell(row, 9).value.strip() # Database
        
        loc = Location.objects.get(location=host['loc']) 
        
        x = re.search("\d", host['db'])
        if x:
            name = host['db'][:x.start() - 1]
            version = host['db'][x.start():]
        else:
            name = host['db']
            version = None
            
        db = Database.objects.get(name=name, version=version)
        
        x = host['os'].find('x') 
        if x != -1: 
            bit = int(host['os'][x + 1:x + 3])
            if x == 0: 
                os_name = host['os'][x + 3:]
            else:
                os_name = host['os'][:x - 3]
        else:
            os_name, bit = host['os'], None
          
        os = OS.objects.get(name=str(os_name), bit=bit)    
        
        hos = Host(name=host['name'],
                   vn=host['vn'],
                   sbea=host['sbea'],
                   RAM=int(host['ram'] or 0),
                   HDD_all=int(host['hdd'] or 0),
                   HDD_occup=int(host['hdd_occ'] or 0),
                   location=loc,
                   database=db,
                   OS=os)
        hos.save()
    
    for row in Host.objects.all():
        if Host.objects.filter(name=row.name).count() > 1:
            row.delete()
    print 'Hosts loading finished'

load_oses()
load_dbs()
load_locs()
load_hosts()
