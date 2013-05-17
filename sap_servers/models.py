from django.db import models

# Create your models here.
class OS(models.Model):
    name = models.CharField(max_length=35) # Windows
    bit = models.IntegerField(default=64) 
    
    def __unicode__(self):
        return u'%s %s' % (self.name, self.bit)
    
class Database(models.Model):
    name = models.CharField(max_length=30) #Oracle
    version = models.CharField(max_length=20) #11.2.0.3
    
    def __unicode__(self):
        return u'%s %s' % (self.name, self.version)
    
class Location(models.Model):
    location = models.CharField(max_length=20) # K1
    
    def __unicode__(self):
        return self.location   
    
class Host(models.Model):    
    name = models.CharField(max_length=20) # evbyminsd1270
    isVirtual = models.BooleanField(default=True) # V/H
    location = models.ForeignKey(Location)
    SBEA = models.BooleanField(default=False)
    OS = models.ForeignKey(OS)
    RAM = models.IntegerField(default=0)
    HDD_all = models.IntegerField(default=0)
    HDD_occup = models.IntegerField(default=0)
    database = models.ForeignKey(Database)
    
    def __unicode__(self):
        return self.name

# 
# class Instance(models.Model):
#     sid = models.CharField(max_length=10)
#     instance_nr = models.DecimalField()
#     instance_type = models.CharField(max_length=20)
#     
# class Projects(models.Model):
#     name = models.CharField(max_length=10)
#     
# class Products(models.Model):
#     name = models.CharField(max_length=30)
#     version = models.CharField(max_length=20)
#     
# class Servers(models.Model):
#     name = models.CharField(max_length=20)
#     pool = models.CharField(max_length=30)
#     host = models.ManyToManyField(Hosts)
#     status = models.CharField(max_length=15)
#     landscape = models.CharField(max_length=20)
#     projects = models.ManyToManyField(Projects)
#     instance = models.ManyToManyField(Instance)
#     product = models.ManyToManyField(Products)
#     specification = models.CharField(max_length=100)
#     uc = models.BooleanField(default=False)
#     clients = models.CharField(max_length=30)
#     owner = models.CharField(max_length=60)
#     license = models.DecimalField()
#     license_exp = models.DateField()
#     HWU = models.DecimalField()
#     HWU_exp = models.DateField()
#     
#     