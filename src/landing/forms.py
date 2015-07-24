from django import forms
from models import Subscription, SubscriptionMerchant


class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = ['email']


class SubscriptionMerchantForm(forms.ModelForm):

    class Meta:
        model = SubscriptionMerchant
        fields = [
            'title', 'first_name', 'last_name', 'email', 'phone', 'store', 
            'street', 'street2', 'zipcd', 'category', 'pos'
        ]

    def __init__(self, *args, **kwargs):
        super(SubscriptionMerchantForm, self).__init__(*args, **kwargs)
        #self.fields['category'].empty_label = '- Category -'
        self.fields['category'].empty_label = None
