from django.views import generic
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import views
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.debug import sensitive_post_parameters


from .. import models, mixins, forms


decorators = [never_cache, login_required]


def index(request):
    return render(request, template_name='index.html')


class LoginView(views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        success_url = reverse_lazy('send_new_code')
        if self.request.GET.get('next') is not None:
            success_url += "?next=" + self.request.GET['next']
        return success_url

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class TwoFactorSendNewView(LoginRequiredMixin, generic.RedirectView):
    redirect_field_name = reverse_lazy('verify')

    def get(self, request, *args, **kwargs):
        models.TwoFactor.objects.update_or_create(user=request.user)
        self.send_verification_request()
        return super().get(request, *args, **kwargs)

    def send_verification_request(self):
        return self.request.user.two_factor.send_code()

    def get_redirect_url(self, *args, **kwargs):
        if self.request.GET.get('next') is not None:
            self.redirect_field_name += "?next=" + self.request.GET['next']
        return self.redirect_field_name


class TwoFactorVerifyView(LoginRequiredMixin, generic.UpdateView):
    model = models.TwoFactor
    template_name = 'verify.html'
    form_class = forms.TwoFactorVerifyForm
    not_verified_url = reverse_lazy('verify')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TwoFactorVerifyView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.two_factor

    def form_valid(self, form):
        if self.request.session.get('verified', False) is True:
            self.request.session['verified'] = False
            return HttpResponseRedirect(self.not_verified_url)

        self.request.session['verified'] = True
        if self.request.GET.get('next') is not None:
            return HttpResponseRedirect(self.request.GET['next'])
        return HttpResponseRedirect(reverse_lazy('index'))


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
