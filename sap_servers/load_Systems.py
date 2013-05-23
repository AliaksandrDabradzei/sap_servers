from xlrd import open_workbook  
from sap_servers.models import Systems

sheet = open_workbook('d:\PROGRAMMING\servers.xls').sheet_by_index(0)
first_row = sheet.row_values(0)

def load_Systems():
    print 'Systems loading'
    Systems.objects.all().delete() 

    for row in range(1, sheet.nrows):
        host = {}
        for col in first_row:
            host[col] = sheet.cell(row, first_row.index(col)).value
 # [u'Servers pool', u'V/H', u'Location', u'SBEA', u'OS', u'Mem', u'Disk space full', u'Occupied disk space', u'Database', u'Server name', u'Status', u'Landscape',
# u'Projects', u'Instance/Service', u'Number', u'Instance Type', u'Product', u'Specification', u'UC', u'Clients', u'DEV fixed', u'Owner', u'License', u'License exp.',
# u'HWU', u'HWU end date']
               
        system = Systems(servers_pool=host['Servers pool'],
                        v_h=host['V/H'],
                        location=host['Location'],
                        sbea=host['SBEA'],
                        os=host['OS'],
                        mem=host['Mem'],
                        disk_space_full=host['Disk space full'],
                        occupied_disk_space=host['Occupied disk space'],
                        database=host['Database'],
                        server_name=host['Server name'],
                        status=host['Status'],
                        landscape=host['Landscape'],
                        projects=host['Projects'],
                        instance_service=host['Instance/Service'],
                        number=host['Number'],
                        instance_type=host['Instance Type'],
                        product=host['Product'],
                        specification=host['Specification'],
                        uc=host['UC'],
                        clients=host['Clients'],
                        dev_fixed=host['DEV fixed'],
                        owner=host['Owner'],
                        license=host['License'],
                        license_exp=host['License exp.'],
                        hwu=host['HWU'],
                        hwu_end_date=host['HWU end date']
                         )
        
        system.save()
    
    print 'Systems loading finished'
    
load_Systems()