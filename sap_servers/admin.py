from django.contrib import admin
from sap_servers import models
import sys
import inspect
#from sap_servers.models import OS, Database, Location, Host, Project


# class OSAdmin(admin.ModelAdmin):
#     list_display = ('name', 'bit')
#     ordering = ('name',)
#     
# class DatabaseAdmin(admin.ModelAdmin):
#     list_display = ('name', 'version')
#     ordering = ('name',)
#     
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'version')
#     ordering = ('name',)
#     search_fields = ('name',)
#     
# class ProjectAdmin(admin.ModelAdmin):
#     ordering = ('name',)
#     search_fields = ('name',)
#     
# class LicenseAdmin(admin.ModelAdmin):
#     list_display = ('license','license_exp','isTemp')
# 
# class SystemOwnerAdmin(admin.ModelAdmin):
#     list_display = ('email','first_name','last_name',)
#     search_fields = ('last_name','first_name',)
#     ordering = ('email',)
# 
# class HostAdmin(admin.ModelAdmin):
#     list_display = ('name',
#                     'OS',
#                     'database',
#                     'location',
#                     'pool',
#                     'vn',
#                     'sbea',
#                     'RAM',
#                     'HDD_all',
#                     'HDD_occup',)
#     search_fields = ('name',)
#     ordering = ('name',)
#     
# class InstanceAdmin(admin.ModelAdmin):
#     list_display = ('sid', 'instance_nr', 'instance_type', 'admin_hosts')
#     filter_horizontal = ( 'hosts',)
#     search_fields = ('sid',)
#     ordering = ('sid','-isSap', )
#     
# class HWUAdmin(admin.ModelAdmin):
#     list_display = ('name', 'hwu_exp')
#     ordering = ('name',)
#     
# class SystemAdmin(admin.ModelAdmin):
#     list_display = ('name', 'isOnline', 'status', 'landscape', 'specification', 'uc', 'clients', 'owner', 'license', "admin_projects", "admin_instances", "admin_products", "admin_hwus")
#     filter_horizontal = ( 'projects', 'instance', 'product', 'HWU')
# 
# def register_all():         
#     for name, obj in inspect.getmembers(models): # for all classes in models
#         if inspect.isclass(obj):
#             try:
#                 adminObj = getattr(sys.modules[__name__], name+'Admin') # check if Admin class exists
#             except AttributeError:
#                 admin.site.register(obj) # register model.class
#             else:
#                 admin.site.register(obj, adminObj) # register model.class with admin.class
# 
# def register_spec():
#     admin.site.register(models.Host, HostAdmin)
#     admin.site.register(models.System, SystemAdmin)
#     admin.site.register(models.Instance, InstanceAdmin)
# 
# register_spec()
#register_all()   
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'publisher', 'publication_date')
#     list_filter = ('publication_date',)
#     date_hierarchy = 'publication_date'
#     ordering = ('-publication_date',)
#     fields = ('title', 'authors', 'publisher', 'publication_date')
#     filter_horizontal = ('authors',)
#     raw_id_fields = ('publisher',)

class SystemsAdmin(admin.ModelAdmin):
    list_display = ('server_name', 'instance_service','servers_pool', 'v_h', 'location', 'sbea', 'os', 'mem', 'disk_space_full', 'occupied_disk_space', 'database', 
                    'status', 'landscape', 'projects',  'number', 'instance_type', 'product', 
                    'specification', 'uc', 'clients', 'dev_fixed', 'owner', 'license', 'license_exp', 'hwu', 'hwu_end_date')

admin.site.register(models.Systems, SystemsAdmin)