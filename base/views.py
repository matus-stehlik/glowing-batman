from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, RedirectView


class BaseView(TemplateView):

    template_name = "base/base.html"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class SecureBaseView(BaseView):

    template_name = "base/base.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)


class IndexView(TemplateView):

    template_name = "base/index.html"


class RedirectBackView(RedirectView):

    default_return_view = None
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.default_return_view:
            default_url = reverse_lazy(self.default_return_view)
        else:
            default_url = '/'

        return self.request.META.get('HTTP_REFERER', default_url)
