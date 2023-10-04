from django import forms
from stripe import Product

from store.models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta :
        model =  ReviewRating
        fields = ['subject','review','rating']

class ProdForm(forms.Form):
    class Meta :
        model = Product
        fields = '__all__'
        

