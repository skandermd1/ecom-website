from core.models import category, product, productimage, cartOrder, wishlist, orderedItems

def default(request):
    categories = category.objects.all()
    
    # Get cart count from session (total quantity of all items)
    cart_count = 0
    if 'cart_data_object' in request.session:
        cart_data = request.session['cart_data_object']
        cart_count = sum(int(item.get('quantity', 0)) for item in cart_data.values())
    
    # Get wishlist count for authenticated users
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = wishlist.objects.filter(user=request.user).count()
    
    return {
        'categories': categories,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }