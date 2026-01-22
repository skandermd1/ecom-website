from django import forms
from core.models import ProductReview,mail

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'review']
class mailForm(forms.ModelForm):
    class Meta:
        model=mail
        fields=['email']
