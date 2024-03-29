from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy

from forms import SubscriptionForm, SubscriptionMerchantForm
from middleware import RefererMiddleware


class IndexView(FormView):
    template_name = 'landing/index.html'
    form_class = SubscriptionForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        request = self.request
        context['subscription'] = request.session.get('subscription', False)

        return context

    def form_valid(self, form):
        request = self.request
        request.session['subscription'] = True

        subscription = form.save(commit=False)
        subscription.referer = request.session.get(RefererMiddleware.REFERER)
        subscription.save()

        return super(IndexView, self).form_valid(form)


class MerchantView(FormView):
    template_name = 'landing/merchant.html'
    form_class = SubscriptionMerchantForm
    success_url = reverse_lazy('landign:merchant')

    def get_context_data(self, **kwargs):
        context = super(MerchantView, self).get_context_data(**kwargs)

        request = self.request
        context['subscription_merchant'] = request.session.get('subscription', False)

        return context

    def form_valid(self, form):
        request = self.request
        request.session['subscription_merchant'] = True

        subscription = form.save(commit=False)
        subscription.referer = request.session.get(RefererMiddleware.REFERER)
        subscription.save()

        return super(MerchantView, self).form_valid(form)

