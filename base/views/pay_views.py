from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
import json
import stripe

from base.models import Item, Order


stripe.api_key = settings.STRIPE_API_SECRET_KEY
MY_DOMAIN = settings.MY_DOMAIN

class SuccessView(LoginRequiredMixin, TemplateView):
    model = Item
    template_name = 'pages/success.html'

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user).order_by('-created_at')[0]
        order.is_confirmed = True
        order.save()
            
        del request.session['cart']
        return super().get(request, *args, **kwargs)


class CancelView(LoginRequiredMixin, TemplateView):
    model = Item
    template_name = 'pages/cancel.html'

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user).order_by('-created_at')[0]
        
        for el in json.loads(order.items):
            item = Item.objects.get(pk=el['pk'])
            item.stock += el['quantity']
            item.sold_count -= el['quantity']
            item.save()
        
        if not order.is_confirmed:
            order.delete()
        
        return super().get(request, *args, **kwargs)


tax_rate = stripe.TaxRate.create(
    display_name='消費税',
    description='消費税',
    country='JP',
    jurisdiction='JP',
    percentage=settings.TAX_RATE * 100,
    inclusive=False,  # 外税を指定（内税の場合はTrue）
)

def check_profile_filled(profile):
    if profile.first_name is None or profile.first_name == '':
        return False
    elif profile.zipcode is None or profile.zipcode == '':
        return False
    elif profile.prefecture is None or profile.prefecture == '':
        return False
    elif profile.address1 is None or profile.address1 == '':
        return False
    elif profile.address2 is None or profile.address2 == '':
        return False
    return True

@login_required
def create_checkout_session(request):
    cart = request.session.get('cart', None)

    if request.method == 'POST':
        if not check_profile_filled(request.user.profile):
            messages.error(request, '配送先を入力する必要があります。')
            return redirect('/profile/')

    if cart is None or len(cart) == 0:
        return redirect('/cart/')
    
    items = []
    line_items = []
    for item_pk, quantity in cart['items'].items():
        item = Item.objects.get(pk=item_pk)

        line_items.append({
        'price_data': {
            'currency': 'JPY',
            'unit_amount': item.price,
            'product_data': {'name': item.name,}
        },
        'quantity': quantity,
        'tax_rates': [tax_rate.id],
        })

        # Order
        items.append({
            'pk': item.pk,
            'name': item.name,
            'images': str(item.images),
            'price': item.price,
            'quantity': quantity,
        })

        # Adjusting stock and sold_count
        item.stock -= quantity
        item.sold_count += quantity
        item.save()

    Order.objects.create(
        user = request.user,
        uid = request.user.pk,
        items = json.dumps(items),
        shipping_for = serializers.serialize('json', [request.user.profile]),
        amount = cart['total'],
        tax_included = cart['tax_included_total']
    )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=request.user.email,
        line_items=line_items,
        mode='payment',
        success_url=MY_DOMAIN + '/pay/success/',
        cancel_url=MY_DOMAIN + '/pay/cancel',
    )

    return redirect(session.url, code=303)