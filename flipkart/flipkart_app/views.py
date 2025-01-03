from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView, DetailView
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Review, Seller, WishlistItem, UserProfile, User
from django.http import JsonResponse
import torch
from .ml_models import run_ml_model  # Assuming you have a module that handles ML models

# Home View for both customers and sellers
class HomeView(ListView):
    model = Product
    template_name = 'flipkart_app/home.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(stock__gt=0)
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        if category:
            queryset = queryset.filter(category__name=category)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# User registration for both customers and sellers
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        user_type = request.POST.get('user_type')  # 'customer' or 'seller'

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_customer = (user_type == 'customer')
        user.is_seller = (user_type == 'seller')
        user.save()

        user_profile = UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            user_type=user_type
        )

        if user_type == 'seller':
            Seller.objects.create(user_profile=user_profile, is_verified=False)

        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')

    return render(request, 'flipkart_app/register.html')

# User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_seller:
                return redirect('seller_dashboard') 
            else:
                return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'flipkart_app/login.html')

# User logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# Cart details for customers
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all() if not created else []
    
    return render(request, 'flipkart_app/cart.html', {'cart': cart, 'cart_items': cart_items})

# Add item to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{product.name} added to cart.')
    return redirect('cart')

# Update cart items (increase, decrease, remove)
@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
    elif action == 'remove':
        cart_item.delete()

    return redirect('cart')

# Checkout process for customers
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if cart.items.count() == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        phone_number = request.POST.get('phone_number')
        payment_method = request.POST.get('payment_method')
        if not shipping_address or not phone_number or not payment_method:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('checkout')
        
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            phone_number=phone_number,
            payment_method=payment_method,
            total_amount=cart.get_total()
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discounted_price(),
            )

        cart.items.all().delete()

        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'flipkart_app/checkout.html', {'cart': cart})

# Order confirmation
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'flipkart_app/order_confirmation.html', {'order': order})

# Order history for customers
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'flipkart_app/order_history.html', {'orders': orders})

# User profile view
@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        if phone_number and address and city and state and pincode:
            profile.phone_number = phone_number
            profile.address = address
            profile.city = city
            profile.state = state
            profile.pincode = pincode
            profile.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'flipkart_app/user_profile.html', {'profile': profile})

# Wishlist management
@login_required
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'flipkart_app/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return JsonResponse({'added': True}, status=200)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.filter(user=request.user, product=product).delete()
    return JsonResponse({'removed': True}, status=200)

# Seller Dashboard
@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('home')

    seller = request.user.seller
    orders = Order.objects.filter(items__product__seller=seller).distinct()

    return render(request, 'flipkart_app/seller_dashboard.html', {'orders': orders})

# Manage products for sellers
@login_required
def manage_products(request):
    if not request.user.is_seller:
        messages.error(request, 'You do not have permission to manage products.')
        return redirect('home')

    products = Product.objects.filter(seller=request.user.seller)
    return render(request, 'flipkart_app/manage_products.html', {'products': products})

# Add or edit product for sellers
@login_required
def add_edit_product(request, product_id=None):
    if not request.user.is_seller:
        messages.error(request, 'You do not have permission to add or edit products.')
        return redirect('home')

    if product_id:
        product = get_object_or_404(Product, id=product_id, seller=request.user.seller)
    else:
        product = None

    if request.method == 'POST':
        name = request.POST.get('name')
        category = get_object_or_404(Category, id=request.POST['category'])
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        discount_percentage = request.POST.get('discount_percentage')
        image = request.FILES.get('image')

        if product:
            product.name = name
            product.category = category
            product.description = description
            product.price = price
            product.stock = stock
            product.discount_percentage = discount_percentage
            if image:
                product.image = image
            product.save()
            messages.success(request, 'Product updated successfully.')
        else:
            Product.objects.create(
                seller=request.user.seller,
                category=category,
                name=name,
                description=description,
                price=price,
                stock=stock,
                discount_percentage=discount_percentage,
                image=image,
            )
            messages.success(request, 'Product added successfully.')

        return redirect('manage_products')

    categories = Category.objects.all()
    return render(request, 'flipkart_app/add_edit_product.html', {'product': product, 'categories': categories})

# Order processing with ML integration for sellers
@login_required
def order_processing(request):
    if not request.user.is_seller:
        messages.error(request, 'You do not have permission to process orders.')
        return redirect('home')

    orders = Order.objects.filter(items__product__seller=request.user.seller, status=Order.STATUS_PENDING)
    return render(request, 'flipkart_app/order_processing.html', {'orders': orders})

# ML Integration Interface for order verification
@login_required
def ml_integration(request, order_id):
    if not request.user.is_seller:
        messages.error(request, 'You do not have permission to access ML verification.')
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)
    verification_result = run_ml_model(order)
    return render(request, 'flipkart_app/verification_summary.html', {'order': order, 'result': verification_result})

# Order tracking for customers
@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'flipkart_app/track_order.html', {'order': order})

# Cancel order for customers
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status in ['delivered', 'cancelled']:
        messages.error(request, 'You cannot cancel a delivered or already cancelled order.')
    else:
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Your order has been cancelled.')

    return redirect('order_history')
