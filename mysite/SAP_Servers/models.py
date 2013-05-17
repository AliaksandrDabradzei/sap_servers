from django.db import models

# Create your models here.
class OS(models.Model):
    name = models.CharField(max_length=15, default="WS2008 R2 SE")  # Windows 2008 or others
    bit = models.IntegerField(default=64)  # 32x or 64

    def __unicode__(self):
        return u'%s x%s' % (self.name, self.bit)
    
class Database(models.Model):
    name = models.CharField(max_length=20, default="Oracle 11.2.0.3.0")  # e.g. Oracle 11g

    def __unicode__(self):
        return self.name
    
class Locations(models.Model):
    location = models.CharField(max_length=20)  # e.g. K1
    
    def __unicode__(self):
        return self.location

class Hosts(models.Model):    
    name = models.CharField(max_length=20)  # e.g. evbyminsd1904
    isVirtual = models.BooleanField()  # Virtual or Hard?
    location = models.ForeignKey(Locations)  # e.g. K1-3
    SBEA = models.BooleanField()
    OS = models.ForeignKey(OS)
    RAM = models.DecimalField()  # in GB
    HDD_all = models.DecimalField()  # in GB
    HDD_occup = models.DecimalField()  # in GB
    database = models.ForeignKey(Database)

    def __unicode__(self):
        return self.name

class Projects(models.Model):
    name = models.CharField(max_length=10)  # e.g. EPMS-PRTS

    def __unicode__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=30)  # e.g. SAP NetWeaver
    version = models.CharField(max_length=20)  # e.g. 7.0

    def __unicode__(self):
        return self.name

class Landscapes(models.Model):
    name = models.CharField(max_length=20)  # e.g. Production

    def __unicode__(self):
        return self.name

class SystemStatus(models.Model):
    status = models.CharField(max_length=20)  # e.g. switched-off

    def __unicode__(self):
        return self.status

class SystemOwners(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class InstanceType(models.Model):
    type = models.CharField(max_lenght=20)  # ABAP, JAVA, ABAP+JAVA, BO

    def __unicode__(self):
        return self.type

class Instance(models.Model):
    sid = models.CharField(max_length=10)
    instance_nr = models.DecimalField()
    instance_type = models.ForeignKey(InstanceType)
    hosts = models.ManyToManyField(Hosts)

    def __unicode__(self):
        return self.sid
    
class Licenses(models.Model):
    license = models.DecimalField()
    license_exp = models.DateField()
    
    def __unicode__(self):
        return self.license
    
class Systems(models.Model):
    name = models.CharField(max_length=20)  # e.g. evbyminsd1904_pi5
    pool = models.CharField(max_length=30)  # e.g. SAP Servers
    isOnline = models.BooleanField(default=False)  # e.g. offline
    status = models.ForeignKey(SystemStatus)
    landscape = models.ForeignKey(Landscapes)
    projects = models.ManyToManyField(Projects)
    instance = models.ForeignKey(Instance)
    product = models.ManyToManyField(Products)
    specification = models.CharField(max_length=100)  # e.g. based on NW7.0 EHP1
    uc = models.BooleanField(default=False)
    clients = models.CharField(max_length=100, default="000, 001,")  # e.g. 000, 001, 100
    owner = models.ForeignKey(SystemOwners)  # e.g. "Aleh Mikhniuk"
    license = models.ForeignKey(Licenses)
    HWU = models.DecimalField()
    HWU_exp = models.DateField()
    
    def __unicode__(self):
        return self.name






    
