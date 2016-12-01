
from django.views.generic.edit import FormView
from shuup.front.checkout import BasicServiceCheckoutPhaseProvider, CheckoutPhaseViewMixin

from shuup_localbitcoins.models import LocalbitcoinsCheckoutPaymentProcessor


class LocalbitcoinsCheckoutPhase(CheckoutPhaseViewMixin, FormView):
    service = None


class LocalbitcoinsCheckoutPhaseProvider(BasicServiceCheckoutPhaseProvider):
    phase_class = None
    service_provider_class = LocalbitcoinsCheckoutPaymentProcessor
