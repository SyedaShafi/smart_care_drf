from django.contrib import admin
from . models import AvailableTime, Designation, Doctor, Specialization, Review
# Register your models here.

class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',),}
    
class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',),}

admin.site.register(AvailableTime)
admin.site.register(Designation, DesignationAdmin)
admin.site.register(Doctor)
admin.site.register(Review)
admin.site.register(Specialization, SpecializationAdmin)