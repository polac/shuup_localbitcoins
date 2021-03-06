from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.db.backends.utils import format_number
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from shuup.core.models import PaymentProcessor, ServiceChoice

from lbcapi import api

acceptable_states_in_zero_conf = ('PAID', 'PAID_IN_LATE', 'PAID_AND_CONFIRMED', 'PAID_IN_LATE_AND_CONFIRMED')

class LocalbitcoinsCheckoutPaymentProcessor(PaymentProcessor):
    api_key = models.CharField(max_length=150, verbose_name=_("API Key"))
    api_secret = models.CharField(max_length=150, verbose_name=_("API Secret"))
    accept_zero_conf = models.BooleanField(verbose_name=_("Accept zero confirmation payments"), default=True)

    def get_service_choices(self):
        return [ServiceChoice('localbitcoins', _("Localbitcoins Checkout"))]

    def process_payment_return_request(self, service, order, request):
        # Missing partially paid function completely
        invoice_id = None
        try:
            invoice_id = str(order.payment_data["localbitcoins"]["id"])
        except KeyError:
            return
        self._update_payment_data(invoice_id, order)
        status = order.payment_data["localbitcoins"]["state"]
        if self.accept_zero_conf and status in acceptable_states_in_zero_conf and order.is_not_paid():
            order.create_payment(
                order.taxful_total_price,
                payment_identifier="Localbitcoins-{}".format(invoice_id),
                description="Localbitcoins payment, id:{}".format(invoice_id)
            )
        else:
            # how should we handle waiting of the confs?
            pass

    def _update_payment_data(self, invoice_id, order):
        url = "/api/merchant/invoice/{invoice_id}/".format(invoice_id=invoice_id)
        response = self.get_api_conn().call('GET', url).json()['data']
        order.payment_data["localbitcoins"] = response['invoice']

    def get_payment_process_response(self, service, order, urls):
        invoice_id = None
        try:
            invoice_id = str(order.payment_data["localbitcoins"]["id"])
        except KeyError:
            pass

        if not invoice_id:
            invoice_data = {
                'currency': order.currency,
                'amount': format_number(order.taxful_total_price_value, None, Decimal(2)),
                'description': _("Payment for order {id} on {shop}").format(
                id=order.identifier, shop=order.shop),
                'return_url': urls.return_url,
            }
            response = self.get_api_conn().call('POST', "/api/merchant/new_invoice/", params=invoice_data,).json()['data']
            order.payment_data["localbitcoins"] = response['invoice']
            order.save()
            return HttpResponseRedirect(order.payment_data["localbitcoins"]["url"])
        else:
            # Update the status of invoice.
            # If not paid redirect to make payment.
            pass

    def get_api_conn(self):
        if not hasattr(self, '_conn') or not self._conn:
            self._conn = api.hmac(self.api_key, self.api_secret)
        return self._conn
