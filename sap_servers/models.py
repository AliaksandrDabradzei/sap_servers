from django.db import models


    #---------------------------------
    # Information about Hosts
    #---------------------------------

class ServerPool(models.Model):
    text = 'Servers pool'
    name = models.CharField(max_length=30)  # SAP Infrastructure
     
    def __unicode__(self):
        return self.name
     
class Location(models.Model):
    text = 'Location'
    location = models.CharField(max_length=20)  # K1
     
    def __unicode__(self):
        return self.location
 
class OS(models.Model):
    text = 'OS'
    name = models.CharField(max_length=30)  # Windows 2008 R2
    bit = models.CharField(max_length=4,
                           blank=True,
                           choices=(('32', 'x32'), ('64', 'x64'))
                           )  # 32x or 64
 
    def __unicode__(self):
        return u'%s %s' % (self.name, self.bit)
     
class Database(models.Model):
    text = 'Database'
    name = models.CharField(max_length=20)  # Oracle
    version = models.CharField(max_length=20, blank=True)  # 11.2.0.3
 
    def __unicode__(self):
        return u'%s %s' % (self.name, self.version)
     
class Landscape(models.Model):
    text = 'Landscape'
    name = models.CharField(max_length=20)  # Production
 
    def __unicode__(self):
        return self.name
 
class HWU(models.Model):
    text = "HWU"
    name = models.CharField(max_length=10) # 27530  # http://pmcmsq.epam.com/hwu/srrView.do?srrId=27530
    hwu_exp = models.DateField(null=True, blank=True) # 12/31/2020
     
    def __unicode__(self):
        return self.name
     
 
class Host(models.Model):    
    text = 'Server name'
    name = models.CharField(max_length=20)  # e.g. evbyminsd1904
    pool = models.ForeignKey(ServerPool)
    isVirtual = models.NullBooleanField(null=True) # Virtual?
    location = models.ForeignKey(Location, null=True, blank=True)
    sbea = models.NullBooleanField(null=True)  # Y or N
    os = models.ForeignKey(OS, null=True, blank=True)
    ram = models.IntegerField(default=0,
                              help_text="Please put memory in GB.")  # RAM in GB
    hdd_all = models.IntegerField(default=0,
                              help_text="Please put memory in GB.")  # HDD in GB
    hdd_occup = models.IntegerField(default=0,
                              help_text="Please put memory in GB.")  # HDD occupied in GB
    database = models.ForeignKey(Database, null=True, blank=True)
    landscape = models.ForeignKey(Landscape, null=True, blank=True)
    hwu = models.ManyToManyField(HWU, null=True, blank=True)
    isOnline = models.BooleanField(default=False) # on or off
     
     
    def __unicode__(self):
        return self.name    
     
#---------------------------------
# Information about Instance
#---------------------------------
 
class InstanceType(models.Model):
    text = 'Instance Type'
    type = models.CharField(max_length=20)  # ABAP, JAVA, ABAP+JAVA, BO
 
    def __unicode__(self):
        return self.type
 
class SystemOwner(models.Model):
    text = 'Owner'
    first_name = models.CharField(max_length=20)  # Aliaksandr
    last_name = models.CharField(max_length=20)  # Dabradzei    
    email = models.EmailField(blank=True)  # Aliaksandr_Dabradzei@epam.com
 
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
     
class License(models.Model):
    text = 'License'
    license = models.CharField(max_length=20, default='INITIAL') # 0020666317 or Initial
    license_exp = models.DateField(null=True, blank=True) # 12/31/9999
    license_tmp = models.CharField(max_length=20, null=True, blank=True) # 2 weeks
     
    def __unicode__(self):
        return self.license
 
class SID(models.Model):
    text = 'Instance/Service'
    name = models.CharField(max_length=15) # SM7
    license = models.ForeignKey(License, blank=True, null=True)
     
    def __unicode__(self):
        return self.name
 
