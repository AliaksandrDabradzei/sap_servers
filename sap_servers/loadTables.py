'''
Created on May 17, 2013

@author: Aliaksandr_Dabradzei
'''
from xlrd import open_workbook  
from sap_servers.models import OS, Database, Location, Host
import re

# [u'Servers pool', u'V/H', u'Location', u'SBEA', u'OS', u'Mem', u'Disk space full',
#              u'Occupied disk space', u'Database', u'Server name', u'Status', u'Landscape',
#              u'Projects', u'Instance/Service', u'Number', u'Instance Type', u'Product',
#              u'Specification', u'UC', u'Clients', u'DEV fixed', u'Owner', u'License',
#              u'License exp.', u'HWU', u'HWU end date']

sheet = open_workbook('c:\Programs\servers.xlsx').sheet_by_index(0)
first_row = sheet.row_values(0)

def load_oses():  # load OSes to database    
    print 'OS loading'
    oses = list(set(sheet.col_values(first_row.index('OS'), 1)))  # list of uniqe OSes
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
    dbs = list(set(sheet.col_values(first_row.index('Database'), 1)))  # list of uniqe OSes
    Database.objects.all().delete()  # clear Databases
    
    for db in dbs:
        db = db.strip()
        x = re.search("\d", db)  # find DB version symbols
        if x:  # if version exist
            name = db[:x.start() - 1]
            version = db[x.start():]
        else:
            name = db
            version = ''
            
        db = Database(name=name,
                      version=version)
        db.save()
            
    for row in Database.objects.all():
        if Database.objects.filter(name=row.name, version=row.version).count() > 1: row.delete()  # delete dublicates
    print 'Database loading finished' 

def load_locs():     
    print 'Locations loading'
    locs = list(set(sheet.col_values(first_row.index('Location'), 1)))  # list of uniqe Locations
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
    # [u'Servers pool', u'V/H', u'Location', u'SBEA', u'OS', u'Mem', u'Disk space full',
#              u'Occupied disk space', u'Database', u'Server name', u'Status', u'Landscape',
#              u'Projects', u'Instance/Service', u'Number', u'Instance Type', u'Product',
#              u'Specification', u'UC', u'Clients', u'DEV fixed', u'Owner', u'License',
#              u'License exp.', u'HWU', u'HWU end date']

    for row in range(1, sheet.nrows):
        host = {}
        host['name'] = sheet.cell(row, first_row.index('Server name')).value  # Server name
        host['vn'] = sheet.cell(row, first_row.index('V/H')).value  # V/H
        host['sbea'] = sheet.cell(row, first_row.index('SBEA')).value  # SBEA
        host['ram'] = sheet.cell(row, first_row.index('Mem')).value  # Mem
        host['hdd'] = sheet.cell(row, first_row.index('Disk space full')).value  # Disk space full
        host['hdd_occ'] = sheet.cell(row, first_row.index('Occupied disk space')).value  # Occupied disk space
        host['loc'] = sheet.cell(row, first_row.index('Location')).value.strip()  # Location
        host['os'] = sheet.cell(row, first_row.index('OS')).value.strip()  # OS
        host['db'] = sheet.cell(row, first_row.index('Database')).value.strip()  # Database
        
        loc = Location.objects.get(location=host['loc']) 
        
        x = re.search("\d", host['db'])
        if x:
            name = host['db'][:x.start() - 1]
            version = host['db'][x.start():]
        else:
            name = host['db']
            version = ''
            
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
