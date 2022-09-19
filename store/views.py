from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from category.models import Category
from store.models import Product
from carts.models import Cart, CartItem
from carts.views import _cart_id

def home(request, category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 6)
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        cart = Cart.objects.get(cart_id=_cart_id(request))
        in_cart = CartItem.objects.filter(
            cart=cart, product=single_product
        ).exists()
    except Exception as e:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        ) 

    context = {
        'single_product': single_product,
        'in_cart': in_cart if 'in_cart' in locals() else False,
    }
    return render(request, 'store/product_detail.html', context)
