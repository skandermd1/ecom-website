from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from core.models import category,product,productimage,ProductReview,cartOrder,wishlist,orderedItems,mail,adress,adress

from django.db.models import Avg
from core.forms import ProductReviewForm,mailForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    products=product.objects.all()
    mailForm1=mailForm()
    context={
        "products":products,
        "mailForm":mailForm1,
    }
    return render(request, "core/index.html",context)
def all_products(request):
    products = product.objects.all()
    categories = category.objects.all()
    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, "core/all_products.html", context)
def category_list_view(request):
    categories= category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, "core/category_list.html", context)
def category_product_list(request,pk):
    cat=category.objects.get(id=pk)
    products=product.objects.filter(category=cat)
    context={
        "products":products,
        "category": cat,
    }
    return render(request, "core/category_product_list.html",context)
def product_detail_view(request,pk):
    prod=product.objects.get(id=pk)
    prod_images=prod.product_images.all()
    ps=product.objects.filter(category=prod.category).exclude(pk=prod.id)
    reviews=ProductReview.objects.filter(product=prod)
    average_rating = reviews.aggregate(rating=Avg('rating'))
    product_review_form = ProductReviewForm()
    context={
        "product":prod,
        "product_images":prod_images,
        "related_products":ps,
        "reviews": reviews,
        "average_rating": average_rating,
        "product_review_form": product_review_form,
    }
    return render(request, "core/product_view.html",context)
def tagged_products(request, tag_slug):
    tagged_products = product.objects.filter(tags__slug=tag_slug)
    context = {
        'tagged_products': tagged_products,
        'tag_slug': tag_slug,
    }
    return render(request, 'core/tagged_products.html', context)
def ajax_review_submission(request,pk):
   product_instance = product.objects.get(id=pk)
   user=request.user
   review=ProductReview.objects.create(
       product=product_instance,
       user=user,
       rating=request.POST.get('rating'),
       review=request.POST.get('review'),)
   context=(
       {
              "review": review.review,
              "user": user.username,
              "rating": review.rating,
       }
   )
   average_rating = ProductReview.objects.filter(product=product_instance).aggregate(rating=Avg('rating'))
   return JsonResponse({
       'new_review': context, 
       'average_rating': average_rating,
       'boolean': True,
       })
def search_results(request):
    query = request.GET.get('q')
    results = product.objects.filter(title__icontains=query)
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'core/search.html', context)

def ajax_filter_products(request):
    # Get filter parameters
    categories = request.GET.getlist('categories[]')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    # Start with all products
    filtered_products = product.objects.all()
    
    # Filter by categories if selected
    if categories:
        filtered_products = filtered_products.filter(category__id__in=categories)
    
    # Filter by price range
    if min_price:
        try:
            filtered_products = filtered_products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            filtered_products = filtered_products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Render the filtered products
    data = render_to_string('core/partial_products_list.html', {
        'products': filtered_products
    })
    
    return JsonResponse({
        'data': data,
        'count': filtered_products.count()
    })

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = mailForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            # ✅ VÉRIFIER SI L'EMAIL EXISTE DÉJÀ
            if mail.objects.filter(email=email).exists():
                messages.warning(request, 'This email is already subscribed! 📧')
                return redirect("index")
            
            try:
                # Créer seulement si n'existe pas
                mail.objects.create(email=email)
                messages.success(request, 'Thank you for subscribing! 🎉')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                
            return redirect("index")
        else:
            messages.error(request, 'Please enter a valid email address.')
            return redirect("index")
    
    return redirect('index')
