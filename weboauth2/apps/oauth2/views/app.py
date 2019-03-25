from django.urls import reverse_lazy
from oauth2_provider import views

from .. import mixins


class ApplicationList(mixins.TwoFactorMixin, mixins.ApplicationViewMixin, views.ApplicationList):
    template_name = 'oauth2/applications/list.html'


class ApplicationRegistration(mixins.ApplicationCreationMixin, mixins.TwoFactorMixin, views.ApplicationRegistration):
    template_name = 'oauth2/applications/register.html'

    def get_success_url(self):
        return reverse_lazy('application_detail', kwargs={'pk': self.object.pk})


class ApplicationDetail(mixins.ApplicationViewMixin, mixins.TwoFactorMixin, views.ApplicationDetail):
    template_name = 'oauth2/applications/detail.html'


class ApplicationDelete(mixins.ApplicationDeleteMixin, mixins.TwoFactorMixin, views.ApplicationDelete):
    template_name = 'oauth2/applications/delete.html'
    success_url = reverse_lazy('application_list')


class ApplicationUpdate(mixins.ApplicationChangeMixin, mixins.TwoFactorMixin, views.ApplicationUpdate):
    template_name = 'oauth2/applications/update.html'

    def get_success_url(self):
        return reverse_lazy('application_detail', kwargs={'pk': self.object.pk})
