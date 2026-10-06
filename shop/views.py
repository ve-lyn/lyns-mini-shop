from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, OrderItem


def product_list(request):
    search = request.GET.get('search', '').strip()

    products = Product.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    categories = Product.CATEGORY_CHOICES

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
    })


def category_products(request, category):
    products = Product.objects.filter(category=category)
    categories = Product.CATEGORY_CHOICES

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'shop/register.html', {
        'form': form
    })


@login_required(login_url='/accounts/login/')
def cart_list(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    return render(request, 'shop/cart_list.html', {
        'cart': cart
    })


@login_required(login_url='/accounts/login/')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_list')


@login_required(login_url='/accounts/login/')
def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_list')


@login_required(login_url='/accounts/login/')
def checkout(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        total = cart.total_price()

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            payment_method=payment_method,
            total=total
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()

        return render(request, 'shop/order_success.html', {
            'full_name': full_name,
            'address': address,
            'payment_method': payment_method,
            'total': total,
        })

    return render(request, 'shop/checkout.html', {
        'cart': cart
    })


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(request, 'shop/product_detail.html', {
        'product': product
    })


@login_required(login_url='/accounts/login/')
def order_success(request):
    return render(request, 'shop/order_success.html')