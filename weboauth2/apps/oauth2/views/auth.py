import logging

from urllib.parse import urlencode
from django.shortcuts import reverse
from oauth2_provider import views, models
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView, TemplateView, DetailView
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponseGone


from .. import mixins

decorators = [never_cache, login_required]


class ApplicationChooseView(mixins.TwoFactorMixin, mixins.ApplicationViewMixin, ListView):
    model = models.Application
    context_object_name = 'applications'
    template_name = 'oauth2/application_choose.html'
    scope = None

    def get_queryset(self):
        try:
            applications = self.request.user.profile.applications.all()
            self.scope = '+'.join(self.request.user.profile.role.scope)
        except Exception as error:
            logging.warning(error)
            applications = None
        return applications

    def get_context_data(self, **kwargs):
        context = super(ApplicationChooseView, self).get_context_data(**kwargs)
        context['scope'] = self.scope
        return context


class ApplicationChooseConfirm(mixins.TwoFactorMixin, mixins.SessionCreationMixin, DetailView):
    model = models.Application
    context_object_name = 'application'
    template_name = 'oauth2/application_choose_confirm.html'
    scope = None

    def get_object(self, queryset=None):
        try:
            self.scope = '+'.join(self.request.user.profile.role.scope)
        except Exception as error:
            logging.error(error)
        return models.Application.objects.get(client_id=self.kwargs['client_id'])

    def get_context_data(self, **kwargs):
        context = super(ApplicationChooseConfirm, self).get_context_data(**kwargs)
        context['scope'] = self.scope
        return context


class RedirectToAuthorizationView(mixins.TwoFactorMixin, mixins.SessionCreationMixin, DetailView):
    permanent = False
    query_string = True
    pattern_name = 'authorize'
    response_type = 'code'

    application = None
    scope = None

    def get_object(self, queryset=None):
        self.application = models.Application.objects.get(client_id=self.kwargs['client_id'])
        try:
            self.scope = ' '.join(self.request.user.profile.role.scope)
        except Exception as error:
            logging.error(str(error))
        return self.application

    def get(self, request, *args, **kwargs):
        self.get_object()
        url = self.get_redirect_url(*args, **kwargs)
        if url:
            if self.permanent:
                return HttpResponsePermanentRedirect(url)
            else:
                return HttpResponseRedirect(url)
        else:
            logging.warning(
                'Gone: %s', request.path,
                extra={'status_code': 410, 'request': request}
            )
            return HttpResponseGone()

    def get_redirect_url(self, *args, **kwargs):
        if self.scope is None:
            return '{}?{}'.format(reverse('application-scope-not-found'), urlencode(kwargs))
        return '{}?{}'.format(reverse(self.pattern_name), urlencode({
            'client_id': self.application.client_id,
            'redirect_uri': self.application.default_redirect_uri,
            'response_type': self.response_type,
            'scope': self.scope
        }))


class AuthorizationView(mixins.TwoFactorMixin, views.AuthorizationView):
    template_name = 'oauth2/authorize.html'


class ScopeNotFoundView(mixins.TwoFactorMixin, TemplateView):
    template_name = 'oauth2/scope_not_found.html'
    application = None

    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        try:
            self.application = models.Application.objects.get(client_id=kwargs['client_id'])
        except Exception as error:
            logging.error(str(error))
        return super(ScopeNotFoundView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ScopeNotFoundView, self).get_context_data(**kwargs)
        context['application'] = self.application
        return context


class TokenView(views.TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        return super(TokenView, self).post(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class RevokeTokenView(views.RevokeTokenView):
    def post(self, request, *args, **kwargs):
        return super(RevokeTokenView, self).post(request, *args, **kwargs)

