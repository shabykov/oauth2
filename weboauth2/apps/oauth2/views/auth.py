import logging

from urllib.parse import urlencode
from oauth2_provider import views, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView, RedirectView

decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
class ApplicationChooseView(ListView):
    model = models.Application
    context_object_name = 'applications'
    template_name = 'oauth2/application_choose.html'
    scope = None

    def get_queryset(self):
        try:
            applications = self.request.user.profile.applications.all()
            self.scope = self.request.user.profile.role.scope
        except Exception as error:
            logging.error(str(error))
            applications = None
        return applications

    def get_context_data(self, **kwargs):
        context = super(ApplicationChooseView, self).get_context_data(**kwargs)
        context['scope'] = self.scope
        return context


@method_decorator(decorators, name='dispatch')
class ApplicationChooseConfirm(TemplateView):
    application = None
    template_name = 'oauth2/application_choose_confirm.html'
    scope = None

    def get(self, request, *args, **kwargs):
        try:
            self.application = models.Application.objects.get(client_id=kwargs['client_id'])
            self.scope = self.request.user.profile.role.scope
        except Exception as error:
            logging.error(error)
        return super(ApplicationChooseConfirm, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ApplicationChooseConfirm, self).get_context_data(**kwargs)
        context['application'] = self.application
        context['scope'] = self.scope
        return context


@method_decorator(decorators, name='dispatch')
class RedirectToAuthorizationView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'authorize'
    response_type = 'code'

    application = None
    scope = None

    def get(self, request, *args, **kwargs):
        try:
            self.application = get_object_or_404(models.Application, pk=kwargs['pk'])
        except Exception as error:
            logging.error(str(error))

        self.scope = request.GET.get('scope')

        return super(RedirectToAuthorizationView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if self.scope is None:
            return '{}?{}'.format(reverse('application-scope-not-found'), urlencode(kwargs))

        return '{}?{}'.format(reverse(self.pattern_name), urlencode({
            'client_id': self.application.client_id,
            'redirect_uri': self.application.default_redirect_uri,
            'response_type': self.response_type,
            'scope': self.scope
        }))


@method_decorator(decorators, name='dispatch')
class ScopeNotFoundView(TemplateView):
    template_name = 'oauth2/scope_not_found.html'

    application = None

    def get(self, request, *args, **kwargs):
        try:
            self.application = get_object_or_404(models.Application, pk=kwargs['pk'])
        except Exception as error:
            logging.error(str(error))
        return super(ScopeNotFoundView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ScopeNotFoundView, self).get_context_data(**kwargs)
        context['application'] = self.application
        return context


@method_decorator(decorators, name='dispatch')
class AuthorizationView(views.AuthorizationView):
    template_name = 'oauth2/authorize.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenView(views.TokenView):
    def post(self, request, *args, **kwargs):
        return super(TokenView, self).post(request, *args, **kwargs)


class RevokeTokenView(views.RevokeTokenView):
    def post(self, request, *args, **kwargs):
        return super(RevokeTokenView, self).post(request, *args, **kwargs)

