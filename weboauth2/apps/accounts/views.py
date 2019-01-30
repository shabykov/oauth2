from django.shortcuts import render
from django.contrib.auth import views


# Create your views here.


def index(request):
    return render(request, template_name='index.html')


class LoginView(views.LogoutView):
    template_name = 'login.html'
    redirect_field_name = 'choose-application'


class LogoutView(views.LogoutView):
    pass


class PasswordResetView(views.PasswordResetView):
    email_template_name = 'password_reset_email.html'
    html_email_template_name = None
    subject_template_name = 'password_reset_subject.txt'
    template_name = 'password_reset_form.html'


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


class PasswordChangeView(views.PasswordChangeView):
    template_name = 'password_change_form.html'


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = 'password_change_done.html'
