from django.contrib import admin
from sap_servers.models import OS, Database, Location, Host

class OsAdmin(admin.ModelAdmin):
    list_display = ('name', 'bit')
    search_fields = ('name',)
    
class HostAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'OS',
                    'database',
                    'location',
                    'isVirtual',
                    'SBEA',
                    'RAM',
                    'HDD_all',
                    'HDD_occup',)
            
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'publisher', 'publication_date')
#     list_filter = ('publication_date',)
#     date_hierarchy = 'publication_date'
#     ordering = ('-publication_date',)
#     fields = ('title', 'authors', 'publisher', 'publication_date')
#     filter_horizontal = ('authors',)
#     raw_id_fields = ('publisher',)
# 
admin.site.register(OS, OsAdmin)
admin.site.register(Database)
admin.site.register(Location)
admin.site.register(Host, HostAdmin)
