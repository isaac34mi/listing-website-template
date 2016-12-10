from django.contrib import admin
from state.models import Category,Products,Images
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name',]
class ProductsAdmin(admin.ModelAdmin):
	list_display = ['title', 'category','user','description','product_price','Fb_url',
					'contact_Name','contact_email','product_location','contact_number','coverImage','date_created','code',]
class ImagesAdmin(admin.ModelAdmin):
	list_display=['post','user','image',]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Products,ProductsAdmin)
admin.site.register(Images,ImagesAdmin)

