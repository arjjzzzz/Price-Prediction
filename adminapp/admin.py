from django.contrib import admin
from .models import WishList, Notification

@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ("product_name", "user", "is_flipkart_lower", "status", "lowest_price", "modified_date") 

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_date')