@login_required
def profile(request):
    reviews = ProductReview.objects.filter(user=request.user)
    r = reviews.count()
    orders = cartOrder.objects.filter(user=request.user)
    wishlists = wishlist.objects.filter(user=request.user)
    adresses = adress.objects.filter(user=request.user)
    wishlist_count = wishlists.count()
    
    if request.method == "POST":
        # CORRECTION: Utiliser "address_line1" au lieu de "adress"
        address_input = request.POST.get("address_line1")
        default_address = request.POST.get("default_address") == "on"
        
        if address_input:  # Vérifier que l'adresse n'est pas vide
            # If setting as default, unset all other defaults
            if default_address:
                adress.objects.filter(user=request.user, default=True).update(default=False)
            
            new = adress.objects.create(
                user=request.user, 
                adress=address_input,
                default=default_address
            )
            messages.success(request, "Address added successfully")
            return redirect("profile")
        else:
            messages.error(request, "Please enter an address")

    context = {
        "reviews": r,
        "orders": orders.count(),
        "wishlists": wishlist_count,
        "adresses": adresses,
    }
    return render(request, "core/profile.html", context)

@login_required
@require_POST
def set_default_address(request, pk):
    """Set an address as default"""
    try:
        addr = get_object_or_404(adress, pk=pk, user=request.user)
        
        # Unset all other default addresses
        adress.objects.filter(user=request.user, default=True).update(default=False)
        
        # Set this one as default
        addr.default = True
        addr.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def delete_address(request, pk):
    """Delete an address"""
    try:
        addr = get_object_or_404(adress, pk=pk, user=request.user)
        addr.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def edit_address(request, pk):
    """Edit an address"""
    addr = get_object_or_404(adress, pk=pk, user=request.user)
    
    if request.method == "POST":
        address_input = request.POST.get("address_line1")
        default_address = request.POST.get("default_address") == "on"
        
        if address_input:
            # If setting as default, unset all other defaults
            if default_address:
                adress.objects.filter(user=request.user, default=True).exclude(pk=pk).update(default=False)
            
            addr.adress = address_input
            addr.default = default_address
            addr.save()
            messages.success(request, "Address updated successfully")
            return redirect("profile")
    
    # GET request - show edit form (will be handled via modal or separate page)
    context = {
        "address": addr,
    }
    return render(request, "core/edit_address.html", context)
def ajax_add_to_cart(request):
    product_id = str(request.GET.get('id'))
    product_price = request.GET.get('price')
    product_quantity = int(request.GET.get('quantity', 1))
    
    # Initialize session cart if it doesn't exist
    if 'cart_data_object' not in request.session:
        request.session['cart_data_object'] = {}
    
    cart_data = request.session['cart_data_object']
    
    # If product already in cart, increment quantity
    if product_id in cart_data:
        cart_data[product_id]['quantity'] = int(cart_data[product_id]['quantity']) + product_quantity
    else:
        # Add new product to cart
        cart_data[product_id] = {
            'price': product_price,
            'quantity': product_quantity
        }
    
    # Save back to session
    request.session['cart_data_object'] = cart_data
    request.session.modified = True
    
    # Calculate total quantity of items
    total_quantity = sum(int(item['quantity']) for item in cart_data.values())
    
    return JsonResponse({
        "data": request.session['cart_data_object'],
        'total_items': total_quantity,
        'success': True
    })
def cart_view(request):
    cart_items = []
    cart_total_amount = 0
    
    if 'cart_data_object' in request.session:
        cart_data = request.session['cart_data_object']
        
        # Get product details from database
        for product_id, item_data in cart_data.items():
            try:
                prod = product.objects.get(id=int(product_id))
                quantity = int(item_data.get('quantity', 1))
                
                # Handle price conversion - use product price from DB for consistency
                # But also check session price if it exists
                price_from_session = item_data.get('price')
                try:
                    if price_from_session:
                        # Convert session price to float (might be string or already numeric)
                        price = float(str(price_from_session))
                    else:
                        # Use product price from database (Decimal to float)
                        price = float(prod.price)
                except (ValueError, TypeError):
                    # Fallback to product price if conversion fails
                    price = float(prod.price)
                
                subtotal = price * quantity
                cart_total_amount += subtotal
                
                cart_items.append({
                    'product': prod,
                    'quantity': quantity,
                    'price': price,
                    'subtotal': subtotal,
                })
            except product.DoesNotExist:
                # Product no longer exists, skip it
                continue
    
    context = {
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'cart_count': len(cart_items)
    }
    return render(request, "core/cart.html", context)

