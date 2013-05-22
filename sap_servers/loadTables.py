'''
Created on May 17, 2013

@author: Aliaksandr_Dabradzei
'''
from xlrd import open_workbook  
from sap_servers.models import *  # @UnusedWildImport
import re
import sap_servers
import datetime
import sys


# https://www.dropbox.com/s/gktkvc4h5mqy1hf/servers.xls
sheet = open_workbook('d:\PROGRAMMING\servers.xls').sheet_by_index(0)
first_row = sheet.row_values(0)
# [u'Servers pool', u'V/H', u'Location', u'SBEA', u'OS', u'Mem', u'Disk space full', u'Occupied disk space', u'Database', u'Server name', u'Status', u'Landscape',
# u'Projects', u'Instance/Service', u'Number', u'Instance Type', u'Product', u'Specification', u'UC', u'Clients', u'DEV fixed', u'Owner', u'License', u'License exp.',
# u'HWU', u'HWU end date']

import inspect
objes = []
for name, obj in inspect.getmembers(sap_servers.models):
    if inspect.isclass(obj):
        objes.append(obj)
#  [<class 'sap_servers.models.Database'>, <class 'sap_servers.models.Host'>, <class 'sap_servers.models.Instance'>, <class 'sap_servers.models.InstanceType'>, 
# <class 'sap_servers.models.Landscape'>, <class 'sap_servers.models.License'>, <class 'sap_servers.models.Location'>, <class 'sap_servers.models.OS'>, 
# <class 'sap_servers.models.Product'>, <class 'sap_servers.models.Project'>, <class 'sap_servers.models.System'>, <class 'sap_servers.models.SystemOwner'>, 
# <class 'sap_servers.models.SystemStatus'>]

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
         
def load_dbs():  # load Databases to database
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

def load_locs():  # load Locations to database   
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

def load_pools():
    text = ServerPool.text
    obj_class = ServerPool
    print text + 's loading'
    objs = list(set(sheet.col_values(first_row.index(text), 1)))  # list of uniqe Inst Types
    obj_class.objects.all().delete() 

    for obj in objs:
        obj = obj.strip()
        obj = obj_class(name=str(obj))
        obj.save()
            
    for row in obj_class.objects.all():
        if obj_class.objects.filter(name=row.name).count() > 1: row.delete()
    print text + ' loading finished'
    
def load_hosts():  # load Hosts to database
    print 'Hosts loading'
    Host.objects.all().delete() 

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
        host['pool'] = sheet.cell(row, first_row.index('Servers pool')).value.strip()
        
        loc = Location.objects.get(location=host['loc']) 
        
        x = re.search("\d", host['db'])
        if x:
            name = host['db'][:x.start() - 1]
            version = host['db'][x.start():]
        else:
            name = host['db']
            version = ''
            
        db = Database.objects.get(name=name, version=version)
        pool = ServerPool.objects.get(name=host['pool'])
        
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
                   OS=os,
                   pool=pool)
        hos.save()
    
    for row in Host.objects.all():
        if Host.objects.filter(name=row.name).count() > 1:
            row.delete()
    print 'Hosts loading finished'

def load_proj():
    text = Project.text
    obj_class = Project
    print text + ' loading'
    objs = list(set(sheet.col_values(first_row.index(text), 1)))  # list of uniqe Projects
    obj_class.objects.all().delete() 

    for obj1 in objs:
        obj1 = obj1.strip().split(',')
        for obj in obj1:
            obj = obj_class(name=str(obj))
            obj.save()

            
    for row in obj_class.objects.all():
        if obj_class.objects.filter(name=row.name).count() > 1: row.delete()
    print text + 's loading finished'
    
def load_inst_type():
    text = InstanceType.text
    obj_class = InstanceType
    print text + 's loading'
    objs = list(set(sheet.col_values(first_row.index(text), 1)))  # list of uniqe Inst Types
    obj_class.objects.all().delete() 

    for obj in objs:
        obj = obj.strip()
        obj = obj_class(type=str(obj))
        obj.save()
            
    for row in obj_class.objects.all():
        if obj_class.objects.filter(type=row.type).count() > 1: row.delete()
    print text + ' loading finished'

