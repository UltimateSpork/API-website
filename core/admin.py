from django.contrib import admin
from .models import * 

# Register your models here.

admin.site.register(LandClass)
admin.site.register(LandCategory)
admin.site.register(State)
admin.site.register(County)
admin.site.register(OffshoreRegion)
admin.site.register(Commodity)
admin.site.register(Disposition)
admin.site.register(ProductionRecord)
