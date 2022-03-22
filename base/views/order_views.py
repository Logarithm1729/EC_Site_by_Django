from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
import json

from base.models import Order


class OrderIndexView(LoginRequiredMixin, ListView):
    template_name = 'pages/orders.html'
    model = Order
    ordering = '-created_at'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'pages/order.html'
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["items"] = json.loads(obj.items)
        context['shipping_for'] = json.loads(obj.shipping_for)
        return context