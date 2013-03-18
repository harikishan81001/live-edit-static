from django.contrib import admin
from models import Records
class RecordsAdmin(admin.ModelAdmin):
    model = Records
    list_display = ('check_sum','file_name','modified_dt','modified_by',)
    list_filter = ('modified_by',)

admin.site.register( Records, RecordsAdmin)


