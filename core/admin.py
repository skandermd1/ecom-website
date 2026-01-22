from django.contrib import admin
from core.models import category,product,productimage,ProductReview,cartOrder,wishlist,orderedItems,adress,mail

# Register your models here.
class adressAdmin(admin.ModelAdmin):
    list_editable = ('default',)
admin.site.register(category)
admin.site.register(product)
admin.site.register(productimage)
admin.site.register(ProductReview)
admin.site.register(cartOrder)
admin.site.register(wishlist)
admin.site.register(orderedItems)
admin.site.register(adress)


