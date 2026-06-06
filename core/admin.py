from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(StaffProfile)
admin.site.register(MenuItem)
admin.site.register(Ingredient)
admin.site.register(MenuItemIngredient)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Notification)