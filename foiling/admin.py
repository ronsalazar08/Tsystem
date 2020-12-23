
from django.contrib import admin
from .models import dr_form, dr_item
# Register your models here.

def set_open(modeladmin, request, queryset):
    queryset.update(status='OPEN')
def set_waiting(modeladmin, request, queryset):
    queryset.update(status='WAITING')
def set_closed(modeladmin, request, queryset):
    queryset.update(status='CLOSED')
set_open.short_description = "Set STATUS to `OPEN`"
set_waiting.short_description = "Set STATUS to `WAITING`"
set_closed.short_description = "Set STATUS to `CLOSED`"

class Drforms(admin.ModelAdmin):
    
    list_display = ( 'control_no', 'customer', 'date_created', 'status')

    search_fields = ['control_no', 'control_no']
    
    # define filter columns list, then a filter widget will be shown at right side of Department list page.
    list_filter = ['control_no', 'customer']
    # define which field will be pre populated.
    #prepopulated_fields = {'dept_name': ('dept_name',)}
    # define model data list ordering.
    #ordering = ('id','dept_name')
    actions = [set_open, set_waiting, set_closed ]

class Dritems(admin.ModelAdmin):
    
    list_display = ( 'product_no', 'wos_no', 'first_quantity', 'second_quantity', 'third_quantity', 'fourth_quantity', 'fifth_quantity', 'control_noFK')

    search_fields = ['product_no', 'wos_no']
    
    # define filter columns list, then a filter widget will be shown at right side of Department list page.
    list_filter = ['product_no', 'wos_no']
    # define which field will be pre populated.
    #prepopulated_fields = {'dept_name': ('dept_name',)}
    # define model data list ordering.
    #ordering = ('id','dept_name')

admin.site.register(dr_form, Drforms)
admin.site.register(dr_item, Dritems)