def load_product():
    text = Product.text
    obj_class = Product
    print text + 's loading'
    objs = list(set(sheet.col_values(first_row.index(text), 1)))  # list of uniqe Inst Types
    obj_class.objects.all().delete() 

    for obj1 in objs:
        obj1 = obj1.strip().split(',')
        for obj in obj1:
            obj = obj.strip()
            x = re.search('\d(?<!R/3).*', obj)
            if x:
                name = obj[:x.start()]
                version = x.group()
            else:
                name = obj
                version = ''
            obj = obj_class(name=name, version=version)
            obj.save()
            
    for row in obj_class.objects.all():
        if obj_class.objects.filter(name=row.name, version=row.version).count() > 1: row.delete()
    print text + ' loading finished'

def load_land():
    text = Landscape.text
    obj_class = Landscape
    print text + 's loading'
    objs = list(set(sheet.col_values(first_row.index(text), 1)))  # list of uniqe Inst Types
    obj_class.objects.all().delete() 

    for obj in objs:
        obj = obj.strip()
        obj = obj_class(name=str(obj))
        obj.save()
            
    for row in obj_class.objects.all():
        if obj_class.objects.filter(name=row.name).count() > 1: row.delete()
    print text + ' loading finished'
    
def load_status():
    text = SystemStatus.text
    obj_class = SystemStatus
    print text + 's loading'
    objs = list(set(sheet.col_values(first_row.index(text), 1)))  # list of uniqe Inst Types
    obj_class.objects.all().delete() 

    for obj in objs:
        obj = obj.strip()
        obj = obj_class(status=str(obj))
        obj.save()
            
    for row in obj_class.objects.all():
        if obj_class.objects.filter(status=row.status).count() > 1: row.delete()
    print text + ' loading finished'

def load_license():
    text = License.text
    obj_class = License
    print text + 's loading'
    obj_class.objects.all().delete() 
    for row in range(1, sheet.nrows):
        name = sheet.cell(row, first_row.index('License')).value  # Server name
        exp = sheet.cell(row, first_row.index('License exp.')).value  # V/H
        if type(exp) == float:
            exp = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=exp)
            isTemp = False
        else:
            exp = None
            isTemp = True
        obj = obj_class(license=name, license_exp=exp, isTemp=isTemp)
        obj.save()
             
    for row in obj_class.objects.all():
        if obj_class.objects.filter(license=row.license, license_exp=row.license_exp, isTemp=row.isTemp).count() > 1: row.delete()
    print text + ' loading finished'

def load_owner():
    text = SystemOwner.text
    obj_class = SystemOwner
    print text + 's loading'
    objs = list(set(sheet.col_values(first_row.index(text), 1)))  # list of uniqe Inst Types
    obj_class.objects.all().delete() 

    for obj in objs:
        obj = obj.strip().split(' ')
        if obj != ['']:
            first_name = obj[0]
            last_name = obj[1]
            email = obj[0] + '_' + obj[1] + '@epam.com'
        else:
            first_name, last_name, email = None, None, ''
        obj = obj_class(first_name=str(first_name), last_name=str(last_name), email=email)
        obj.save()
            
    for row in obj_class.objects.all():
        if obj_class.objects.filter(first_name=row.first_name, last_name=row.last_name).count() > 1: row.delete()
    print text + ' loading finished'

def load_instance():
    text = Instance.text
    obj_class = Instance
    print text + 's loading'
    obj_class.objects.all().delete() 
    for row in range(1, sheet.nrows):
        sids = sheet.cell(row, first_row.index('Instance/Service')).value.split(',')  # Server name
        inst_nr = str(sheet.cell(row, first_row.index('Number')).value)  # V/H
        inst_type = sheet.cell(row, first_row.index('Instance Type')).value
        if len(inst_nr) == 1 : inst_type = '0'+inst_type
        host = sheet.cell(row, first_row.index('Server name')).value
        
        inst_type = InstanceType.objects.get(type=inst_type)
        isSap = inst_type.type in ['ABAP', 'JAVA', 'ABAP+JAVA']
        if sids != ['']:
            for sid in sids:
                    
                obj = obj_class(sid=sid,
                                instance_nr=int(inst_nr or 0),
                                instance_type=inst_type,
                                isSap=isSap)
                obj.save()
                host = Host.objects.get(name=host)
                obj.hosts.add(host)
                             
    for row in obj_class.objects.all():
        if obj_class.objects.filter(sid=row.sid, hosts=row.hosts, instance_nr=row.instance_nr, instance_type=row.instance_type).count() > 1: row.delete()
    print text + ' loading finished'
 
