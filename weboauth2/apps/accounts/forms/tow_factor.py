from django import forms

from ..models import TwoFactor


class TwoFactorVerifyForm(forms.ModelForm):

    error_messages = {
        'invalid_code': {
            'code': 'Код подтверждения не соотвествует введеному, попробуйте отправить ещё раз.'
        },
        'expired_code': {
            'code': 'Код подверждения просрочен, попробуйте отправить ещё раз.'
        },
    }

    code = forms.IntegerField(
        required=True,
        help_text='Код должен быть'
    )

    class Meta:
        model = TwoFactor
        fields = ('code', )

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self.code_field = TwoFactor._meta.get_field("code")

    def clean(self):
        code = self.cleaned_data.get('code')
        if code is not None:
            if not self.instance.check_verification_code(code):
                raise self.get_invalid_code_error()
            if not self.instance.is_alive():
                raise self.get_expired_code_error()

            self.instance.notify_about_verification()
        return self.cleaned_data

    def get_invalid_code_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_code'],
            code='invalid_code',
            params={'code': self.code_field.verbose_name},
        )

    def get_expired_code_error(self):
        return forms.ValidationError(
            self.error_messages['expired_code'],
            code='expired_code',
            params={'code': self.code_field.verbose_name}
        )
