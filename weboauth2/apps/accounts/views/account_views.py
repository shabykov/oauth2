from django.views import generic
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import views
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.debug import sensitive_post_parameters


from .. import models, mixins, forms


def index(request):
    return render(request, template_name='index.html')


class LoginView(views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        success_url = reverse_lazy('verify')
        if self.request.GET.get('next') is not None:
            success_url += "?next=" + self.request.GET['next']
        return success_url

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        models.TwoFactor.objects.update_or_create(user=user)

        self.send_verification_request()
        return HttpResponseRedirect(self.get_success_url())

    def send_verification_request(self):
        return self.request.user.two_factor.send_code()


class TwoFactorVerifyView(LoginRequiredMixin, generic.FormView):
    template_name = 'verify.html'
    form_class = forms.TwoFactorVerifyForm

    not_verified_url = reverse_lazy('verify')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        return super(TwoFactorVerifyView, self).post(request, *args, **kwargs)

    def form_valid(self, form):

        if self.request.session.get('verified', False) is True:
            self.request.session['verified'] = False
            return HttpResponseRedirect(self.not_verified_url)

        if self.verify_code(form.cleaned_data['code']):
            self.request.session['verified'] = True

            if self.request.GET.get('next') is not None:
                return HttpResponseRedirect(self.request.GET['next'])

            return HttpResponseRedirect(reverse_lazy('index'))
        else:

            if self.request.session.get('verified') is not None:
                del self.request.session['verified']

            if self.request.GET.get('next') is not None:
                return HttpResponseRedirect(self.not_verified_url + "?next=" + self.request.GET['next'])

            return HttpResponseRedirect(self.not_verified_url)

    def verify_code(self, code):
        return self.request.user.two_factor.check_verification_code(code)


class PasswordResetView(views.PasswordResetView):
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    template_name = 'password_reset_form.html'


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


class PasswordChangeView(mixins.TwoFactorMixin, views.PasswordChangeView):
    template_name = 'password_change_form.html'


class PasswordChangeDoneView(mixins.TwoFactorMixin, views.PasswordChangeDoneView):
    template_name = 'password_change_done.html'