def load_hwu():
    text = HWU.text
    obj_class = HWU
    print text + 's loading'
    obj_class.objects.all().delete() 
    for row in range(1, sheet.nrows):
        names = re.findall(r"[\w']+", str(sheet.cell(row, first_row.index('HWU')).value))
        exp = sheet.cell(row, first_row.index('HWU end date')).value  # V/H
        if type(exp) == float:
            exp = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=exp)
        else:
            exp = None
        for name in names:
            if name != '0':
                obj = obj_class(name=name, hwu_exp=exp)
                obj.save()
             
    
    for row in obj_class.objects.all():
        if obj_class.objects.filter(name=row.name, hwu_exp=row.hwu_exp).count() > 1: row.delete()
    print text + ' loading finished'
       
def load_system():
    print 'Systems loading'
    System.objects.all().delete() 
    for row in range(1, sheet.nrows):
        systems = {}
        row_vals = sheet.row_values(row)
        sid = row_vals[first_row.index('Instance/Service')]
        systems['name'] = row_vals[first_row.index('Server name')]
        if sid != '':
            systems['name'] += '_'+sid
        systems['isOnline'] = row_vals[first_row.index('Status')] == 'online'
        status = row_vals[first_row.index('Status')]
        systems['status'] = SystemStatus.objects.get(status=status)
        landscape = row_vals[first_row.index('Landscape')]
        systems['landscape'] = Landscape.objects.get(name=landscape)
        systems['specification'] = row_vals[first_row.index('Specification')]
        systems['uc'] = row_vals[first_row.index('UC')] == "Yes"
        systems['clients'] = row_vals[first_row.index('Clients')]
        owner = row_vals[first_row.index('Owner')]
        if owner != '':
            r = re.match(r"(\w+) (\w+)", owner)
            owner = r.group(1) + '_' + r.group(2) + "@epam.com" 
        systems['owner'] = SystemOwner.objects.get(email=owner)              
        license_name = row_vals[first_row.index('License')]
        license_exp = row_vals[first_row.index('License exp.')]  
        if type(license_exp) == float:
            license_exp = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=license_exp)
        else:
            license_exp = None    
        systems['license'] = License.objects.get(license=license_name, license_exp=license_exp)
        
        system = System(name=systems['name'],
                        isOnline=systems['isOnline'],
                        status=systems['status'],
                        landscape=systems['landscape'],
                        # projects=,
                        # instance=systems['instance'],
                        # product=systems['product'],
                        specification=systems['specification'],
                        uc=systems['uc'],
                        clients=systems['clients'],
                        owner=systems['owner'],
                        license=systems['license'])
                        #HWU=systems['HWU'])
        system.save()
        
        systems['project'] = row_vals[first_row.index('Projects')]
        systems['inst'] = row_vals[first_row.index('Instance/Service')]
        systems['prod'] = row_vals[first_row.index('Product')]
        systems['hwu'] = row_vals[first_row.index('HWU')]
       
        try:
            project = Project.objects.get(name=systems['project'])
            system.projects.add(project)
            inst = Instance.objects.get(sid=systems['inst'])
            system.instance.add(inst)
            #prod = Product.objects.get(name=systems['prod'])
            
            for obj in systems['prod'].split(','):
                obj = obj.strip()
                x = re.search('\d(?<!R/3).*', obj)
                if x:
                    name = obj[:x.start()]
                    version = x.group()
                else:
                    name = obj
                    version = ''
                prod = Product.objects.get(name=name, version=version)
                system.product.add(prod)
            if type(systems['prod']) == int:
                hwu = HWU.objects.get(name=systems['hwu'])
                system.HWU.add(hwu)
        except:
            print "error:", sys.exc_info()[0]
            print 'project:', systems['project'], 'inst:', systems['inst'], 'prod:', systems['prod'], 'hwu:',systems['hwu'] 
        
        
        
        
                    
    print 'Systems loading finished'

                        
                        
                        
                        
        
        


def load_tables():
#     load_oses()
#     load_dbs()
#     load_locs()
#     load_pools()
#     load_hosts()
#     load_proj()
#     load_inst_type()
#     load_product()
#     load_land()
#     load_status()
#     load_license()
#     load_owner()
#     load_instance()
#     load_hwu()
    load_system()
    return

load_tables()