def ajax_update_cart_item(request):
    """Update quantity of an item in the cart"""
    try:
        product_id = str(request.GET.get('id', ''))
        new_quantity = int(request.GET.get('quantity', 1))
        
        print(f"DEBUG: Updating cart item - Product ID: {product_id}, Quantity: {new_quantity}")
        
        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required'})
        
        if 'cart_data_object' not in request.session:
            return JsonResponse({'success': False, 'message': 'Cart is empty', 'total_items': 0, 'total_amount': 0})
        
        cart_data = request.session['cart_data_object']
        
        if product_id not in cart_data:
            return JsonResponse({'success': False, 'message': 'Product not in cart'})
        
        if new_quantity <= 0:
            # Remove item if quantity is 0 or less
            del cart_data[product_id]
            item_quantity = 0
        else:
            cart_data[product_id]['quantity'] = new_quantity
            item_quantity = new_quantity
        
        request.session['cart_data_object'] = cart_data
        request.session.modified = True
        
        # Calculate totals with error handling
        total_quantity = 0
        total_amount = 0.0
        
        for item in cart_data.values():
            try:
                qty = int(item.get('quantity', 0))
                total_quantity += qty
                
                price_str = str(item.get('price', '0')).strip()
                price = float(price_str) if price_str else 0.0
                total_amount += price * qty
            except (ValueError, TypeError) as e:
                print(f"Warning: Error calculating totals for item: {e}")
                continue
        
        return JsonResponse({
            'success': True,
            'total_items': total_quantity,
            'total_amount': round(total_amount, 2),
            'item_quantity': item_quantity
        })
    except ValueError as e:
        return JsonResponse({'success': False, 'message': f'Invalid quantity: {str(e)}'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error updating cart: {str(e)}'})

def ajax_delete_cart_item(request):
    """Remove an item from the cart"""
    try:
        product_id = str(request.GET.get('id', ''))
        
        print(f"DEBUG: Deleting cart item - Product ID: {product_id}")
        
        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required'})
        
        if 'cart_data_object' not in request.session:
            return JsonResponse({'success': False, 'message': 'Cart is empty', 'total_items': 0, 'total_amount': 0})
        
        cart_data = request.session['cart_data_object']
        
        if product_id in cart_data:
            # Get item subtotal before deletion for response
            item_data = cart_data[product_id]
            try:
                price_str = str(item_data.get('price', '0')).strip()
                price = float(price_str) if price_str else 0.0
            except (ValueError, TypeError):
                price = 0.0
            
            try:
                quantity = int(item_data.get('quantity', 0))
            except (ValueError, TypeError):
                quantity = 0
            
            deleted_subtotal = price * quantity
            
            del cart_data[product_id]
            
            request.session['cart_data_object'] = cart_data
            request.session.modified = True
            
            # Calculate new totals with error handling
            total_quantity = 0
            total_amount = 0.0
            
            for item in cart_data.values():
                try:
                    qty = int(item.get('quantity', 0))
                    total_quantity += qty
                    
                    price_str = str(item.get('price', '0')).strip()
                    price = float(price_str) if price_str else 0.0
                    total_amount += price * qty
                except (ValueError, TypeError) as e:
                    print(f"Warning: Error calculating totals for item: {e}")
                    continue
            
            return JsonResponse({
                'success': True,
                'total_items': total_quantity,
                'total_amount': round(total_amount, 2),
                'deleted_subtotal': round(deleted_subtotal, 2)
            })
        
        return JsonResponse({'success': False, 'message': 'Product not in cart'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error deleting item: {str(e)}'})

@login_required
def checkout_view(request):
    """Checkout page"""
    if 'cart_data_object' not in request.session or not request.session['cart_data_object']:
        messages.warning(request, "Your cart is empty")
        return redirect("cart_view")
    
    cart_items = []
    cart_total_amount = 0
    
    cart_data = request.session['cart_data_object']
    for product_id, item_data in cart_data.items():
        try:
            prod = product.objects.get(id=int(product_id))
            quantity = int(item_data.get('quantity', 1))
            price = float(str(item_data.get('price', prod.price)))
            subtotal = price * quantity
            cart_total_amount += subtotal
            
            cart_items.append({
                'product': prod,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal,
            })
        except product.DoesNotExist:
            continue
    
    # Get user's addresses
    addresses = adress.objects.filter(user=request.user)
    default_address = addresses.filter(default=True).first()
    
    context = {
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'addresses': addresses,
        'default_address': default_address,
    }
    return render(request, "core/checkout.html", context)

@login_required
def create_payment(request):
    """Create PayPal payment"""
    if 'cart_data_object' not in request.session or not request.session['cart_data_object']:
        return JsonResponse({'success': False, 'message': 'Cart is empty'})
    
    # Calculate total
    cart_data = request.session['cart_data_object']
    total_amount = 0.0
    items = []
    
    for product_id, item_data in cart_data.items():
        try:
            prod = product.objects.get(id=int(product_id))
            quantity = int(item_data.get('quantity', 1))
            price = float(str(item_data.get('price', prod.price)))
            total_amount += price * quantity
            items.append({
                "name": prod.title[:127],  # PayPal limit
                "sku": str(prod.id),
                "price": str(price),
                "currency": "USD",
                "quantity": quantity
            })
        except:
            continue
    
    # Use client-side PayPal integration (simpler and more reliable)
    return JsonResponse({
        'success': True,
        'use_client_side': True,
        'amount': round(total_amount, 2),
        'items': items
    })

@login_required
@require_POST
def execute_payment(request):
    """Execute PayPal payment after approval"""
    try:
        payment_id = request.POST.get('payment_id')
        address_id = request.POST.get('address_id')
        
        if not payment_id:
            return JsonResponse({'success': False, 'message': 'Payment ID is required'})
        
        # Create order
        cart_data = request.session.get('cart_data_object', {})
        
        # Calculate total
        total_amount = 0.0
        for product_id, item_data in cart_data.items():
            try:
                quantity = int(item_data.get('quantity', 1))
                price = float(str(item_data.get('price', 0)))
                total_amount += price * quantity
            except:
                continue
        
        order = cartOrder.objects.create(
            user=request.user,
            price=total_amount,
            paid=True
        )
        
        # Create order items
        for product_id, item_data in cart_data.items():
            try:
                prod = product.objects.get(id=int(product_id))
                quantity = int(item_data.get('quantity', 1))
                price = float(str(item_data.get('price', prod.price)))
                
                orderedItems.objects.create(
                    order=order,
                    quantity=quantity,
                    item=prod.title,
                    price=price,
                    total=price * quantity
                )
            except:
                continue
        
        # Clear cart
        request.session['cart_data_object'] = {}
        request.session.modified = True
        
        return JsonResponse({'success': True, 'message': 'Order placed successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def ajax_add_to_wishlist(request):
    """Add product to wishlist"""
    try:
        product_id = request.GET.get('id')
        
        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required'})
        
        prod = get_object_or_404(product, id=int(product_id))
        
        # Check if already in wishlist
        wishlist_item, created = wishlist.objects.get_or_create(
            user=request.user,
            product=prod
        )
        
        if created:
            return JsonResponse({
                'success': True,
                'message': 'Added to wishlist',
                'in_wishlist': True
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Already in wishlist',
                'in_wishlist': True
            })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def ajax_remove_from_wishlist(request):
    """Remove product from wishlist"""
    try:
        product_id = request.GET.get('id')
        
        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required'})
        
        wishlist_item = wishlist.objects.filter(
            user=request.user,
            product_id=int(product_id)
        ).first()
        
        if wishlist_item:
            wishlist_item.delete()
            return JsonResponse({
                'success': True,
                'message': 'Removed from wishlist',
                'in_wishlist': False
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Item not in wishlist'
            })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def wishlist_view(request):
    """Display user's wishlist"""
    wishlist_items = wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count()
    }
    return render(request, "core/wishlist.html", context)

def ajax_wishlist_count(request):
    """Get wishlist count for authenticated users"""
    if request.user.is_authenticated:
        count = wishlist.objects.filter(user=request.user).count()
        return JsonResponse({'success': True, 'count': count})
    return JsonResponse({'success': True, 'count': 0})