class Instance(models.Model):
    text = 'Instance/Service'
    name = models.CharField(max_length=20) # evbyminsd1251_00
    instance_nr = models.CharField(max_length=2, blank=True, null=True)  # 00
    instance_type = models.ForeignKey(InstanceType, null=True, blank=True) 
    host = models.ForeignKey(Host)
    sid = models.ForeignKey(SID)
    isSap = models.BooleanField(default=False) # 
     
    def __unicode__(self):
        return self.sid
     
#     def admin_hosts(self):
#         return ', '.join([a.name for a in self.hosts.all()])
#     
#     admin_hosts.short_description = "Hosts"
     
     
     
class Product(models.Model):
    text = 'Product'
    name = models.CharField(max_length=30)  # e.g. SAP NetWeaver
    version = models.CharField(max_length=20, null=True, blank=True)  # e.g. 7.0
 
    def __unicode__(self):
        return u'%s %s' % (self.name, self.version)
 
class Project(models.Model):
    text = 'Projects'
    name = models.CharField(max_length=10)  # e.g. EPMS-PRTS
 
    def __unicode__(self):
        return self.name
         
   
class System(models.Model):
    name = models.CharField(max_length=30)  # e.g. evbyminsd1904_pi5
    isOnline = models.BooleanField(default=False)  # e.g. offline
    status = models.CharField(max_length=20)#damaged, deleted, switched-off, non-active, disabled, online
     
    projects = models.ManyToManyField(Project)
    instance = models.ManyToManyField(Instance)
    product = models.ManyToManyField(Product)
    specification = models.CharField(max_length=100, null=True, blank=True)  # e.g. based on NW7.0 EHP1
    uc = models.BooleanField(default=False)
    clients = models.CharField(max_length=100, default="000, 001,", null=True, blank=True)  # e.g. 000, 001, 100
    owner = models.ForeignKey(SystemOwner)  # e.g. "Aleh Mikhniuk"
    license = models.ForeignKey(License)
 
     
    def admin_projects(self):
        return ', '.join([a.name for a in self.projects.all()])
     
    admin_projects.short_description = "Projects"
     
    def admin_instances(self):
        return ', '.join([a.sid for a in self.instance.all()])
     
    admin_instances.short_description = "Instances"
     
    def admin_products(self):
        return ', '.join([a.name for a in self.product.all()])
     
    admin_products.short_description = "Products"
     
    def admin_hwus(self):
        return ', '.join([a.name for a in self.HWU.all()])
     
    admin_hwus.short_description = "HWUs"
     
     
    def __unicode__(self):
        return self.name

class Systems(models.Model):
    servers_pool = models.CharField(max_length=70)
    v_h = models.CharField(max_length=70)
    location = models.CharField(max_length=70)
    sbea = models.CharField(max_length=70)
    os = models.CharField(max_length=70)
    mem = models.CharField(max_length=70)
    disk_space_full = models.CharField(max_length=70)
    occupied_disk_space = models.CharField(max_length=70)
    database = models.CharField(max_length=70)
    server_name = models.CharField(max_length=70)
    status = models.CharField(max_length=70)
    landscape = models.CharField(max_length=70)
    projects = models.CharField(max_length=70)
    instance_service = models.CharField(max_length=70)
    number = models.CharField(max_length=70)
    instance_type = models.CharField(max_length=70)
    product = models.CharField(max_length=70)
    specification = models.CharField(max_length=70)
    uc = models.CharField(max_length=70)
    clients = models.CharField(max_length=70)
    dev_fixed = models.CharField(max_length=70)
    owner = models.CharField(max_length=70)
    license = models.CharField(max_length=70)
    license_exp = models.CharField(max_length=70)
    hwu = models.CharField(max_length=70)
    hwu_end_date = models.CharField(max_length=70)
    
    def __unicode__(self):
        return u"%s %s" % (self.server_name, self.instance_service)





