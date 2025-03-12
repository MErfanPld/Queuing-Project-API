from django import forms
from .models import Wallet


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance']


class AddFundsForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=0, label="مقدار")
