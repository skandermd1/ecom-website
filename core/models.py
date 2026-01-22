from django.db import models
from shortuuid.django_fields import ShortUUIDField
from taggit.managers import TaggableManager

STATUS_CHOICES=(
    ('process','processing'),
    ('shipped','shipped'),
    ('delivered','delivered'),
)
RATING=(
    (1,'⭐'),
    (2,'⭐⭐'), 
    (3,'⭐⭐⭐'),
    (4,'⭐⭐⭐⭐'),
    (5,'⭐⭐⭐⭐⭐'),
)
# Create your models here.
class category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="category")
    class Meta:
        verbose_name="Category"
        verbose_name_plural="Categories"
    def __str__(self):
        return self.title
class product(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    old_price=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE,related_name="NB_products")
    
    image=models.ImageField(upload_to="products")
    product_status=models.CharField(choices=STATUS_CHOICES,default='process',max_length=20)
    in_stock=models.BooleanField(default=True)
    tags=TaggableManager( blank=True)

    class Meta:
        verbose_name="Product"
        verbose_name_plural="Products"
    def __str__(self):
        return self.title
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return round(discount, 2)
        return 0
class productimage(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE,related_name="product_images")
    image=models.ImageField(upload_to="productimages",default="products.png",)
    class Meta:
        verbose_name="Product Image"
        verbose_name_plural="Product Images"
    def __str__(self):
        return self.product.title
#########################################################,card,order,ordereditems,######################################################
class cartOrder(models.Model):
    user=models.ForeignKey("userauth.User",on_delete=models.CASCADE)
    added_at=models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    paid=models.BooleanField(default=False)
    class Meta:
        verbose_name="Cart Order "
        verbose_name_plural="Cart Order"
class orderedItems(models.Model):
    order=models.ForeignKey(cartOrder,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    item=models.CharField(max_length=100)
    added_at=models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    total=models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name="Ordered Item"
        verbose_name_plural="Ordered Items"
########################################################,review,##################################################################################
class ProductReview(models.Model):
    user=models.ForeignKey("userauth.User",on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.SET_NULL,null=True)
    review=models.TextField()
    rating=models.IntegerField(choices=RATING,default=None)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="product review"
        verbose_name_plural="product reviews"
    def __str__(self):
        return self.product.title
class wishlist(models.Model):
    user=models.ForeignKey("userauth.User",on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.SET_NULL,null=True)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="wishlist"
        verbose_name_plural="wishlists"
    def __str__(self):
        return self.product.title
class adress(models.Model):
    user=models.ForeignKey("userauth.User",on_delete=models.CASCADE)
    adress=models.CharField(max_length=100)
    default=models.BooleanField(default=False)
    class Meta:
        verbose_name="adress"
        verbose_name_plural="adresses"
class mail(models.Model):
    email=models.EmailField()
    class Meta:
        verbose_name="mail"
        verbose_name_plural="mails"



