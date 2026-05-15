from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from myproject.utils.core import compare_prices
from django.http import HttpResponse
from .models import WishList, Notification
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Replace 'home' with your home page URL name
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        res = compare_prices(request.POST['productname'])
        return render(request, 'home.html', {'res': res})
    return render(request, 'home.html')

@login_required
def addtowishlist(request):
    if request.method == 'POST':
        user = request.user  # Get the currently logged-in user
        product_name = request.POST.get("product_name")  # Get product name from form
        is_flipkart_lower = int(request.POST.get("is_flipkart_lower", 0))  # Default to 0 if not provided
        status = request.POST.get("status")  # Default status is "active"
        lowest_price = float(request.POST.get("lowestprice", 0.0))  # Convert price to float
        print('lowest_price', lowest_price)
        print('request.POST', request.POST)
        # Create and save the record
        wishlist_item = WishList.objects.create(
            product_name=product_name,
            user=user,
            is_flipkart_lower=is_flipkart_lower,
            status=status,
            lowest_price=lowest_price
        )
        messages.success(request, f"'{product_name}' has been added to your wishlist!")
        
        return redirect('home')
    return redirect('home')

@login_required
def wishlist(request):
    wishlist_items = WishList.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, item_id):
    item = WishList.objects.get(id=item_id, user=request.user)
    item.delete()
    return redirect('wishlist')

@login_required
def notifications(request):
    # Get all notifications for the current user, newest first
    notifications = Notification.objects.filter(user=request.user).order_by('-created_date')
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'notifications.html', context)

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('notifications')

@login_required
def dismiss_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('notifications')

@login_required
def mark_all_notifications_read(request):
    # Mark all unread notifications as read for the current user
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'count': 0})
    
    return redirect('notifications')

@login_required
def dismiss_all_notifications(request):
    # Delete all notifications for the current user
    Notification.objects.filter(user=request.user).delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'count': 0})
    
    return redirect('notifications')

@login_required
def checkForPriceDrop(request):
    wishlistItem = list(WishList.objects.filter(user=request.user))
    for item in wishlistItem:
        compareResult = compare_prices_dummy(item.product_name, item.lowest_price)
        # compareResult = compare_prices(item.product_name)
        print('compareResult', compareResult['lowestPrice'])
        print('item', item.lowest_price)
        if compareResult['lowestPrice'] > -1 and compareResult['lowestPrice'] < item.lowest_price:
            message="Your Product " + item.product_name +" has been price dropped from " + str(item.lowest_price) + " to " + str(compareResult['lowestPrice'])
            print(message)
            item.lowest_price = compareResult['lowestPrice']
            item.save()
            notification = Notification.objects.create(
                user=request.user,
                message=message
            )
    
    messages.success(request, f"Price drop check completed you can check notification or wishlist to see changes")
    return redirect('home')
        


def compare_prices_dummy(product_name, product_price):
    return {'product_name' : product_name, 'lowestPrice' : (product_price-1)}