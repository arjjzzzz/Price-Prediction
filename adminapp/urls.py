from django.contrib import admin
from django.urls import path
from adminapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('addtowishlist/', views.addtowishlist, name='addtowishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/dismiss/<int:pk>/', views.dismiss_notification, name='dismiss_notification'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/dismiss-all/', views.dismiss_all_notifications, name='dismiss_all_notifications'),
    path('checkpricedrop/', views.checkForPriceDrop, name='checkForPriceDrop'),
]
