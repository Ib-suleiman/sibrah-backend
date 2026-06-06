from django import forms

class OrderForm(forms.Form):
    customer_name    = forms.CharField(max_length=100, label='Full Name')
    customer_email   = forms.EmailField(label='Email Address')
    customer_phone   = forms.CharField(max_length=20, label='Phone Number')
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Delivery Address', required=False
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label='Additional Notes', required=False
    )
