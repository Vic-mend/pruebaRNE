from django.contrib import admin

from .models import radioaficionados
from .models import bitacoras

# Register your models here.
admin.site.register(radioaficionados)
admin.site.register(bitacoras)

#user: admim
#pass: admin
