from django.shortcuts import redirect
from django.views.generic import View, ListView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from collections import OrderedDict

from base.models import Item


class CartListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'pages/cart.html'

    def get_queryset(self):
        cart = self.request.session.get('cart', None)

        if cart is None or len(cart) == 0:
            return redirect('/')

        self.queryset = []
        self.total = 0

        for item_pk, quantity in cart['items'].items():
            item = Item.objects.get(pk=item_pk)
            item.quantity = quantity
            item.subtotal = item.price * quantity
            self.queryset.append(item)
            self.total += item.subtotal

        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1))
        self.str_tax_included_total = '{:,}'.format(int(self.total * (settings.TAX_RATE + 1)))
        self.str_total = '{:,}'.format(self.total)
        cart['str_total'] = self.str_total
        cart['str_tax_included_total'] = self.str_tax_included_total
        cart['total'] = self.total
        cart['tax_included_total'] = self.tax_included_total
        self.request.session['cart'] = cart
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['str_total'] = self.str_total
            context['str_tax_included_total'] = self.str_tax_included_total
        except Exception:
            pass
        return context

class AddCartView(LoginRequiredMixin, View):
    
    def post(self, request):
        item_pk = request.POST.get('item_pk')
        quantity = int(request.POST.get('quantity'))

        cart = request.session.get('cart', None)

        if cart is None or len(cart) == 0:
            item_info = {}
            cart = {'items': item_info}
        
        if item_pk in cart['items']:
            cart['items'][item_pk] += quantity
        elif item_pk not in cart['items']:
            cart['items'][item_pk] = quantity
        else:
            raise Exception('カートに入れれませんでした。')
        
        request.session['cart'] = cart

        return redirect('/cart/')

@login_required
def remove_item_from_cart(request, pk):
    cart = request.session.get('cart', None)
    if cart is not None or len(cart) == 0:
        del cart['items'][pk]
        request.session['cart'] = cart
    return redirect('/cart/')