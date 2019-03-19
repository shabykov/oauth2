from django import forms


class TwoFactorVerifyForm(forms.Form):

    code = forms.IntegerField(
        min_value=10000,
        max_value=99999,
        required=True
    )
