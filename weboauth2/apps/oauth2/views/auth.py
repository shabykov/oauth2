import logging

from urllib.parse import urlencode
from oauth2_provider import views, models, scopes
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView, RedirectView

decorators = [never_cache, login_required]


@method_decorator(decorators, name='dispatch')
class ChooseApplicationView(ListView):
    model = models.Application
    context_object_name = 'applications'
    template_name = 'oauth2/choose_application.html'

    def get_queryset(self):
        try:
            applications = self.request.user.profile.applications.all()
        except Exception as error:
            logging.error(str(error))
            applications = None
        return applications


@method_decorator(decorators, name='dispatch')
class ChooseScopeView(TemplateView):
    application = None
    template_name = 'oauth2/choose_scope.html'

    def get(self, request, *args, **kwargs):
        try:
            self.application = get_object_or_404(models.Application, pk=kwargs['pk'])
        except Exception as error:
            logging.error(str(error))
        return super(ChooseScopeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChooseScopeView, self).get_context_data(**kwargs)
        context['application'] = self.application
        context['scopes'] = scopes.get_scopes_backend().get_all_scopes()
        return context


@method_decorator(decorators, name='dispatch')
class RedirectToAuthorizationView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'authorize'
    response_type = 'code'
    application = None
    scope = 'read'

    def get(self, request, *args, **kwargs):
        try:
            self.application = get_object_or_404(models.Application, pk=kwargs['pk'])
        except Exception as error:
            logging.error(str(error))
        self.scope = request.GET.get('scope', 'read')

        return super(RedirectToAuthorizationView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return '{}?{}'.format(reverse(self.pattern_name), urlencode({
            'client_id': self.application.client_id,
            'redirect_uri': self.application.default_redirect_uri,
            'response_type': self.response_type,
            'scope': self.scope
        }))


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

