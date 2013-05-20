from django.db import models

class OS(models.Model):
    text = 'OS'
    name = models.CharField(max_length=25, default="WS2008 R2 SE")  # Windows 2008 or others
    bit = models.IntegerField(blank=True, null=True)  # 32x or 64

    def __unicode__(self):
        if self.bit: self.bit = 'x'+str(self.bit)
        return u'%s %s' % (self.name, self.bit)
    
class Database(models.Model):
    text = 'Database'
    name = models.CharField(max_length=20, default="Oracle")  # e.g. Oracle
    version = models.CharField(max_length=20, null=True, blank=True) #11.2.0.3

    def __unicode__(self):
        return u'%s %s' % (self.name, self.version)
    
class Location(models.Model):
    text = 'Location'
    location = models.CharField(max_length=20)  # e.g. K1
    
    def __unicode__(self):
        return self.location

class Host(models.Model):    
    text = 'Server name'
    name = models.CharField(max_length=20)  # e.g. evbyminsd1904
    vn = models.CharField(max_length=1, null=True, blank=True)  # Virtual or Hard?
    location = models.ForeignKey(Location, null=True, blank=True)  # e.g. K1-3
    sbea = models.CharField(max_length=1, null=True, blank=True) # Y or N
    OS = models.ForeignKey(OS, null=True, blank=True)
    RAM = models.IntegerField(default=0)  # in GB
    HDD_all = models.IntegerField(default=0)  # in GB
    HDD_occup = models.IntegerField(default=0)  # in GB
    database = models.ForeignKey(Database, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    text = 'Projects'
    name = models.CharField(max_length=10)  # e.g. EPMS-PRTS

    def __unicode__(self):
        return self.name

class Product(models.Model):
    text = 'Product'
    name = models.CharField(max_length=30)  # e.g. SAP NetWeaver
    version = models.CharField(max_length=20)  # e.g. 7.0

    def __unicode__(self):
        return self.name

class Landscape(models.Model):
    text = 'Landscape'
    name = models.CharField(max_length=20)  # e.g. Production

    def __unicode__(self):
        return self.name

class SystemStatus(models.Model):
    text = 'Status'
    status = models.CharField(max_length=20)  # e.g. switched-off

    def __unicode__(self):
        return self.status

class SystemOwner(models.Model):
    text = 'Owner'
    first_name = models.CharField(max_length=20) #Aliaksandr
    last_name = models.CharField(max_length=20)  #Dabradzei    
    email = models.EmailField(blank=True)   #Aliaksandr_Dabradzei@epam.com

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class InstanceType(models.Model):
    text = 'Instance Type'
    type = models.CharField(max_length=20)  # ABAP, JAVA, ABAP+JAVA, BO

    def __unicode__(self):
        return self.type

class Instance(models.Model):
    text = 'Instance/Service'
    sid = models.CharField(max_length=10) # SM7
    instance_nr = models.IntegerField() # 00
    instance_type = models.ForeignKey(InstanceType) 
    hosts = models.ManyToManyField(Host)

    def __unicode__(self):
        return self.sid
    
class License(models.Model):
    text = 'License'
    license = models.IntegerField()
    license_exp = models.DateField()
    
    def __unicode__(self):
        return self.license
    
class System(models.Model):
    name = models.CharField(max_length=20)  # e.g. evbyminsd1904_pi5
    pool = models.CharField(max_length=30)  # e.g. SAP Servers
    isOnline = models.BooleanField(default=False)  # e.g. offline
    status = models.ForeignKey(SystemStatus)
    landscape = models.ForeignKey(Landscape)
    projects = models.ManyToManyField(Project)
    instance = models.ForeignKey(Instance)
    product = models.ManyToManyField(Product)
    specification = models.CharField(max_length=100)  # e.g. based on NW7.0 EHP1
    uc = models.BooleanField(default=False)
    clients = models.CharField(max_length=100, default="000, 001,")  # e.g. 000, 001, 100
    owner = models.ForeignKey(SystemOwner)  # e.g. "Aleh Mikhniuk"
    license = models.ForeignKey(License)
    HWU = models.IntegerField()
    HWU_exp = models.DateField()
    
    def __unicode__(self):
        return self.name






    