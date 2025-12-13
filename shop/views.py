from django.http import  JsonResponse
from django.shortcuts import redirect, render
from shop.forms import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from shop.forms import CheckoutForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import random
import string
import json
 
 
def home(request):
  products=Product.objects.filter(trending=1)
  return render(request,"shop/index.html",{"products":products})
 
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
 
 
 
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"shop/cart.html",{"cart":cart})
  else:
    return redirect("/")
 
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
 
 
 
def fav_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['pid']
            product_status = Product.objects.get(id=product_id)
            
            if product_status:
                # Check if already in favourites
                existing_fav = Favourite.objects.filter(user=request.user, product_id=product_id)
                
                if existing_fav:
                    # REMOVE from favourites
                    existing_fav.delete()
                    return JsonResponse({'status': 'Product Removed from Favourite'}, status=200)
                else:
                    # ADD to favourites
                    Favourite.objects.create(user=request.user, product_id=product_id)
                    return JsonResponse({'status': 'Product Added to Favourite'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Favourite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)
 
 
def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            
            product_status=Product.objects.get(id=product_id)
            if product_status:
                # Check if product already exists in cart
                if Cart.objects.filter(user=request.user.id, product_id=product_id).exists():
                    # Update quantity instead of rejecting
                    cart_item = Cart.objects.get(user=request.user.id, product_id=product_id)
                    new_qty = cart_item.product_qty + product_qty
                    
                    # Check stock availability
                    if product_status.quantity >= new_qty:
                        cart_item.product_qty = new_qty
                        cart_item.save()
                        return JsonResponse({'status': 'Product quantity updated in cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Not enough stock available'}, status=200)
                else:
                    # Add new item to cart
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)
 
def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")
 
 
def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"shop/login.html")
 
def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"shop/register.html",{'form':form})
 
 
def collections(request):
  catagory=Category.objects.filter(status=0)
  return render(request,"shop/collections.html",{"catagory":catagory})
 
def collectionsview(request,name):
  if(Category.objects.filter(name=name,status=0)):
      products=Product.objects.filter(category__name=name)
      return render(request,"shop/products/index.html",{"products":products,"category_name":name})
  else:
    messages.warning(request,"No Such Category Found")
    return redirect('collections')
 
 
def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"shop/products/product_details.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('collections')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('collections')
  
def search(request):
    query = request.GET.get('query', '')  # Changed from 'q' to 'query'
    results = Product.objects.filter(name__icontains=query) if query else []
    context = {'results': results, 'query': query}
    return render(request, 'shop/search_results.html', context)


def navbar_context(request):
    categories = Category.objects.all()
    cart_count = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    fav_count = Favourite.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return {
        'categories': categories,
        'cart_count': cart_count,
        'fav_count': fav_count
    }
    
def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
        fav_count = Favourite.objects.filter(user=request.user).count()
        return JsonResponse({
            'cart_count': cart_count,
            'fav_count': fav_count
        })
    return JsonResponse({'cart_count': 0, 'fav_count': 0})
  
  
  
def generate_order_number():
    """Generate unique order number"""
    return 'ORD' + ''.join(random.choices(string.digits, k=8))

@login_required(login_url='login')
def checkout(request):
    # Get cart items
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart_page')
    
    # Calculate total
    total_amount = sum(item.total_cost for item in cart_items)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            order.user = request.user
            order.order_number = generate_order_number()
            order.total_amount = total_amount
            order.payment_mode = 'Cash on Delivery'
            order.status = 'Confirmed'
            order.save()
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.product_qty,
                    price=cart_item.product.selling_price,
                    total=cart_item.total_cost
                )
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, f'Order placed successfully! Order Number: {order.order_number}')
            return redirect('order_confirmation', order_id=order.id)
    else:
        # Pre-fill form with user data if available
        initial_data = {
            'full_name': request.user.get_full_name(),
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'shop/checkout.html', context)


@login_required(login_url='login')
def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        
        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(request, 'shop/order_confirmation.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found!')
        return redirect('shop_home')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'shop/my_orders.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        
        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(request, 'shop/order_detail.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found!')
        return redirect('my_orders')


@login_required(login_url='login')
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        if order.status in ['Pending', 'Confirmed']:
            order.status = 'Cancelled'
            order.save()
            messages.success(request, 'Order cancelled successfully!')
        else:
            messages.warning(request, 'This order cannot be cancelled!')
        return redirect('order_detail', order_id=order_id)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found!')
        return redirect('my_orders')
      
@login_required(login_url='login')
def delete_order(request, order_id):
    if request.method == 'POST':
        try:
            # Get order belonging to current user only
            order = Order.objects.get(id=order_id, user=request.user)
            order_number = order.order_number
            
            # Delete the order (this will also delete related OrderItems if CASCADE is set)
            order.delete()
            
            messages.success(request, f'Order #{order_number} has been deleted successfully.')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found!')
    
    return redirect('my_orders')
      
def send_order_status_email(order):
    """Send email notification when order status changes"""
    subject = f'Order #{order.order_number} - Status Update'
    
    status_messages = {
        'Confirmed': 'Your order has been confirmed and will be processed soon.',
        'Processing': 'Your order is being processed and will be shipped shortly.',
        'Shipped': 'Your order has been shipped and is on the way!',
        'Delivered': 'Your order has been delivered. Thank you for shopping with us!',
        'Cancelled': 'Your order has been cancelled. If you have any questions, please contact us.',
    }
    
    message = f"""
    Dear {order.full_name},
    
    Your order #{order.order_number} status has been updated to: {order.status}
    
    {status_messages.get(order.status, 'Your order status has been updated.')}
    
    Order Details:
    - Total Amount: ₹{order.total_amount}
    - Payment Method: {order.payment_mode}
    
    You can track your order at: http://yourdomain.com/order-detail/{order.id}/
    
    Thank you for shopping with ShopKart!
    
    Best regards,
    ShopKart Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")


def collections(request):
    category = Category.objects.all()
    return render(request, 'shop/collections.html', {'category': category})