from django.shortcuts import render
from django.views.generic import ListView, DetailView

from base.models import Item, Category, Tag

class IndexView(ListView):
    model = Item
    template_name = 'pages/index.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'pages/item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = Item.objects.get(pk=self.kwargs['pk'])
        # Add , to price of items
        splited_price = '{:,}'.format(item.price)
        context['splited_price'] = splited_price
        return context

class CategoryListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 2

    def get_queryset(self):
        self.category = Category.objects.get(cat_slug=self.kwargs['pk'])
        return Item.objects.filter(category=self.category, is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.category.cat_name
        return context

class TagListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 2

    def get_queryset(self):
        self.tag = Tag.objects.get(tag_slug=self.kwargs['pk'])
        return Item.objects.filter(tags=self.tag, is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.tag.tag_name
        return context
    
    