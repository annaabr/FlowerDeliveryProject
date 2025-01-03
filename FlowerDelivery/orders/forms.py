from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'delivery_date', 'delivery_time_interval', 'customer_comment']

        widgets = {
            'customer_comment': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)