from django.contrib import admin
from sap_servers import models
import sys
import inspect
#from sap_servers.models import OS, Database, Location, Host, Project


class OSAdmin(admin.ModelAdmin):
    list_display = ('name', 'bit')
    search_fields = ('name',)
    
class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'version')

class HostAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'OS',
                    'database',
                    'location',
                    'vn',
                    'sbea',
                    'RAM',
                    'HDD_all',
                    'HDD_occup',)
    search_fields = ('name',)
    ordering = ('name',)
            
for name, obj in inspect.getmembers(models): # for all classes in models
    if inspect.isclass(obj):
        try:
            adminObj = getattr(sys.modules[__name__], name+'Admin') # check if Admin class exists
        except AttributeError:
            admin.site.register(obj) # register model.class
        else:
            admin.site.register(obj, adminObj) # register model.class with admin.class
      
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'publisher', 'publication_date')
#     list_filter = ('publication_date',)
#     date_hierarchy = 'publication_date'
#     ordering = ('-publication_date',)
#     fields = ('title', 'authors', 'publisher', 'publication_date')
#     filter_horizontal = ('authors',)
#     raw_id_fields = ('publisher',)
