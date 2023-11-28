from django.forms import ModelForm
from app.models import Products

class ProductsForm(ModelForm):
    class Meta:
        model = Products
        fields = ['user_id','product','categoria','ratings']