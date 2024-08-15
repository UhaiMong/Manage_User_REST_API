from django.contrib import admin
from .models import AboutUs
# Register your models here.

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['contributor_first_name','contributor_last_name','bio','contribution']
    def contributor_first_name(self,obj):
        return obj.about.user.first_name
    def contributor_last_name(self,obj):
        return obj.about.user.last_name
admin.site.register(AboutUs,AboutUsAdmin)