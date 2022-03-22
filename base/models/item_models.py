from django.db import models
from django.utils.crypto import get_random_string
import os


def create_random_id():
    return get_random_string(32)

def upload_image_to(instance, filename):
    item_id = instance.id
    return os.path.join('static', 'items', item_id, filename)

class Category(models.Model):
    cat_slug = models.CharField(primary_key=True, max_length=32)
    cat_name = models.CharField('カテゴリ名', max_length=32)

    def __str__(self):
        return self.cat_name

class Tag(models.Model):
    tag_slug = models.CharField(primary_key=True, max_length=32)
    tag_name = models.CharField('タグ名', max_length=32)

    def __str__(self):
        return self.tag_name

class Item(models.Model):
    id = models.CharField(primary_key=True, default=create_random_id, max_length=32, editable=False)
    name = models.CharField('商品名', default='', max_length=50)
    price = models.PositiveIntegerField('値段', default=0)
    stock = models.PositiveIntegerField('在庫', default=0)
    sold_count = models.PositiveIntegerField('売上個数', default=0)
    description = models.TextField('詳細', max_length=1000, blank=True)
    images = models.ImageField('関連画像', default='', blank=True, upload_to=upload_image_to)
    is_published = models.BooleanField('販売状況', default=False)
    created_at = models.DateTimeField('登録日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name 
